from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.db.models.functions import TruncDay
import json
from core import models
from core.models import ExportCsvMixin


class UserAdmin(BaseUserAdmin, ExportCsvMixin):
    ordering = ['id']
    list_display = ['id', 'email', 'name', ]
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {
         'fields': ('information_status',
                    'name',
                    'gender',
                    'age',
                    'profile_image',
                    'height',
                    'weight',
                    'region',
                    'primary_style',
                    'secondary_style'
                    )}),
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
    actions = ['export_as_csv']
    search_fields = ['email', 'name']

    def changelist_view(self, request, extra_context=None):
        # Aggregate new subscribers per day
        chart_data = (
            models.User.objects.annotate(date=TruncDay("created_at"))
            .values("date")
            .annotate(y=Count("id"))
            .order_by("-date")
        )

        # Serialize and attach the chart data to the template context
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data": as_json}

        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)


admin.site.register(models.Notice)
admin.site.register(models.UserPushToken)
admin.site.register(models.Region)
admin.site.register(models.User, UserAdmin)
