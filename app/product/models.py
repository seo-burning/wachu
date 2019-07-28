from django.db import models
from django.utils.translation import ugettext_lazy as _


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ProductCategory(TimeStampedModel):
    name = models.CharField(_('Product Category'), max_length=255)

    def __str__(self):
        return self.name


class ProductColor(TimeStampedModel):
    name = models.CharField(_('Product Color'), max_length=255)

    def __str__(self):
        return self.name


class ProductSize(TimeStampedModel):
    name = models.CharField(_('Product Size'), max_length=255)

    def __str__(self):
        return self.name


class Product(TimeStampedModel):
    store = models.ForeignKey('store.Store', on_delete=models.CASCADE)
    name = models.CharField(_('Product Model'), max_length=255)
    category = models.ForeignKey(
        ProductCategory, on_delete=models.SET_NULL, null=True)
    color = models.ManyToManyField(
        ProductColor)
    price = models.PositiveIntegerField(null=True)
    size = models.ManyToManyField(
        ProductSize)

    def __str__(self):
        return self.name
