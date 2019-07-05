from django.contrib import admin
from product import models
# Register your models here.


@admin.register(models.ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    fields = ['name']


@admin.register(models.ProductColor)
class ProductColor(admin.ModelAdmin):
    fields = ['name']
