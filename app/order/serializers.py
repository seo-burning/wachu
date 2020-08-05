from rest_framework import serializers
from order.models import Order, OrderedProduct, \
    Coupon, AppliedCoupon, OrderStatusLog, DeliveryStatus
from product.serializers import ProductSerializer, ProductOptionSerializer


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'


class OrderedProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False)
    product_option = ProductOptionSerializer(many=False)

    class Meta:
        model = OrderedProduct
        fields = '__all__'


class AppliedCouponSerializer(serializers.ModelSerializer):
    coupon = CouponSerializer(many=False)

    class Meta:
        model = AppliedCoupon
        fields = ['coupon', ]
# TODO EAGER LOADING


class OrderSerializer(serializers.ModelSerializer):
    orderedproduct_set = OrderedProductSerializer(many=True)
    applied_coupons = AppliedCouponSerializer(many=True)

    class Meta:
        model = Order
        fields = ['order_status',
                  'delivery_company',
                  'delivery_tracking_code',
                  'applied_coupons',
                  'orderedproduct_set',
                  'slug', 'original_price', 'discount_price',
                  'discount_rate', 'is_free_ship', 'shipping_price', 'currency',
                  'total_price',  'payment', 'coupon_discounted',
                  'recipient_name', 'contact_number', 'country',
                  'city', 'district', 'ward', 'additional_address',
                  'extra_message', 'created_at', 'updated_at', 'pk']

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        # select_related for "to-one" relationships
        queryset = queryset.select_related(
            'customer',)
        queryset = queryset.prefetch_related(
            'applied_coupons',
            'applied_coupons__coupon',
            'orderedproduct_set',
            'orderedproduct_set__product',
            'orderedproduct_set__product_option',
            'orderedproduct_set__product_option__color',
            'orderedproduct_set__product_option__size',
            'orderedproduct_set__product__post__post_image_set',
            'orderedproduct_set__product__color',
            'orderedproduct_set__product__style',
            'orderedproduct_set__product__size',
            'orderedproduct_set__product__extra_option',
            'orderedproduct_set__product__favorite_users',
            'orderedproduct_set__product__category',
            'orderedproduct_set__product__sub_category',
            'orderedproduct_set__product__shopee_rating',
            'orderedproduct_set__product__store__favorite_users',
            'orderedproduct_set__product__store__category',
            'orderedproduct_set__product__product_image_set',
            'orderedproduct_set__product__store__product_category',
            'orderedproduct_set__product__store__age',
            'orderedproduct_set__product__store__primary_style',
            'orderedproduct_set__product__store__secondary_style',
            'orderedproduct_set__product__product_options',
            'orderedproduct_set__product__product_options__color',
            'orderedproduct_set__product__product_options__size',
        )
        return queryset


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ['customer', 'currency', 'country', 'slug']


class OrderStatusLogCreateSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())

    class Meta:
        model = OrderStatusLog
        fields = ['order', 'order_status', 'delivery_status']


class DeliveryStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryStatus
        exclude = ['order', ]
