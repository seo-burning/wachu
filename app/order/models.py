from django.utils.crypto import get_random_string
from django.db import models
from django.conf import settings

from product.models import PriceModel, Product, ProductOption
from user.models import RecipientModel

from utils.helper.model.abstract_model import TimeStampedModel, ActiveModel, PublicModel
# Create your models here.


class OrderStatusModel(models.Model):
    class Meta:
        abstract = True

    STATUS_CHOICES = [
        ('order-processing', '주문 완료'),
        ('delivery', '배송 중'),
        ('delivered', '배송 완료'),
        ('order-complete', '구매 완료'),
        ('cancelled', '주문 취소'),
        ('change-processing', '교환'),
        ('refund-processing', '환불'),
        ('refund-complete', '환불 완료'),
        ('change-complete', '교환 완료'),

    ]
    order_status = models.CharField(u'주문상태', default='order-processing', max_length=50, choices=STATUS_CHOICES)


class PaymentModel(models.Model):
    class Meta:
        abstract = True
    PAYMENT_CHOICES = [('cod', 'COD')]
    payment = models.CharField(u'결제 방식', max_length=50)


class DeliveryTrackingCodeModel(models.Model):
    class Meta:
        abstract = True
    DELIVERY_COMPANY_CHOICES = [('J&T Express', 'JT_Express'), ('Giao Hàng Nhanh', 'Giao_Hang_Nhanh'), ]

    delivery_company = models.CharField(u'배송업체', choices=DELIVERY_COMPANY_CHOICES,
                                        max_length=50, blank=True, null=True, default=None)
    delivery_tracking_code = models.CharField(u'배송조회 번호', max_length=50, blank=True, null=True, default=None)


# TODO Order Status Update Make Automatically Push and blah blah
class DeliveryStatusModel(models.Model):
    class Meta:
        abstract = True

    delivery_status = models.CharField(u'배송상태', max_length=50, blank=True)


class CouponModel(models.Model):
    class Meta:
        abstract = True
    SCOPE_CHOICES = [('total', 'TOTAL_PRICE'), ('shipping', 'SHIPPING'), ('product', 'PRODUCT')]

    discount_price = models.IntegerField(null=True, blank=True)
    discount_rate = models.IntegerField(null=True, blank=True)
    max_discount_price = models.IntegerField(null=True, blank=True)
    minimun_order_price = models.IntegerField(null=True, blank=True)
    code = models.CharField(max_length=10)
    description = models.CharField(max_length=255, blank=True)
    valid_date = models.DateTimeField()
    scope = models.CharField(default='total', max_length=50,
                             choices=SCOPE_CHOICES)


class CouponRestrictionModel(models.Model):
    class Meta:
        abstract = True
    RESTRICTION_CHOICES = [('none', 'NONE')]
    restriction = models.CharField(default='none', max_length=50,
                                   choices=RESTRICTION_CHOICES)
# Coupon Type 설계 필요.


class Coupon(ActiveModel, CouponModel, TimeStampedModel, CouponRestrictionModel, PublicModel):
    class Meta:
        verbose_name = u'쿠폰'
        verbose_name_plural = verbose_name


class AppliedCoupon(TimeStampedModel):
    class Meta:
        verbose_name = u'사용 쿠폰'
        verbose_name_plural = verbose_name

    coupon = models.ForeignKey(Coupon, verbose_name=u'쿠폰', on_delete=models.SET_NULL,
                               null=True, related_name='used_coupons')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'유저', on_delete=models.SET_NULL,
                             null=True, related_name='used_coupons')
    order = models.ForeignKey('Order', verbose_name=u'주문',
                              on_delete=models.SET_NULL, null=True, related_name='applied_coupons')


class OrderedProduct(PriceModel, TimeStampedModel):
    # 주문한 시점의 상태를 기록할 필요가 있음, 가격 등의 변동이 있을 가능성이 존재함.
    class Meta:
        verbose_name = u'주문 제품'
        verbose_name_plural = verbose_name
        ordering = ['-created_at', 'order']

    order = models.ForeignKey('Order', verbose_name=u'주문서',
                              on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, verbose_name=u'제품',
                                on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(u'수량', default=1)
    product_option = models.ForeignKey(ProductOption, verbose_name=u'제품 옵션',
                                       on_delete=models.SET_NULL,
                                       null=True)

    def __str__(self):
        ordered_product_string = ''
        if self.order:
            ordered_product_string = 'order ' + str(self.order.pk)
        ordered_product_string = ordered_product_string + ' / option ' + \
            str(self.product_option) + ' / quantity ' + str(self.quantity)
        return ordered_product_string


class OrderStatusLog(OrderStatusModel, TimeStampedModel):
    class Meta:
        verbose_name = u'주문 상태'
        verbose_name_plural = verbose_name
        ordering = ['-created_at', 'order']

    order = models.ForeignKey('Order', verbose_name=u'주문',
                              on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.order)


class Order(OrderStatusModel, TimeStampedModel, PriceModel, ActiveModel,
            RecipientModel, PaymentModel, DeliveryTrackingCodeModel):
    class Meta:
        verbose_name = u'주문'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    customer = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.SET_NULL, null=True)
    extra_message = models.CharField(max_length=255, blank=True)
    coupon_discounted = models.IntegerField(default=0)
    total_price = models.IntegerField(default=0)
    # blank if it needs to be migrated to a model that didn't already have this
    slug = models.SlugField(max_length=8, blank=True)

    def __str__(self):
        return str(self.pk) + ' ' + self.created_at.strftime("%m/%d/%Y, %H:%M:%S")

    def save(self, *args, **kwargs):
        """ Add Slug creating/checking to save method. """
        # TODO 이전 필드랑 비교하는 것..?
        slug_save(self)  # call slug_save, listed below
        super(Order, self).save(*args, **kwargs)


def slug_save(obj):
    if not obj.slug:  # if there isn't a slug
        obj.slug = get_random_string(8).upper()  # create one
        slug_is_wrong = True
        while slug_is_wrong:  # keep checking until we have a valid slug
            slug_is_wrong = False
            other_objs_with_slug = type(obj).objects.filter(slug=obj.slug)
            if len(other_objs_with_slug) > 0:
                # if any other objects have current slug
                slug_is_wrong = True
            naughty_words = ['sex', 'fuck']
            if obj.slug in naughty_words:
                slug_is_wrong = True
            if slug_is_wrong:
                # create another slug and check it again
                obj.slug = get_random_string(8)


class DeliveryStatus(models.Model):
    class Meta:
        ordering = ['-status_timestamp']

    delivery_status = models.CharField(u'배송상태', max_length=500, blank=True)
    order = models.ForeignKey('Order', verbose_name=u'주문서',
                              on_delete=models.CASCADE, null=True)
    status_timestamp = models.DateTimeField(blank=True)

    def __str__(self):
        return self.delivery_status
