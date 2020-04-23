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
from store.models import UserFavoriteStore, Store
from core.models import UserPushToken
from .models import UserFavoriteProduct, ProductReview
from product.models import Product


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


class ProductReviewDestroyView(generics.DestroyAPIView):
    queryset = ProductReview.objects.all()
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        data = self.queryset.filter(
            pk=kwargs['pk'], user=request.user)
        data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductReviewListByUserView(generics.ListAPIView):
    serializer_class = serializers.ProductReviewSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        queryset = ProductReview.objects.filter(user=user)
        return queryset


class ProductReviewListByProductView(generics.ListAPIView):
    serializer_class = serializers.ProductReviewSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        product = self.request.query_params.get('product')
        print(product)
        queryset = ProductReview.objects.filter(product__pk=product)
        return queryset


class ProductReviewListByStoreView(generics.ListAPIView):
    serializer_class = serializers.ProductReviewSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        store = self.request.query_params.get('store')
        queryset = ProductReview.objects.filter(store__pk=store)
        return queryset


class ProductReviewCreateView(generics.CreateAPIView):
    serializer_class = serializers.ProductReviewSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_store_sum(self, store_pk, rating):
        store_obj = Store.objects.get(pk=store_pk)
        review_list = ProductReview.objects.filter(store=store_obj)
        review_sum = sum(review_obj.rating for review_obj in review_list)
        new_review_sum = review_sum + int(rating)
        new_review_count = review_list.count()+1
        print(new_review_sum, new_review_count)
        new_current_review_rating = new_review_sum / new_review_count
        store_obj.current_review_rating = new_current_review_rating
        print(new_current_review_rating)
        store_obj.save()

    def get_product_sum(self, product_pk, rating):
        product_obj = Product.objects.get(pk=product_pk)
        review_list = ProductReview.objects.filter(product=product_obj)
        review_sum = sum(review_obj.rating for review_obj in review_list)
        new_review_sum = review_sum + int(rating)
        new_review_count = review_list.count()+1
        print(new_review_sum, new_review_count)
        new_current_review_rating = new_review_sum / new_review_count
        product_obj.current_review_rating = new_current_review_rating
        print(new_current_review_rating)
        product_obj.save()

    def create(self, request, *args, **kwargs):
        product_pk = request.data.__getitem__('product')
        store_pk = request.data.__getitem__('store')
        rating = request.data.__getitem__('rating')
        self.get_product_sum(product_pk, rating)
        self.get_store_sum(store_pk, rating)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReviewImageCreateView(generics.CreateAPIView):
    'Create a new image instance'
    serializer_class = serializers.ReviewImageCreateSerializer
    authentication_classes = (authentication.TokenAuthentication,)

    def post(self, request):
        serializer = serializers.ReviewImageCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
