from rest_framework import serializers

from store.models import StorePost, Store, PostImage

from django.db.models import Prefetch

from publish import models

# TODO Need to 최적화 (Nested Serializer)


class StoreSerializer(serializers.ModelSerializer):
    primary_style = serializers.StringRelatedField(many=False)
    secondary_style = serializers.StringRelatedField(many=False)
    age = serializers.StringRelatedField(many=False)
    category = serializers.StringRelatedField(many=True)
    favorite_users_count = serializers.SerializerMethodField()

    class Meta:
        model = Store
        fields = ('pk', 'insta_id', 'insta_url', 'name', 'age',
                  'primary_style',
                  'secondary_style',
                  'category',
                  'current_review_rating',
                  'facebook_id',
                  'facebook_numeric_id',
                  'current_ranking',
                  'facebook_url',
                  'homepage_url', 'shopee_url',
                  'facebook_numeric_id',
                  'facebook_id',
                  'profile_image',
                  'favorite_users_count',
                  )

    def get_favorite_users_count(self, obj):
        return obj.favorite_users.count()


class LinkingBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LinkingBanner
        fields = ('ordering', 'title', 'list_thumb_picture',
                  'cover_picture_1',
                  'cover_picture_2',
                  'cover_picture_3',
                  'cover_picture_4',
                  'link_url', 'banner_type')


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ('source_thumb', 'post_image_type', 'source')


class StorePostSerializer(serializers.ModelSerializer):
    post_image_set = PostImageSerializer(read_only=True, many=True)
    store = StoreSerializer(read_only=True, many=False)

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


class PostGroupSerializer(serializers.ModelSerializer):
    post_list = StorePostSerializer(many=True)

    class Meta:
        model = models.PostGroup
        fields = ('ordering', 'title', 'post_list',
                  'cover_picture', 'list_thumb_picture')


class PostTagGroupSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(many=False)
    sub_category = serializers.StringRelatedField(many=False)
    color = serializers.StringRelatedField(many=False)
    style = serializers.StringRelatedField(many=False)
    store = serializers.StringRelatedField(many=False)

    class Meta:
        model = models.PostTagGroup
        fields = ('__str__', 'category', 'sub_category',
                  'color', 'style', 'store')


class MainPagePublishSerializer(serializers.ModelSerializer):
    posttaggroup_set = PostTagGroupSerializer(many=True)

    class Meta:
        model = models.MainPagePublish
        fields = ('posttaggroup_set',)

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        # select_related for "to-one" relationships
        queryset = queryset.prefetch_related(
            'posttaggroup_set',
            'posttaggroup_set__store',
            'posttaggroup_set__category',
            'posttaggroup_set__sub_category',
            'posttaggroup_set__color',
            'posttaggroup_set__style',
        )

        return queryset

# https://medium.com/quant-five/speed-up-django-nested-foreign-key-serializers-w-prefetch-related-ae7981719d3f


class BannerPublishSerializer(serializers.ModelSerializer):
    postgroup_set = PostGroupSerializer(read_only=True, many=True)
    linkingbanner_set = LinkingBannerSerializer(read_only=True, many=True)

    class Meta:
        model = models.BannerPublish
        fields = ('date', 'postgroup_set', 'linkingbanner_set')

# https://medium.com/quant-five/speed-up-django-nested-foreign-key-serializers-w-prefetch-related-ae7981719d3f
    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        # select_related for "to-one" relationships
        queryset = queryset.prefetch_related(Prefetch(
            'postgroup_set',
            queryset=models.PostGroup.objects.order_by('ordering')))
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


class MagazinePublishSerializer(serializers.ModelSerializer):
    postgroup_set = PostGroupSerializer(read_only=True, many=True)

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
            queryset=models.PostGroup.objects.order_by('ordering')))
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
