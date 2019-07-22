from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from store.models import UserFavoriteStore, Store, UserFavoritePost
from rest_framework import serializers


# TODO SELECT_RELATED
class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ('insta_id',)


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('favorite_stores', 'favorite_posts')


class FavoriteStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFavoriteStore
        fields = ('store', 'user')


class FavoritePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFavoritePost
        fields = ('store_post', 'user')


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password', 'name')
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
