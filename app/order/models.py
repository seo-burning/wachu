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


class Order(OrderStatusModel, TimeStampedModel, PriceModel, ActiveModel, RecipientModel):
    class Meta:
        verbose_name = u'주문'
        verbose_name_plural = verbose_name
    customer = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.SET_NULL, null=True)
    extra_message = models.CharField(max_length=255)

    def __str__(self):
        return self.customer.name + self.created_at.strftime("%m/%d/%Y, %H:%M:%S")
