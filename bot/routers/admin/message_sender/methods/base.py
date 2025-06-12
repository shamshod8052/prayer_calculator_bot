from typing import Dict, Any

from aiogram.enums import ContentType
from aiogram.types import InputMediaPhoto, InputMediaVideo, InputMediaAudio, InputMediaDocument

from .copy_messages import CopyMessagesContent
from .forward_messages import ForwardMessagesContent
from .media_group import MediaGroupContent
from .send_poll import SendPollContent
from .send_message import SendMessageContent

def json2media_obj(media_jsons):
    media = []
    for m in media_jsons:
        if m['content_type'] == ContentType.PHOTO:
            media.append(InputMediaPhoto(
                media=m['file_id'],
                caption=m['caption']
            ))
        elif m['content_type'] == ContentType.VIDEO:
            media.append(InputMediaVideo(
                media=m['file_id'],
                caption=m['caption']
            ))
        elif m['content_type'] == ContentType.AUDIO:
            media.append(InputMediaAudio(
                media=m['file_id'],
                caption=m['caption']
            ))
        elif m['content_type'] == ContentType.DOCUMENT:
            media.append(InputMediaDocument(
                media=m['file_id'],
                caption=m['caption']
            ))
    return media


class ContentFactory:
    """Kontentni avtomatik aniqlash va yaratish uchun fabrika"""

    @staticmethod
    def create(data: Dict[str, Any]) -> (
            MediaGroupContent |
            ForwardMessagesContent |
            CopyMessagesContent |
            SendPollContent |
            SendMessageContent
    ):
        if 'media' in data:

            return MediaGroupContent(media=json2media_obj(data['media']))
        if 'from_chat_id' in data and 'message_ids' in data:
            if data.get('filters', {}).get('send_method') == 'forward':
                return ForwardMessagesContent(
                    from_chat_id=data['from_chat_id'],
                    message_ids=data['message_ids']
                )
            return CopyMessagesContent(
                from_chat_id=data['from_chat_id'],
                message_ids=data['message_ids'],
                caption=data.get('caption')
            )
        if 'question' in data and 'options' in data:
            return SendPollContent(
                question=data['question'],
                options=data['options'],
                type=data.get('type', 'quiz'),
                correct_option_id=data.get('correct_option_id')
            )
        return SendMessageContent(text=data.get('text', ''))
