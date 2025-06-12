import logging
from typing import List

from asgiref.sync import sync_to_async
from django.db.models import Q

from Admin.models import CustomUser as User

logger = logging.getLogger(__name__)


class UserManager:
    """Foydalanuvchilarni filtrlash"""

    @staticmethod
    @sync_to_async
    def get_users(data: dict, django_filter: Q=Q()) -> List[int]:
        filters = Q()

        if data.get('audience'):
            filters &= Q(chat_type__in=data['audience'])

        if data.get('lang'):
            filters &= Q(language__in=data['lang'])

        status_filter = Q()
        if 'active' in data.get('status', []):
            status_filter |= Q(tg_status=1)
        if 'inactive' in data.get('status', []):
            status_filter |= ~Q(tg_status=1)

        if data.get('send_test', False):
            filters &= Q(send_test=True)

        filters &= status_filter
        filters &= django_filter

        return list(User.objects.filter(filters).values_list('telegram_id', flat=True))