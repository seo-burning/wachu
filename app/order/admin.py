from django.contrib import admin
from .models import Order, OrderedProduct, OrderStatusLog
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
    pass


@admin.register(OrderedProduct)
class OrderedProductAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderStatusLog)
class OrderStatusLogAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'order_status', 'created_at']
    list_filter = ['order_status', ]
    search_fields = ['customer__name']
