from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from preorder import serializers, models
from product.serializers import ProductSerializer


class PreorderListView(generics.ListAPIView):
    serializer_class = serializers.PreorderCampaignSerialzier
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = models.PreorderCampaign.objects.filter(is_active=True)
        return queryset


class PreorderProductView(generics.ListAPIView):
    serializer_class = ProductSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        pk = self.kwargs['pk']
        preorder_object = models.PreorderCampaign.objects.get(pk=pk)
        queryset = preorder_object.product_set
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset
