from django.contrib import admin
from .models import PreorderCampaign
from product.models import Product
# Register your models here.


class ProductInline(admin.StackedInline):
    model = Product
    fields = ['id']
    extra = 0


@admin.register(PreorderCampaign)
class PreorderCampaign(admin.ModelAdmin):
    list_display = ['display_name']
    inlines = [ProductInline, ]
