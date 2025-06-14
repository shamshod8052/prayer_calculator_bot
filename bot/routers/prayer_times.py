from aiogram import Router, types, F

from Admin.models import District
from bot.keyboards.prayer_times_kbs import province_kb, district_kb

router = Router(name=__name__)


@router.callback_query(F.data.startswith('page_province:'))
@router.callback_query(F.data == 'prayer_times')
async def select_province(call: types.CallbackQuery):
    page_num = int(call.data.split(':')[1]) if 'page_province' in call.data else 1
    await call.message.edit_text(
        "Qaysi viloyat uchun namoz vaqtlarini bilmoqchisiz?",
        reply_markup=province_kb(page_num)
    )


@router.callback_query(F.data.startswith('page_district:'))
@router.callback_query(F.data.startswith('province:'))
async def select_district(call: types.CallbackQuery):
    if call.data.startswith('province:'):
        province_id = int(call.data.split(':')[1])
    else:
        province_id = None
    if call.data.startswith('page_district:'):
        page_num = int(call.data.split(':')[2])
        province_id = int(call.data.split(':')[1])
    else:
        page_num = 1
    await call.message.edit_text(
        "Qaysi tuman uchun namoz vaqtlarini bilmoqchisiz?",
        reply_markup=district_kb(province_id, page_num)
    )


@router.callback_query(F.data.startswith('district:'))
async def view_district_prayer_time(call: types.CallbackQuery):
    district_id = int(call.data.split(':')[1])
    district = District.objects.get(id=district_id)
    try:
        await call.message.answer(f"{district.prayer_time}")
    except ValueError as e:
        await call.message.answer(f"Xatolik: {e}")
    await call.answer()
