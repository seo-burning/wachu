from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from . import serializers, models


class ProductRecommendKeywordListViewAPI(generics.ListAPIView):
    serializer_class = serializers.ProductRecommendKeywordSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = models.ProductRecommendKeyword.objects.all()\
        .filter(is_published=True)


class StoreRecommendKeywordListViewAPI(generics.ListAPIView):
    serializer_class = serializers.StoreRecommendKeywordSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = models.StoreRecommendKeyword.objects.all()\
        .filter(is_published=True)
