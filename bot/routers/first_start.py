from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from Admin.models import CustomUser as User
from bot.filters.states import InputState
from bot.keyboards.start import first_input_user_kb, is_qada_calculate, not_year_for_day, not_day_for_year
from bot.routers.start import on_start

router = Router(name=__name__)


@router.callback_query(F.data == 'qazo_nima')
async def qazo_nima(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text(
        "Qazo - bu o'z vaqtida o'qilmagan farz yoki vojib namozning qarzi hisoblanadi. "
        "Namozni belgilangan vaqtda o'qish farzdir. Agar biror sabab bilan namozni o'z "
        "vaqtida o'qiy olmasangiz uning qazosini o'qib qo'yish kerak.",
        reply_markup=first_input_user_kb([0, 2]),
    )


@router.callback_query(F.data == 'qazo_yoq')
async def qazo_yoq(call: types.CallbackQuery, state: FSMContext):
    await on_start(call.message, False, state)
    await call.message.delete()


@router.callback_query(F.data == 'qazo_hisoblash')
async def qazo_hisoblash(call: types.CallbackQuery):
    await call.message.edit_text(
        "Avvalo birinchi bir nechta muhim qismlarni bilishingiz kerak.\n\n"
        "- Namozning farz bo'lishi\n"
        "- Balog'at yosh\n"
        "- Shayx video roliklari",
        reply_markup=is_qada_calculate()
    )


@router.callback_query(F.data == 'back_first_start')
async def back_first_start(call: types.CallbackQuery):
    await call.message.edit_text(
        "Assalomu alaykum! 😊\n"
        "Bu bot sizning namoz qazolaringizni doimiy hisoblab borishda ko'maklashadi.\n\n"
        "Keling birinchi navbatda, qancha namozingiz qazo bo'lganini hisoblashda yordam beramiz. "
        "Hisoblash uchun pastdagi \"Qazo hisoblash\" tugmasidan foydalaning.",
        reply_markup=first_input_user_kb()
    )


@router.callback_query(F.data == 'input_year')
@router.callback_query(F.data == 'calculate_qada')
async def calculate_qada(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        "Sizda necha yillik qazo namozingiz bor(Yilda kiriting!)?",
        reply_markup=not_year_for_day()
    )
    await state.set_state(InputState.YEAR)


@router.message(InputState.YEAR)
async def input_qada_year(message: types.Message, user: User, state: FSMContext):
    if not message.text.isdigit():
        return await message.reply("Xato qiymat kiritdingiz!\n\nYilni kiriting!")
    try:
        user.qadas.update(number=int(message.text) * 365)
    except:
        await message.answer("Qazolaringiz qiymati yangilanmadi!")
    else:
        await message.answer("Qazolaringiz qiymati yangilandi!")
    await on_start(message, False, state)


@router.callback_query(F.data == 'input_day')
async def calculate_qada(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        "Sizda necha kunlik qazo namozingiz bor(Kunda kiriting!)?",
        reply_markup=not_day_for_year()
    )
    await state.set_state(InputState.DAY)


@router.message(InputState.DAY)
async def input_qada_year(message: types.Message, user: User, state: FSMContext):
    if not message.text.isdigit():
        return await message.reply("Xato qiymat kiritdingiz!\n\nKunni kiriting!")
    try:
        user.qadas.update(number=int(message.text))
    except:
        await message.answer("Qazolaringiz qiymati yangilanmadi!")
    else:
        await message.answer("Qazolaringiz qiymati yangilandi!")
    await on_start(message, False, state)
