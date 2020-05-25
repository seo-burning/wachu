from django.db import models
from django.utils.translation import ugettext_lazy as _
from core.abstract_models import TimeStampedModel, ActiveModel, OrderingModel
from store.models import StorePost
from product import models as p_models
from store.models import Store
# Create your models here.


class PostGroup(TimeStampedModel):
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


BANNER_TYPE = [('linking', 'LINKING'), ('base', 'BASIC'), ('coupon', 'COUPON')]


class LinkingBanner(TimeStampedModel, ActiveModel, OrderingModel):
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

    class Meta:
        ordering = ('-is_active', 'ordering',)

    def __str__(self):
        return self.title


class PostTagGroup(TimeStampedModel):
    class Meta:
        ordering = ('ordering',)

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
        product_number = 'limit=' + str(self.product_number)
        if (self.category):
            category = self.category.name + '/?'
        if (self.sub_category):
            sub_category = 'sub-category='+self.sub_category.name+'&'
        if (self.color):
            color = 'color='+self.color.name + '&'
        if (self.style):
            style = 'style='+self.style.name + '&'
        if (self.store):
            store = 'store='+str(self.store.pk) + '&'
        return ('http://dabivn.com/api/product/category/' +
                category+sub_category+color+style+store+product_number)


class MainPagePublish(TimeStampedModel):
    is_published = models.BooleanField(default=False)
    date = models.DateField(_('Published Date'))

    def __str__(self):
        return self.date.strftime("%Y-%m-%d")


class BannerPublish(TimeStampedModel):
    is_published = models.BooleanField(default=False)
    date = models.DateField(_('Published Date'))

    def __str__(self):
        return self.date.strftime("%Y-%m-%d")


class MagazinePublish(TimeStampedModel):
    is_published = models.BooleanField(default=False)
    date = models.DateField(_('Published Date'))

    def __str__(self):
        return self.date.strftime("%Y-%m-%d")
