
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from random import randint
from publish import serializers, models
from django.db.models import Case, When, IntegerField


class MainPagePublishView(generics.ListAPIView):
    serializer_class = serializers.MainPagePublishSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = models.MainPagePublish.objects.all().filter(
            is_published=True).order_by('-date')
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset


class ProductTagGroupListView(generics.ListAPIView):
    serializer_class = serializers.ProductTagGroupSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

# https://medium.com/@chrisjune_13837/django-5-orm-queries-you-should-know-a0f4533b31e8
# 100개 만들고, 셔플 기능, 날짜별 퍼블리싱 기능
# 매일 화면이 바뀌는 느낌이 들어야 한다.
# 여기에 커스텀 해주는 로직을 조금 더 넣는 것도 방법
    def get_queryset(self):
        user = self.request.user
        primary_style = user.primary_style
        secondary_style = user.secondary_style
        print(primary_style, secondary_style)
        # need to suffle
        if primary_style is not None and secondary_style is not None:
            queryset = models.ProductTagGroup.objects.filter(is_active=True
                                                             ).annotate(weighted_ordering=Case(
                                                                 When(
                                                                     style=primary_style,
                                                                     then=randint(0, 20)
                                                                 ), When(
                                                                     style=secondary_style,
                                                                     then=10+randint(0, 20)
                                                                 ), default=30, output_field=IntegerField()
                                                             )).order_by('weighted_ordering', 'ordering')
        else:
            queryset = models.ProductTagGroup.objects.filter(is_active=True)
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset


class BannerPublishView(generics.ListAPIView):
    serializer_class = serializers.BannerPublishSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = models.BannerPublish.objects.all().filter(
            is_published=True).order_by('-date')
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset


class MagazinePublishView(generics.ListAPIView):
    serializer_class = serializers.MagazinePublishSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = models.MagazinePublish.objects.all().filter(
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
