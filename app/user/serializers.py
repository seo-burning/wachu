from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from store.models import UserFavoriteStore, Store
from rest_framework import serializers
from product.serializers import ProductSerializer

from core.models import UserPushToken
from user.models import UserFavoriteProduct, \
    ProductReview, ReviewImage, Recipient, UserProductView


# TODO SELECT_RELATED
from django.core.files.base import ContentFile
import base64
import six
import uuid
import imghdr


class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12]  # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension


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
        fields = ('gender', 'age', 'region')


class UserStyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = []


class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('name',)


class UserInformationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('information_status',)


class UserProfileImageCreateSerializer(serializers.ModelSerializer):
    profile_image = Base64ImageField(max_length=None, use_url=True)

    class Meta:
        model = get_user_model()
        fields = ('profile_image',)


class UserSerializer(serializers.ModelSerializer):
    get_user_favorite_stores_count = serializers.IntegerField(
        source='favorite_stores.count', read_only=True)
    get_user_favorite_posts_count = serializers.IntegerField(
        source='favorite_posts.count', read_only=True)

    class Meta:
        model = get_user_model()
        fields = ('information_status',
                  'id', 'email', 'password', 'name',
                  'age', 'height', 'weight', 'gender',
                  'get_user_favorite_stores_count',
                  'get_user_favorite_posts_count', 'profile_image')
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


class ReviewImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewImage
        fields = ('source', 'pk')


class ProductReviewCreateSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    review_image_set = ReviewImageSerializer(many=True, read_only=True)
    # product = ProductSerializer(many=False, read_only=True)

    class Meta:
        model = ProductReview
        fields = ('pk', 'store', 'product', 'rating', 'description', 'created_at', 'user', 'review_image_set')


class ProductReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    review_image_set = ReviewImageSerializer(many=True, read_only=True)
    product = ProductSerializer(many=False, read_only=True)

    class Meta:
        model = ProductReview
        fields = ('pk', 'store', 'product', 'rating', 'description', 'created_at', 'user', 'review_image_set')

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        queryset = queryset.select_related(
            'user',
            'product__category',
            'product__shopee_rating',
            'product__style',
            'product__sub_category',
            'product__store',
            'product__store__age',
            'product__store__primary_style',
            'product__store__secondary_style',
            'store',
            'store__age',
            'store__primary_style',
            'store__secondary_style')
        queryset = queryset.prefetch_related(
            'product__post__post_image_set',
            'product__color',
            'product__size',
            'product__product_image_set',
            'product__store__favorite_users',
            'product__store__category',
            'product__store__product_category',
            'product__favorite_users',
            'product__extra_option',
            'store__favorite_users',
            'store__category',
            'store__product_category',
            'review_image_set'
        )
        return queryset


class ReviewImageCreateSerializer(serializers.ModelSerializer):
    source = Base64ImageField(max_length=None, use_url=True)

    class Meta:
        model = ReviewImage
        fields = ('pk', 'source', 'review')


class RecipientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipient
        exclude = ('user',)


class UserProductViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProductView
        exclude = ('user', 'count')
