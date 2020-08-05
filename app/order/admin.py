from django.contrib import admin
from .models import Order, OrderedProduct, OrderStatusLog, Coupon, AppliedCoupon
# Register your models here.
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from utils.helper.admin.mixins import ToggleActiveMixin


class OrderedProductInline(admin.TabularInline):
    model = OrderedProduct
    fields = ['product_thumbnail_image',
              'product_link',
              'product_option', 'quantity',
              'original_price',
              'discount_price',
              'discount_rate',
              'is_free_ship']
    readonly_fields = ['product_thumbnail_image', 'product_link',
                       'product_option', 'quantity',
                       'original_price',
                       'discount_price',
                       'discount_rate',
                       'is_free_ship']
    extra = 0

    def product_link(self, instance):
        return format_html('<a href="%s"  target="_blank">Buy</a>' % (instance.product.product_link))

    def product_thumbnail_image(self, instance):
        return mark_safe('<img src="{url}" \
        width="50" height="50" border="1" />'.format(
            url=instance.product.product_thumbnail_image
        ))


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin, ToggleActiveMixin):
    inlines = [OrderedProductInline, ]
    list_display = ['is_active', 'order_status', 'created_at', 'slug', 'customer']
    actions = ['make_activate', 'make_deactivate', ]


@admin.register(OrderedProduct)
class OrderedProductAdmin(admin.ModelAdmin):
    raw_id_fields = ['product', 'order']
    readonly_fields = ['product', 'order']

    def get_queryset(self, request):
        qs = super(OrderedProductAdmin, self).get_queryset(request)
        return qs.select_related('product', 'order')


@admin.register(OrderStatusLog)
class OrderStatusLogAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'order_status', 'created_at']
    list_filter = ['order_status', ]
    search_fields = ['customer__name']


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'is_active', 'is_public', 'scope', 'valid_date', 'restriction',
                    'discount_rate', 'discount_price',
                    'max_discount_price', 'minimun_order_price']


@admin.register(AppliedCoupon)
class AppliedCouponAdmin(admin.ModelAdmin):
    pass
