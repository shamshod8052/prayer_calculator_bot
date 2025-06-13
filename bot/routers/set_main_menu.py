from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from bot.filters.multilang_utils import get_translations
from bot.keyboards.start import main_menu_kb

router = Router(name=__name__)


@router.callback_query(F.data == '_')
async def main_menu(call: types.CallbackQuery):
    await call.answer()


@router.callback_query(F.data == 'main_menu')
async def main_menu(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text(
        "Assalomu alaykum! 😊\n"
            "Yana siz bilan ko'rishganimizdan xursandmiz. Sizga qanday yordam bera olamiz?\n\n"
            "Quyidagi tugmalardan birini tanlang:",
        reply_markup=main_menu_kb()
    )


@router.message(F.text.in_(get_translations("Main menu")))
async def main_menu(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Assalomu alaykum! 😊\n"
            "Yana siz bilan ko'rishganimizdan xursandmiz. Sizga qanday yordam bera olamiz?\n\n"
            "Quyidagi tugmalardan birini tanlang:",
        reply_markup=main_menu_kb()
    )
