from rest_framework import serializers
from order.models import Order, OrderedProduct
from product.serializers import ProductSerializer


class OrderedProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False)

    class Meta:
        model = OrderedProduct
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    orderedproduct_set = OrderedProductSerializer(many=True)

    class Meta:
        model = Order
        fields = ['orderedproduct_set', 'slug', 'original_price', 'discount_price',
                  'discount_rate', 'is_free_ship', 'shipping_price', 'currency',
                  'total_price',  'payment', 'order_status',
                  'recipient_name', 'contact_number', 'country',
                  'city', 'district', 'ward', 'additional_address',
                  'extra_message', ]

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        # select_related for "to-one" relationships
        queryset = queryset.select_related(
            'customer',)
        queryset = queryset.prefetch_related(
            'orderedproduct_set',
            'orderedproduct_set__product',
            'orderedproduct_set__product__post__post_image_set',
            'orderedproduct_set__product__color',
            'orderedproduct_set__product__size',
            'orderedproduct_set__product__style',
            'orderedproduct_set__product__extra_option',
            'orderedproduct_set__product__favorite_users',
            'orderedproduct_set__product__store__favorite_users',
            'orderedproduct_set__product__store__category',
            'orderedproduct_set__product__product_image_set',
            'orderedproduct_set__product__store__product_category'
        )
        return queryset


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ['customer', 'currency', 'country', 'slug']
