from rest_framework import serializers

from product import models
from publish.serializers import StorePostSerializer


# class StorePostSerializer(serializers.ModelSerializer):
#     post_image_set = PostImageSerializer(read_only=True, many=True)
#     store = serializers.PrimaryKeyRelatedField(read_only=True, many=False)

#     class Meta:
#         model = StorePost
#         fields = ('pk', 'post_url', 'post_type', 'post_thumb_image',
#                   'video_source',
#                   'post_description', 'post_image_set', 'store')

#     @staticmethod
#     def setup_eager_loading(queryset):
#         """ Perform necessary eager loading of data. """
#         # select_related for "to-one" relationships
#         queryset = queryset.select_related('store')
#         queryset = queryset.prefetch_related('post_image_set')
#         return queryset


class ProductSerializer(serializers.ModelSerializer):
    tag = serializers.StringRelatedField(many=True)
    sub_category = serializers.StringRelatedField(many=False)
    style = serializers.StringRelatedField(many=False)
    post = StorePostSerializer(many=False)

    class Meta:
        model = models.Product
        fields = ('pk', 'name', 'tag',  'style',
                  'post', 'color', 'sub_category')

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        # select_related for "to-one" relationships
        queryset = queryset.select_related(
            'post',
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
