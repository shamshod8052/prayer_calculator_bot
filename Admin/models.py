from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import URLValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from helpers.reducer import text_reducer
from .managers import UserManager


class Channel(models.Model):
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=100,
        unique=True,
        help_text=_("Official name of the channel")
    )
    chat_id = models.CharField(
        verbose_name=_("Chat ID"),
        max_length=64,
        unique=True,
        db_index=True,
        help_text=_("Unique identifier or username for the channel/group (@username or -100125369547)")
    )
    url = models.URLField(
        verbose_name=_("Offer link"),
        max_length=255,
        validators=[URLValidator(schemes=['http', 'https', 'tg'])],
        help_text=_("Full URL to access the channel")
    )
    is_active = models.BooleanField(
        verbose_name=_("Is active"),
        default=True,
        db_index=True,
        help_text=_("Whether the channel is currently active")
    )
    is_required = models.BooleanField(
        verbose_name=_("Is required"),
        default=True,
        db_index=True,
        help_text=_("Whether users must join this channel to use the bot")
    )
    created_at = models.DateTimeField(
        verbose_name=_("Created at"),
        auto_now_add=True,
        editable=False
    )
    updated_at = models.DateTimeField(
        verbose_name=_("Updated at"),
        auto_now=True,
        editable=False
    )

    class Meta:
        verbose_name = _("Channel")
        verbose_name_plural = _("Channels")
        ordering = ['name']
        indexes = [
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.name}"

    def get_invite_link(self):
        """Generate proper Telegram invite link"""
        return self.url

    def get_chat_id(self):
        return self.chat_id if self.chat_id.isalpha() else int(self.chat_id)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    class TgStatus(models.IntegerChoices):
        ACTIVE = 1, _('✅ Active')
        BOT_BLOCKED = 2, _('🚫 Blocked the bot')
        TELEGRAM_NOT_FOUND = 3, _('🔴 Telegram Not Found')
        BLOCKED = 4, _('⛔️ Blocked')
        FAILED = 5, _('❗️ Failed')

    password = models.CharField(_("Password"), max_length=128, blank=True)
    first_name = models.CharField(_("First name"), max_length=150, blank=True)
    last_name = models.CharField(_("Last name"), max_length=150, null=True, blank=True)
    username = models.CharField(_("Username"), max_length=150, null=True, blank=True)
    language = models.CharField(max_length=15, choices=settings.LANGUAGES, default='uz')
    telegram_id = models.BigIntegerField(null=True, blank=True, unique=True)
    tg_status = models.IntegerField(choices=TgStatus.choices, default=TgStatus.ACTIVE)
    is_staff = models.BooleanField(
        _("Site admin status"),
        default=False,
        help_text=_("Specifies whether the user can access this admin site"),
    )
    is_tg_admin = models.BooleanField(
        _("Telegram admin status"),
        default=False,
        help_text=_("Specifies whether the user can access the bot admin panel."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()
    USERNAME_FIELD = "telegram_id"

    class Meta:
        ordering = ('-id',)
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        swappable = "AUTH_USER_MODEL"

    def __str__(self):
        return text_reducer(self.full_name or '-', 32)

    @property
    def full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = ' '.join([self.first_name or '', self.last_name or ''])

        return full_name.strip()
