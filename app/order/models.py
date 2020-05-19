from django.utils.crypto import get_random_string
from django.db import models
from django.conf import settings

from product.models import PriceModel, Product
from user.models import RecipientModel
# Create your models here.


class TimeStampedModel(models.Model):
    class Meta:
        abstract = True
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderStatusModel(models.Model):
    class Meta:
        abstract = True

    STATUS_CHOICES = [
        ('order-processing', '주문 완료'),
        ('delivery', '배송 중'),
        ('delivered', '배송 완료'),
        ('done', '구매 완료'),
        ('cancelled', '주문 취소'),
        ('change-processing', '교환'),
        ('refund-processing', '환불'),
    ]
    order_status = models.CharField(u'주문상태', default='order-processing', max_length=50, choices=STATUS_CHOICES)


class PaymentModel(models.Model):
    class Meta:
        abstract = True
    PAYMENT_CHOICES = [('cod', 'COD')]
    payment = models.CharField(u'결제 방식', max_length=50)


class DeliveryStatusModel(models.Model):
    class Meta:
        abstract = True

    delivery_status = models.CharField(u'배송상태', max_length=50, blank=True)


class ActiveModel(models.Model):
    class Meta:
        abstract = True
    is_active = models.BooleanField(default=False)


class OrderedProduct(PriceModel, TimeStampedModel):
    # 주문한 시점의 상태를 기록할 필요가 있음, 가격 등의 변동이 있을 가능성이 존재함.
    class Meta:
        verbose_name = u'주문 제품'
        verbose_name_plural = verbose_name
    order = models.ForeignKey('Order', verbose_name=u'주문서',
                              on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, verbose_name=u'제품', on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(u'수량', default=1)


class OrderStatusLog(OrderStatusModel, TimeStampedModel, DeliveryStatusModel):
    class Meta:
        verbose_name = u'주문 상태'
        verbose_name_plural = verbose_name

    order = models.ForeignKey('Order', verbose_name=u'주문',
                              on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.order)


class Order(OrderStatusModel, TimeStampedModel, PriceModel, ActiveModel, RecipientModel, PaymentModel):
    class Meta:
        verbose_name = u'주문'
        verbose_name_plural = verbose_name
    customer = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.SET_NULL, null=True)
    extra_message = models.CharField(max_length=255, blank=True)
    total_price = models.IntegerField(default=0)
    # blank if it needs to be migrated to a model that didn't already have this
    slug = models.SlugField(max_length=8, blank=True)

    def __str__(self):
        return self.customer.name + ' ' + self.created_at.strftime("%m/%d/%Y, %H:%M:%S")

    def save(self, *args, **kwargs):
        """ Add Slug creating/checking to save method. """
        slug_save(self)  # call slug_save, listed below
        super(Order, self).save(*args, **kwargs)


def slug_save(obj):
    """ A function to generate a 8 character slug and see if it has been used and contains naughty words."""
    if not obj.slug:  # if there isn't a slug
        obj.slug = get_random_string(8).upper()  # create one
        slug_is_wrong = True
        while slug_is_wrong:  # keep checking until we have a valid slug
            slug_is_wrong = False
            other_objs_with_slug = type(obj).objects.filter(slug=obj.slug)
            if len(other_objs_with_slug) > 0:
                # if any other objects have current slug
                slug_is_wrong = True
            naughty_words = ['dabi', 'dacbiet']
            if obj.slug in naughty_words:
                slug_is_wrong = True
            if slug_is_wrong:
                # create another slug and check it again
                obj.slug = get_random_string(8)
