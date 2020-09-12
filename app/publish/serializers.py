from rest_framework import serializers
from django.db.models import Prefetch
from publish import models

# TODO Need to 최적화 (Nested Serializer)


class LinkingBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LinkingBanner
        fields = ('ordering', 'title', 'list_thumb_picture',
                  'cover_picture_1',
                  'cover_picture_2',
                  'cover_picture_3',
                  'cover_picture_4',
                  'link_url',
                  'coupon_code',
                  'banner_type',
                  'primary_color',
                  'secondary_color', 'data')


class ProductGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProductGroup
        fields = ('ordering', 'title',
                  'cover_picture', 'list_thumb_picture')


class ProductTagGroupSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(many=False)
    sub_category = serializers.StringRelatedField(many=False)
    color = serializers.StringRelatedField(many=False)
    style = serializers.StringRelatedField(many=False)
    store = serializers.StringRelatedField(many=False)
    pattern = serializers.StringRelatedField(many=False)

    class Meta:
        model = models.ProductTagGroup
        fields = ('__str__', 'category', 'sub_category',
                  'color', 'style', 'store', 'pattern')

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        # select_related for "to-one" relationships
        queryset = queryset.prefetch_related(
            'store',
            'category',
            'sub_category',
            'color',
            'style',
            'pattern',
        )

        return queryset


class MainPagePublishSerializer(serializers.ModelSerializer):
    producttaggroup_set = ProductTagGroupSerializer(many=True)

    class Meta:
        model = models.MainPagePublish
        fields = ('producttaggroup_set',)

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        # select_related for "to-one" relationships
        queryset = queryset.prefetch_related(
            'producttaggroup_set',
            'producttaggroup_set__store',
            'producttaggroup_set__category',
            'producttaggroup_set__sub_category',
            'producttaggroup_set__color',
            'producttaggroup_set__style',
        )

        return queryset

# https://medium.com/quant-five/speed-up-django-nested-foreign-key-serializers-w-prefetch-related-ae7981719d3f


class BannerPublishSerializer(serializers.ModelSerializer):
    productgroup_set = ProductGroupSerializer(read_only=True, many=True)
    linkingbanner_set = LinkingBannerSerializer(read_only=True, many=True)

    class Meta:
        model = models.BannerPublish
        fields = ('date', 'productgroup_set', 'linkingbanner_set')

# https://medium.com/quant-five/speed-up-django-nested-foreign-key-serializers-w-prefetch-related-ae7981719d3f
    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        # select_related for "to-one" relationships
        # queryset = queryset.prefetch_related(Prefetch(
        #     'postgroup_set',
        #     queryset=models.ProductGroup.objects.order_by('ordering')))
        # queryset = queryset.prefetch_related(
        #     'postgroup_set__post_list',
        #     'postgroup_set__post_list__post_image_set',
        #     'postgroup_set__post_list__store',
        #     'postgroup_set__post_list__store__category',
        #     'postgroup_set__post_list__store__primary_style',
        #     'postgroup_set__post_list__store__secondary_style',
        #     'postgroup_set__post_list__store__age',
        # )
        return queryset


class MagazinePublishSerializer(serializers.ModelSerializer):
    postgroup_set = ProductGroupSerializer(read_only=True, many=True)

    class Meta:
        model = models.MagazinePublish
        fields = ('date', 'postgroup_set',)

# https://medium.com/quant-five/speed-up-django-nested-foreign-key-serializers-w-prefetch-related-ae7981719d3f
    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        # select_related for "to-one" relationships
        queryset = queryset.prefetch_related(Prefetch(
            'postgroup_set',
            queryset=models.ProductGroup.objects.order_by('ordering')))
        queryset = queryset.prefetch_related(
            'postgroup_set__post_list',
            'postgroup_set__post_list__post_image_set',
            'postgroup_set__post_list__store',
            'postgroup_set__post_list__store__category',
            'postgroup_set__post_list__store__primary_style',
            'postgroup_set__post_list__store__secondary_style',
            'postgroup_set__post_list__store__age',
        )

        return queryset
