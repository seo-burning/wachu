from django.contrib import admin
from .models import Order, OrderedProduct, OrderStatusLog, Coupon, AppliedCoupon
# Register your models here.


class OrderedProductInline(admin.TabularInline):
    model = OrderedProduct
    fields = ['product', 'quantity',
              'original_price',
              'discount_price',
              'discount_rate',
              'is_free_ship']
    readonly_fields = ['product', 'quantity',
                       'original_price',
                       'discount_price',
                       'discount_rate',
                       'is_free_ship']
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderedProductInline, ]
    list_display = ['is_active', 'order_status', 'created_at', 'slug', 'customer']


@admin.register(OrderedProduct)
class OrderedProductAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderStatusLog)
class OrderStatusLogAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'order_status', 'created_at']
    list_filter = ['order_status', ]
    search_fields = ['customer__name']


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'is_active', 'scope', 'valid_date', 'restriction',
                    'discount_rate', 'discount_price',
                    'max_discount_price', 'minimun_order_price']


@admin.register(AppliedCoupon)
class AppliedCouponAdmin(admin.ModelAdmin):
    pass
