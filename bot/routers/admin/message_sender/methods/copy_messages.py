from typing import Union, List, Optional, Any

from aiogram.methods import CopyMessages


class CopyMessagesContent(CopyMessages):
    from_chat_id: Union[int, str]
    """Unique identifier for the chat where the original messages were sent (or channel username in the format :code:`@channelusername`)"""
    message_ids: List[int]
    """A JSON-serialized list of 1-100 identifiers of messages in the chat *from_chat_id* to copy. The identifiers must be specified in a strictly increasing order."""
    message_thread_id: Optional[int] = None
    """Unique identifier for the target message thread (topic) of the forum; for forum supergroups only"""
    disable_notification: Optional[bool] = None
    """Sends the messages `silently <https://telegram.org/blog/channels-2-0#silent-messages>`_. Users will receive a notification with no sound."""
    protect_content: Optional[bool] = None
    """Protects the contents of the sent messages from forwarding and saving"""
    remove_caption: Optional[bool] = None
    """Pass :code:`True` to copy the messages without their captions"""

    def __init__(
            self,
            from_chat_id: Union[int, str],
            message_ids: List[int],
            message_thread_id: Optional[int] = None,
            disable_notification: Optional[bool] = None,
            protect_content: Optional[bool] = None,
            remove_caption: Optional[bool] = None,
            **__pydantic_kwargs: Any,
    ) -> None:

        super().__init__(
            chat_id=1,
            from_chat_id=from_chat_id,
            message_ids=message_ids,
            message_thread_id=message_thread_id,
            disable_notification=disable_notification,
            protect_content=protect_content,
            remove_caption=remove_caption,
            **__pydantic_kwargs,
        )
