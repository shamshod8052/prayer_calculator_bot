from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from Admin.models import CustomUser as User
from bot.filters.states import InputState
from bot.keyboards.about_bot import back_kb
from bot.keyboards.start import first_input_user_kb, main_menu_kb, my_qadas_kb

router = Router(name=__name__)


@router.message(Command("start"))
async def on_start(message: types.Message, is_created_user: bool, state: FSMContext):
    await state.clear()
    if is_created_user:
        text = (
            "Assalomu alaykum! 😊\n"
            "Bu bot sizning namoz qazolaringizni doimiy hisoblab borishda ko'maklashadi.\n\n"
            "Keling birinchi navbatda, qancha namozingiz qazo bo'lganini hisoblashda yordam beramiz. "
            "Hisoblash uchun pastdagi \"Qazo hisoblash\" tugmasidan foydalaning."
        )
        kb = first_input_user_kb()
    else:
        text = (
            "Assalomu alaykum! 😊\n"
            "Yana siz bilan ko'rishganimizdan xursandmiz. Sizga qanday yordam bera olamiz?\n\n"
            "Quyidagi tugmalardan birini tanlang:"
        )
        kb = main_menu_kb()
    await message.answer(text, reply_markup=kb)


@router.callback_query(F.data == 'qazolarim')
async def my_qadas(call: types.CallbackQuery, user: User):
    await call.message.edit_text(
        "Sizdagi mavjud qazolar:\n\n"
        "- Qazo oson o'qish usuli\n"
        "- 1 oyda 15 yillik qazo o'qish",
        reply_markup=my_qadas_kb(user.qadas)
    )


@router.callback_query(F.data.startswith('qada_'))
async def add_or_remove_qada_num(call: types.CallbackQuery, user: User):
    qada_id = int(call.data.split(':')[1])
    if qada_id in user.qadas.values_list('id', flat=True):
        qada = user.qadas.get(id=qada_id)
        if call.data.startswith('qada_add'):
            qada.increment()
        elif call.data.startswith('qada_remove'):
            qada.decrement()
    user.refresh_from_db()
    await call.message.edit_text(
        "Sizdagi mavjud qazolar:\n\n"
        "- Qazo oson o'qish usuli\n"
        "- 1 oyda 15 yillik qazo o'qish",
        reply_markup=my_qadas_kb(user.qadas)
    )


@router.callback_query(F.data.startswith('change_qada_number:'))
async def change_qada_number(call: types.CallbackQuery, user: User, state: FSMContext):
    qada_id = int(call.data.split(':')[1])
    qada = user.qadas.get(id=qada_id)
    await state.set_state(InputState.QADA_NUMBER)
    await state.set_data({'qada_id': qada_id})
    await call.message.edit_text(
        f"{qada.name} namozi uchun qazolar sonini kiriting...",
        reply_markup=back_kb('qazolarim')
    )


@router.message(InputState.QADA_NUMBER)
async def input_qada_number(message: types.Message, user: User, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("Xato qiymat kiritdingiz!\n\nQazolar sonini kiriting!")
    data = await state.get_data()
    qada_id = data['qada_id']
    qada = user.qadas.get(id=qada_id)
    qada.number = int(message.text)
    qada.save()
    user.refresh_from_db()
    await state.clear()
    await message.answer(
        f"{qada.name} namozi uchun qazolar sonini {qada.number} ga o'zgartirildi!"
    )
    await message.answer(
        "Sizdagi mavjud qazolar:\n\n"
        "- Qazo oson o'qish usuli\n"
        "- 1 oyda 15 yillik qazo o'qish",
        reply_markup=my_qadas_kb(user.qadas)
    )
