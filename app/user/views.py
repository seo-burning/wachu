from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework import status
from allauth.account.adapter import get_adapter

from django.contrib.auth import get_user_model
from user import serializers
from allauth.socialaccount.providers.facebook.views \
    import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView, SocialConnectView
from store.models import UserFavoriteStore, Store
from core.models import UserPushToken
from .models import UserFavoriteProduct, ProductReview, Recipient, UserStyleTaste, UserProductView
from product.models import Product, ProductStyle


class FacebookLoginConnect(SocialConnectView):
    adapter_class = FacebookOAuth2Adapter
    authentication_classes = (authentication.TokenAuthentication,)

    def process_login(self):
        print(self.request)
        get_adapter(self.request).login(self.request, self.request.user)


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    authentication_classes = (authentication.TokenAuthentication,)


class CreateUserView(generics.CreateAPIView):
    """Create a new user"""
    authentication_classes = (authentication.TokenAuthentication,)
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
    authentication_classes = (authentication.TokenAuthentication,)


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
class FavoriteProductListView(generics.ListAPIView):
    serializer_class = serializers.ProductSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = Product.objects.filter(favorite_users=self.request.user)
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


class UserNameUpdateView(generics.RetrieveUpdateAPIView):
    """Update user basic infomation"""
    serializer_class = serializers.UserNameSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user


class UserInformationStatusUpdateView(generics.RetrieveUpdateAPIView):
    """Update user basic infomation"""
    serializer_class = serializers.UserInformationStatusSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user


class UserStyleUpdateView(APIView):
    serializer_class = serializers.UserStyleSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        user = self.request.user
        pickAB_results = user.pickAB_results.select_related('pick_AB').prefetch_related('pick_AB__picks').all()
        points = {'simple': 0,
                  'sexy': 0,
                  'feminine': 0,
                  'lovely': 0,
                  'street': 0, }
        for pick_result_obj in pickAB_results:
            selection = pick_result_obj.selection
            selected_pick = pick_result_obj.pick_AB.picks.all()[int(selection)]
            primary_style = selected_pick.primary_style
            secondary_style = selected_pick.secondary_style
            points[str(primary_style)] += 4
            points[str(secondary_style)] += 1
        p_style = None
        p_v = 0
        s_style = None
        s_v = 0
        for key, value in points.items():
            if value > s_v:
                s_v = value
                s_style = key
            if value > p_v:
                s_style = p_style
                s_v = p_v
                p_style = key
                p_v = value
        print(p_style, s_style)
        primary_style = ProductStyle.objects.get(name=p_style)
        secondary_style = ProductStyle.objects.get(name=s_style)
        UserStyleTaste.objects.create(user=user,
                                      lovely=points['lovely'],
                                      sexy=points['sexy'],
                                      simple=points['simple'],
                                      street=points['street'],
                                      feminine=points['feminine'],
                                      primary_style=primary_style,
                                      secondary_style=secondary_style)
        user.primary_style = primary_style
        user.secondary_style = secondary_style
        user.save()
        print(points, primary_style, secondary_style)
        return Response({'primary_style': p_style, 'secondary_style': s_style})


class UserProfileImageUpdateView(generics.RetrieveUpdateAPIView):
    """Update user basic infomation"""
    serializer_class = serializers.UserProfileImageCreateSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user


class ProductReviewCreateView(generics.CreateAPIView):
    serializer_class = serializers.ProductReviewCreateSerializer
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


class ProductReviewDestroyView(generics.DestroyAPIView):
    queryset = ProductReview.objects.all()
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_store_sum(self, store_obj):
        review_list = ProductReview.objects.filter(store=store_obj)
        review_sum = sum(review_obj.rating for review_obj in review_list)
        new_current_review_rating = review_sum / review_list.count()
        store_obj.current_review_rating = new_current_review_rating
        print(new_current_review_rating)
        store_obj.save()

    def get_product_sum(self, product_obj):
        review_list = ProductReview.objects.filter(product=product_obj)
        review_sum = sum(review_obj.rating for review_obj in review_list)
        new_current_review_rating = review_sum / review_list.count()
        product_obj.current_review_rating = new_current_review_rating
        print(new_current_review_rating)
        product_obj.save()

    def destroy(self, request, *args, **kwargs):
        data = self.queryset.get(
            pk=kwargs['pk'], user=request.user)
        store_obj = data.store
        product_obj = data.product
        data.delete()
        print(store_obj, product_obj)
        self.get_store_sum(store_obj)
        self.get_product_sum(product_obj)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductReviewListByUserView(generics.ListAPIView):
    serializer_class = serializers.ProductReviewSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        queryset = ProductReview.objects.filter(user=user)
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset


class ProductReviewListByProductView(generics.ListAPIView):
    serializer_class = serializers.ProductReviewSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        product = self.request.query_params.get('product')
        print(product)
        queryset = ProductReview.objects.filter(product__pk=product)
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset


class ProductReviewListByStoreView(generics.ListAPIView):
    serializer_class = serializers.ProductReviewSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        store = self.request.query_params.get('store')
        queryset = ProductReview.objects.filter(store__pk=store)
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset


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


class RecipientCreateView(generics.CreateAPIView):
    serializer_class = serializers.RecipientSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        primary = request.data.__getitem__('primary')
        if (primary):
            recipient_list = Recipient.objects.filter(user=request.user)
            for recipient_obj in recipient_list:
                recipient_obj.primary = False
                recipient_obj.save()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class RecipientDestroyView(generics.DestroyAPIView):
    queryset = Recipient.objects.all()
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        data = self.queryset.filter(
            id=kwargs['pk'], user=request.user)
        data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecipientListByUserView(generics.ListAPIView):
    serializer_class = serializers.RecipientSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        queryset = Recipient.objects.filter(user=user)
        return queryset


class RecipientUpdateView(generics.UpdateAPIView):
    serializer_class = serializers.RecipientSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Recipient.objects.all()

    def update(self, request, *args, **kwargs):
        primary = request.data.__getitem__('primary')
        if (primary):
            recipient_list = Recipient.objects.filter(user=request.user)
            for recipient_obj in recipient_list:
                recipient_obj.primary = False
                recipient_obj.save()
        return super(RecipientUpdateView, self).update(request, *args, **kwargs)


class UserProductViewCreateView(APIView):
    serializer_class = serializers.UserProductViewSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        user = request.user
        product_pk = request.data.__getitem__('product')
        product_obj = Product.objects.get(pk=product_pk)
        product_obj.view += 1
        product_obj.save()
        user_product_view_object, is_created = UserProductView.objects.get_or_create(user=user, product=product_obj)
        user_product_view_object.count += 1
        user_product_view_object.save()
        return Response({'product-view-count': product_obj.view})
