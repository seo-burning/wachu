
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from product import serializers, models


class SlidingBannerSectionView(generics.ListAPIView):
    serializer_class = serializers.SlidingBannerSectionSerializer
    queryset = models.SlidingBannerSection.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(is_published=True)


class MainSectionView(generics.ListAPIView):
    serializer_class = serializers.MainSectionSerializer
    queryset = models.MainSection.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(is_published=True)
