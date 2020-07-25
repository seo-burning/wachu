from django.db import models
from utils.helper.model.abstract_model import TimeStampedModel, ActiveModel
from django.contrib.auth import get_user_model


class BasePointModel(TimeStampedModel):
    class Meta:
        abstract = True
        ordering = ['created_at']
    # 소유자, 이유, 내용, 수명, 근거(관계)
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    expire = models.BooleanField(default=False)
    expire_date = models.DateTimeField(null=True, blank=True)
    amount = models.IntegerField(blank=True)


class Point(BasePointModel):
    def save(self, *args, **kwargs):
        super(Point, self).save(*args, **kwargs)


ACCUMULATE_TYPE = [('order', 'order'), ('delivery_fee', 'delivery_fee'),
                   ('daily_check', 'daily_check'), ('recommendation', 'recommendation'),
                   ('initial', 'initial'), ('event', 'event'), ('use', 'use')]


class PointLog(BasePointModel, ActiveModel):
    point = models.ForeignKey(Point, null=True, blank=True, on_delete=models.SET_NULL)
    point_title = models.CharField(max_length=200, blank=True)
    point_description = models.CharField(max_length=1000, blank=True)
    accumulate_type = models.CharField(max_length=200, blank=True, choices=ACCUMULATE_TYPE)
