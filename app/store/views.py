from rest_framework import viewsets, mixins, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from store import serializers
from store.models import Store, StorePost


class StoreViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Manage store in the database w/Viewset"""
    serializer_class = serializers.StoreSerializer
    queryset = Store.objects.all().order_by('current_ranking')
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects that is_activated only"""
        return self.queryset.filter(is_active=True)


class StorePostView(generics.ListAPIView):
    """Manage store post in the database w/View"""
    serializer_class = serializers.StorePostSerializer
    queryset = StorePost.objects.all().order_by('-post_taken_at_timestamp')

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects that is_activated only"""
        return self.queryset.filter(
            store__insta_id=self.kwargs['store_insta_id'])\
            .filter(is_active=True)
