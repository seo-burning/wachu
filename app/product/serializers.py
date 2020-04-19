from rest_framework import serializers

from product import models
from publish.serializers import StoreSerializer
from datetime import datetime, timezone, timedelta


class ProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductSize
        fields = ('display_name',)


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductImage
        fields = ('source_thumb', 'post_image_type', 'source')


class ProductSerializer(serializers.ModelSerializer):
    product_image_set = ProductImageSerializer(read_only=True, many=True)
    sub_category = serializers.StringRelatedField(many=False)
    style = serializers.StringRelatedField(many=False)
    category = serializers.StringRelatedField(many=False)
    color = serializers.StringRelatedField(many=True)
    size = serializers.StringRelatedField(many=True)
    store = StoreSerializer(many=False)
    favorite_users_count = serializers.SerializerMethodField()
    is_new = serializers.SerializerMethodField()

    class Meta:
        model = models.Product
        fields = (
            'pk',
            'product_source',
            'product_link',
            'is_new',

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


            'favorite_users_count'
        )

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        # select_related for "to-one" relationships
        queryset = queryset.select_related(
            'category',
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
            'store__category',
            'product_image_set'
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
