from django.contrib import admin
from .models import PushNotification, UserNotification, PushNotificationResult
from .expo_notification import send_multiple_push_message
from core.models import UserPushToken
from datetime import datetime
# https://github.com/expo-community/expo-server-sdk-python


# TODO User - Notification Model 도 만들어야함. 이걸로 현재 알람 내역에 대한 리스트 연동 필요.
@admin.register(PushNotification)
class PushNotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'body', 'user_scope', 'is_active', 'publish_date']
    actions = ['make_activate',
               'make_deactivate', 'execute_push_notification']

    def make_activate(self, request, queryset):
        updated_count = queryset.update(is_active=True)
        self.message_user(
            request, '{} Activated 상태로 변경'.format(updated_count))
    make_activate.short_description = 'Activate 상태로 변경'

    def make_deactivate(self, request, queryset):
        updated_count = queryset.update(is_active=False)
        self.message_user(
            request, '{} Deavtivate 상태로 변경'.format(updated_count))
    make_deactivate.short_description = 'Deactivate 상태로 변경'

    # TODO 너무 많아서 Timeout 걸림. 다른 방식 적용 필요.
    def execute_push_notification(self, request, queryset):
        for object in queryset.all():
            user_scope = object.user_scope
            if user_scope == 'ALL':
                push_token_list = UserPushToken.objects.filter(is_active=True)
            total_push = len(push_token_list)
            send_multiple_push_message(token=push_token_list,
                                       title=object.title,
                                       body=object.body,)
            for push_token_obj in push_token_list:
                UserNotification.objects.create(title=object.title,
                                                body=object.body,
                                                data=object.data,
                                                ttl=object.ttl,
                                                expiration=object.expiration,
                                                priority=object.priority,
                                                subtitle=object.subtitle,
                                                sound=object.sound,
                                                badge=object.badge,
                                                channel_id=object.channel_id,
                                                publish_date=datetime.now(),
                                                notification=object,
                                                user=push_token_obj.user,
                                                thumb_image=object.thumb_image,
                                                push_token=push_token_obj
                                                )
            PushNotificationResult.objects.create(notification=object,
                                                  total_push=total_push,
                                                  success_push=total_push,
                                                  fail_push=0)
        queryset.update(is_active=True, publish_date=datetime.now())
    execute_push_notification.short_description = 'Push Notification 실행'


@admin.register(UserNotification)
class UserNotificationAdmin(admin.ModelAdmin):
    pass


@admin.register(PushNotificationResult)
class PushNotificationResultAdmin(admin.ModelAdmin):
    pass
