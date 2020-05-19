from rest_framework import generics, authentication, permissions
from order import serializers, models
from rest_framework.response import Response
from rest_framework import status
from product.models import Product


class OrderListView(generics.ListAPIView):
    serializer_class = serializers.OrderSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = models.Order.objects.filter(customer=self.request.user)
        queryset = self.get_serializer_class().setup_eager_loading(queryset)
        return queryset


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
            ordered_product = models.OrderedProduct.objects.create(
                product=product_obj,
                order=created_order,
                quantity=ordered_product_obj['quantity'],
                original_price=ordered_product_obj['original_price'],
                discount_rate=ordered_product_obj['discount_rate'],
                is_free_ship=ordered_product_obj['is_free_ship'],
            )
            if(ordered_product_obj['discount_price']):
                ordered_product.discount_price = ordered_product_obj['discount_price']
                ordered_product.save()
        models.OrderStatusLog.objects.create(order=created_order, order_status='order-processing')
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # 주문을 만드면서, 각 단계에 대한 Order Status Log를 만들어야한다.
    # 주문을 만드면서, 해당 상태에서 고정된 상품을 생성해야 한다.


# class OrderCreateView(generics.CreateAPIView):
#     serializer_class = serializers.OrderedProductSerializer
#     authentication_classes = (authentication.TokenAuthentication,)
#     permission_classes = (permissions.IsAuthenticated,)

    # 주문을 만드면서, 각 단계에 대한 Order Status Log를 만들어야한다.
    # 주문을 만드면서, 해당 상태에서 고정된 상품을 생성해야 한다.
