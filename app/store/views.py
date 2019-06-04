from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from store import serializers
from store.models import Store


class StoreViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Manage store in the database"""
    serializer_class = serializers.StoreSerializer
    queryset = Store.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects that is_activated only"""
        return self.queryset.filter(is_active=True)
