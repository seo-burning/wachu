from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import TimeStampedModel
from store.models import Store


class ChuPickSet(TimeStampedModel):
    is_published = models.BooleanField(default=False)
    date = models.DateField(_('Section Published Date'), max_length=30)

    def __str__(self):
        return "{}".format(self.date)


class ChuPickRating(TimeStampedModel):
    is_published = models.BooleanField(default=False)
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE,
        related_name='chu_pick_rating_set', default=None)
    pick_image = models.ImageField(blank=True, upload_to='pick/%Y/%m')
    pick_set = models.ForeignKey(
        ChuPickSet, on_delete=models.SET_NULL,
        related_name='chu_pick_rating_set', default=None, null=True)

    def __str__(self):
        return "{} - {} - ".format(self.store, self.pk)


class ChuPickAB(TimeStampedModel):
    is_published = models.BooleanField(default=False)
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE,
        related_name='chu_pick_AB_set', default=None)
    pick_image_a = models.ImageField(blank=True, upload_to='pick/%Y/%m')
    pick_image_b = models.ImageField(blank=True, upload_to='pick/%Y/%m')
    pick_set = models.ForeignKey(
        ChuPickSet, on_delete=models.SET_NULL,
        related_name='chu_pick_AB_set', default=None, null=True)

    def __str__(self):
        return "{} - {} - ".format(self.store, self.pk)
