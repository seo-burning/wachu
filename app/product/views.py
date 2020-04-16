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
        queryset = models.Product.objects.all().order_by('-pk')
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
        region = self.request.query_params.get('region')
        if (region):
            region_filter = region.split(',')
            queryset = queryset.filter(store__region__name__in=region_filter)
        store = self.request.query_params.get('store')
        if (store):
            queryset = queryset.filter(store__pk=store)
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset


class ProductSearchListView(generics.ListAPIView):
    serializer_class = serializers.ProductSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = models.Product.objects.all().order_by('-pk')
        q_filter = []
        q = self.request.query_params.get('q')
        if(q):
            q_filter = q.split(',')
        queryset = queryset.filter(Q(color__name__in=q_filter) | Q(
            sub_category__name__in=q_filter) | Q(category__name__in=q_filter)
            | Q(style__name__in=q_filter) |
            Q(post__store__insta_id__in=q_filter))
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset
