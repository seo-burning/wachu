from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe

from product.models import Product, ProductStyle
from store.models import Store


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserFavoriteProduct(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)


class ReviewImage(TimeStampedModel):
    source = models.ImageField(
        blank=True, upload_to='review/%Y/%m')
    review = models.ForeignKey(
        'ProductReview', on_delete=models.CASCADE, related_name='review_image_set')

    def __str__(self):
        return mark_safe('<img src="{url}" \
        width="100" height="100" border="1" />'.format(
            url=self.source
        ))


class ProductReview(TimeStampedModel):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                blank=True)
    description = models.TextField()
    rating = models.IntegerField()

    def __str__(self):
        return self.store.insta_id + self.user.name


class RecipientModel(models.Model):
    class Meta:
        abstract = True
    recipient_name = models.CharField(
        max_length=250, null=True)
    contact_number = models.CharField(
        max_length=250, null=True)
# 159 Xa lộ Hà Nội, Thảo Điền, Quận 2, Hồ Chí Minh
    country = models.CharField(
        max_length=50, null=True, default='Việt Nam')
    city = models.CharField(u'Tỉnh/Thành Phố',
                            max_length=50, null=True)
    district = models.CharField(u'Quận/Huyện',
                                max_length=50, null=True)
    ward = models.CharField(u'Phường/Xã',
                            max_length=50, null=True)
    additional_address = models.CharField(u'Địa chỉ cụ thể',
                                          max_length=250, null=True)


class Recipient(RecipientModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, null=True)
    primary = models.BooleanField(default=False)

    def __str__(self):
        return self.city + ' ' + self.district + ' ' + self.ward + ' ' + self.additional_address

    class Meta:
        ordering = ['-primary', ]


class UserStyleTaste(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, null=True)
    lovely = models.IntegerField(default=0)
    sexy = models.IntegerField(default=0)
    simple = models.IntegerField(default=0)
    street = models.IntegerField(default=0)
    feminine = models.IntegerField(default=0)
    primary_style = models.ForeignKey(
        ProductStyle, on_delete=models.SET_NULL,
        related_name='user_style_tastes_on_primary_style',
        null=True, blank=True)
    secondary_style = models.ForeignKey(
        ProductStyle, on_delete=models.SET_NULL,
        related_name='user_style_tastes_on_secondary_style',
        null=True, blank=True)
