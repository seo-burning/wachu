from rest_framework import serializers

from store.models import Store, StorePost, PostImage


class StoreInlineSerializer(serializers.ModelSerializer):
    primary_style = serializers.StringRelatedField(many=False)
    secondary_style = serializers.StringRelatedField(many=False)
    age = serializers.StringRelatedField(many=False)
    category = serializers.StringRelatedField(many=True)
    favorite_users_count = serializers.SerializerMethodField()

    class Meta:
        model = Store
        fields = ('insta_id', 'insta_url', 'name', 'age',
                  'primary_style', 'secondary_style', 'category',
                  'facebook_numeric_id', 'facebook_id', 'profile_image',
                  'recent_post_1',
                  'recent_post_2',
                  'recent_post_3', 'favorite_users_count')

    def get_favorite_users_count(self, obj):
        return obj.favorite_users.count()


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ('source_thumb', 'post_image_type', 'source')


class StorePostSerializer(serializers.ModelSerializer):
    post_image_set = PostImageSerializer(read_only=True, many=True)
    store = StoreInlineSerializer(many=False)

    class Meta:
        model = StorePost
        fields = ('pk', 'post_url', 'post_type', 'post_thumb_image',
                  'video_source',
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
    favorite_users_count = serializers.SerializerMethodField()

    class Meta:
        model = Store
        fields = ('pk', 'is_new_post', 'insta_id',
                  'current_ranking',
                  'insta_url',
                  'profile_image',
                  'region',
                  'category',
                  'primary_style',
                  'secondary_style',
                  'age',
                  'facebook_numeric_id',
                  'facebook_id',
                  'recent_post_1',
                  'recent_post_2',
                  'recent_post_3',
                  'favorite_users_count'
                  )
        read_only_fields = ('insta_id', 'pk', 'is_new_post',
                            'current_ranking',
                            'insta_url',
                            'profile_image',
                            'region',
                            'category',
                            'primary_style',
                            'secondary_style',
                            'age',
                            'facebook_numeric_id',
                            'facebook_id',
                            'recent_post_1',
                            'recent_post_2',
                            'recent_post_3',
                            'favorite_users_count')

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
        queryset = queryset.prefetch_related('favorite_users')
        return queryset

    def get_favorite_users_count(self, obj):
        return obj.favorite_users.count()


class StoreListSerializer(serializers.ModelSerializer):
    """Serailizer for Store objects"""

    class Meta:
        model = Store
        fields = (
            'is_new_post',
            'insta_id',
            'current_ranking',
            'recent_post_1',
            'recent_post_2',
            'recent_post_3')
        read_only_fields = ('is_new_post',
                            'insta_id',
                            'current_ranking',
                            'recent_post_1',
                            'recent_post_2',
                            'recent_post_3')
