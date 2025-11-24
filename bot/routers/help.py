from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

router = Router(name=__name__)


@router.message(F.text == "/help")
async def help_func(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Bu bot namoz vaqtlari haqida ma'lumot beradi!"
    )
