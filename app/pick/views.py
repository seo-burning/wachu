from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from pick import serializers, models
from product.serializers import ProductSerializer
from product.models import Product


class PickSetView(generics.ListAPIView):
    serializer_class = serializers.PickABSerializer
    queryset = models.PickAB.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(is_published=True)


class MyPickListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        pickAB_results = self.request.user.pickAB_results.select_related(
            'pick_A', 'pick_A__product', 'pick_AB', 'pick_B', 'pick_B__product').all().order_by('-created_at')
        product_pk_list = []
        for pickAB_obj in pickAB_results:
            product_pk = None
            if pickAB_obj.pick_AB:
                continue
            if pickAB_obj.selection == '0' and pickAB_obj.pick_A:
                if pickAB_obj.pick_A.product:
                    product_pk = pickAB_obj.pick_A.product.pk
            elif pickAB_obj.selection == '1' and pickAB_obj.pick_B:
                if pickAB_obj.pick_B.product:
                    product_pk = pickAB_obj.pick_B.product.pk
            if product_pk:
                product_pk_list.append(product_pk)
            else:
                print(pickAB_obj)

        used = set()
        print(product_pk_list)
        unique_product_pk_list = [x for x in product_pk_list if x not in used and (used.add(x) or True)]

        queryset = Product.objects.filter(pk__in=unique_product_pk_list, is_active=True)
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        # TODO SQL call duplicated two times
        queryset = sorted(queryset,  key=lambda x: unique_product_pk_list.index(x.id))
        return queryset


class RandomPickListView(APIView):
    serializer_class = serializers.PickSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        pick_list_queryset = models.Pick.objects.filter(is_active=True).order_by('?')
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
