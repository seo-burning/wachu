from rest_framework import serializers
from .models import UserNotification, PushNotification


class PushNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PushNotification
        fields = ['title', 'body', 'publish_date', 'pk',
                  'thumb_image', 'data']


class UserNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNotification
        fields = ['title', 'body', 'publish_date', 'pk',
                  'thumb_image', 'data', 'is_read']


class UserNotificationReadUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNotification
        fields = ['is_read', ]
