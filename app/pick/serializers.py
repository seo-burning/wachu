from rest_framework import serializers
from pick import models


class PickSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Pick
        fields = ['image', 'outlink']


class PickABSerializer(serializers.ModelSerializer):
    picks = PickSerializer(many=True)

    class Meta:
        model = models.PickAB
        fields = ('title',
                  'picks', 'is_published')
