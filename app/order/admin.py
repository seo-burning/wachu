from django.contrib import admin
from .models import Order, OrderedProduct, OrderStatusLog, \
    Coupon, AppliedCoupon, DeliveryStatus, \
    OrderGroup, OrderGroupStatusLog
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


class OrderGroupStatusLogInline(admin.TabularInline):
    model = OrderGroupStatusLog
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


class OrderInline(admin.TabularInline):
    model = Order
    fields = ['is_active',
              'order_status', 'store',  'total_price', 'product_num', ]
    readonly_fields = ['is_active', 'total_price', 'store', 'product_num',
                       'order_status', ]
    extra = 0
    show_change_link = True

    def product_num(self, instance):
        return len(instance.orderedproduct_set.all())


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin, ToggleActiveMixin):
    inlines = [OrderStatusLogInline, OrderedProductInline, DeliveryStatusInline]
    list_display = ['is_active', 'store',
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


@admin.register(OrderGroup)
class OrderGroupAdmin(admin.ModelAdmin, ToggleActiveMixin):
    inlines = [OrderInline, OrderGroupStatusLogInline]
    list_display = ['is_active',
                    'order_status', 'created_at', 'slug', 'customer']


@admin.register(OrderGroupStatusLog)
class OrderGroupStatusLogAdmin(admin.ModelAdmin):
    pass


# for obj in Order.objects.all():
#     group_obj, is_created = OrderGroup.objects.get_or_create(
#         is_active=obj.is_active,
#         customer=obj.customer,
#         extra_message=obj.extra_message,
#         coupon_discounted=obj.coupon_discounted,
#         total_price=obj.total_price,
#         slug=obj.slug,
#         order_status=obj.order_status,
#         original_price=obj.original_price,
#         discount_price=obj.discount_price,
#         discount_rate=obj.discount_rate,
#         currency=obj.currency,
#         is_free_ship=obj.is_free_ship,
#         shipping_price=obj.shipping_price,
#         # created_at=obj.created_at,
#         # updated_at=obj.updated_at,
#         payment=obj.payment,
#         recipient_name=obj.recipient_name,
#         contact_number=obj.contact_number,
#         country=obj.country,
#         city=obj.city,
#         district=obj.district,
#         ward=obj.ward,
#         additional_address=obj.additional_address
#     )
#     group_obj.created_at = obj.created_at
#     group_obj.updated_at = obj.updated_at
#     group_obj.save()
#     print(group_obj, is_created)
#     obj.order_group = group_obj
#     OrderGroupStatusLog.objects.get_or_create(order_group=group_obj, order_status=group_obj.order_status)
#     obj.save()
