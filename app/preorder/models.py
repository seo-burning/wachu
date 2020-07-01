from django.db import models
from utils.helper.model.abstract_model import TimeStampedModel, ActiveModel, OrderingModel, DispalyNameModel, ViewModel
# Create your models here.


class PreorderCampaign(TimeStampedModel, ActiveModel, OrderingModel, ViewModel, DispalyNameModel):
    start_at = models.DateTimeField(auto_now=False)
    end_at = models.DateTimeField(auto_now=False)
    estimated_delivery_date = models.DateField(auto_now=False)
    cover_picture = models.ImageField(
        blank=True, upload_to='pre-order/%Y/%m')
    list_thumb_picture = models.ImageField(
        blank=True, upload_to='pre-order/%Y/%m')

    def __str__(self):
        return self.display_name
