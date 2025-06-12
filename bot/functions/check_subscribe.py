import logging
import traceback

from aiogram import Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from Admin.models import Channel


def get_channels_kb(missing_channels: list[Channel]):
    if not missing_channels:
        return
    buttons = [
        [
            InlineKeyboardButton(text=f"{n + 1}. {kb.name}", url=kb.url)
        ] for n, kb in enumerate(missing_channels)
    ]
    kb_markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    return kb_markup


async def is_user_subscribed(bot: Bot, user_chat_id: int) -> tuple[bool, InlineKeyboardMarkup | None]:
    """
        Foydalanuvchining barcha majburiy kanallarga obuna bo‘lganini tekshiradi.
        True bo‘lsa - ruxsat, False bo‘lsa - obuna bo‘lmaganlar ro‘yxati bilan.
    """
    unsubscribed_channels = []
    required_channels = Channel.objects.filter(is_required=True, is_active=True)

    for channel in required_channels:
        try:
            member = await bot.get_chat_member(channel.get_chat_id(), user_chat_id)
            if member.status in ["left", "kicked"]:
                unsubscribed_channels.append(channel)
        except Exception as e:
            logging.error(traceback.format_exc())  # Kanal topilmasa yoki boshqa xato

    return len(unsubscribed_channels) == 0, get_channels_kb(unsubscribed_channels)
