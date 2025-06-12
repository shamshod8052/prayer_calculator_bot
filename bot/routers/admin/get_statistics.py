from datetime import timedelta
from aiogram import types, Router
from aiogram.filters import Command
from django.db.models import Count, Q
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from Admin.models import CustomUser as User

router = Router(name=__name__)


class Statistics:
    INACTIVE_STATUSES = [
        User.TgStatus.BOT_BLOCKED,
        User.TgStatus.TELEGRAM_NOT_FOUND,
        User.TgStatus.FAILED
    ]

    @classmethod
    async def get_stats(cls):
        today = now().date()
        last_week = today - timedelta(days=7)
        last_month = today - timedelta(days=30)

        # Status-based statistics
        status_stats = await User.objects.aaggregate(
            all_users=Count('id'),
            active_users=Count('id', filter=Q(tg_status=User.TgStatus.ACTIVE)),
            inactive_users=Count('id', filter=Q(tg_status__in=cls.INACTIVE_STATUSES))
        )

        # Growth statistics
        growth_stats = await User.objects.aaggregate(
            today=Count('id', filter=Q(date_joined__date=today)),
            week=Count('id', filter=Q(date_joined__date__gte=last_week)),
            month=Count('id', filter=Q(date_joined__date__gte=last_month))
        )

        return {
            'status': status_stats,
            'growth': growth_stats,
            'current_time': now().strftime("%Y-%m-%d %H:%M:%S")
        }


@router.message(Command("statistics"))
async def send_statistics(message: types.Message, user: User):
    stats = await Statistics.get_stats()

    if user.is_tg_admin:
        text = _(
            f"📊 <b>Statistics</b>\n\n"
            f"👥 <b>Total Users:</b>\n"
            f"1️⃣ All users: {stats['status']['all_users']}\n"
            f"🟢 Active users: {stats['status']['active_users']}\n"
            f"🔴 Inactive users: {stats['status']['inactive_users']}\n\n"
            f"📈 <b>User Growth:</b>\n"
            f"🌅 Today: {stats['growth']['today']}\n"
            f"🗓️ Last week: {stats['growth']['week']}\n"
            f"📆 Last month: {stats['growth']['month']}\n\n"
            f"🕟 <b>Current time:</b> {stats['current_time']}\n"
            f"💻 <b>Admin:</b> @ShamshodR_py"
        )
    else:
        text = _(
            f"📊 <b>Statistics</b>\n\n"
            f"1️⃣ All users: {stats['status']['all_users']}\n\n"
            f"📈 <b>User Growth:</b>\n"
            f"🌅 Today: {stats['growth']['today']}\n"
            f"📆 Last month: {stats['growth']['month']}\n\n"
            f"🕟 <b>Current time:</b> {stats['current_time']}\n"
            f"💻 <b>Admin:</b> @ShamshodR_py"
        )

    await message.answer(str(text))
