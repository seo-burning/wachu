from rest_framework import serializers

from store.models import Store, StorePost, PostImage, StoreAddress
from product.models import ProductCategory


class ProductCategoryMinSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCategory
        fields = ('display_name', 'name')


class StoreInlineSerializer(serializers.ModelSerializer):
    primary_style = serializers.StringRelatedField(many=False)
    secondary_style = serializers.StringRelatedField(many=False)
    age = serializers.StringRelatedField(many=False)
    category = serializers.StringRelatedField(many=True)
    favorite_users_count = serializers.SerializerMethodField()
    product_category = ProductCategoryMinSerializer(many=True)

    class Meta:
        model = Store
        fields = ('pk', 'insta_id', 'insta_url', 'name', 'age',
                  'primary_style', 'secondary_style', 'category',
                  'shopee_url',
                  'phone',
                  'facebook_id',
                  'facebook_numeric_id',
                  'current_ranking',
                  'insta_url',
                  'facebook_url',
                  'dosiin_url',
                  'homepage_url',
                  'profile_image',
                  'current_review_rating',
                  'recent_post_1',
                  'recent_post_2',
                  'recent_post_3', 'favorite_users_count',
                  'product_category'
                  )

    def get_favorite_users_count(self, obj):
        return obj.favorite_users.count()


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ('source_thumb', 'post_image_type', 'source')


class StoreAddressSerializer(serializers.ModelSerializer):
    store = StoreInlineSerializer(many=False)

    class Meta:
        model = StoreAddress
        fields = ('store', 'address', 'region', 'google_map_url',
                  'X_axis', 'Y_axis')

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        # select_related for "to-one" relationships
        queryset = queryset.select_related('store__primary_style')
        queryset = queryset.select_related('store__secondary_style')
        queryset = queryset.select_related('store__age')
        queryset = queryset.prefetch_related('store__store_address_set__region')
        queryset = queryset.prefetch_related('store__category')
        queryset = queryset.prefetch_related('store__favorite_users')
        queryset = queryset.prefetch_related('store__store_address_set')
        queryset = queryset.prefetch_related('store__product_category')

        return queryset


class StoreAddressInlineSerializer(serializers.ModelSerializer):
    region = serializers.StringRelatedField(many=False)

    class Meta:
        model = StoreAddress
        fields = ('address', 'region', 'google_map_url',
                  'X_axis', 'Y_axis')


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
    primary_style = serializers.StringRelatedField(many=False)
    secondary_style = serializers.StringRelatedField(many=False)
    age = serializers.StringRelatedField(many=False)
    favorite_users_count = serializers.SerializerMethodField()
    # store_address_set = StoreAddressInlineSerializer(many=True)
    product_category = ProductCategoryMinSerializer(many=True)

    class Meta:
        model = Store
        fields = ('pk', 'is_new_post', 'insta_id',
                  'profile_image',
                  'category',
                  'primary_style',
                  'secondary_style',
                  'age',
                  'phone',
                  'current_review_rating',
                  'current_ranking',
                  'shopee_url',
                  'facebook_id',
                  'facebook_numeric_id',
                  'insta_url',
                  'facebook_url',
                  'dosiin_url',
                  'homepage_url',
                  'recent_post_1',
                  'recent_post_2',
                  'recent_post_3',
                  'favorite_users_count',
                  #   'store_address_set',
                  'product_category'
                  )
        read_only_fields = ('insta_id', 'pk', 'is_new_post',
                            'profile_image',
                            'category',
                            'primary_style',
                            'secondary_style',
                            'age',
                            'facebook_numeric_id',
                            'current_review_rating',
                            'facebook_id',
                            'recent_post_1',
                            'recent_post_2',
                            'recent_post_3',
                            'favorite_users_count',
                            # 'store_address_set',
                            'product_category'
                            )

    # https://trameltonis.com/en/blog/optimizing-slow-django-rest-framework-performance/
    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        # select_related for "to-one" relationships
        queryset = queryset.select_related('primary_style')
        queryset = queryset.select_related('secondary_style')
        queryset = queryset.select_related('age')
        queryset = queryset.prefetch_related('store_address_set__region')
        queryset = queryset.prefetch_related('category')
        queryset = queryset.prefetch_related('favorite_users')
        queryset = queryset.prefetch_related('store_address_set', 'product_category')

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
            'recent_post_1',
            'recent_post_2',
            'recent_post_3')
        read_only_fields = ('is_new_post',
                            'insta_id',
                            'recent_post_1',
                            'recent_post_2',
                            'recent_post_3')


class StoreRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ('current_review_rating',)
