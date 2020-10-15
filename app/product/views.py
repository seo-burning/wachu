from django.db.models import Q
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from product import serializers, models
from user.models import UserProductView
from utils.slack import slack_notify
from operator import and_
from functools import reduce


class ProductDetailView(generics.RetrieveAPIView):
    serializer_class = serializers.ProductSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = models.Product.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()  # here the object is retrieved
        user = request.user
        instance.view += 1
        instance.save()
        user_product_view_object, is_created = UserProductView.objects.get_or_create(user=user, product=instance)
        user_product_view_object.count += 1
        user_product_view_object.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ProductCategoryListView(generics.ListAPIView):
    serializer_class = serializers.ProductSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = models.Product.objects.filter(is_active=True)
        try:
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
                queryset = queryset.filter(Q(original_price__gte=min_price, is_discount=False) | Q(discount_price__gte=min_price, is_discount=True))
            max_price = self.request.query_params.get('max-price')
            if (max_price):
                queryset = queryset.filter(Q(original_price__lte=max_price, is_discount=False) | Q(discount_price__lte=max_price, is_discount=True))
            is_discount = self.request.query_params.get('is-discount')
            print(is_discount)
            if (is_discount):
                queryset = queryset.filter(is_discount=is_discount)
            order_by = self.request.query_params.get('order-by')
            if (order_by):
                queryset = queryset.order_by(order_by)
        except Exception as e:
            queryset = models.Product.objects.filter(is_active=True)
            slack_notify('error occured during get product list', channel='#6_qc')
            slack_notify(e, channel='#6_qc')
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset


class ProductSearchListView(generics.ListAPIView):
    serializer_class = serializers.ProductSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = models.Product.objects.filter(is_active=True)
        q_filter_list = []
        q = self.request.query_params.get('q').lower()
        # 여러가지 키워드가 날라오는거 기반으로 초반에 설계함
        if(q):
            q_filter_list = q.split('_')
            queryset = queryset.filter(reduce(and_, [Q(name__icontains=query) for query in q_filter_list]))
            print(q_filter_list)
            queryset = self.get_serializer_class().setup_eager_loading(queryset)
            return queryset
        else:
            return []


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
