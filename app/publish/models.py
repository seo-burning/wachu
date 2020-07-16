from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.db.models.constraints import UniqueConstraint
from django.db.models import Q

from core.abstract_models import TimeStampedModel, ActiveModel, OrderingModel
from store.models import StorePost
from product import models as p_models
from store.models import Store
# Create your models here.
BANNER_TYPE = [('linking', 'LINKING'), ('base', 'BASIC'), ('coupon', 'COUPON')]


class LinkingBanner(TimeStampedModel, ActiveModel, OrderingModel):
    class Meta:
        ordering = ('-is_active', 'ordering',)
        verbose_name = u'배너 / Banner'
        verbose_name_plural = verbose_name

    title = models.CharField(_('Post Group Title'), max_length=50)
    list_thumb_picture = models.ImageField(
        blank=True, upload_to='post-group-list-thumb/%Y/%m')
    cover_picture_1 = models.ImageField(
        blank=True, upload_to='post-group-cover/%Y/%m')
    cover_picture_2 = models.ImageField(
        blank=True, upload_to='post-group-cover/%Y/%m')
    cover_picture_3 = models.ImageField(
        blank=True, upload_to='post-group-cover/%Y/%m')
    cover_picture_4 = models.ImageField(
        blank=True, upload_to='post-group-cover/%Y/%m')
    link_url = models.URLField(null=True, blank=True, max_length=500)
    coupon_code = models.CharField(null=True, blank=True, max_length=20)
    published_banner = models.ForeignKey(
        'BannerPublish', on_delete=models.SET_NULL, null=True, blank=True,)
    banner_type = models.CharField(default='base', max_length=20, choices=BANNER_TYPE)
    primary_color = models.CharField(max_length=20, blank=True)
    secondary_color = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.title


class PostGroup(TimeStampedModel):
    class Meta:
        ordering = ('ordering',)
        verbose_name = u'상품 그룹 / Product Group'
        verbose_name_plural = verbose_name

    ordering = models.IntegerField(default=999, null=True)
    title = models.CharField(_('Post Group Title'), max_length=50)
    cover_picture = models.ImageField(
        blank=True, upload_to='post-group-cover/%Y/%m')
    list_thumb_picture = models.ImageField(
        blank=True, upload_to='post-group-list-thumb/%Y/%m')
    post_list = models.ManyToManyField(StorePost, blank=True,
                                       symmetrical=False,
                                       related_name="post_set")
    published_banner = models.ForeignKey(
        'BannerPublish', on_delete=models.SET_NULL, null=True, blank=True,)
    published_magazine = models.ForeignKey(
        'MagazinePublish', on_delete=models.SET_NULL, null=True, blank=True,)

    def __str__(self):
        return self.title


class ProductTagGroup(TimeStampedModel, ActiveModel):

    class Meta:
        ordering = ('ordering',)
        verbose_name = u'상품 그룹 태그 / Product Group by Tag'
        verbose_name_plural = verbose_name
        constraints = [
            UniqueConstraint(fields=['category', 'sub_category',
                                     'color', 'style', 'pattern', 'store'],
                             name='pick_unique_with_everything'),
            UniqueConstraint(fields=['category', 'sub_category',
                                     'color', 'style', 'pattern', 'store'],
                             condition=Q(category=None),
                             name='pick_unique_with_everything_with_category_none'),
            UniqueConstraint(fields=['category', 'sub_category',
                                     'color', 'style', 'pattern', 'store'],
                             condition=Q(sub_category=None),
                             name='pick_unique_with_everything_with_sub_category_none'),
            UniqueConstraint(fields=['category', 'sub_category',
                                     'color', 'style', 'pattern', 'store'],
                             condition=Q(color=None),
                             name='pick_unique_with_everything_with_primary_style_none'),
            UniqueConstraint(fields=['category', 'sub_category',
                                     'color', 'style', 'pattern', 'store'],
                             condition=Q(style=None),
                             name='pick_unique_with_everything_with_style_none'),
            UniqueConstraint(fields=['category', 'sub_category',
                                     'color', 'style', 'pattern', 'store'],
                             condition=Q(pattern=None),
                             name='pick_unique_with_everything_with_pattern_none'),
            UniqueConstraint(fields=['category', 'sub_category',
                                     'color', 'style', 'pattern', 'store'],
                             condition=Q(store=None),
                             name='pick_unique_with_everything_with_store_none'),
        ]
    ordering = models.IntegerField(default=999, null=True)
    category = models.ForeignKey(
        p_models.ProductCategory, on_delete=models.SET_NULL,
        null=True, blank=True)
    sub_category = models.ForeignKey(
        p_models.ProductSubCategory, on_delete=models.SET_NULL,
        null=True, blank=True)
    color = models.ForeignKey(
        p_models.ProductColor, on_delete=models.SET_NULL,
        null=True, blank=True)
    style = models.ForeignKey(
        p_models.ProductStyle, on_delete=models.SET_NULL,
        null=True, blank=True)
    pattern = models.ForeignKey(
        p_models.ProductPattern, on_delete=models.SET_NULL,
        null=True, blank=True)
    store = models.ForeignKey(
        Store, on_delete=models.SET_NULL, null=True, blank=True)
    product_number = models.IntegerField(default=10)

    published_banner = models.ForeignKey(
        'MainPagePublish', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        category = 'all/?'
        sub_category = ''
        color = ''
        style = ''
        store = ''
        pattern = ''
        product_number = 'limit=' + str(self.product_number)
        if (self.category):
            category = self.category.name + '/?'
        if (self.sub_category):
            sub_category = 'sub-category='+self.sub_category.name+'&'
        if (self.color):
            color = 'color='+self.color.name + '&'
        if (self.style):
            style = 'style='+self.style.name + '&'
        if (self.pattern):
            pattern = 'pattern='+self.pattern.name + '&'
        if (self.store):
            store = 'store='+str(self.store.pk) + '&'
        return ('http://dabivn.com/api/product/category/' +
                category+sub_category+color+style+pattern+store+product_number)

    def get_related_queryset(self):
        queryset = p_models.Product.objects.filter(is_active=True)
        if (self.category):
            queryset = queryset.filter(category=self.category)
        sub_category = self.sub_category
        if (sub_category):
            queryset = queryset.filter(sub_category=sub_category)
        color = self.color
        if (color):
            queryset = queryset.filter(color=color)
        style = self.style
        if (style):
            queryset = queryset.filter(style=style)
        pattern = self.pattern
        if (pattern):
            queryset = queryset.filter(pattern=pattern)
        store = self.store
        if (store):
            queryset = queryset.filter(store=store)
        return queryset

    def related_product_num(self):
        queryset = self.get_related_queryset()
        return queryset.count()

    def preview(self):
        image_string = ''
        queryset = self.get_related_queryset()
        for obj in queryset.all()[:10]:
            image_string += '<a href="https://dabivn.com/admin/product/product/{pk}">{image}</a>'.format(
                pk=obj.pk, image=str(obj))
        return mark_safe('</td><tr/><tr class="row2"><td colspan=13>'+image_string+'</td><tr/>')


class MainPagePublish(TimeStampedModel):
    class Meta:
        verbose_name = u'홈 화면 발행 / Home Pulish'
        verbose_name_plural = verbose_name
    is_published = models.BooleanField(default=False)
    date = models.DateField(_('Published Date'))

    def __str__(self):
        return self.date.strftime("%Y-%m-%d")


class BannerPublish(TimeStampedModel):
    class Meta:
        verbose_name = u'배너 발행 / Banner Publish'
        verbose_name_plural = verbose_name

    is_published = models.BooleanField(default=False)
    date = models.DateField(_('Published Date'))

    def __str__(self):
        return self.date.strftime("%Y-%m-%d")


class MagazinePublish(TimeStampedModel):
    is_published = models.BooleanField(default=False)
    date = models.DateField(_('Published Date'))

    def __str__(self):
        return self.date.strftime("%Y-%m-%d")
