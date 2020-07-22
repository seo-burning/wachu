from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.models import Case, When, IntegerField

from store import serializers
from store.models import Store, StorePost, StoreAddress


class StoreView(generics.ListAPIView):
    serializer_class = serializers.StoreSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        primary_style = user.primary_style
        secondary_style = user.secondary_style
        print(primary_style, secondary_style)
        if primary_style is not None and secondary_style is not None:
            queryset = Store.objects.filter(is_active=True
                                            ).annotate(weighted_ordering=Case(
                                                When(
                                                    primary_style__name=str(secondary_style),
                                                    then=3
                                                ), When(
                                                    secondary_style__name=str(secondary_style),
                                                    then=4
                                                ),
                                                When(
                                                    primary_style__name=str(primary_style),
                                                    then=1
                                                ), When(
                                                    secondary_style__name=str(primary_style),
                                                    then=2
                                                ), default=5, output_field=IntegerField()
                                            )).order_by('weighted_ordering', 'current_ranking')
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset


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


class StoreAddressListView(generics.ListAPIView):
    serializer_class = serializers.StoreAddressSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = StoreAddress.objects.filter(is_active=True)
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset


class StoreRatingView(generics.RetrieveAPIView):
    queryset = Store.objects.all()
    serializer_class = serializers.StoreRatingSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
