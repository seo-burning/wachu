from rest_framework import serializers

from store.models import StorePost, Store, PostImage
from publish import models

# TODO Need to 최적화 (Nested Serializer)


class StoreSerializer(serializers.ModelSerializer):
    primary_style = serializers.StringRelatedField(many=False)
    secondary_style = serializers.StringRelatedField(many=False)
    age = serializers.StringRelatedField(many=False)

    class Meta:
        model = Store
        fields = ('insta_id', 'insta_url', 'name', 'age',
                  'primary_style', 'secondary_style',
                  'facebook_url', 'shopee_url', 'profile_image')


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ('source_thumb',)


class StorePostSerializer(serializers.ModelSerializer):
    post_image_set = PostImageSerializer(read_only=True, many=True)
    store = StoreSerializer(read_only=True, many=False)

    class Meta:
        model = StorePost
        fields = ('post_url', 'post_type', 'post_thumb_image', 'video_source',
                  'post_description', 'post_image_set', 'store')

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        # select_related for "to-one" relationships
        queryset = queryset.prefetch_related('post_image_set')
        return queryset


class PostGroupSerializer(serializers.ModelSerializer):
    post_list = StorePostSerializer(many=True)

    class Meta:
        model = models.PostGroup
        fields = ('title', 'post_list',)


class MainPagePublishSerializer(serializers.ModelSerializer):
    top_section_post_group = PostGroupSerializer(many=False)
    main_section_post_group_list = PostGroupSerializer(many=True)

    class Meta:
        model = models.MainPagePublish
        fields = ('top_section_post_group', 'main_section_post_group_list',)

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        # select_related for "to-one" relationships
        queryset = queryset.select_related('top_section_post_group')
        queryset = queryset.prefetch_related('main_section_post_group_list')
        return queryset
