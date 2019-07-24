from rest_framework import serializers
from core.models import Notice


class NoticeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notice
        fields = ('date', 'title', 'content')
