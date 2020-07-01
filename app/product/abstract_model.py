from django.db import models


class SoldModel(models.Model):
    class Meta:
        abstract = True
    sold = models.PositiveIntegerField(default=0)
