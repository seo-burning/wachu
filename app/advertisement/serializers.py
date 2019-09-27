from rest_framework import serializers
from advertisement.models import ProductRecommendKeyword, StoreRecommendKeyword


class ProductRecommendKeywordSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductRecommendKeyword
        fields = ('keyword',)


class StoreRecommendKeywordSerializer(serializers.ModelSerializer):

    class Meta:
        model = StoreRecommendKeyword
        fields = ('keyword',)
