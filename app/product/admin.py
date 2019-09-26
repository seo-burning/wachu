from django.contrib import admin
from product import models
# Register your models here.


@admin.register(models.ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    fields = ['name']


@admin.register(models.ProductSubCategory)
class ProductSubCategoryAdmin(admin.ModelAdmin):
    fields = ['name', 'category']


@admin.register(models.ProductLength)
class ProductLengthAdmin(admin.ModelAdmin):
    fields = ['name']


@admin.register(models.ProductSleeveLength)
class ProductSleeveLengthAdmin(admin.ModelAdmin):
    fields = ['name']


@admin.register(models.ProductMaterial)
class ProductMaterialAdmin(admin.ModelAdmin):
    fields = ['name']


@admin.register(models.ProductDetail)
class ProductDetailAdmin(admin.ModelAdmin):
    fields = ['name']


@admin.register(models.ProductColor)
class ProductColorAdmin(admin.ModelAdmin):
    fields = ['name']


@admin.register(models.ProductStyle)
class ProductStyleAdmin(admin.ModelAdmin):
    fields = ['name']


@admin.register(models.ProductTag)
class ProductTagAdmin(admin.ModelAdmin):
    fields = ['name']


@admin.register(models.Product)
class Product(admin.ModelAdmin):
    fields = ['is_checked',
              'is_active',
              'name',
              'category',
              'style',
              'sub_category',
              'length',
              'sleeve_length',
              'material',
              'detail',
              'tag',
              'store',
              'color',
              'post']
    raw_id_fields = ['store', 'post']
    list_display = ['__str__',
                    'is_checked',
                    'is_active',
                    'store',
                    'category',
                    'sub_category',
                    'style',
                    'length',
                    'sleeve_length',
                    'material',
                    'detail']
    list_filter = ['is_checked',
                   'is_active',
                   'category',
                   'sub_category',
                   'style',
                   'length',
                   'sleeve_length',
                   'material',
                   'detail']
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
