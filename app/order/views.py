from rest_framework import generics, authentication, permissions
from order import serializers, models
from rest_framework.response import Response
from rest_framework import status
from product.models import Product, ProductOption
from rest_framework.views import APIView
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist


class CouponValidateView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        code = request.query_params['code']
        try:
            coupon_obj = models.Coupon.objects.filter(is_active=True).get(code=code)
        except ObjectDoesNotExist:
            coupon_obj = None

        if coupon_obj:
            serializer = serializers.CouponSerializer(coupon_obj)
            print(code, coupon_obj)
            return Response({'validation': True, 'code': serializer.data})
        else:
            return Response({'validation': False})


class OrderListView(generics.ListAPIView):
    serializer_class = serializers.OrderSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

# https://www.django-rest-framework.org/api-guide/filtering/
    def get_queryset(self):
        order_status = self.kwargs['status']
        if (order_status == 'all'):
            queryset = models.Order.objects.filter(customer=self.request.user)
        elif (order_status == 'cancel-refund-exchange'):
            queryset = models.Order.objects.filter(customer=self.request.user)
            queryset = models.Order.objects.filter(Q(order_status='cancelled') | Q(
                order_status='change-processing') | Q(order_status='refund-processing') |
                Q(order_status='refund-complete'))
        else:
            queryset = models.Order.objects.filter(customer=self.request.user, order_status=order_status)
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset


class OrderSummaryView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return Response({'some': 'data'})


class OrderRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.OrderSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = models.Order.objects.all()
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset


class OrderCreateView(generics.CreateAPIView):
    serializer_class = serializers.OrderCreateSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        created_order = models.Order.objects.get(id=serializer.data['id'])
        ordered_product_list = request.data.__getitem__('orderedProductList')
        for ordered_product_obj in ordered_product_list:
            product_obj = Product.objects.get(pk=ordered_product_obj['product'])
            product_option_obj = ProductOption.objects.get(pk=ordered_product_obj['product_option'])
            ordered_product = models.OrderedProduct.objects.create(
                product=product_obj,
                product_option=product_option_obj,
                order=created_order,
                quantity=ordered_product_obj['quantity'],
                original_price=ordered_product_obj['original_price'],
                discount_rate=ordered_product_obj['discount_rate'],
                is_free_ship=ordered_product_obj['is_free_ship'],
            )
            if(ordered_product_obj['discount_price']):
                ordered_product.discount_price = ordered_product_obj['discount_price']
                ordered_product.save()
        coupon_id = request.data.__getitem__('coupon_code')
        if coupon_id:
            coupon_obj = models.Coupon.objects.get(id=coupon_id)
            models.AppliedCoupon.objects.create(coupon=coupon_obj, user=request.user, order=created_order)
        models.OrderStatusLog.objects.create(order=created_order, order_status='order-processing')
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # 주문을 만드면서, 각 단계에 대한 Order Status Log를 만들어야한다.
    # 주문을 만드면서, 해당 상태에서 고정된 상품을 생성해야 한다.


class OrderStatusLogCreateView(generics.CreateAPIView):
    serializer_class = serializers.OrderStatusLogCreateSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        order_pk = request.data.__getitem__('order')
        order_status = request.data.__getitem__('order_status')
        order_obj = models.Order.objects.get(pk=order_pk)
        order_obj.order_status = order_status
        order_obj.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
