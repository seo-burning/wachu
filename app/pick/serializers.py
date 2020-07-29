from rest_framework import serializers
from pick import models


class PickSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Pick
        fields = ['pk', 'image', 'image_outlink', 'outlink', 'product']


class PickABSerializer(serializers.ModelSerializer):
    picks = PickSerializer(many=True)

    class Meta:
        model = models.PickAB
        fields = ('title', 'pk',
                  'picks', 'is_published')


class PickABResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PickABResult
        fields = ('pick_AB', 'pick_A', 'pick_B', 'selection')
