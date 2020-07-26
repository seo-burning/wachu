from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from pick import serializers, models


class PickSetView(generics.ListAPIView):
    serializer_class = serializers.PickABSerializer
    queryset = models.PickAB.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(is_published=True)


class RandomPickListView(APIView):
    serializer_class = serializers.PickSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        pick_list_queryset = models.Pick.objects.all().order_by('?')
        pick_ab_result_queryset = models.PickABResult.objects.select_related('pick_A', 'pick_B').filter(user=user)
        pick_list = list(pick_list_queryset)
        pick_ab_list = []
        while (len(pick_ab_list) < 8):
            picks = []
            pick_a = pick_list.pop()
            pick_b = pick_list.pop()

            ab_exist = pick_ab_result_queryset.filter(pick_A=pick_a, pick_B=pick_b).exists()
            ba_exist = pick_ab_result_queryset.filter(pick_A=pick_b, pick_B=pick_a).exists()
            print(ab_exist, ba_exist, len(pick_ab_result_queryset), pick_ab_result_queryset.filter(pick_A=pick_a, pick_B=pick_b).count())
            if (ab_exist is False and ba_exist is False):
                picks.append(self.serializer_class(pick_a).data)
                picks.append(self.serializer_class(pick_b).data)
                pick_ab_dict = {'picks': picks}
                pick_ab_list.append(pick_ab_dict)
            else:
                print('duplicated')
                continue
        return Response(pick_ab_list)


class PickABResultCreateView(generics.CreateAPIView):
    serializer_class = serializers.PickABResultSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
