from rest_framework import serializers

from store.models import Store, StorePost, PostImage, UserFavoriteStore, UserFavoritePost


class StoreInlineSerializer(serializers.ModelSerializer):
    primary_style = serializers.StringRelatedField(many=False)
    secondary_style = serializers.StringRelatedField(many=False)
    age = serializers.StringRelatedField(many=False)

    class Meta:
        model = Store
        fields = ('insta_id', 'insta_url', 'name', 'age',
                  'primary_style', 'secondary_style', 'category',
                  'facebook_url', 'shopee_url', 'profile_image')


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ('source_thumb',)


class StorePostSerializer(serializers.ModelSerializer):
    post_image_set = PostImageSerializer(read_only=True, many=True)
    store = StoreInlineSerializer(many=False)

    class Meta:
        model = StorePost
        fields = ('post_url', 'post_type', 'post_thumb_image', 'video_source',
                  'post_description', 'post_image_set', 'store')

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        # select_related for "to-one" relationships
        queryset = queryset.select_related('store')
        queryset = queryset.select_related('store__age')
        queryset = queryset.select_related('store__secondary_style')
        queryset = queryset.select_related('store__primary_style')
        queryset = queryset.prefetch_related('store__category')
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
