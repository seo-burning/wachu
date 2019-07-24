from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core import serializers, models


class NoticeListViewAPI(generics.ListAPIView):
    serializer_class = serializers.NoticeSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = models.Notice.objects.all().order_by('-date')
