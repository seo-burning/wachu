from rest_framework import serializers

from product import models
from publish.serializers import StorePostSerializer


class ProductSerializer(serializers.ModelSerializer):
    tag = serializers.StringRelatedField(many=True)
    sub_category = serializers.StringRelatedField(many=False)
    style = serializers.StringRelatedField(many=False)
    category = serializers.StringRelatedField(many=False)
    color = serializers.StringRelatedField(many=True)
    post = StorePostSerializer(many=False)

    class Meta:
        model = models.Product
        fields = ('pk', 'name', 'tag',  'style',
                  'post', 'color', 'sub_category', 'price',
                  'category', 'thumb_image_pk', )

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        # select_related for "to-one" relationships
        queryset = queryset.select_related(
            'post', 'category',
            'style',
            'sub_category',
            'post__store',
            'post__store__age',
            'post__store__primary_style',
            'post__store__secondary_style')
        queryset = queryset.prefetch_related('tag',
                                             'post__post_image_set',
                                             'color',
                                             'post__store__category',
                                             )
        return queryset
