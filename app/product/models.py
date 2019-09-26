from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ProductCategory(TimeStampedModel):
    name = models.CharField(_('Product Category'), max_length=255)

    def __str__(self):
        return self.name


class ProductSubCategory(TimeStampedModel):
    name = models.CharField(_('Product SubCategory'), max_length=255)
    category = models.ForeignKey(
        ProductCategory, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class ProductLength(TimeStampedModel):
    name = models.CharField(_('Product Length'), max_length=255)

    def __str__(self):
        return self.name


class ProductSleeveLength(TimeStampedModel):
    name = models.CharField(_('Product Sleeve Length'), max_length=255)

    def __str__(self):
        return self.name


class ProductMaterial(TimeStampedModel):
    name = models.CharField(_('Product Material'), max_length=255)

    def __str__(self):
        return self.name


class ProductDetail(TimeStampedModel):
    name = models.CharField(_('Product Detail'), max_length=255)

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


class Product(TimeStampedModel):
    is_active = models.BooleanField(default=False)
    store = models.ForeignKey('store.Store',
                              on_delete=models.CASCADE)
    name = models.CharField(_('Product Name'), max_length=255, blank=True)
    category = models.ForeignKey(
        ProductCategory, on_delete=models.SET_NULL,

        null=True, blank=True)
    sub_category = models.ForeignKey(
        ProductSubCategory, on_delete=models.SET_NULL,
        null=True, blank=True)

    length = models.ForeignKey(
        ProductLength, on_delete=models.SET_NULL,
        null=True, blank=True)
    sleeve_length = models.ForeignKey(
        ProductSleeveLength, on_delete=models.SET_NULL,
        null=True, blank=True)

    material = models.ForeignKey(
        ProductMaterial, on_delete=models.SET_NULL,
        null=True, blank=True)
    detail = models.ForeignKey(
        ProductDetail, on_delete=models.SET_NULL,
        null=True, blank=True)
    color = models.ManyToManyField(
        ProductColor, blank=True)

    tag = models.ManyToManyField(
        ProductTag, blank=True)
    post = models.ForeignKey(
        'store.StorePost', on_delete=models.CASCADE)

    def __str__(self):
        return mark_safe('<img src="{url}" \
        width="300" height="300" border="1" />'.format(
            url=self.post.post_thumb_image
        ))
