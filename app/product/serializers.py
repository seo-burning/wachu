from rest_framework import serializers

from store.models import StorePost, Store
from product import models


class StoreSerializer(serializers.ModelSerializer):
    primary_style = serializers.StringRelatedField(many=False)
    secondary_style = serializers.StringRelatedField(many=False)
    age = serializers.StringRelatedField(many=False)

    class Meta:
        model = Store
        fields = ('insta_url', 'name', 'age',
                  'primary_style', 'secondary_style',
                  'facebook_url', 'shopee_url', 'profile_image')


class StorePostSerializer(serializers.ModelSerializer):
    store = StoreSerializer(read_only=True, many=False)

    class Meta:
        model = StorePost
        fields = ('post_image', 'name', 'store', 'ordering_keyword')


class SlidingBannerSectionSerializer(serializers.ModelSerializer):
    sliding_banner_post_set = StorePostSerializer(read_only=True, many=True)

    class Meta:
        model = models.SlidingBannerSection
        fields = ('title_head', 'title_colored_keyword',
                  'title_foot', 'sliding_banner_post_set')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["sliding_banner_post_set"] = sorted(
            response["sliding_banner_post_set"],
            key=lambda x: x["ordering_keyword"])
        return response


class MainSectionSerializer(serializers.ModelSerializer):
    main_banner_post_set = StorePostSerializer(read_only=True, many=True)

    class Meta:
        model = models.MainSection
        fields = ('date', 'main_banner_post_set')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["main_banner_post_set"] = sorted(
            response["main_banner_post_set"],
            key=lambda x: x["ordering_keyword"])
        return response
