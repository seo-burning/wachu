from django.contrib import admin
from product import models
# Register your models here.


@admin.register(models.ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    fields = ['is_active', 'name']
    list_filter = ['is_active', ]
    actions = ['make_activate', 'make_deactivate']

    def make_activate(self, request, queryset):
        updated_count = queryset.update(is_active=True)
        self.message_user(
            request, '{}건의 상품을 Activated 상태로 변경'.format(updated_count))
    make_activate.short_description = '지정 상품을 Activate 상태로 변경'

    def make_deactivate(self, request, queryset):
        updated_count = queryset.update(is_active=False)
        self.message_user(
            request, '{}건의 상품을 Deavtivate 상태로 변경'.format(updated_count))
    make_deactivate.short_description = '지정 상품을 Deactivate 상태로 변경'


@admin.register(models.ProductColor)
class ProductColor(admin.ModelAdmin):
    fields = ['name']


@admin.register(models.ProductSize)
class ProductSize(admin.ModelAdmin):
    fields = ['name']


@admin.register(models.ProductTag)
class ProductTag(admin.ModelAdmin):
    fields = ['name']


@admin.register(models.Product)
class Product(admin.ModelAdmin):
    fields = ['name', 'category', 'tag', 'store']
    raw_id_fields = ['store']
