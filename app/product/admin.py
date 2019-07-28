from django.contrib import admin
from product import models
# Register your models here.


@admin.register(models.ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    fields = ['name']


@admin.register(models.ProductColor)
class ProductColor(admin.ModelAdmin):
    fields = ['name']


@admin.register(models.ProductSize)
class ProductSize(admin.ModelAdmin):
    fields = ['name']


@admin.register(models.Product)
class Product(admin.ModelAdmin):
    fields = ['name', 'category', 'color', 'size', 'store']
    raw_id_fields = ['store']
