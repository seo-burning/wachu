from rest_framework import serializers
from .models import UserNotification, PushNotification


class PushNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PushNotification
        fields = ['title', 'body', 'publish_date', 'thumb_image']


class UserNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNotification
        fields = ['title', 'body', 'publish_date', 'thumb_image']
