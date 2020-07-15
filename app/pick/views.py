from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from pick import serializers, models


class PickSetView(generics.ListAPIView):
    serializer_class = serializers.PickABSerializer
    queryset = models.PickAB.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(is_published=True)
