from typing import List

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def generate_inline_keyboard(
        buttons: List[List[dict]],
        lang: str,
        text=None,
        data=None,
) -> InlineKeyboardMarkup:
    """Dinamik inline keyboard yaratish"""
    if text is None:
        text = {}
    if data is None:
        data = {}
    keyboard = []
    for row in buttons:
        kb_btn = []
        for btn in row:
            answer = btn['text'][lang].format(**text) if text else btn['text'][lang]
            callback_data = btn['data'].format(**data) if data else btn['data']
            kb_btn.append(InlineKeyboardButton(text=answer, callback_data=callback_data))
        if kb_btn:
            keyboard.append(kb_btn)

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

confirm_yes = {
    'text': {
        'uz': "✅ Jo'natish",
        'en': "✅ Send",
        'ru': "✅ Отправить"
    },
    'data': 'confirm:yes'
}
confirm_no = {
    'text': {
        'uz': "❌ Bekor qilish",
        'en': "❌ Cancel",
        'ru': "❌ Отмена"
    },
    'data': 'confirm:no'
}

# type
media_group_kb = {
    'text': {
        'uz': "Rasm/Video guruhi",
        'en': "Media Group",
        'ru': "Группа медиа"
    },
    'data': 'message_type:media_group'
}
message_kb = {
    'text': {
        'uz': "Oddiy xabar",
        'en': "Simple message",
        'ru': "Простое сообщение"
    },
    'data': 'message_type:message'
}
type_kb = [
    [
        media_group_kb,
        message_kb
    ],
]

# method
forward_kb = {
    'text': {
        'uz': "Forward",
        'en': "Forward",
        'ru': "Переслать"
    },
    'data': 'send_method:forward'
}
copy_kb = {
    'text': {
        'uz': "Copy",
        'en': "Copy",
        'ru': "Копировать"
    },
    'data': 'send_method:copy'
}
method_kb = [
    [
        forward_kb,
        copy_kb
    ]
]

# audience
channels_kb = {
    'text': {
        'uz': "Kanallar",
        'en': "Channels",
        'ru': "Каналы"
    },
    'data': 'audience:channel'
}
groups_kb = {
    'text': {
        'uz': "Guruhlar",
        'en': "Groups",
        'ru': "Группы"
    },
    'data': 'audience:group'
}
supergroups_kb = {
    'text': {
        'uz': "Super guruhlar",
        'en': "Super groups",
        'ru': "Супер группы"
    },
    'data': 'audience:supergroup'
}
private_kb = {
    'text': {
        'uz': "Shaxsiylar",
        'en': "Private Chats",
        'ru': "Приватные чаты"
    },
    'data': 'audience:private'
}
audience_kb = [
    [
        channels_kb,
    ],
    [
        groups_kb,
    ],
    [
        supergroups_kb,
    ],
    [
        private_kb
    ]
]

# status
active_kb = {
    'text': {
        'uz': "Aktiv",
        'en': "Active",
        'ru': "Активные"
    },
    'data': 'status:active'
}
not_active_kb = {
    'text': {
        'uz': "Aktiv emas",
        'en': "Not Active",
        'ru': "Не активно"
    },
    'data': 'status:inactive'
}
status_kb = [
    [
        active_kb,
    ],
    [
        not_active_kb
    ]
]

# lang
uzbek_kb = {
    'text': {
        'uz': "O'zbek",
        'en': "Uzbek",
        'ru': "Узбекский"
    },
    'data': 'lang:uz'
}
english_kb = {
    'text': {
        'uz': "Ingliz",
        'en': "English",
        'ru': "Английский"
    },
    'data': 'lang:en'
}
russian_kb = {
    'text': {
        'uz': "Rus",
        'en': "Russian",
        'ru': "Русский"
    },
    'data': 'lang:ru'
}
lang_kb = [
    [
        uzbek_kb,
    ],
    [
        english_kb,
    ],
    [
        russian_kb
    ]
]

next_kb = {
    'text': {
        'uz': "⏭ Keyingi",
        'en': "⏭ Next",
        'ru': "⏭ Далее"
    },
    'data': 'get_messages'
}

get_messages_kb = [
    [next_kb]
]

refresh_kb = {
    'text': {
        'uz': "🔄 Yangilash",
        'en': "🔄 Refresh",
        'ru': "🔄 Обновить"
    },
    'data': 'update_process:{process_id}'
}

stop_kb = {
    'text': {
        'uz': "⛔ To‘xtatish",
        'en': "⛔ Stop",
        'ru': "⛔ Остановить"
    },
    'data': 'stop_process:{process_id}'
}

update_kb = [
    [refresh_kb],
    [stop_kb]
]


async def get_filter_keyboard(lang, filters=None):
    # Yangilangan tugmalarni yaratish
    if filters is None:
        filters = {}
    keyboards = [
        type_kb,
        method_kb,
        # audience_kb,
        status_kb,
        lang_kb,
        get_messages_kb
    ]

    inline_kb_list = []
    for kb_type in keyboards:
        for row in kb_type:
            buttons_list = []
            for btn in row:
                is_selected = check_selection(btn['data'], filters)
                text = f"{'✅ ' if is_selected else ''}{btn['text'][lang]}"
                buttons_list.append(InlineKeyboardButton(text=text, callback_data=btn['data']))
            if buttons_list:
                inline_kb_list.append(buttons_list)

    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def check_selection(btn_data, filters):
    if ':' not in btn_data:
        return False
    category, value = btn_data.split(':')
    if category in ['type', 'method']:
        return filters.get(category, '') == value
    return value in filters.get(category, [])
