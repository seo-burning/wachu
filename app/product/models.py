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


class ProductTag(TimeStampedModel):
    name = models.CharField(_('Product Tag'), max_length=255, unique=True)

    def __str__(self):
        return self.name


class ProductSize(TimeStampedModel):
    name = models.CharField(_('Product Size'), max_length=255)

    def __str__(self):
        return self.name


class Product(TimeStampedModel):
    is_active = models.BooleanField(default=False)
    store = models.ForeignKey('store.Store', on_delete=models.CASCADE)
    name = models.CharField(_('Product Model'), max_length=255)
    category = models.ForeignKey(
        ProductCategory, on_delete=models.SET_NULL, null=True, blank=True)
    color = models.ManyToManyField(
        ProductColor, blank=True)
    tag = models.ManyToManyField(
        ProductTag)
    price = models.PositiveIntegerField(null=True, blank=True)
    size = models.ManyToManyField(
        ProductSize, blank=True)
    post = models.ForeignKey(
        'store.StorePost', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
