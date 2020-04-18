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


class ProductSize(TimeStampedModel):
    name = models.CharField(_('Product Length'), max_length=255)

    def __str__(self):
        return self.name


class ProductColor(TimeStampedModel):
    name = models.CharField(
        _('Product Color'), max_length=255, blank=True, null=True)
    display_name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class ProductTag(TimeStampedModel):
    name = models.CharField(_('Product Tag'),
                            max_length=255, unique=True)

    def __str__(self):
        return self.name


class ProductStyle(TimeStampedModel):
    name = models.CharField(_('Product Style'),
                            max_length=255, unique=True)

    def __str__(self):
        return self.name


class ProductExtraOption(TimeStampedModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


POST_IMAGE_TYPE = (('P', _('Picture')), ('V', _('Video')))


class ProductImage(TimeStampedModel):
    post_image_type = models.CharField(
        max_length=25, choices=POST_IMAGE_TYPE, null=True)
    source = models.CharField(_('URL Source'), max_length=1024, null=True)
    source_thumb = models.CharField(
        _('Thumb Small Link'), max_length=1024, null=True)
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, related_name='product_image_set')

    def __str__(self):
        return mark_safe('<img src="{url}" \
        width="100" height="100" border="1" />'.format(
            url=self.source_thumb
        ))


class ShopeeCategory(TimeStampedModel):
    display_name = models.CharField(max_length=255)
    catid = models.IntegerField()
    no_sub = models.BooleanField(default=False)
    is_default_subcat = models.BooleanField(default=False)

    def __str__(self):
        return self.display_name


class ShopeeRating(TimeStampedModel):
    # review-rate
    shopee_view_count = models.IntegerField(default=0)
    shopee_liked_count = models.IntegerField(default=0)
    shopee_sold_count = models.IntegerField(default=0)
    shopee_review_count = models.IntegerField(default=0)
    shopee_rating_star = models.FloatField(default=0)
    product = models.OneToOneField(
        'Product', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.product.pk) + ' ' + self.product.name


CURRENCY_TYPE = (('VND', _('VND')), )
PRODUCT_SOURCE_TYPE = (('SHOPEE', _('Shopee')),
                       ('INSTAGRAM', _('Instagram')),
                       ('HOMEPAGE', _('Homepage')), )


class Product(TimeStampedModel):
    is_active = models.BooleanField(default=False)
    is_discount = models.BooleanField(default=False)
    product_source = models.CharField(
        choices=PRODUCT_SOURCE_TYPE, max_length=255)
    product_link = models.URLField(
        max_length=1024, blank=True, null=True)
    store = models.ForeignKey('store.Store',
                              on_delete=models.CASCADE)
    name = models.CharField(_('Product Name'),
                            max_length=255, blank=True)
    description = models.TextField()
    shopee_item_id = models.CharField(
        max_length=255, blank=True, null=True)
    # image
    product_thumbnail_image = models.CharField(
        _('Post Thumb Image'), null=True, max_length=1024)

    # price & stock
    original_price = models.IntegerField(default=0)
    discount_price = models.IntegerField(null=True, blank=True)
    discount_rate = models.IntegerField(null=True, blank=True)
    currency = models.CharField(choices=CURRENCY_TYPE, max_length=20)
    is_free_ship = models.BooleanField(default=False)
    stock = models.IntegerField(default=0)

    category = models.ForeignKey(
        ProductCategory, on_delete=models.SET_NULL,
        null=True, blank=True)
    sub_category = models.ForeignKey(
        ProductSubCategory, on_delete=models.SET_NULL,
        null=True, blank=True)
    style = models.ForeignKey(
        ProductStyle, on_delete=models.SET_NULL,
        null=True, blank=True)

    shopee_category = models.ManyToManyField(
        ShopeeCategory, blank=True)
    size = models.ManyToManyField(
        ProductSize, blank=True)
    size_chart = models.CharField(null=True, max_length=1024, blank=True)
    color = models.ManyToManyField(
        ProductColor, blank=True)
    extra_option = models.ManyToManyField(
        ProductExtraOption, blank=True)

    post = models.ForeignKey(
        'store.StorePost', on_delete=models.CASCADE, null=True, blank=True)
    thumb_image_pk = models.IntegerField(
        _('Product Thumb Image'), default=1)

    def __str__(self):
        if self.product_thumbnail_image:
            thumb_image = self.product_thumbnail_image
        elif self.thumb_image_pk == 1:
            thumb_image = self.post.post_thumb_image
        else:
            thumb_image = self.post.post_image_set.all()[self.thumb_image_pk-1]

        return mark_safe('<img src="{url}" \
        width="100" height="100" border="1" />'.format(
            url=thumb_image
        ))
