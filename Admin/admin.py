from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from Admin.models import CustomUser
from .models import Channel


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('name', 'chat_id', 'is_active', 'is_required', 'created_at')
    list_filter = ('is_active', 'is_required')
    search_fields = ('name', 'chat_id', 'url')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('name', 'chat_id', 'url')
        }),
        ('Status', {
            'fields': ('is_active', 'is_required')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    list_editable = ('is_active', 'is_required')
    ordering = ('-id',)
    list_per_page = 20
    actions = ['activate_channels', 'deactivate_channels']

    def get_invite_link(self, obj):
        return obj.get_invite_link()
    get_invite_link.short_description = _('Invite Link')

    @admin.action(description=_('Activate selected channels'))
    def activate_channels(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, _('Activated {} channels').format(updated))

    @admin.action(description=_('Deactivate selected channels'))
    def deactivate_channels(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, _('Deactivated {} channels').format(updated))

    def get_queryset(self, request):
        return super().get_queryset(request).select_related()


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("telegram_id", "password")}),
        (_("Personal info"), {"fields": ("username", "first_name", "last_name", 'language')}),
        (
            _("Permissions"),
            {
                "fields": ("is_active", "is_staff", "is_tg_admin", "is_superuser", "tg_status",),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("telegram_id", "password1", "password2"),
            },
        ),
    )

    list_display = ("id", "telegram_id", "display_name", "is_staff", "is_tg_admin", "language", "tg_status")
    search_fields = ("id", "telegram_id", "first_name", "last_name")
    ordering = ('-id',)
    list_filter = ("is_staff", "is_superuser", "is_active", "language", "tg_status")
    readonly_fields = ("last_login", "date_joined")

    def display_name(self, obj):
        return f"{obj}"

    display_name.short_description = _('Display name')
    display_name.admin_order_field = 'first_name'
