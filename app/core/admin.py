from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Helper function for translation
from django.utils.translation import gettext as _

from core import models


class UserAdmin(BaseUserAdmin):
    # Create a custom user admin

    # List them by email and name and ordering by id
    ordering = ['id']
    list_display = ['email', 'name']

    # This is from Django admin doc:
    # https://docs.djangoproject.com/en/2.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.fieldsets
    fieldsets = (
        (
            None,
            {'fields': ('email', 'password')}
        ),
        (
            _('Personal Info'),
            {'fields': ('name',)}
        ),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (
            _('Important dates'),
            {'fields': ('last_login',)}
        )
    )

    # Customize default fieldset to only use email, password, password2
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )


admin.site.register(models.User, UserAdmin)
