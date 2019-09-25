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
        queryset = queryset.filter(
            category__name=self.kwargs['product_category'])
        sub_category = self.request.query_params.get('sub-category')
        if (sub_category):
            queryset = queryset.filter(sub_category__name=sub_category)
        color = self.request.query_params.get('color')
        if (color):
            color_filter = color.split(',')
            queryset = queryset.filter(color__name__in=color_filter)
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
            sub_category__name__in=q_filter) | Q(category__name__in=q_filter))
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset
