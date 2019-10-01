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
    fields = [
        'is_active',
        'category',
        'sub_category',
        'style',
        'color',
        'store',
        'post']
    raw_id_fields = ['store', 'post']
    list_display = ['__str__',
                    'is_active',
                    'store',
                    'category',
                    'sub_category',
                    'style',
                    ]
    search_fields = ['store__insta_id']
    list_filter = [
        'is_active',
        'category',
        'sub_category',
        'style',
    ]
    actions = ['make_activate', 'make_deactivate',
               'categorize_bag', 'categorize_jewelry', 'categorize_shoes']

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

    def categorize_bag(self, request, queryset):
        category_bag = models.ProductCategory.objects.get(name='bag')
        updated_count = queryset.update(category=category_bag)
        self.message_user(
            request, '{}건의 상품을 Bag으로 분류'.format(updated_count))
    categorize_bag.short_description = '상품을 Bag으로 분류'

    def categorize_jewelry(self, request, queryset):
        category_jewelry = models.ProductCategory.objects.get(name='jewelry')
        updated_count = queryset.update(category=category_jewelry)
        self.message_user(
            request, '{}건의 상품을 jewelry으로 분류'.format(updated_count))
    categorize_jewelry.short_description = '상품을 jewelry으로 분류'

    def categorize_shoes(self, request, queryset):
        category_shoes = models.ProductCategory.objects.get(name='shoes')
        updated_count = queryset.update(category=category_shoes)
        self.message_user(
            request, '{}건의 상품을 shoes으로 분류'.format(updated_count))
    categorize_shoes.short_description = '상품을 shoes으로 분류'
