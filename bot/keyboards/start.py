from itertools import islice

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from django.db.models import QuerySet

from Admin.models import Qada


def main_menu_kb():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Qazolarim", callback_data="qazolarim"),
                InlineKeyboardButton(text="Ko'p berilgan savollar", callback_data="faq"),
            ],
            [
                InlineKeyboardButton(text="Namoz vaqtlari", callback_data="prayer_times"),
                InlineKeyboardButton(text="Bot haqida", callback_data="about_bot"),
            ],
        ]
    )

    return kb

def first_input_user_kb(btn_indexes: list[int] = None):
    if btn_indexes is None:
        btn_indexes = [0, 1, 2]
    buttons = [
        [
            InlineKeyboardButton(text="Qazo hisoblash", callback_data="qazo_hisoblash"),
            InlineKeyboardButton(text="Qazo nima?", callback_data="qazo_nima"),
            InlineKeyboardButton(text="Menda qazolar yo'q", callback_data="qazo_yoq"),
        ][i] for i in btn_indexes
    ]
    it = iter(buttons)
    inline_keyboard = list(iter(lambda: list(islice(it, 2)), []))
    kb = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    return kb

def is_qada_calculate():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Hisoblashni boshlash", callback_data="calculate_qada"),
            ],
            [
                InlineKeyboardButton(text="Orqaga", callback_data="back_first_start"),
            ]
        ]
    )

    return kb

def not_year_for_day():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Men kunda kiritaman", callback_data="input_day"),
            ],
            [
                InlineKeyboardButton(text="Orqaga", callback_data="qazo_hisoblash"),
            ]
        ]
    )

    return kb

def not_day_for_year():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Men yilda kiritaman", callback_data="input_year"),
            ],
            [
                InlineKeyboardButton(text="Orqaga", callback_data="qazo_hisoblash"),
            ]
        ]
    )

    return kb


def my_qadas_kb(qadas: QuerySet[Qada]):
    inline_keyboard = []
    for qada in qadas.all():
        inline_keyboard.append(
            [
                InlineKeyboardButton(text=qada.name, callback_data=f"_")
            ]
        )
        inline_keyboard.append(
            [
                InlineKeyboardButton(text='-', callback_data=f"qada_remove:{qada.id}"),
                InlineKeyboardButton(text=f"{qada.number}", callback_data=f"change_qada_number:{qada.id}"),
                InlineKeyboardButton(text='+', callback_data=f"qada_add:{qada.id}"),
            ]
        )
    inline_keyboard.append(
        [
            InlineKeyboardButton(text="Orqaga", callback_data="main_menu"),
        ]
    )
    kb = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    return kb
