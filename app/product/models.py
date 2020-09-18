from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from utils.helper.model.abstract_model import TimeStampedModel, ActiveModel, OrderingModel, DispalyNameModel, ViewModel
from .abstract_model import SoldModel
from preorder.models import PreorderCampaign
from django.db.models import Q
from django.db.models.constraints import UniqueConstraint


class ProductCategory(TimeStampedModel, DispalyNameModel, ActiveModel, OrderingModel):

    class Meta:
        ordering = ['ordering']
        verbose_name = u'제품 상위 카테고리 / Product Category'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.display_name


class ProductSubCategory(TimeStampedModel, DispalyNameModel, ActiveModel, OrderingModel):
    class Meta:
        ordering = ['category', 'ordering']
        verbose_name = u'제품 하위 카테고리 / Product SubCategory'
        verbose_name_plural = verbose_name
    category = models.ForeignKey(
        ProductCategory, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.display_name


class ProductSize(TimeStampedModel, DispalyNameModel, OrderingModel):
    class Meta:
        ordering = ['ordering', 'display_name']
        verbose_name = u'제품 사이즈 / Product Size'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.display_name


class ProductPattern(TimeStampedModel, DispalyNameModel, OrderingModel):
    class Meta:
        ordering = ['ordering', 'display_name']
        verbose_name = u'제품 패턴 / Product Pattern'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.display_name


class ProductColor(TimeStampedModel, DispalyNameModel, OrderingModel):
    class Meta:
        ordering = ['ordering', 'display_name']
        verbose_name = u'제품 색상 / Product Color'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.display_name


class ProductStyle(TimeStampedModel, DispalyNameModel):
    class Meta:
        verbose_name = u'제품 스타일 / Product Style'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class ProductExtraOption(TimeStampedModel, DispalyNameModel):
    class Meta:
        verbose_name = u'제품 기타 옵션 / Product Extra Option'
        verbose_name_plural = verbose_name
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class SourceExtraOption(TimeStampedModel):
    class Meta:
        verbose_name = u'소스 - 기타 옵션 / Product Source Extra Option'
        verbose_name_plural = verbose_name
    variation_group = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255)
    source_thumb = models.CharField(max_length=1024, null=True)
    source = models.CharField(max_length=1024, null=True)

    def __str__(self):
        return self.name


POST_IMAGE_TYPE = (('P', _('Picture')), ('V', _('Video')))


class ProductImage(TimeStampedModel):
    post_image_type = models.CharField(
        max_length=25, choices=POST_IMAGE_TYPE, null=True, default='P')
    source = models.CharField(_('URL Source'), max_length=1024, null=True)
    source_thumb = models.CharField(
        _('Thumb Small Link'), max_length=1024, null=True)
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, related_name='product_image_set')

    def __str__(self):
        return mark_safe('<img src="{url}" \
        width="700" height="700" border="1" />'.format(
            url=self.source_thumb
        ))


class ShopeeCategory(TimeStampedModel):
    display_name = models.CharField(max_length=255)
    catid = models.IntegerField()
    no_sub = models.BooleanField(default=False)
    is_default_subcat = models.BooleanField(default=False)
    category = models.ForeignKey(
        ProductCategory, on_delete=models.SET_NULL,
        null=True, blank=True)
    sub_category = models.ForeignKey(
        ProductSubCategory, on_delete=models.SET_NULL,
        null=True, blank=True)
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return self.display_name


class ShopeeColor(TimeStampedModel):
    display_name = models.CharField(max_length=255)
    color = models.ForeignKey(
        ProductColor, on_delete=models.SET_NULL,
        null=True, blank=True)
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return self.display_name


class ShopeeSize(TimeStampedModel):
    display_name = models.CharField(max_length=255)
    size = models.ForeignKey(
        ProductSize, on_delete=models.SET_NULL,
        null=True, blank=True)
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return self.display_name


class ShopeeRating(TimeStampedModel):
    # review-rate
    shopee_view_count = models.IntegerField(default=0)
    shopee_liked_count = models.IntegerField(default=0)
    shopee_sold_count = models.IntegerField(default=0)
    shopee_review_count = models.IntegerField(default=0)
    shopee_rating_star = models.FloatField(default=0)
    shopee_1_star_count = models.IntegerField(default=0)
    shopee_2_star_count = models.IntegerField(default=0)
    shopee_3_star_count = models.IntegerField(default=0)
    shopee_4_star_count = models.IntegerField(default=0)
    shopee_5_star_count = models.IntegerField(default=0)

    product = models.OneToOneField(
        'Product', on_delete=models.CASCADE, null=True, blank=True, related_name='shopee_rating')

    def __str__(self):
        return str(self.product.pk) + ' ' + self.product.name


class ProductBackEndRate(TimeStampedModel):
    product_backend_rating = models.DecimalField(
        max_digits=4, decimal_places=1, default=0)
    review_count = models.IntegerField(null=True, blank=True)
    review_rate = models.FloatField(null=True, blank=True)
    shopee_review_count = models.IntegerField(null=True, blank=True)
    shopee_review_rate = models.FloatField(null=True, blank=True)
    shopee_view_count = models.IntegerField(null=True, blank=True)
    shopee_liked_count = models.IntegerField(null=True, blank=True)
    shopee_sold_count = models.IntegerField(null=True, blank=True)
    post_like = models.IntegerField(null=True, blank=True)
    post_comment = models.IntegerField(null=True, blank=True)
    app_click_count = models.IntegerField(null=True, blank=True)
    app_outlink_count = models.IntegerField(null=True, blank=True)
    user_favorite_count = models.IntegerField(null=True, blank=True)
    product_infomation_quality = models.IntegerField(null=True, blank=True)
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, null=True, blank=True, related_name='product_backend_rating_set')

    def __str__(self):
        return str(self.product_backend_rating) + ' ' + self.product.name


CURRENCY_TYPE = (('VND', _('VND')), )
PRODUCT_SOURCE_TYPE = (('SHOPEE', _('Shopee')),
                       ('INSTAGRAM', _('Instagram')),
                       ('HOMEPAGE', _('Homepage')),
                       ('DOSIIN', _('Dosi-in')))

PRODUCT_IMAGE_TYPE = (('SP', _('Single Picture')),
                      ('MP', _('Multiple Picture')), ('V', _('Video')))
PRODUCT_VALIDATION_TYPE = (('R', _('확인 필요')),
                           ('V', _('확인 완료')),
                           ('N', _('비정상 상품')),
                           ('D', _('삭제 상품')))


class PriceModel(models.Model):
    class Meta:
        abstract = True
    original_price = models.IntegerField(default=0)
    discount_price = models.IntegerField(null=True, blank=True)
    discount_rate = models.IntegerField(null=True, blank=True)
    currency = models.CharField(choices=CURRENCY_TYPE, max_length=20, default='VND')
    is_free_ship = models.BooleanField(default=False)
    shipping_price = models.IntegerField(default=None, null=True, blank=True)


class Product(TimeStampedModel, PriceModel, ActiveModel, ViewModel, SoldModel):
    class Meta:
        verbose_name = u'제품 / Product'
        verbose_name_plural = verbose_name
        ordering = ['-created_at', 'current_product_backend_rating', ]

    stock_available = models.BooleanField(default=False)
    validation = models.CharField(
        choices=PRODUCT_VALIDATION_TYPE, max_length=255, default='R')
    is_discount = models.BooleanField(default=False)
    is_preorder = models.BooleanField(default=False)
    preorder_campaign = models.ForeignKey(
        PreorderCampaign, on_delete=models.SET_NULL,
        null=True, blank=True)

    current_review_rating = models.DecimalField(_('Review'),
                                                max_digits=2, decimal_places=1, default=0)
    current_product_backend_rating = models.DecimalField(_('Point'),
                                                         max_digits=4, decimal_places=1, default=0)
    product_source = models.CharField(
        choices=PRODUCT_SOURCE_TYPE, max_length=255)
    product_link = models.URLField(
        max_length=1024, blank=True, null=True, unique=True)
    store = models.ForeignKey('store.Store',
                              on_delete=models.CASCADE)
    name = models.CharField(_('Product Name'),
                            max_length=255, blank=True)
    description = models.TextField(null=True)
    shopee_item_id = models.CharField(
        max_length=255, blank=True, null=True)
    # image
    product_image_type = models.CharField(
        choices=PRODUCT_IMAGE_TYPE, max_length=255, default='MP')
    product_thumbnail_image = models.CharField(null=True, max_length=1024, default="https://dabivn.com")
    video_source = models.CharField(null=True, max_length=1024)

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
    shopee_color = models.ManyToManyField(
        ShopeeColor, blank=True)
    shopee_size = models.ManyToManyField(
        ShopeeSize, blank=True)
    source_extra_option = models.ManyToManyField(
        SourceExtraOption, blank=True)
    size = models.ManyToManyField(
        ProductSize, blank=True)

    size_chart_url = models.URLField(null=True, max_length=1024, blank=True)
    size_chart = models.ImageField(null=True,
                                   blank=True, upload_to='size-chart/%Y/%m')
    color = models.ManyToManyField(
        ProductColor, blank=True, related_name='product_set')
    extra_option = models.ManyToManyField(
        ProductExtraOption, blank=True)
    pattern = models.ManyToManyField(
        ProductPattern, blank=True)

    post = models.ForeignKey(
        'store.StorePost', on_delete=models.CASCADE, null=True, blank=True)
    thumb_image_pk = models.IntegerField(
        _('Product Thumb Image'), default=1)

    def __str__(self):
        if self.product_thumbnail_image:
            thumb_image = self.product_thumbnail_image
        else:
            thumb_image = "http://dabivn.comm"

        return mark_safe('<img src="{url}" \
        width="250" height="250" border="1" />'.format(
            url=thumb_image
        ))


class ProductOption(PriceModel, TimeStampedModel):
    class Meta:
        verbose_name = u'제품 옵션 / Product Option'
        verbose_name_plural = verbose_name
        ordering = ['-created_at', 'product']
        # https://stackoverflow.com/questions/33307892/django-unique-together-with-nullable-foreignkey/33308014
        constraints = [
            UniqueConstraint(fields=['product', 'size', 'color', 'extra_option'],
                             name='unique_with_size_color'),
            UniqueConstraint(fields=['product', 'size', 'extra_option'],
                             condition=Q(color=None),
                             name='unique_without_color'),
            UniqueConstraint(fields=['product', 'color', 'extra_option'],
                             condition=Q(size=None),
                             name='unique_without_size'),
            UniqueConstraint(fields=['product', 'color', 'size'],
                             condition=Q(extra_option=None),
                             name='unique_without_extra'),
        ]

    shopee_item_id = models.CharField(
        max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    name = models.CharField(max_length=255, blank=True)
    stock = models.IntegerField(default=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_options')
    size = models.ForeignKey(ProductSize, on_delete=models.SET_NULL,
                             null=True, blank=True)
    color = models.ForeignKey(ProductColor, on_delete=models.SET_NULL,
                              null=True, blank=True)
    extra_option = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        option_string = 'product : ' + str(self.product.pk)
        if self.size:
            option_string = option_string + ' size : ' + self.size.name
        if self.color:
            option_string = option_string + ' color : ' + self.color.name
        if self.extra_option:
            option_string = option_string + ' extra_option : ' + self.extra_option
        return "#" + str(self.pk) + ' ' + self.name + '\n' + option_string
