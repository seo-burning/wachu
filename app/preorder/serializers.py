from rest_framework import serializers
from preorder.models import PreorderCampaign
from product.serializers import ProductSerializer


class PreorderCampaignSerialzier(serializers.ModelSerializer):
    product_set = ProductSerializer(many=True)

    class Meta:
        model = PreorderCampaign
        fields = ['start_at', 'end_at', 'estimated_delivery_date',
                  'cover_picture', 'list_thumb_picture', 'name',
                  'display_name', 'product_set']

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        # select_related for "to-one" relationships
        queryset = queryset.select_related(
        )
        queryset = queryset.prefetch_related(
            'product_set__category',
            'product_set__shopee_rating',
            'product_set__style',
            'product_set__sub_category',
            'product_set__store',
            'product_set__store__age',
            'product_set__store__primary_style',
            'product_set__store__secondary_style',
            'product_set__post__post_image_set',
            'product_set__color',
            'product_set__size',
            'product_set__extra_option',
            'product_set__favorite_users',
            'product_set__store__favorite_users',
            'product_set__store__category',
            'product_set__product_image_set',
            'product_set__store__product_category',
            'product_set__product_options',
            'product_set__product_options__size',
            'product_set__product_options__color',
            'product_set__product_options__extra_option',

        )
        return queryset
