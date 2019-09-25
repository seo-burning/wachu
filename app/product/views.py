from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from product import serializers, models


class ProductCategoryListView(generics.ListAPIView):
    serializer_class = serializers.ProductSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        color = self.request.query_params.get('color')
        color_filter = color.split(',')
        print(color_filter)
        queryset = models.Product.objects.all().order_by('-pk')
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset.filter(category__name=self.kwargs['product_category'],
                               color__name__in=color_filter)
