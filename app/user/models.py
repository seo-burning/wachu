from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe

from product.models import Product
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
