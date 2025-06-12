from typing import Any, Union, Optional

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.base import BaseSession

from .methods.copy_messages import CopyMessagesContent
from .methods.forward_messages import ForwardMessagesContent
from .methods.media_group import MediaGroupContent
from .methods.send_poll import SendPollContent
from .methods.send_message import SendMessageContent


class CustomBot(Bot):
    def __init__(
        self,
        token: str,
        session: Optional[BaseSession] = None,
        default: Optional[DefaultBotProperties] = None,
        **kwargs: Any
    ) -> None:
        super().__init__(token, session, default, **kwargs)

    async def send(
            self,
            chat_id: Union[str, int],
            content: (
                    MediaGroupContent |
                    ForwardMessagesContent |
                    CopyMessagesContent |
                    SendPollContent |
                    SendMessageContent
            )
    ):
        kwargs = dict(
            **content.__dict__
        )
        kwargs['chat_id'] = chat_id
        if isinstance(content, MediaGroupContent):
            return await self.send_media_group(**kwargs)
        elif isinstance(content, ForwardMessagesContent):
            return await self.forward_messages(**kwargs)
        elif isinstance(content, CopyMessagesContent):
            return await self.copy_messages(**kwargs)
        elif isinstance(content, SendPollContent):
            return await self.send_poll(**kwargs)
        elif isinstance(content, SendMessageContent):
            return await self.send_message(**kwargs)
        else:
            raise ValueError(f"Unsupported content type: {content.content_type}")
