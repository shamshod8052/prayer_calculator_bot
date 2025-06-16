from aiogram import BaseMiddleware
from aiogram.types import Update
from typing import Callable, Dict, Awaitable, Any
from django.utils.translation import gettext_lazy as _

from Admin.models import CustomUser as User
from bot.functions.check_subscribe import is_user_subscribed


class AuthenticationMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
                       event: Update,
                       data: Dict[str, Any]
                       ) -> Any:
        bot_user = data['event_from_user']
        if bot_user is None:
            return await handler(event, data)

        user, is_created = await User.objects.aget_or_create(telegram_id=bot_user.id)
        data['is_created_user'] = False
        if not user.qadas.exists():
            user.qadas.create_default_qadas(user)
            data['is_created_user'] = True
        user.first_name = bot_user.first_name
        user.last_name = bot_user.last_name
        user.username = bot_user.username
        await user.asave()

        data['user'] = user

        if (event.message and event.message.chat.type != 'private' or
                event.callback_query and event.callback_query.message.chat.type != 'private'):
            return

        is_subscribed, channels_kb = await is_user_subscribed(event.bot, bot_user.id)

        if not is_subscribed:
            text = _("Please subscribe to the following channels:\n\n"
                     "Once subscribed, send the /start command again.")
            return await event.message.answer(str(text), reply_markup=channels_kb)

        return await handler(event, data)
