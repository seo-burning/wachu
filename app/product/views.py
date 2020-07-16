from django.db.models import Q


from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from product import serializers, models


class ProductCategoryListView(generics.ListAPIView):
    serializer_class = serializers.ProductSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = models.Product.objects.filter(is_active=True)
        category = self.kwargs['product_category']
        if (category != 'all'):
            queryset = queryset.filter(category__name=category)
        sub_category = self.request.query_params.get('sub-category')
        if (sub_category):
            queryset = queryset.filter(sub_category__name=sub_category)
        color = self.request.query_params.get('color')
        if (color):
            color_filter = color.split(',')
            queryset = queryset.filter(color__name__in=color_filter)
        style = self.request.query_params.get('style')
        if (style):
            style_filter = style.split(',')
            queryset = queryset.filter(style__name__in=style_filter)
        pattern = self.request.query_params.get('pattern')
        if (pattern):
            pattern_filter = pattern.split(',')
            queryset = queryset.filter(pattern__name__in=pattern_filter)
        region = self.request.query_params.get('region')
        if (region):
            region_filter = region.split(',')
            queryset = queryset.filter(store__region__name__in=region_filter)
        store = self.request.query_params.get('store')
        if (store):
            queryset = queryset.filter(store__pk=store)
        min_price = self.request.query_params.get('min-price')
        if (min_price):
            queryset = queryset.filter(Q(original_price__gte=min_price, is_discount=False)
                                       | Q(discount_price__gte=min_price, is_discount=True))
        max_price = self.request.query_params.get('max-price')
        if (max_price):
            queryset = queryset.filter(Q(original_price__lte=max_price, is_discount=False)
                                       | Q(discount_price__lte=max_price, is_discount=True))
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset


class ProductSearchListView(generics.ListAPIView):
    serializer_class = serializers.ProductSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = models.Product.objects.filter(is_active=True)
        q_filter = []
        q = self.request.query_params.get('q')
        if(q):
            q_filter = q.split(',')
        print(q_filter)
        # 여러가지 키워드가 날라오는거 기반으로 초반에 설계함
        queryset = queryset.filter(Q(color__name__in=q_filter) | Q(
            sub_category__name__in=q_filter) | Q(category__name__in=q_filter)
            | Q(style__name__in=q_filter) | Q(name__icontains=q_filter))
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset


class ProductRatingView(generics.RetrieveAPIView):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductRatingSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


class CategoryListView(generics.ListAPIView):
    serializer_class = serializers.ProductCategorySerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = models.ProductCategory.objects.filter(is_active=True)
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset
