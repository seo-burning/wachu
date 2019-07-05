from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from store import serializers
from store.models import Store, StorePost


class StoreView(generics.ListAPIView):
    serializer_class = serializers.StoreSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Store.objects.all().order_by('current_ranking')
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset.filter(is_active=True)


class StorePostView(generics.ListAPIView):
    serializer_class = serializers.StorePostSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = StorePost.objects.all().order_by('-post_taken_at_timestamp')
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset.filter(
            store__insta_id=self.kwargs['store_insta_id'])\
            .filter(is_active=True)
