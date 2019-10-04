from django.db import models
from django.utils.translation import ugettext_lazy as _
from core.models import TimeStampedModel
from store.models import StorePost
from django.utils.safestring import mark_safe


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
    published_page = models.ForeignKey(
        'MainPagePublish', on_delete=models.SET_NULL, null=True, blank=True,)
    published_banner = models.ForeignKey(
        'BannerPublish', on_delete=models.SET_NULL, null=True, blank=True,)
    published_magazine = models.ForeignKey(
        'MagazinePublish', on_delete=models.SET_NULL, null=True, blank=True,)

    def __str__(self):
        return mark_safe('<img src="{url}" \
        width="300" height="300" border="1" />'.format(
            url=self.list_thumb_picture
        ))


class LinkingBanner(TimeStampedModel):
    ordering = models.IntegerField(default=999, null=True)
    title = models.CharField(_('Post Group Title'), max_length=50)
    list_thumb_picture = models.ImageField(
        blank=True, upload_to='post-group-list-thumb/%Y/%m')
    cover_picture = models.ImageField(
        blank=True, upload_to='post-group-cover/%Y/%m')
    link_url = models.URLField(null=True, blank=True, max_length=500)
    published_banner = models.ForeignKey(
        'BannerPublish', on_delete=models.SET_NULL, null=True, blank=True,)

    def __str__(self):
        return mark_safe('<img src="{url}" \
        width="300" height="300" border="1" />'.format(
            url=self.list_thumb_picture
        ))


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
