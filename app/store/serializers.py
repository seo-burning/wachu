from rest_framework import serializers

from store.models import Store, StorePost, PostImage


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ('source_thumb',)


class StorePostSerializer(serializers.ModelSerializer):
    post_image_set = PostImageSerializer(read_only=True, many=True)

    class Meta:
        model = StorePost
        fields = ('post_url', 'post_type', 'post_thumb_image', 'video_source',
                  'post_description', 'post_image_set', )

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        # select_related for "to-one" relationships
        queryset = queryset.prefetch_related('post_image_set')
        return queryset


class StoreSerializer(serializers.ModelSerializer):
    """Serailizer for Store objects"""
    category = serializers.StringRelatedField(many=True)
    region = serializers.StringRelatedField(many=True)
    primary_style = serializers.StringRelatedField(many=False)
    secondary_style = serializers.StringRelatedField(many=False)
    age = serializers.StringRelatedField(many=False)

    class Meta:
        model = Store
        fields = ('insta_id',
                  'current_ranking',
                  'current_ranking_changed',
                  'insta_url',
                  'profile_image',
                  'region',
                  'category',
                  'primary_style',
                  'secondary_style',
                  'age',
                  'facebook_url',
                  'shopee_url',)
        read_only_fields = ('insta_id',
                            'current_ranking',
                            'current_ranking_changed',
                            'insta_url',
                            'profile_image',
                            'region',
                            'category',
                            'primary_style',
                            'secondary_style',
                            'age',
                            'facebook_url',
                            'shopee_url')

    # https://trameltonis.com/en/blog/optimizing-slow-django-rest-framework-performance/
    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        # select_related for "to-one" relationships
        queryset = queryset.select_related('primary_style')
        queryset = queryset.select_related('secondary_style')
        queryset = queryset.select_related('age')
        queryset = queryset.prefetch_related('category')
        queryset = queryset.prefetch_related('region')
        return queryset
