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
from .models import UserFavoriteProduct, ProductReview, \
    Recipient, UserStyleTaste, UserProductView, UserStoreView
from product.models import Product, ProductStyle
from django.core.exceptions import ObjectDoesNotExist


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

    def create(self, request, *args, **kwargs):
        push_token = request.data.__getitem__('push_token')
        try:
            default_push_token = UserPushToken.objects.get(push_token=push_token)
            if default_push_token.user != request.user:
                default_push_token.delete()
        except ObjectDoesNotExist:
            print('no default token exist')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserUserPushTokenUpdateView(generics.RetrieveUpdateAPIView):
    """Update user basic infomation"""
    serializer_class = serializers.PushTokenSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)


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
        pickAB_results = user.pickAB_results.select_related(
            'pick_AB', 'pick_A', 'pick_B', 'pick_A__primary_style',
            'pick_A__secondary_style', 'pick_B__primary_style', 'pick_B__secondary_style').prefetch_related(
            'pick_A',
            'pick_B',
            'pick_AB__picks',
            'pick_AB__picks__primary_style',
            'pick_AB__picks__secondary_style').all()
        points = {'simple': 0,
                  'sexy': 0,
                  'feminine': 0,
                  'lovely': 0,
                  'street': 0,
                  'vintage': 0}
        for pick_result_obj in pickAB_results:
            selection = pick_result_obj.selection
            if pick_result_obj.pick_AB:
                selected_pick = pick_result_obj.pick_AB.picks.all()[int(selection)]
                primary_style = selected_pick.primary_style
                secondary_style = selected_pick.secondary_style
                points[str(primary_style)] += 8
                points[str(secondary_style)] += 2
            elif pick_result_obj.pick_A and pick_result_obj.pick_B:
                if selection == '0':
                    if pick_result_obj.pick_A.primary_style:
                        primary_style = pick_result_obj.pick_A.primary_style
                        points[str(primary_style)] += 8
                        if pick_result_obj.pick_A.secondary_style:
                            secondary_style = pick_result_obj.pick_A.secondary_style
                            points[str(secondary_style)] += 2
                    else:
                        print(pick_result_obj.pick_A.pk)
                elif selection == '1':
                    if pick_result_obj.pick_B.primary_style:
                        primary_style = pick_result_obj.pick_B.primary_style
                        points[str(primary_style)] += 8
                        if pick_result_obj.pick_B.secondary_style:
                            secondary_style = pick_result_obj.pick_B.secondary_style
                            points[str(secondary_style)] += 2
                    else:
                        print('error')
                else:
                    print('??')
            else:
                # TODO need to optimiaze and 예외처리
                pass
        user_product_views = user.view_products.select_related('style').all()
        for product_obj in user_product_views:
            if product_obj.style:
                points[str(product_obj.style)] += 1
        user_store_views = user.view_stores.select_related('primary_style').select_related('secondary_style').all()
        for store_obj in user_store_views:
            if store_obj.primary_style:
                points[str(store_obj.primary_style)] += 2
            if store_obj.secondary_style:
                points[str(store_obj.secondary_style)] += 1

        sort_points = sorted(points.items(), key=lambda x: x[1], reverse=True)
        primary_style = ProductStyle.objects.get(name=sort_points[0][0])
        secondary_style = ProductStyle.objects.get(name=sort_points[1][0])
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
        return Response({'primary_style': sort_points[0][0],
                         'secondary_style': sort_points[1][0],
                         'user_style': sort_points})


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


class UserStoreViewCreateView(APIView):
    serializer_class = serializers.UserStoreViewSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        user = request.user
        store_pk = request.data.__getitem__('store')
        store_obj = Store.objects.get(pk=store_pk)
        store_obj.view += 1
        store_obj.save()
        user_store_view_object, is_created = UserStoreView.objects.get_or_create(user=user, store=store_obj)
        user_store_view_object.count += 1
        user_store_view_object.save()
        return Response({'store-view-count': store_obj.view})


class UserProductViewListView(generics.ListAPIView):
    serializer_class = serializers.ProductSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = self.request.user.view_products.order_by('user_product_view_set')
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset
