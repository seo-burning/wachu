from rest_framework import serializers
from order.models import Order, OrderedProduct, \
    Coupon, AppliedCoupon, OrderStatusLog, DeliveryStatus, OrderGroup
from product.serializers import ProductSerializer, ProductOptionSerializer, ProductThumbSerializer


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
    store = serializers.StringRelatedField(many=False)

    class Meta:
        model = Order
        fields = ['order_status',
                  'store',
                  'delivery_company',
                  'delivery_tracking_code',
                  'estimated_delivery_date',
                  'applied_coupons',
                  'orderedproduct_set',
                  'slug',
                  'original_price', 'discount_price',
                  'is_free_ship', 'shipping_price', 'currency',
                  'total_price', 'payment',
                  'coupon_discounted',
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


class OrderedProductInlineSerializer(serializers.ModelSerializer):
    product = ProductThumbSerializer(many=False)
    product_option = ProductOptionSerializer(many=False)

    class Meta:
        model = OrderedProduct
        fields = ['product', 'product_option']


class OrderInlineSerializer(serializers.ModelSerializer):
    orderedproduct_set = OrderedProductInlineSerializer(many=True)

    class Meta:
        model = Order
        fields = ['order_status',
                  'orderedproduct_set',
                  'slug',  'created_at', 'updated_at', 'pk']

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        # select_related for "to-one" relationships
        queryset = queryset.select_related(
            'customer',)
        queryset = queryset.prefetch_related(
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


class OrderGroupListSerializer(serializers.ModelSerializer):
    order_set = OrderInlineSerializer(many=True)

    class Meta:
        model = OrderGroup
        fields = ['order_status',
                  'slug',
                  'created_at',
                  'updated_at',
                  'pk',
                  'recipient_name', 'contact_number',
                  'country', 'city', 'district', 'ward', 'additional_address',
                  'original_price', 'discount_price',
                  'is_free_ship', 'shipping_price', 'currency',
                  'total_price', 'payment',
                  'extra_message',
                  'order_set']

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        # select_related for "to-one" relationships
        queryset = queryset.select_related(
            'customer',)
        queryset = queryset.prefetch_related(
            'order_set__orderedproduct_set',
            'order_set__orderedproduct_set__product',
            'order_set__orderedproduct_set__product_option',
            'order_set__orderedproduct_set__product_option__color',
            'order_set__orderedproduct_set__product_option__size',
            'order_set__orderedproduct_set__product__post__post_image_set',
            'order_set__orderedproduct_set__product__color',
            'order_set__orderedproduct_set__product__style',
            'order_set__orderedproduct_set__product__size',
            'order_set__orderedproduct_set__product__extra_option',
            'order_set__orderedproduct_set__product__favorite_users',
            'order_set__orderedproduct_set__product__category',
            'order_set__orderedproduct_set__product__sub_category',
            'order_set__orderedproduct_set__product__shopee_rating',
            'order_set__orderedproduct_set__product__store__favorite_users',
            'order_set__orderedproduct_set__product__store__category',
            'order_set__orderedproduct_set__product__product_image_set',
            'order_set__orderedproduct_set__product__store__product_category',
            'order_set__orderedproduct_set__product__store__age',
            'order_set__orderedproduct_set__product__store__primary_style',
            'order_set__orderedproduct_set__product__store__secondary_style',
            'order_set__orderedproduct_set__product__product_options',
            'order_set__orderedproduct_set__product__product_options__color',
            'order_set__orderedproduct_set__product__product_options__size',
        )
        return queryset


class OrderGroupDetailSerializer(serializers.ModelSerializer):
    order_set = OrderSerializer(many=True)
    store = serializers.StringRelatedField(many=False)

    class Meta:
        model = OrderGroup
        fields = ['order_status',
                  'store',
                  'slug',
                  'created_at',
                  'updated_at',
                  'pk',
                  'recipient_name', 'contact_number',
                  'country', 'city', 'district', 'ward', 'additional_address',
                  'original_price', 'discount_price', 'coupon_discounted',
                  'is_free_ship', 'shipping_price', 'currency',
                  'total_price', 'payment',
                  'extra_message',
                  'order_set']

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        # select_related for "to-one" relationships
        queryset = queryset.select_related(
            'customer',)
        queryset = queryset.prefetch_related(
            'order_set__orderedproduct_set',
            'order_set__orderedproduct_set__product',
            'order_set__orderedproduct_set__product_option',
            'order_set__orderedproduct_set__product_option__color',
            'order_set__orderedproduct_set__product_option__size',
            'order_set__orderedproduct_set__product__post__post_image_set',
            'order_set__orderedproduct_set__product__color',
            'order_set__orderedproduct_set__product__style',
            'order_set__orderedproduct_set__product__size',
            'order_set__orderedproduct_set__product__extra_option',
            'order_set__orderedproduct_set__product__favorite_users',
            'order_set__orderedproduct_set__product__category',
            'order_set__orderedproduct_set__product__sub_category',
            'order_set__orderedproduct_set__product__shopee_rating',
            'order_set__orderedproduct_set__product__store__favorite_users',
            'order_set__orderedproduct_set__product__store__category',
            'order_set__orderedproduct_set__product__product_image_set',
            'order_set__orderedproduct_set__product__store__product_category',
            'order_set__orderedproduct_set__product__store__age',
            'order_set__orderedproduct_set__product__store__primary_style',
            'order_set__orderedproduct_set__product__store__secondary_style',
            'order_set__orderedproduct_set__product__product_options',
            'order_set__orderedproduct_set__product__product_options__color',
            'order_set__orderedproduct_set__product__product_options__size',
        )
        return queryset


class OrderGroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderGroup
        exclude = ['customer',  'currency', 'country', 'slug', ]


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ['customer', 'currency', 'country', 'slug', 'store', 'order_group', 'estimated_delivery_date']


class OrderStatusLogCreateSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())

    class Meta:
        model = OrderStatusLog
        fields = ['order', 'order_status', ]


class DeliveryStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryStatus
        exclude = ['order', ]
