from rest_framework import serializers

from store.models import StorePost
from product import models


class StorePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorePost
        fields = ('post_image',)


class SlidingBannerSectionSerializer(serializers.ModelSerializer):
    sliding_banner_post_set = StorePostSerializer(read_only=True, many=True)

    class Meta:
        model = models.SlidingBannerSection
        fields = ('title_head', 'title_colored_keyword',
                  'title_foot', 'sliding_banner_post_set')


class MainSectionSerializer(serializers.ModelSerializer):
    main_banner_post_set = StorePostSerializer(read_only=True, many=True)

    class Meta:
        model = models.MainSection
        fields = ('date', 'main_banner_post_set')
