from django.db import models
from django.utils.translation import ugettext_lazy as _


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ProductCategory(TimeStampedModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class ProductColor(TimeStampedModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class SlidingBannerSection(TimeStampedModel):
    is_published = models.BooleanField(default=False)
    title_head = models.CharField(_('Section title head'), max_length=30)
    title_colored_keyword = models.CharField(
        _('Colored Keyword'), max_length=30)
    title_foot = models.CharField(_('Section title foot'), max_length=30)
    date = models.DateField(_('Section Published Date'), max_length=30)

    def __str__(self):
        return "@{} - {} {} {}".format(self.date,
                                       self.title_head,
                                       self.title_colored_keyword,
                                       self.title_foot)


class MainSection(TimeStampedModel):
    is_published = models.BooleanField(default=False)
    date = models.DateField(_('Section Published Date'), max_length=30)

    def __str__(self):
        return "{}".format(self.date)
