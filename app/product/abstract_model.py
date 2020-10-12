from django.db import models
from django.conf import settings


class SoldModel(models.Model):
    class Meta:
        abstract = True
    sold = models.PositiveIntegerField(default=0)


class InpectionModel(models.Model):
    class Meta:
        abstract = True
    inspector = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  on_delete=models.SET_NULL, null=True)
