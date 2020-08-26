from rest_framework import generics, authentication, permissions
from order import serializers, models
from rest_framework.response import Response
from rest_framework import status
from product.models import Product, ProductOption
from rest_framework.views import APIView
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from utils.slack import slack_notify
from notification.expo_notification import send_push_message


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


class CouponListView(generics.ListAPIView):
    serializer_class = serializers.CouponSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = models.Coupon.objects.filter(is_active=True, is_public=True)
        return queryset


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
            queryset = queryset.filter(Q(order_status='cancelled') | Q(
                order_status='change-processing') | Q(order_status='refund-processing') |
                Q(order_status='refund-complete'))
        else:
            queryset = models.Order.objects.filter(customer=self.request.user, order_status=order_status)
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset


class OrderGroupListView(generics.ListAPIView):
    serializer_class = serializers.OrderGroupListSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

# https://www.django-rest-framework.org/api-guide/filtering/
    def get_queryset(self):
        order_status = self.kwargs['status']
        if (order_status == 'all'):
            queryset = models.OrderGroup.objects.filter(customer=self.request.user)
        elif (order_status == 'cancel-refund-exchange'):
            queryset = models.OrderGroup.objects.filter(customer=self.request.user)
            queryset = queryset.filter(Q(order_status='cancelled') | Q(
                order_status='change-processing') | Q(order_status='refund-processing') |
                Q(order_status='refund-complete'))
        else:
            queryset = models.OrderGroup.objects.filter(customer=self.request.user, order_status=order_status)
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


class OrderGroupDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.OrderGroupDetailSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = models.OrderGroup.objects.all()
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset


class OrderGroupCreateView(generics.CreateAPIView):
    serializer_class = serializers.OrderGroupCreateSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        created_order_group = models.OrderGroup.objects.get(id=serializer.data['id'])
        ordered_product_list = request.data.__getitem__('orderedProductList')
        for ordered_product_obj in ordered_product_list:
            product_obj = Product.objects.get(pk=ordered_product_obj['product'])

            # 스토어별 주문 생성
            created_order, is_created = models.Order.objects.get_or_create(
                customer=created_order_group.customer,
                store=product_obj.store,
                order_group=created_order_group)

            if is_created:
                created_order.is_active = True
                created_order.order_status = 'order-processing'
                created_order.payment = created_order_group.payment
                created_order.recipient_name = created_order_group.recipient_name
                created_order.contact_number = created_order_group.contact_number
                created_order.city = created_order_group.city
                created_order.district = created_order_group.district
                created_order.ward = created_order_group.ward
                created_order.additional_address = created_order_group.additional_address
                models.OrderStatusLog.objects.create(order=created_order, order_status='order-processing')

            # 가격처리
            original_price = ordered_product_obj['original_price']
            created_order.original_price += original_price
            if ('discount_price' in ordered_product_obj and ordered_product_obj['discount_price']):
                if created_order.discount_price:
                    created_order.discount_price += ordered_product_obj['discount_price']
                else:
                    created_order.discount_price = ordered_product_obj['discount_price']
                discount_price = ordered_product_obj['discount_price']
                created_order.total_price += discount_price
            else:
                discount_price = None
                created_order.total_price += original_price

            created_order.save()
            # 상품 생성
            product_option_obj = ProductOption.objects.get(pk=ordered_product_obj['product_option'])
            models.OrderedProduct.objects.create(
                product=product_obj,
                product_option=product_option_obj,
                order=created_order,
                quantity=ordered_product_obj['quantity'],
                original_price=original_price,
                discount_price=discount_price,
                discount_rate=ordered_product_obj['discount_rate'],
                is_free_ship=ordered_product_obj['is_free_ship'],
            )
        models.OrderGroupStatusLog.objects.create(order_group=created_order_group, order_status='order-processing')
        headers = self.get_success_headers(serializer.data)
        # 토큰 생성 여부
        message_body = 'Mã số đơn hàng: : ' + created_order_group.slug
        push_response_success = 'Failed'
        try:
            user_push_token_set = created_order.customer.userpushtoken_set.all()
            for token_object in user_push_token_set:
                push_response = send_push_message(token_object.push_token, message_body, 'Xác nhận đặt hàng')
                if push_response:
                    push_response_success = 'Sent'
        except Exception as e:
            print(e)
        try:
            slack_notify('#{pk} - Order Group created (Push : {push})+ https://dabivn.com/admin/order/ordergroup/{pk}'.format(
                push=push_response_success, pk=created_order_group.pk), channel='#7_order')
        except Exception:
            pass
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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
            if ('discount_price' in ordered_product_obj):
                ordered_product.discount_price = ordered_product_obj['discount_price']
                ordered_product.save()
        try:
            coupon_id = request.data.__getitem__('coupon_code')
            if coupon_id:
                coupon_obj = models.Coupon.objects.get(id=coupon_id)
                models.AppliedCoupon.objects.create(coupon=coupon_obj, user=request.user, order=created_order)
        except Exception:
            pass
        models.OrderStatusLog.objects.create(order=created_order, order_status='order-processing')
        headers = self.get_success_headers(serializer.data)
        # 토큰 생성 여부
        message_body = 'Mã số đơn hàng: : ' + created_order.slug
        push_response_success = 'Failed'
        try:
            user_push_token_set = created_order.customer.userpushtoken_set.all()
            for token_object in user_push_token_set:
                push_response = send_push_message(token_object.push_token, message_body, 'Xác nhận đặt hàng')
                if push_response:
                    push_response_success = 'Sent'
        except Exception as e:
            print(e)
        try:
            slack_notify('#{pk} - Order created (Push : {push})+ https://dabivn.com/admin/order/order/{pk}'.format(
                push=push_response_success, pk=created_order.pk), channel='#7_order')
        except Exception:
            pass
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
        previous_status = order_obj.order_status
        if order_status == 'cancelled':
            order_obj.is_active = False
        order_obj.order_status = order_status
        order_obj.save()
        slack_notify('#{pk} - Order Status Change {previous_status} => {order_status} https://dabivn.com/admin/order/order/{pk}'.format(
            previous_status=previous_status, order_status=order_status, pk=order_obj.pk), channel='#7_order')

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class DeliveryStatusView(generics.ListAPIView):
    serializer_class = serializers.DeliveryStatusSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        order_slug = self.kwargs['slug']
        queryset = models.DeliveryStatus.objects.filter(order__slug=order_slug)
        return queryset
