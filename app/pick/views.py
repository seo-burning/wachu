from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from pick import serializers, models


class ChuPickSetView(generics.ListAPIView):
    serializer_class = serializers.ChuPickSetSerializer
    queryset = models.ChuPickSet.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(is_published=True)
