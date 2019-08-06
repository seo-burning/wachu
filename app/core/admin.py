from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from core import models


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['id', 'email', 'name', ]
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {
         'fields': ('name', 'gender', 'height', 'weight', 'age')}),
        (
            _('Permission'),
            {
                'fields': ('is_active', 'is_staff', 'is_superuser')
            }
        ),
        (_('Important dates'), {
         'fields': ('last_login', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )


admin.site.register(models.Notice)
admin.site.register(models.User, UserAdmin)
