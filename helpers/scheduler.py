from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from django.conf import settings
from django.utils.timezone import now

from Admin.managers import Prayer
from Admin.models import CustomUser
from bot.routers.admin.message_sender.managers import MessageSender
from bot.routers.admin.message_sender.methods.send_message import SendMessageContent


def keyboard():
    inline_keyboard = [
        [
            InlineKeyboardButton(text=now().strftime("%Y-%m-%d"), callback_data="_"),
        ]
    ]

    for key, name in Prayer.choices:
        inline_keyboard.append(
            [
                InlineKeyboardButton(text=str(name), callback_data=f"_"),
                InlineKeyboardButton(text="O'qidim", callback_data=f"qada:{key}:1"),
            ]
        )

    inline_keyboard.append(
        [
            InlineKeyboardButton(text="Saqlash", callback_data="save_qadas"),
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

async def qada_keyboard_sender(bot):
    users = CustomUser.actives.all()
    sender = MessageSender(bot, settings.ADMINS[0], users.count())
    content = SendMessageContent(
        text="...",
        reply_markup=keyboard()
    )

    for user in users:
        await sender.broadcast(content, [user.telegram_id])
