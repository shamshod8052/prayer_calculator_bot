import logging
import traceback

from aiogram import Router, types, F, Bot
from aiogram.fsm.context import FSMContext

from Admin.models import CustomUser as User
from bot.filters.states import InputState
from bot.keyboards.about_bot import about_bot_kb, back_kb

router = Router(name=__name__)


@router.callback_query(F.data == 'back_about_bot')
@router.callback_query(F.data == 'about_bot')
async def about_bot(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    if call.data == 'back_about_bot':
        await call.message.answer(
            "Bu bot sizning namoz qazolaringizni doimiy hisoblab borishda ko'maklashadi.\n\n"
            "Bizning ijtimoiy tarmoqlarga obuna bo'ling:\n\n"
            "<a href='https://t.me/xushnudbek'>Telegram</a>   "
            "<a href='https://www.instagram.com/xushnudbek/'>Instagram</a>",
            disable_web_page_preview=True,
            reply_markup=about_bot_kb(),
            reply_to_message_id=None
        )
        await call.message.delete()
    else:
        await call.message.edit_text(
            "Bu bot sizning namoz qazolaringizni doimiy hisoblab borishda ko'maklashadi.\n\n"
            "Bizning ijtimoiy tarmoqlarga obuna bo'ling:\n\n"
            "<a href='https://t.me/xushnudbek'>Telegram</a>   "
            "<a href='https://www.instagram.com/xushnudbek/'>Instagram</a>",
            disable_web_page_preview=True,
            reply_markup=about_bot_kb(),
            reply_to_message_id=None
        )


@router.callback_query(F.data == 'bot_video')
async def about_bot(call: types.CallbackQuery):
    await call.message.answer_video(
        video='https://app.botmother.com/api/files/684bd9a78a7f79001a83caee',
        caption="Bu bot haqidagi video"
    )
    await call.answer()


@router.callback_query(F.data == 'send_question')
async def send_question(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(InputState.QUESTION)
    await call.message.answer(
        "Sizga qanday yordam bera olamiz?\n\nIltimos savolingizni yozing...",
        reply_markup=back_kb('about_bot'),
    )
    await call.message.delete()

@router.message(InputState.QUESTION)
async def input_question(message: types.Message, bot: Bot):
    admins = User.tg_admins.all()
    for admin in admins:
        try:
            await bot.forward_message(admin.telegram_id, message.from_user.id, message.message_id)
        except:
            logging.error(traceback.format_exc())
    await message.reply(
        "Savolingiz qa'bul qilindi! Tez orada adminlarimiz javob berishadi!\n\n"
        "Yana savol yuborishda davom etishingiz mumkin!",
        reply_markup=back_kb('back_about_bot')
    )
