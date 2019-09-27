from rest_framework import serializers
from store.models import Store

from pick import models


class StoreSerializer(serializers.ModelSerializer):
    primary_style = serializers.StringRelatedField(many=False)
    secondary_style = serializers.StringRelatedField(many=False)
    age = serializers.StringRelatedField(many=False)

    class Meta:
        model = Store
        fields = ('insta_id', 'insta_url', 'name', 'age',
                  'primary_style', 'secondary_style',
                  'facebook_url', 'facebook_id', 'profile_image')


class ChuPickRatingSerializer(serializers.ModelSerializer):
    store = StoreSerializer(read_only=True, many=False)

    class Meta:
        model = models.ChuPickRating
        fields = ('title', 'store', 'outlink', 'pick_image',)


class ChuPickABSerializer(serializers.ModelSerializer):
    store_a = StoreSerializer(read_only=True, many=False)
    store_b = StoreSerializer(read_only=True, many=False)

    class Meta:
        model = models.ChuPickAB
        fields = ('title',
                  'store_a', 'store_b',
                  'outlink_a', 'outlink_b',
                  'pick_image_a', 'pick_image_b')


class ChuPickSetSerializer(serializers.ModelSerializer):
    chu_pick_rating_set = ChuPickRatingSerializer(read_only=True, many=True)
    chu_pick_AB_set = ChuPickABSerializer(read_only=True, many=True)

    class Meta:
        model = models.ChuPickSet
        fields = ('chu_pick_rating_set', 'chu_pick_AB_set', 'date')
