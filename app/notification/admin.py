from django.contrib import admin
from .models import PushNotification


@admin.register(PushNotification)
class PushNotificationAdmin(admin.ModelAdmin):
    pass
