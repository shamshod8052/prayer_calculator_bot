from django.contrib import auth
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.db import models
from django.utils.translation import gettext_lazy as _


class Prayer(models.TextChoices):
    BOMDOD = 'bomdod', _("Bomdod")
    PESHIN = 'peshin', _('Peshin')
    ASR = 'asr', _('Asr')
    SHOM = 'shom', _('Shom')
    XUFTON = 'xufton', _('Xufton')
    VITR = 'vitr', _('Vitr')


class QadaManager(models.Manager):
    def _create_qada(self, user, prayer, number=0):
        qada = self.model(user=user, prayer=prayer, number=number)
        qada.save(using=self._db)
        return qada

    def create_qada(self, user, prayer, number=0):
        return self._create_qada(user, prayer, number)

    def create_default_qadas(self, user, number=0):
        for prayer, name in Prayer.choices:
            self.create_qada(user, prayer, number)


class UserAdminManager(BaseUserManager):
    use_in_migrations = True
    def get_queryset(self):
        return super().get_queryset().filter(is_tg_admin=True)


class TgUserActiveManager(BaseUserManager):
    use_in_migrations = True
    def get_queryset(self):
        return super().get_queryset().filter(tg_status__in=[1, 5])


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, telegram_id, password, **extra_fields):
        """
        Create and save a user with the given telegram_id and password.
        """
        if not telegram_id:
            raise ValueError("The given username must be set")
        user = self.model(telegram_id=telegram_id, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, telegram_id, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(telegram_id, password, **extra_fields)

    def create_superuser(self, telegram_id, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(telegram_id, password, **extra_fields)

    def with_perm(
            self, perm, is_active=True, include_superusers=True, backend=None, obj=None
    ):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    "You have multiple authentication backends configured and "
                    "therefore must provide the `backend` argument."
                )
        elif not isinstance(backend, str):
            raise TypeError(
                "backend must be a dotted import path string (got %r)." % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, "with_perm"):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)
