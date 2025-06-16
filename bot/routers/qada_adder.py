import logging
import traceback

from aiogram import Router, types, F

from Admin.models import Qada

router = Router(name=__name__)


@router.callback_query(F.data.startswith('qada:'))
async def edit_kb(call: types.CallbackQuery):
    _, prayer, status = call.data.split(':')
    reply_markup = call.message.reply_markup
    for kb in reply_markup.inline_keyboard:
        for btn in kb:
            if prayer in btn.callback_data:
                btn.text = ["O'qidim", "O'qiy olmadim"][int(status)]
                btn.callback_data = f'qada:{prayer}:{[1, 0][int(status)]}'
    await call.message.edit_reply_markup(reply_markup=reply_markup)


@router.callback_query(F.data == 'save_qadas')
async def save_qadas(call: types.CallbackQuery):
    for kb in call.message.reply_markup.inline_keyboard:
        for btn in kb:
            if not 'qada:' in btn.callback_data:
                continue
            _, prayer, status = btn.callback_data.split(':')
            if status == '1':
                continue
            try:
                qada = Qada.objects.get(user__telegram_id=call.from_user.id, prayer=prayer)
            except:
                logging.error(traceback.format_exc())
            else:
                qada.increment(1)
    await call.answer("Saqlandi!")
    await call.message.delete()
