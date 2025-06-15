from itertools import islice

from aiogram import Router, types, F
from aiogram.types import InlineKeyboardButton

from Admin.models import FAQ
from bot.keyboards.keyboard_paginator import Paginator, BackButton

router = Router(name=__name__)
THUMBNAIL_URL = "https://fv5-7.files.fm/thumb_show.php?i=sgfdexsnbv&view&v=1&PHPSESSID=1118e8efd6460177c58c328b67807e1ad6c923b2"


@router.callback_query(F.data.startswith('page_faq:'))
@router.callback_query(F.data == 'faq')
async def view_faq(call: types.CallbackQuery):
    if call.data.startswith('page_faq:'):
        page_num = int(call.data.split(':')[1])
    else:
        page_num = 1
    quests_num = 10
    text = "<b>Ko'p beriladigan savollar</b>\n\n"
    begin = (page_num - 1) * quests_num
    end = page_num * quests_num
    text += '\n'.join(
        [
            f"{n + 1}. {faq.question}"
            for n, faq in zip(
                range(begin, end), FAQ.actives.all()[begin:end])
        ]
    )
    rows_list = [
        InlineKeyboardButton(text=f"{n}", switch_inline_query_current_chat=f"{n}")
        for n in range(1, FAQ.actives.count() + 1)
    ]
    it = iter(rows_list)
    rows_list = list(iter(lambda: list(islice(it, 5)), []))
    back = BackButton(text="Orqaga", callback_data="main_menu")
    paginator = Paginator(rows_list, 2, back, True)
    kb = paginator.get_page(page_num, 'faq').as_markup()

    await call.message.edit_text(text, reply_markup=kb)


@router.inline_query()
async def inline_query_handler(inline_query: types.InlineQuery):
    results = []
    if inline_query.query and inline_query.query.isdigit():
        faq_id = int(inline_query.query)
        try:
            faq_obj = FAQ.actives.get(id=faq_id)
        except:
            ...
        else:
            if faq_obj.video:
                results = [
                    types.InlineQueryResultVideo(
                        id=f"{faq_id}",
                        title="Savol-javob",
                        mime_type="video/mp4",
                        video_url=faq_obj.video_file_id,
                        thumbnail_url=THUMBNAIL_URL,
                        caption=f"{faq_obj.question}\n\n{faq_obj.answer}",
                        description=f"{faq_obj.question}\n\n{faq_obj.answer}",
                    ),
                ]
            elif faq_obj.photo:
                results = [
                    types.InlineQueryResultPhoto(
                        id=f"{faq_id}",
                        title="Savol-javob",
                        photo_url=faq_obj.photo_file_id,
                        thumbnail_url=THUMBNAIL_URL,
                        caption=f"{faq_obj.question}\n\n{faq_obj.answer}",
                        description=f"{faq_obj.question}\n\n{faq_obj.answer}",
                    ),
                ]
            elif faq_obj.voice:
                results = [
                    types.InlineQueryResultVoice(
                        id=f"{faq_id}",
                        title="Savol-javob",
                        voice_url=faq_obj.voice_file_id,
                        caption=f"{faq_obj.question}\n\n{faq_obj.answer}",
                        description=f"{faq_obj.question}\n\n{faq_obj.answer}",
                    ),
                ]
            else:
                results = [
                    types.InlineQueryResultArticle(
                        id=f"{faq_id}",
                        title="Savol-javob",
                        caption=faq_obj.question or '',
                        thumbnail_url=THUMBNAIL_URL,
                        input_message_content=types.InputTextMessageContent(
                            message_text=f"{faq_obj.question}\n\n{faq_obj.answer}",
                            disable_web_page_preview=True,
                        ),
                        description=f"{faq_obj.question}\n\n{faq_obj.answer}",
                    ),
                ]
    if not results:
        results = [
            types.InlineQueryResultArticle(
                id="-1",
                title="Mavjud emas",
                input_message_content=types.InputTextMessageContent(
                    message_text="Bunday savol-javob topilmadi!"
                ),
                description="Bunday savol-javob topilmadi!",
            ),
        ]
    await inline_query.answer(results, cache_time=1)
