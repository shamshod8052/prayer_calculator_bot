from aiogram.filters import Filter
from aiogram.types import Message

from Admin.models import CustomUser as User


class AdminFilter(Filter):
    async def __call__(self, message: Message) -> bool:
        try:
            user = User.objects.get(telegram_id=message.from_user.id)
            return user.is_tg_admin
        except User.DoesNotExist:
            ...
        return False