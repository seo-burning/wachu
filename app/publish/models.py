from django.db import models
from django.utils.translation import ugettext_lazy as _
from core.models import TimeStampedModel
from store.models import StorePost


# Create your models here.
class PostGroup(TimeStampedModel):
    ordering = models.IntegerField(default=999, null=True)
    title = models.CharField(_('Post Group Title'), max_length=50)
    post_list = models.ManyToManyField(StorePost, blank=True,
                                       symmetrical=False,
                                       related_name="post_set")
    published_page = models.ForeignKey(
        'MainPagePublish', on_delete=models.SET_NULL, null=True, blank=True,)

    def __str__(self):
        return self.title


class MainPagePublish(TimeStampedModel):
    is_published = models.BooleanField(default=False)
    date = models.DateField(_('Published Date'))

    def __str__(self):
        return self.date.strftime("%Y-%m-%d")
