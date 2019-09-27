from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ProductRecommendKeyword(TimeStampedModel):
    class Meta:
        ordering = ('ordering',)

    is_published = models.BooleanField(
        _("is published"), default=False)
    ordering = models.IntegerField(_("Ordering"), null=True)
    keyword = models.CharField(_("Keyword"), max_length=255)

    def __str__(self):
        return self.keyword


class StoreRecommendKeyword(TimeStampedModel):
    class Meta:
        ordering = ('ordering',)

    is_published = models.BooleanField(
        _("is published"), default=False)
    ordering = models.IntegerField(_("Ordering Keyword"), null=True)
    keyword = models.CharField(_("Keyword"), max_length=255)

    def __str__(self):
        return self.keyword
