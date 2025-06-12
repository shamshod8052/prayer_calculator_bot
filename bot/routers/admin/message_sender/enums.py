from typing import Optional


class Localization:
    """Til resurslarini markazlashtirilgan boshqaruv"""

    TEXTS = {
        # Asosiy interfeys
        'select_message_type': {
            'uz': "⏳ Xabar turini tanlang:",
            'en': "⏳ Select message type:",
            'ru': "⏳ Выберите тип сообщения:"
        },
        'select_send_method': {
            'uz': "📤 Xabar yuborish usulini tanlang:",
            'en': "📤 Choose sending method:",
            'ru': "📤 Выберите способ отправки:"
        },
        'select_audience': {
            'uz': "🎯 Kimlarga yuboramiz?",
            'en': "🎯 Select audience:",
            'ru': "🎯 Выберите аудиторию:"
        },
        'input_message': {
            'uz': "📝 Xabaringizni kirating yoki media jo'nating:",
            'en': "📝 Enter your message or send media:",
            'ru': "📝 Введите сообщение или отправьте медиа:"
        },
        'confirm_send': {
            'uz': "⚠️ Quyidagi xabarni yuborishni tasdiqlaysizmi?",
            'en': "⚠️ Confirm sending this message?",
            'ru': "⚠️ Подтвердите отправку этого сообщения?"
        },

        # Xabarlar va ogohlantirishlar
        'no_users': {
            'uz': "❌ Yuborish uchun foydalanuvchilar topilmadi!",
            'en': "❌ No users found to send!",
            'ru': "❌ Нет пользователей для отправки!"
        },
        'sending_started': {
            'uz': "🚀 Xabar yuborish boshlandi! Jami: {count} ta",
            'en': "🚀 Sending started! Total: {count}",
            'ru': "🚀 Начата отправка! Всего: {count}"
        },
        'sending_completed': {
            'uz': "✅ Xabar yuborish tugallandi!\nMuvaffaqiyatli: {success}\nXatolar: {failed}",
            'en': "✅ Sending completed!\nSuccess: {success}\nFailed: {failed}",
            'ru': "✅ Отправка завершена!\nУспешно: {success}\nОшибки: {failed}"
        },
        'operation_canceled': {
            'uz': "❌ Amal bekor qilindi!",
            'en': "❌ Operation canceled!",
            'ru': "❌ Операция отменена!"
        },

        # Tugma matnlari
        'btn_media_group': {
            'uz': "🖼 Media guruhi",
            'en': "🖼 Media group",
            'ru': "🖼 Группа медиа"
        },
        'btn_text_message': {
            'uz': "📝 Oddiy xabar",
            'en': "📝 Text message",
            'ru': "📝 Текстовое сообщение"
        },
        'btn_forward': {
            'uz': "↗️ Forward",
            'en': "↗️ Forward",
            'ru': "↗️ Переслать"
        },
        'btn_copy': {
            'uz': "📋 Copy",
            'en': "📋 Copy",
            'ru': "📋 Копировать"
        },
        'btn_all_users': {
            'uz': "👥 Hammaga",
            'en': "👥 Everyone",
            'ru': "👥 Всем"
        },
        'btn_active_users': {
            'uz': "⭐️ Faollar",
            'en': "⭐️ Actives",
            'ru': "⭐️ Активные"
        },

        # Statistika
        'stats_header': {
            'uz': "📊 Bot statistikasi:",
            'en': "📊 Bot statistics:",
            'ru': "📊 Статистика бота:"
        },
        'stats_total': {
            'uz': "👤 Jami foydalanuvchilar:",
            'en': "👤 Total users:",
            'ru': "👤 Всего пользователей:"
        },
        'stats_active': {
            'uz': "✅ Faol foydalanuvchilar:",
            'en': "✅ Active users:",
            'ru': "✅ Активные пользователи:"
        },

        # Xatoliklar
        'err_general': {
            'uz': "⚠️ Xatolik yuz berdi! Iltimos qayta urinib ko'ring.",
            'en': "⚠️ An error occurred! Please try again.",
            'ru': "⚠️ Произошла ошибка! Пожалуйста, попробуйте снова."
        },
        'err_admin_only': {
            'uz': "⛔ Bu buyruq faqat adminlar uchun!",
            'en': "⛔ This command is for admins only!",
            'ru': "⛔ Эта команда только для админов!"
        },

        # Quiz bilan bog'liq
        'quiz_question': {
            'uz': "❓ Savol: {question}",
            'en': "❓ Question: {question}",
            'ru': "❓ Вопрос: {question}"
        },
        'quiz_correct': {
            'uz': "✅ To'g'ri javob!",
            'en': "✅ Correct answer!",
            'ru': "✅ Правильный ответ!"
        },
        'quiz_wrong': {
            'uz': "❌ Noto'g'ri! To'g'ri javob: {answer}",
            'en': "❌ Wrong! Correct answer: {answer}",
            'ru': "❌ Неправильно! Правильный ответ: {answer}"
        }
    }

    @classmethod
    async def get_text(cls, key: str, lang: Optional[str]=None, **kwargs) -> str:
        """Formatlash imkoniyati bilan matnni olish"""
        text = cls.TEXTS.get(key, {}).get(lang or 'uz')
        return text.format(**kwargs) if kwargs else text
