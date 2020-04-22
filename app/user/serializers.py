from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from store.models import UserFavoriteStore, Store
from rest_framework import serializers
from product.serializers import ProductSerializer

from core.models import UserPushToken
from user.models import UserFavoriteProduct, StoreReview
# TODO SELECT_RELATED


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ('insta_id',)

# TODO Optimize


class FavoriteSerializer(serializers.ModelSerializer):
    favorite_products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = get_user_model()
        fields = ('favorite_stores', 'favorite_products')

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        # select_related for "to-one" relationships
        queryset = queryset.prefetch_related(
            'favorite_products_posts',
            'favorite_products_posts__post_image_set',
            'favorite_products_posts__store',
            'favorite_products_posts__store__category',
            'favorite_products_posts__store__primary_style',
            'favorite_products_posts__store__secondary_style',
            'favorite_products_posts__store__age',
        )
        return queryset


class FavoriteProductListSerializer(serializers.ModelSerializer):
    favorite_products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = get_user_model()
        fields = ('favorite_products',)

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        # select_related for "to-one" relationships
        queryset = queryset.prefetch_related(
            'favorite_products_posts',
            'favorite_products_posts__post_image_set',
            'favorite_products_posts__store',
            'favorite_products_posts__store__category',
            'favorite_products_posts__store__primary_style',
            'favorite_products_posts__store__secondary_style',
            'favorite_products_posts__store__age',
        )
        return queryset


class FavoriteStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFavoriteStore
        fields = ('store', 'user')


class FavoriteProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFavoriteProduct
        fields = ('product', 'user')


class UserBasicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('gender', 'age',)


class UserAdditionalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('height', 'weight')


class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('name',)


class UserSerializer(serializers.ModelSerializer):
    get_user_favorite_stores_count = serializers.IntegerField(
        source='favorite_stores.count', read_only=True)
    get_user_favorite_posts_count = serializers.IntegerField(
        source='favorite_posts.count', read_only=True)

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password', 'name',
                  'age', 'height', 'weight', 'gender',
                  'get_user_favorite_stores_count',
                  'get_user_favorite_posts_count')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 6}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
        return user

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        # select_related for "to-one" relationships
        queryset = queryset.prefetch_related(
            'favorite_posts',
            'favorite_stores',
        )
        return queryset


class AuthTokenSerializer(serializers.Serializer):
    """serializer for user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs


class PushTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPushToken
        fields = ('push_token',)


class FacebookPhoneNumberAccountCreateSerailizer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ()


class StoreReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)

    class Meta:
        model = StoreReview
        fields = ('pk', 'store', 'product', 'rating', 'description', 'created_at', 'user'
                  )
