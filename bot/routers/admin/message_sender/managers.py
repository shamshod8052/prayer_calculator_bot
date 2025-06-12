import asyncio
import logging
import time
from typing import List, Union

from aiogram import Bot
from aiogram.exceptions import (
    TelegramRetryAfter,
    TelegramForbiddenError,
    TelegramNotFound,
    TelegramBadRequest
)
from aiogram.types import ReplyKeyboardRemove

from .bot import CustomBot
from .config import MAX_CONCURRENT
from .statistics import MailingStatistics
from .methods.copy_messages import CopyMessagesContent
from .methods.forward_messages import ForwardMessagesContent
from .methods.media_group import MediaGroupContent
from .methods.send_poll import SendPollContent
from .methods.send_message import SendMessageContent

logger = logging.getLogger(__name__)


class MessageSender:
    """Xabarlarni ketma-ketlik va rate limit boshqaruvi bilan yuborish"""

    def __init__(self, bot: Bot, author_chat_id: Union[int, str], chat_ids_num: int):
        self.bot = CustomBot(bot.token, **bot.__dict__)
        self.author_chat_id = author_chat_id
        self.chat_ids_num = chat_ids_num

        self.process_id = MailingStatistics.start(author_chat_id, chat_ids_num)
        self.stats: MailingStatistics = MailingStatistics.processes[self.process_id]
        self._semaphore = asyncio.Semaphore(MAX_CONCURRENT)
        self._global_cooldown = 0.0
        self._cooldown_lock = asyncio.Lock()

    async def stop(self):
        if not self.stats.stop:
            MailingStatistics.stop_process(self.process_id)

    async def format_stats(self):
        return MailingStatistics.get_process(self.process_id).format_stats()

    async def _handle_global_cooldown(self):
        """Global kutish vaqtini boshqarish"""
        async with self._cooldown_lock:
            if self._global_cooldown > time.time():
                wait_time = self._global_cooldown - time.time()
                logger.warning(f"Global rate limit: {wait_time:.1f}s kutamiz...")
                await asyncio.sleep(wait_time)

    async def _process_user(
            self,
            chat_id: int,
            content: (
                    MediaGroupContent |
                    ForwardMessagesContent |
                    CopyMessagesContent |
                    SendPollContent |
                    SendMessageContent
            )
    ):
        """Bitta foydalanuvchiga xabarlarni yuborish"""
        async with self._semaphore:
            if self.stats.stop:
                return

            try:
                success = await self._send_message_with_retry(chat_id, content)
                if success:
                    await MailingStatistics.update_counter(
                        self.process_id, 'success'
                    )
            except Exception as e:
                logger.error(f"{chat_id} ga yuborishda kritik xato: {str(e)}")
                await MailingStatistics.update_counter(
                    self.process_id, 'failed'
                )

    async def _send_message_with_retry(
            self,
            chat_id: int,
            content: (
                    MediaGroupContent |
                    ForwardMessagesContent |
                    CopyMessagesContent |
                    SendPollContent |
                    SendMessageContent
            )
    ) -> bool:
        """Qayta urinishlar bilan xabar yuborish"""
        while True:
            try:
                await self._handle_global_cooldown()
                if self.stats.stop:
                    return False

                return await self.bot.send(chat_id, content)

            except TelegramRetryAfter as e:
                async with self._cooldown_lock:
                    new_cooldown = time.time() + e.retry_after
                    if new_cooldown > self._global_cooldown:
                        self._global_cooldown = new_cooldown
                MailingStatistics.record_sleep(self.process_id, e.retry_after)
                await asyncio.sleep(e.retry_after)

            except TelegramForbiddenError:
                await MailingStatistics.update_counter(self.process_id, 'blocked')
                return False
            except (TelegramNotFound, TelegramBadRequest):
                await MailingStatistics.update_counter(self.process_id, 'invalid')
                return False

    async def broadcast(
            self,
            content: (
                    MediaGroupContent |
                    ForwardMessagesContent |
                    CopyMessagesContent |
                    SendPollContent |
                    SendMessageContent
            ),
            chat_ids: List[Union[int, str]],
            send_stats=True,
    ):
        """Xabarlarni barcha foydalanuvchilarga yuborish"""

        tasks = [
            asyncio.create_task(self._process_user(chat_id, content))
            for chat_id in chat_ids
        ]

        await asyncio.gather(*tasks)

        if send_stats:
            await self.stop()
            stats_text = self.stats.format_stats()
            await self.bot.send_message(
                self.author_chat_id,
                f"✅ Yakunlandi!\n{stats_text}",
                reply_markup=ReplyKeyboardRemove()
            )
            return True

        return False
