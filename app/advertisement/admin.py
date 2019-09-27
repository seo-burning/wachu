from django.contrib import admin

# Register your models here.
from . import models


@admin.register(models.ProductRecommendKeyword)
class ProductRecommendKeywordAdmin(admin.ModelAdmin):
    fields = ['is_published', 'ordering', 'keyword']
    list_display = ['keyword', 'is_published', 'ordering']
    list_filter = ['is_published', ]


@admin.register(models.StoreRecommendKeyword)
class StoreRecommendKeywordAdmin(admin.ModelAdmin):
    fields = ['is_published', 'ordering', 'keyword']
    list_display = ['keyword', 'is_published', 'ordering']
    list_filter = ['is_published', ]
