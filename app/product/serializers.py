from rest_framework import serializers

from product import models
from store.serializers import StoreInlineSerializer
from datetime import datetime, timezone, timedelta


class ProductOptionSerializer(serializers.ModelSerializer):
    size = serializers.StringRelatedField(many=False)
    color = serializers.StringRelatedField(many=False)
    extra_option = serializers.StringRelatedField(many=False)

    class Meta:
        model = models.ProductOption
        fields = '__all__'


class ProductSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductSubCategory
        fields = ('display_name', 'name', 'is_active')


class ProductCategorySerializer(serializers.ModelSerializer):
    productsubcategory_set = ProductSubCategorySerializer(many=True)

    class Meta:
        model = models.ProductCategory
        fields = ('display_name', 'name', 'productsubcategory_set')

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        # select_related for "to-one" relationships
        queryset = queryset.prefetch_related('productsubcategory_set')
        return queryset


class ProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductSize
        fields = ('display_name',)


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductImage
        fields = ('source_thumb', 'post_image_type', 'source')


class ProductRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ('current_review_rating',)


class ShopeeRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ShopeeRating
        fields = ('shopee_view_count', 'shopee_liked_count', 'shopee_sold_count',
                  'shopee_review_count', 'shopee_rating_star',
                  'shopee_1_star_count', 'shopee_2_star_count',
                  'shopee_3_star_count', 'shopee_4_star_count', 'shopee_5_star_count')


class ProductSerializer(serializers.ModelSerializer):
    product_image_set = ProductImageSerializer(read_only=True, many=True)
    sub_category = serializers.StringRelatedField(many=False)
    style = serializers.StringRelatedField(many=False)
    category = serializers.StringRelatedField(many=False)
    color = serializers.StringRelatedField(many=True)
    size = serializers.StringRelatedField(many=True)
    store = StoreInlineSerializer(many=False)
    favorite_users_count = serializers.SerializerMethodField()
    is_new = serializers.SerializerMethodField()
    shopee_rating = ShopeeRatingSerializer(many=False)
    product_options = ProductOptionSerializer(many=True)

    class Meta:
        model = models.Product
        fields = (
            'pk',
            'product_source',
            'product_link',
            'is_new',
            'current_review_rating',
            'shopee_rating',

            'store',
            'post',

            'name',
            'description',

            'product_image_type',
            'product_thumbnail_image',
            'video_source',
            'product_image_set',


            'is_discount',
            'is_free_ship',
            'currency',
            'original_price',
            'discount_price',
            'discount_rate',
            'sold',

            'stock',
            'size',
            'size_chart',

            'category',
            'sub_category',

            'style',
            'color',
            'extra_option',

            'thumb_image_pk',
            'post',

            'product_options',
            'favorite_users_count',
            'updated_at'
        )

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        # select_related for "to-one" relationships
        queryset = queryset.select_related(
            'category',
            'shopee_rating',
            'style',
            'sub_category',
            'store',
            'store__age',
            'store__primary_style',
            'store__secondary_style')
        queryset = queryset.prefetch_related(
            'post__post_image_set',
            'color',
            'size',
            'extra_option',
            'favorite_users',
            'store__favorite_users',
            'store__category',
            'product_image_set',
            'store__product_category',
            'product_options',
            'product_options__size',
            'product_options__color',

        )
        return queryset

    def get_favorite_users_count(self, obj):
        return obj.favorite_users.count()

    def get_is_new(self, obj):
        is_new = False
        time_diff = datetime.now(timezone.utc) - obj.created_at - timedelta(2)
        if time_diff.days < 0:
            is_new = True
        return is_new
