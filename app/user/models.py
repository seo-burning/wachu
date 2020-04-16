from django.db import models
from django.conf import settings

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


class StoreReview(TimeStampedModel):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                blank=True)
    description = models.TextField()
    rating = models.IntegerField()

    def __str__(self):
        return self.store.insta_id + self.user.name
