from django.contrib import admin
from .models import Order, OrderedProduct, OrderStatusLog, \
    Coupon, AppliedCoupon, DeliveryStatus
# Register your models here.
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from utils.helper.admin.mixins import ToggleActiveMixin


class DeliveryStatusInline(admin.TabularInline):
    model = DeliveryStatus
    fields = ['delivery_status', 'status_timestamp']
    extra = 0


class OrderStatusLogInline(admin.TabularInline):
    model = OrderStatusLog
    readonly_fields = ['order_status', 'created_at']
    fields = ['order_status', 'created_at']
    extra = 0
    can_delete = False


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
    inlines = [OrderStatusLogInline, OrderedProductInline, DeliveryStatusInline]
    list_display = ['is_active',
                    'order_status', 'created_at', 'slug', 'customer']
    actions = ['make_activate', 'make_deactivate', ]
    list_filter = ['is_active', ]

    def save_model(self, request, obj, form, change):
        if 'order_status' in form.changed_data:
            new_order_status = form.cleaned_data.get('order_status')
            OrderStatusLog.objects.create(order_status=new_order_status,
                                          order=obj)
        super().save_model(request, obj, form, change)
        # TODO Push Alarm 1. Navagation 가능한 Data 심기, 2. 푸쉬 알림 보내기 확인 창 띄우기(쉽지 않아 보임.), 3. 무조건 보낸다..?, 4. 별도의 푸쉬 알림 보내는 걸 만든다?


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
