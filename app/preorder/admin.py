from django.contrib import admin
from .models import PreorderCampaign

# Register your models here.


@admin.register(PreorderCampaign)
class PreorderCampaign(admin.ModelAdmin):
    pass
