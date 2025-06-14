from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def about_bot_kb():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Botni ishlatish bo'yicha video", callback_data="bot_video"),
            ],
            [
                InlineKeyboardButton(text="Savol yuborish", callback_data="send_question"),
            ],
            [
                InlineKeyboardButton(text="Orqaga", callback_data="main_menu"),
            ],
        ]
    )

    return kb


def back_kb(callback_data):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Orqaga", callback_data=callback_data),
            ],
        ]
    )

    return kb
