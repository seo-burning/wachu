from rest_framework import serializers

from product import models
from publish.serializers import StorePostSerializer


class ProductSerializer(serializers.ModelSerializer):
    tag = serializers.StringRelatedField(many=True)
    post = StorePostSerializer(many=False)

    class Meta:
        model = models.Product
        fields = ('pk', 'name', 'tag', 'post')

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        # select_related for "to-one" relationships
        queryset = queryset.select_related('post')
        queryset = queryset.prefetch_related('tag',
                                             'post__post_image_set',
                                             'post__store',
                                             'post__store__category',
                                             'post__store__primary_style',
                                             'post__store__secondary_style',
                                             'post__store__age',
                                             )
        return queryset
