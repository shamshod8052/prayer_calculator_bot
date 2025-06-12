import asyncio

from aiogram import F, Router, Bot
from aiogram.enums import ContentType
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message, CallbackQuery, ReplyKeyboardMarkup,
    KeyboardButton
)

from bot.filters.admin_filter import AdminFilter
from .enums import Localization
from .keyboards import generate_inline_keyboard, confirm_yes, confirm_no, get_filter_keyboard, update_kb
from .managers import MessageSender
from .methods.base import ContentFactory
from .states import AdminStates
from .statistics import MailingStatistics
from .users import UserManager

router = Router()

@router.message(AdminFilter(), Command("send_message"))
async def send_message_func(message: Message):
    kb = await get_filter_keyboard('uz')
    await message.answer("Xabar tarqatiladigan foydalanuvchilar filter'larini tanlang...", reply_markup=kb)


# state_data = {
#     'message_type': ('media_group', 'message'),
#     'send_method': ('forward', 'copy'),
#     'filters': {
#         'audience': ['group', 'supergroup', 'channel', 'private'],
#         'status': ['active', 'inactive'],
#         'lang': ['uz', 'en', 'ru']
#     },
#     'media': [],
#     'from_chat_id': Union[str, int],
#     'message_ids': [],
# }


@router.callback_query(F.data.startswith(('message_type:', 'send_method:', 'audience:', 'status:', 'lang:')))
async def handle_filters(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    current_filters = user_data.get('filters', {})
    category, value = callback.data.split(':')

    # Tugma holatini yangilash
    if category in ['message_type', 'send_method']:  # Faqat bitta tanlov
        current_filters[category] = value
    else:  # Bir nechta tanlov
        if value in current_filters.get(category, []):
            current_filters[category].remove(value)
        else:
            current_filters.setdefault(category, []).append(value)

    await state.update_data(filters=current_filters)

    # Tugmalarni yangilab qayta jo'natish
    kb = await get_filter_keyboard('uz', current_filters)
    await callback.message.edit_reply_markup(reply_markup=kb)


@router.callback_query(F.data == 'get_messages')
async def get_messages(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Xabarlaringizni kiriting!")
    await state.set_state(AdminStates.CONFIRM_SENDING)
    await callback.answer()


@router.message(AdminFilter(), AdminStates.CONFIRM_SENDING, F.text == "✅ Tayyor")
async def finalize_contents(message: Message, state: FSMContext, bot: Bot):
    """Media guruhni yakunlash"""
    data = await state.get_data()
    media = data.get('media', [])
    from_chat_id = data.get('from_chat_id', [])
    message_ids = data.get('message_ids', [])

    if not (media or (from_chat_id and message_ids)):
        await message.answer("❌ Siz xabar yubormadingiz!")
        return

    sender = MessageSender(bot, message.from_user.id, 1)

    stat_msg = await message.answer(
        sender.stats.format_stats(),
        reply_markup=await generate_inline_keyboard(
            update_kb, 'uz', data={'process_id': sender.process_id}
        )
    )

    try:
        content = ContentFactory.create(data)
        await sender.broadcast(content, [message.from_user.id], False)
        await sender.stop()
    except ValueError:
        await message.answer("Ma'lumotlar yetarli emas!")
        return

    await stat_msg.delete()
    await message.answer(
        await Localization.get_text('confirm_send'),
        reply_markup=await generate_inline_keyboard(
            [
                [confirm_yes], [confirm_no]
            ],
            'uz'
        )
    )

lock = asyncio.Lock()

@router.message(AdminStates.CONFIRM_SENDING)
async def process_content(message: Message, state: FSMContext):
    async with lock:
        """Xabar kontentini qayta ishlash"""
        data = await state.get_data()
        filters = data.get('filters', {})
        caption = message.caption or ""

        if filters.get('message_type', '') == 'media_group':
            media = data.get('media', [])

            if message.content_type == ContentType.PHOTO:
                file_id = message.photo[-1].file_id
            elif message.content_type == ContentType.VIDEO:
                file_id = message.video.file_id
            elif message.content_type == ContentType.AUDIO:
                file_id = message.audio.file_id
            elif message.content_type == ContentType.DOCUMENT:
                file_id = message.document.file_id
            else:
                await message.reply("Faqat rasm, video, audio va fayllar yuboring! Chunki siz media_group ni tanlagansiz!")
                return
            media.append(
                {
                    'content_type': message.content_type, 'file_id': file_id, 'caption': caption
                }
            )
            await state.update_data(media=media)
        else:
            message_ids = data.get('message_ids', [])
            from_chat_id = message.chat.id
            message_ids.append(message.message_id)
            await state.update_data(
                {
                    'from_chat_id': from_chat_id,
                    'message_ids': message_ids,
                    'caption': caption,
                }
            )
        await message.reply(
            "✅.", reply_markup=ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text="✅ Tayyor")]], resize_keyboard=True
            )
        )


@router.callback_query(AdminFilter(), F.data.startswith('confirm:yes'), AdminStates.CONFIRM_SENDING)
async def confirm_sending(call: CallbackQuery, state: FSMContext, bot: Bot):
    """Yuborishni tasdiqlash"""
    data = await state.get_data()
    await state.clear()

    data = data.copy()
    filters = data.get('filters', {}).copy()

    await call.message.delete()
    users = await UserManager.get_users(filters)
    if not users:
        await call.message.answer(await Localization.get_text('no_users'))
        return

    sender = MessageSender(bot, call.from_user.id, len(users))

    stat_msg = await call.message.answer(
        sender.stats.format_stats(),
        reply_markup=await generate_inline_keyboard(
            update_kb, 'uz', data={'process_id': sender.process_id}
        )
    )

    try:
        content = ContentFactory.create(data)
    except ValueError:
        await call.message.answer("Ma'lumotlar yetarli emas!")
        return
    else:
        is_send_stat = await sender.broadcast(content, users)
        if is_send_stat:
            await sender.stop()
            await stat_msg.delete()

@router.callback_query(AdminFilter(), F.data.startswith('confirm:no'), AdminStates.CONFIRM_SENDING)
async def confirm_sending(call: CallbackQuery, state: FSMContext):
    """Yuborishni to'xtatish"""
    await state.clear()
    await call.message.answer("✅ Bekor qilindi!")
    await call.message.delete()

@router.callback_query(AdminFilter(), F.data.startswith('confirm:yes'))
@router.callback_query(AdminFilter(), F.data.startswith('confirm:no'))
async def confirm_sending(call: CallbackQuery):
    await call.message.answer("✅ Bekor qilingan edi!")
    await call.message.delete()


@router.callback_query(AdminFilter(), F.data.startswith('update_process:'))
async def update_sending_process(call: CallbackQuery):
    """Jo'natishni to'xtatish"""
    process_id = int(call.data.split(':')[1])
    process = MailingStatistics.get_process(process_id)
    kb = None
    if not process:
        await call.message.edit_reply_markup(kb)
        return
    if not process.stop:
        kb = await generate_inline_keyboard(
            update_kb, 'uz', data={'process_id': process_id}
        )
    text = process.format_stats()
    try:
        await call.message.edit_text(text, reply_markup=kb)
    except TelegramBadRequest as e:
        if "message is not modified" in str(e):
            await call.answer("✅ Updated")
        else:
            raise


@router.callback_query(AdminFilter(), F.data.startswith('stop_process:'))
async def stop_sending_process(call: CallbackQuery):
    """Jo'natishni to'xtatish"""
    process_id = int(call.data.split(':')[1])
    process = MailingStatistics.get_process(process_id)
    if not process:
        await call.message.edit_reply_markup(None)
        return
    if not process.stop:
        MailingStatistics.stop_process(process_id)
    await call.message.edit_text(
        f"✅ To'xtatildi!\n{process.format_stats()}",
        reply_markup=None
    )


async def main():
    """Asosiy ishchi funksiya"""
    from bot.misc import dp, bot
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
