from itertools import islice

from aiogram.types import InlineKeyboardButton, WebAppInfo

from Admin.models import Province, District
from bot.keyboards.keyboard_paginator import BackButton, Paginator
from helpers.value_insert import insert_values_every_n


def province_kb(page_num=1):
    buttons = [
        InlineKeyboardButton(text=province.name, callback_data=f"province:{province.id}") for province in Province.actives.all()
    ]
    it = iter(buttons)
    rows_list = list(iter(lambda: list(islice(it, 1)), []))
    rows_list = insert_values_every_n(
        rows_list, 4,
        [InlineKeyboardButton(text="Web view", web_app=WebAppInfo(url="https://prayer-time-tafsoft.vercel.app/"))]
    )

    back = BackButton(text="Orqaga", callback_data="main_menu")
    paginator = Paginator(rows_list, 5, back, True)
    page = paginator.get_page(page_num, 'province').as_markup()

    return page


def district_kb(province_id, page_num=1):
    buttons = [
        InlineKeyboardButton(text=district.name, callback_data=f"district:{district.id}") for district in District.actives.filter(province__id=province_id).all()
    ]
    it = iter(buttons)
    rows_list = list(iter(lambda: list(islice(it, 1)), []))
    back = BackButton(text="Orqaga", callback_data="prayer_times")
    paginator = Paginator(rows_list, 5, back, True)
    page = paginator.get_page(page_num, f"district:{province_id}")

    return page.as_markup()
