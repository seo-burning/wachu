from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ActiveModel(models.Model):
    class Meta:
        abstract = True
    is_active = models.BooleanField(default=False)


class PublicModel(models.Model):
    class Meta:
        abstract = True
    is_public = models.BooleanField(default=False)


class OrderingModel(models.Model):
    class Meta:
        abstract = True
    ordering = models.IntegerField(default=999)


class DispalyNameModel(models.Model):
    class Meta:
        abstract = True
    name = models.CharField(max_length=255)
    display_name = models.CharField(default='Need to tranlate', max_length=255)

# https://stackoverflow.com/questions/28832731/django-view-counter


class ViewModel(models.Model):
    class Meta:
        abstract = True
    view = models.PositiveIntegerField(default=0)
