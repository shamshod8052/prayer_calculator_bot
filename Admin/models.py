import logging

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import URLValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from helpers.reducer import text_reducer
from helpers.tele_bot import tele_bot
from .managers import UserManager, QadaManager, Prayer, UserAdminManager, ActiveManager, ActiveManager, \
    TgUserActiveManager
from .prayer import PresentDay


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
    actives = TgUserActiveManager()
    tg_admins = UserAdminManager()
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

class Qada(models.Model):
    objects = QadaManager()

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='qadas',
        db_index=True,
        verbose_name=_('User')
    )
    prayer = models.CharField(
        max_length=6,
        choices=Prayer.choices,
        db_index=True,
        verbose_name=_('Prayer')
    )
    number = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Number of qada(Day)'),
        help_text=_('Count of missed prayers to be made up')
    )
    last_updated = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Last updated'),
        editable=False
    )

    class Meta:
        verbose_name = _('Qada prayer')
        verbose_name_plural = _('Qada prayers')
        unique_together = ('user', 'prayer')
        ordering = ['id']
        indexes = [
            models.Index(fields=['user', 'prayer']),
            models.Index(fields=['last_updated']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(number__gte=0),
                name='non_negative_qada_count'
            )
        ]

    def __str__(self):
        return f"{self.get_prayer_display()} ({self.number}) - {self.user}"

    @property
    def name(self):
        return f"{Prayer(self.prayer).label}"

    def increment(self, value=1, save=True):
        """Atomically increment the qada count"""
        if value < 0:
            raise ValueError("Increment value must be positive")
        self.number = models.F('number') + value
        if save:
            self.save(update_fields=['number', 'last_updated'])
        return self

    def decrement(self, value=1, save=True):
        """Atomically decrement the qada count, preventing negative values"""
        if value < 0:
            raise ValueError("Decrement value must be positive")
        self.number = models.F('number') - value
        if save:
            # Use Greatest to prevent negative numbers
            self.number = models.functions.Greatest(models.F('number') - value, 0)
            self.save(update_fields=['number', 'last_updated'])
        return self

    def reset(self, save=True):
        """Reset the qada count to zero"""
        self.number = 0
        if save:
            self.save(update_fields=['number', 'last_updated'])
        return self

    @property
    def is_outstanding(self):
        """Check if there are any qada prayers to make up"""
        return self.number > 0


class Province(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)

    actives = ActiveManager()

    class Meta:
        verbose_name = _("Province")
        verbose_name_plural = _("Provinces")
        ordering = ['name']

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, unique=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='districts')
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    actives = ActiveManager()

    class Meta:
        verbose_name = _("District")
        verbose_name_plural = _("Districts")
        unique_together = ('name', 'province', 'slug')
        ordering = ['name']

    def __str__(self):
        return f"{self.name}, {self.province.name}"

    @property
    def prayer_time(self):
        return PresentDay(self.name, self.province.slug)


class FAQ(models.Model):
    question = models.TextField(verbose_name=_('Question'))
    answer = models.TextField(verbose_name=_('Answer'))
    video = models.FileField(verbose_name=_('Video'), upload_to='faq_videos', blank=True, null=True)
    photo = models.ImageField(verbose_name=_('Photo'), upload_to='faq_photos', blank=True, null=True)
    voice = models.FileField(verbose_name=_('Voice'), upload_to='faq_voices', blank=True, null=True)
    video_file_id = models.CharField(max_length=100, null=True, blank=True, editable=False)
    photo_file_id = models.CharField(max_length=100, null=True, blank=True, editable=False)
    voice_file_id = models.CharField(max_length=100, null=True, blank=True, editable=False)
    saved_video_path = models.CharField(_('Saved Video Path'), max_length=255, null=True, blank=True, editable=False)
    saved_photo_path = models.CharField(_('Saved Photo Path'), max_length=255, null=True, blank=True, editable=False)
    saved_voice_path = models.CharField(_('Saved Voice Path'), max_length=255, null=True, blank=True, editable=False)

    created_at = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("Updated at"), auto_now=True)
    is_active = models.BooleanField(verbose_name=_("Is active"), default=True)

    actives = ActiveManager()

    class Meta:
        verbose_name = _("FAQ")
        verbose_name_plural = _("FAQs")
        ordering = ['id']

    def __str__(self):
        return text_reducer(self.question, 32)

    def is_video_synchronized(self):
        return self.video and self.video.path == self.saved_video_path

    def is_photo_synchronized(self):
        return self.photo and self.photo.path == self.saved_photo_path

    def is_voice_synchronized(self):
        return self.voice and self.voice.path == self.saved_voice_path

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        updated_fields = []

        # VIDEO
        if not self.is_video_synchronized():
            try:
                with open(self.video.path, 'rb') as f:
                    response = tele_bot.send_video(
                        chat_id=settings.DEFAULT_BOT_CHAT,
                        video=f
                    )
            except Exception as e:
                logging.error(f"[FAQ][Video] Telegramga yuborishda xatolik: {e}")
            else:
                self.video_file_id = response.video.file_id
                self.saved_video_path = self.video.path
                updated_fields += ['video_file_id', 'saved_video_path']

        # PHOTO
        if not self.is_photo_synchronized():
            try:
                with open(self.photo.path, 'rb') as f:
                    response = tele_bot.send_photo(
                        chat_id=settings.DEFAULT_BOT_CHAT,
                        photo=f
                    )
            except Exception as e:
                logging.error(f"[FAQ][Photo] Telegramga yuborishda xatolik: {e}")
            else:
                self.photo_file_id = response.photo[-1].file_id  # eng katta o‘lcham
                self.saved_photo_path = self.photo.path
                updated_fields += ['photo_file_id', 'saved_photo_path']

        # VOICE
        if not self.is_voice_synchronized():
            try:
                with open(self.voice.path, 'rb') as f:
                    response = tele_bot.send_voice(
                        chat_id=settings.DEFAULT_BOT_CHAT,
                        voice=f
                    )
            except Exception as e:
                logging.error(f"[FAQ][Voice] Telegramga yuborishda xatolik: {e}")
            else:
                self.voice_file_id = response.voice.file_id
                self.saved_voice_path = self.voice.path
                updated_fields += ['voice_file_id', 'saved_voice_path']

        # Update only if needed
        if updated_fields:
            super().save(update_fields=updated_fields)
