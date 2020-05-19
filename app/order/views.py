from rest_framework import generics, authentication, permissions
from order import serializers, models


class OrderListView(generics.ListAPIView):
    serializer_class = serializers.OrderSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = models.Order.objects.filter(customer=self.request.user)
        return queryset


class OrderCreateView(generics.CreateAPIView):
    serializer_class = serializers.OrderSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)
