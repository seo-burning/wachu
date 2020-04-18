from django.contrib import admin
from product import models
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.db.models.functions import TruncDay
import json

# Register your models here.


@admin.register(models.ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    fields = ['name']
    list_display = ['name', 'product_num']

    def product_num(self, obj):
        product_num = obj.product_set.all().filter(category=obj).count()
        return format_html('<a href="http://dabivn.com/'
                           'admin/product/product/'
                           '?category__id__exact=%s">%s</a>'
                           % (obj.pk, product_num)
                           )


@admin.register(models.ProductSubCategory)
class ProductSubCategoryAdmin(admin.ModelAdmin):
    fields = ['name']
    list_display = ['name', 'product_num']

    def product_num(self, obj):
        product_num = obj.product_set.all().filter(sub_category=obj).count()
        return format_html('<a href="http://dabivn.com/'
                           'admin/product/product/'
                           '?sub_category__id__exact=%s">%s</a>'
                           % (obj.pk, product_num)
                           )


@admin.register(models.ProductSize)
class ProductSizeAdmin(admin.ModelAdmin):
    fields = ['name', ]
    list_display = ['name', 'product_num', 'created_at']

    def product_num(self, obj):
        product_num = obj.product_set.all().filter(size=obj).count()
        return product_num


@admin.register(models.ProductColor)
class ProductColorAdmin(admin.ModelAdmin):
    fields = ['name', 'display_name']
    list_display = ['name', 'product_num']

    def product_num(self, obj):
        product_num = obj.product_set.all().filter(color=obj).count()
        return product_num


@admin.register(models.ProductStyle)
class ProductStyleAdmin(admin.ModelAdmin):
    fields = ['name']
    list_display = ['name', 'product_num']

    def product_num(self, obj):
        product_num = obj.product_set.all().filter(style=obj).count()
        return format_html('<a href="http://dabivn.com/'
                           'admin/product/product/?style__id__exact=%s">%s</a>'
                           % (obj.pk, product_num)
                           )


@admin.register(models.ShopeeRating)
class ShopeeRatingAdmin(admin.ModelAdmin):
    fields = ['__all__', ]


@admin.register(models.ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['__str__', ]


@admin.register(models.ProductTag)
class ProductTagAdmin(admin.ModelAdmin):
    fields = ['name']


class ProductImageInline(admin.StackedInline):
    model = models.ProductImage
    fields = ['post_image_type', ]
    readonly_fields = ['post_image_type', ]
    extra = 0
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)

    def post_image_shot(self, obj):
        return mark_safe('<img src="{url}" \
            width="300" height="300" border="1" />'.format(
            url=obj.source_thumb
        ))


class ShopeeRatingInline(admin.StackedInline):
    model = models.ShopeeRating
    extra = 0


@admin.register(models.Product)
class Product(admin.ModelAdmin):
    inlines = [ShopeeRatingInline, ProductImageInline, ]
    raw_id_fields = ['store', 'post']
    list_display = [
        'is_active',
        'product_source',
        '__str__',
        'store',
        'sub_category',
        'original_price',
        'discount_price',
        'color_num',
        'size_num'
    ]
    list_display_links = ['is_active', '__str__', ]
    search_fields = ['store__insta_id']
    list_filter = [
        'is_active',
        'sub_category',
        'product_source',
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

    def changelist_view(self, request, extra_context=None):
        # Aggregate new subscribers per day
        # https://findwork.dev/blog/integrating-chartjs-django-admin/

        chart_data = (
            models.Product.objects.annotate(date=TruncDay("created_at"))
            .values("date")
            .annotate(y=Count("id"))
            .order_by("-date")
        )

        # Serialize and attach the chart data to the template context
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data": as_json}

        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)

    def color_num(self, obj):
        color_num = obj.color.count()
        return color_num

    def size_num(self, obj):
        size_num = obj.size.count()
        return size_num
