from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework import status
from allauth.account.adapter import get_adapter

from django.contrib.auth import get_user_model
from user import serializers
from allauth.socialaccount.providers.facebook.views \
    import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView, SocialConnectView
from store.models import UserFavoriteStore
from core.models import UserPushToken
from .models import UserFavoriteProduct, StoreReview


class FacebookLoginConnect(SocialConnectView):
    adapter_class = FacebookOAuth2Adapter
    authentication_classes = (authentication.TokenAuthentication,)

    def process_login(self):
        print(self.request)
        get_adapter(self.request).login(self.request, self.request.user)


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class CreateUserView(generics.CreateAPIView):
    """Create a new user"""
    serializer_class = serializers.UserSerializer


class CreatUserPushToken(generics.CreateAPIView):
    """Create a new user"""
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.PushTokenSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserPushTokenListView(generics.ListAPIView):
    """Create a new user"""
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = serializers.PushTokenSerializer
    queryset = UserPushToken.objects.all()


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = serializers.AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class FavoriteListView(generics.RetrieveAPIView):
    serializer_class = serializers.FavoriteSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user

    def get_queryset(self):
        queryset = get_user_model()
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset


# TODO Optimized this to send it through product model.
class FavoriteProductListView(generics.RetrieveAPIView):
    serializer_class = serializers.FavoriteProductListSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user

    def get_queryset(self):
        queryset = get_user_model()
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset


class FavoriteStoreView(generics.DestroyAPIView):
    queryset = UserFavoriteStore.objects.all()
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        data = self.queryset.filter(
            store=kwargs['pk'], user=request.user)
        data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteProductView(generics.DestroyAPIView):
    queryset = UserFavoriteProduct.objects.all()
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        data = self.queryset.filter(
            product=kwargs['pk'], user=request.user)
        data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteStoreCreateView(generics.CreateAPIView):
    serializer_class = serializers.FavoriteStoreSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)


class FavoriteProductCreateView(generics.CreateAPIView):
    serializer_class = serializers.FavoriteProductSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = serializers.UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user


class UserBasicInfoUpdateView(generics.RetrieveUpdateAPIView):
    """Update user basic infomation"""
    serializer_class = serializers.UserBasicInfoSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user


class UserAdditionalInfoUpdateView(generics.RetrieveUpdateAPIView):
    """Update user basic infomation"""
    serializer_class = serializers.UserAdditionalInfoSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user


class UserNameUpdateView(generics.RetrieveUpdateAPIView):
    """Update user basic infomation"""
    serializer_class = serializers.UserNameSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user


class StoreReviewDestroyView(generics.DestroyAPIView):
    queryset = StoreReview.objects.all()
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        data = self.queryset.filter(
            pk=kwargs['pk'], user=request.user)
        data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StoreReviewListByUserView(generics.ListAPIView):
    serializer_class = serializers.StoreReviewSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        queryset = StoreReview.objects.filter(user=user)
        return queryset


class StoreReviewCreateView(generics.CreateAPIView):
    serializer_class = serializers.StoreReviewSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
