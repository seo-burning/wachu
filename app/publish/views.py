
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from publish import serializers, models


class MainPagePublishView(generics.ListAPIView):
    serializer_class = serializers.MainPagePublishSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = models.MainPagePublish.objects.all().filter(
            is_published=True).order_by('-date')
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset


class TestPostSerializer(generics.ListAPIView):
    serializer_class = serializers.StorePostSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = models.StorePost.objects.all()[0:300]
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset
