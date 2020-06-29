from django.contrib import admin
from product import models
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.db.models.functions import TruncDay
import json

# Register your models here.


@admin.register(models.ProductPattern)
class ProductPatternAdmin(admin.ModelAdmin):
    list_display = ['name', 'display_name', 'product_active_num', 'product_num']

    def product_active_num(self, obj):
        product_num = obj.product_set.filter(is_active=True).filter(pattern=obj).count()
        return product_num

    def product_num(self, obj):
        product_num = obj.product_set.all().filter(pattern=obj).count()
        return product_num


@admin.register(models.ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    fields = ['name', 'display_name', 'is_active', 'ordering']
    list_display = ['is_active', 'name', 'display_name', 'product_active_num', 'product_num']
    actions = ['make_activate', 'make_deactivate', ]

    def product_num(self, obj):
        product_num = obj.product_set.all().filter(category=obj).count()
        return format_html('<a href="http://dabivn.com/'
                           'admin/product/product/'
                           '?category__id__exact=%s">%s</a>'
                           % (obj.pk, product_num)
                           )

    def product_active_num(self, obj):
        product_num = obj.product_set.filter(is_active=True).filter(category=obj).count()
        return format_html('<a href="http://dabivn.com/'
                           'admin/product/product/'
                           '?category__id__exact=%s">%s</a>'
                           % (obj.pk, product_num)
                           )

    def make_activate(self, request, queryset):
        updated_count = queryset.update(is_active=True)
        self.message_user(
            request, '{} Activated 상태로 변경'.format(updated_count))
    make_activate.short_description = 'Activate 상태로 변경'

    def make_deactivate(self, request, queryset):
        updated_count = queryset.update(is_active=False)
        self.message_user(
            request, '{} Deavtivate 상태로 변경'.format(updated_count))
    make_deactivate.short_description = 'Deactivate 상태로 변경'


@admin.register(models.ProductSubCategory)
class ProductSubCategoryAdmin(admin.ModelAdmin):
    fields = ['name', 'display_name', 'category', 'is_active', 'ordering']
    list_display = ['is_active', 'name', 'display_name', 'product_active_num', 'product_num', 'category']
    actions = ['make_activate', 'make_deactivate', ]

    def product_num(self, obj):
        product_num = obj.product_set.all().filter(sub_category=obj).count()
        return format_html('<a href="http://dabivn.com/'
                           'admin/product/product/'
                           '?sub_category__id__exact=%s">%s</a>'
                           % (obj.pk, product_num)
                           )

    def product_active_num(self, obj):
        product_num = obj.product_set.filter(is_active=True).filter(sub_category=obj).count()
        return format_html('<a href="http://dabivn.com/'
                           'admin/product/product/'
                           '?sub_category__id__exact=%s">%s</a>'
                           % (obj.pk, product_num)
                           )

    def make_activate(self, request, queryset):
        updated_count = queryset.update(is_active=True)
        self.message_user(
            request, '{} Activated 상태로 변경'.format(updated_count))
    make_activate.short_description = 'Activate 상태로 변경'

    def make_deactivate(self, request, queryset):
        updated_count = queryset.update(is_active=False)
        self.message_user(
            request, '{} Deavtivate 상태로 변경'.format(updated_count))
    make_deactivate.short_description = 'Deactivate 상태로 변경'


class ProductSizeThroughInline(admin.TabularInline):
    model = models.Product.size.through
    fields = ['product_thumbnail_image', 'product_link',
              'product_out_link', ]
    readonly_fields = ['product_thumbnail_image',
                       'product_link', 'product_out_link']
    extra = 0

    def product_thumbnail_image(self, instance):
        return mark_safe('<img src="{url}" \
        width="400" height="400" border="1" />'.format(
            url=instance.product.product_thumbnail_image
        ))

    def product_link(self, instance):
        return mark_safe(
            '<a href="http://dabivn.com/admin/product/product/%s"\
                target="_blank">%s</a>'
            % (instance.product.pk, "product page"))

    def product_out_link(self, instance):
        return mark_safe('<a href="%s" target="_blank">%s</a>' % (
            instance.product.product_link, "product_out_link"
        ))


class ProductShopeeCategoryThroughInline(admin.TabularInline):
    model = models.Product.shopee_category.through
    fields = ['product_thumbnail_image', 'product_link',
              'product_out_link', ]
    readonly_fields = ['product_thumbnail_image',
                       'product_link', 'product_out_link']
    extra = 0

    def product_thumbnail_image(self, instance):
        return mark_safe('<img src="{url}" \
        width="400" height="400" border="1" />'.format(
            url=instance.product.product_thumbnail_image
        ))

    def product_link(self, instance):
        return mark_safe(
            '<a href="http://dabivn.com/admin/product/product/%s"\
                target="_blank">%s</a>'
            % (instance.product.pk, "product page"))

    def product_out_link(self, instance):
        return mark_safe('<a href="%s" target="_blank">%s</a>' % (
            instance.product.product_link, "product_out_link"
        ))


class ProductShopeeColorThroughInline(admin.TabularInline):
    model = models.Product.shopee_color.through
    fields = ['product_thumbnail_image', 'product_link',
              'product_out_link', ]
    readonly_fields = ['product_thumbnail_image',
                       'product_link', 'product_out_link']
    extra = 0

    def product_thumbnail_image(self, instance):
        return mark_safe('<img src="{url}" \
        width="400" height="400" border="1" />'.format(
            url=instance.product.product_thumbnail_image
        ))

    def product_link(self, instance):
        return mark_safe(
            '<a href="http://dabivn.com/admin/product/product/%s" target="_blank">%s</a>'
            % (instance.product.pk, "product page"))

    def product_out_link(self, instance):
        return mark_safe('<a href="%s" target="_blank">%s</a>' % (
            instance.product.product_link, "product_out_link"
        ))


class ProductShopeeSizeThroughInline(admin.TabularInline):
    model = models.Product.shopee_size.through
    fields = ['product_thumbnail_image', 'product_link',
              'product_out_link', ]
    readonly_fields = ['product_thumbnail_image',
                       'product_link', 'product_out_link']
    extra = 0

    def product_thumbnail_image(self, instance):
        return mark_safe('<img src="{url}" \
        width="400" height="400" border="1" />'.format(
            url=instance.product.product_thumbnail_image
        ))

    def product_link(self, instance):
        return mark_safe(
            '<a href="http://dabivn.com/admin/product/product/%s" target="_blank">%s</a>'
            % (instance.product.pk, "product page"))

    def product_out_link(self, instance):
        return mark_safe('<a href="%s" target="_blank">%s</a>' % (
            instance.product.product_link, "product_out_link"
        ))


@admin.register(models.ProductBackEndRate)
class ProductBackEndRateAdmin(admin.ModelAdmin):
    list_display = ['product_backend_rating', 'product',
                    'shopee_review_count', 'post_like']


class ProductExtraOptionThroughInline(admin.TabularInline):
    model = models.Product.extra_option.through
    fields = ['product_thumbnail_image', 'product_link',
              'product_out_link', ]
    readonly_fields = ['product_thumbnail_image',
                       'product_link', 'product_out_link']
    extra = 0

    def product_thumbnail_image(self, instance):
        return mark_safe('<img src="{url}" \
        width="400" height="400" border="1" />'.format(
            url=instance.product.product_thumbnail_image
        ))

    def product_link(self, instance):
        return mark_safe(
            '<a href="http://dabivn.com/admin/product/product/%s" target="_blank">%s</a>'
            % (instance.product.pk, "product page"))

    def product_out_link(self, instance):
        return mark_safe('<a href="%s" target="_blank">%s</a>' % (
            instance.product.product_link, "product_out_link"
        ))


@admin.register(models.ProductSize)
class ProductSizeAdmin(admin.ModelAdmin):
    fields = ['display_name', 'name', ]
    list_display = ['name', 'display_name', 'product_num', 'created_at']
    list_filter = ['name']
    # inlines = [ProductSizeThroughInline, ]

    def product_num(self, obj):
        product_num = obj.product_set.all().filter(size=obj).count()
        return product_num


@admin.register(models.ProductColor)
class ProductColorAdmin(admin.ModelAdmin):
    fields = ['display_name', 'name', ]
    list_display = ['name', 'display_name', 'product_num', 'created_at']
    search_fields = ['display_name']
    # list_filter = ['name']

    def product_num(self, obj):
        product_num = obj.product_set.all().filter(color=obj).count()
        return product_num


@admin.register(models.ProductStyle)
class ProductStyleAdmin(admin.ModelAdmin):
    fields = ['name']
    list_display = ['name', 'product_active_num', 'product_num']

    def product_active_num(self, obj):
        product_num = obj.product_set.filter(is_active=True).filter(style=obj).count()
        return product_num

    def product_num(self, obj):
        product_num = obj.product_set.all().filter(style=obj).count()
        return format_html('<a href="http://dabivn.com/'
                           'admin/product/product/?style__id__exact=%s">%s</a>'
                           % (obj.pk, product_num)
                           )


@admin.register(models.ShopeeRating)
class ShopeeRatingAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ShopeeCategory)
class ShopeeCategoryAdmin(admin.ModelAdmin):
    list_display = ['catid', 'is_valid', 'no_sub', 'display_name', 'category', 'sub_category', 'product_num']
    # list_editable = ['category', 'sub_category']
    list_filter = ['category', 'sub_category', 'no_sub', 'is_valid']
    search_fields = ['display_name', ]
    inlines = [ProductShopeeCategoryThroughInline, ]

    def product_num(self, obj):
        product_num = obj.product_set.all().filter(shopee_category=obj).count()
        return product_num


@admin.register(models.ShopeeSize)
class ShopeeSizeAdmin(admin.ModelAdmin):
    list_display = ['is_valid', 'display_name', 'size', 'product_num']
    list_filter = ['is_valid', ]
    search_fields = ['display_name', ]
    inlines = [ProductShopeeSizeThroughInline, ]

    def product_num(self, obj):
        product_num = obj.product_set.all().filter(shopee_size=obj).count()
        return product_num


@admin.register(models.ShopeeColor)
class ShopeeColorAdmin(admin.ModelAdmin):
    list_display = ['is_valid', 'display_name', 'color', 'product_num']
    list_filter = ['is_valid', ]
    search_fields = ['display_name', ]
    inlines = [ProductShopeeColorThroughInline, ]

    def product_num(self, obj):
        product_num = obj.product_set.all().filter(shopee_color=obj).count()
        return product_num


@admin.register(models.ProductExtraOption)
class ProductExtraOptionAdmin(admin.ModelAdmin):
    list_display = ['name', 'variation_group', 'product_num']
    inlines = [ProductExtraOptionThroughInline, ]

    def product_num(self, obj):
        product_num = obj.product_set.all().filter(extra_option=obj).count()
        return product_num


@admin.register(models.ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['__str__', ]
    list_filter = ['post_image_type', ]


@admin.register(models.ProductOption)
class ProductOptionAdmin(admin.ModelAdmin):
    list_display = ['is_active', 'name', 'original_price', 'discount_price', 'stock']


class ProductOptionInline(admin.StackedInline):
    model = models.ProductOption
    fields = ['is_active', 'name', 'original_price',
              'discount_price', 'stock', 'size', 'color']
    extra = 0


class ProductImageInline(admin.StackedInline):
    model = models.ProductImage
    fields = ['post_image_type', 'source', 'source_thumb']
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
    inlines = [ShopeeRatingInline, ProductImageInline, ProductOptionInline]
    raw_id_fields = ['store', 'post']
    list_display = [
        'is_active',
        'is_valid',
        'stock',
        '__str__',
        'created_at',
        'current_product_backend_rating',
        'product_source',
        'current_review_rating',
        'get_product_link',
        'name',
        'store',
        'sub_category',
        'original_price',
        'discount_price',
        'color_num',
        'size_num',
        'product_thumbnail_image'
    ]
    fieldsets = [('Status', {'fields': ['is_active',
                                        'is_valid',
                                        'stock_available',
                                        'view', 'current_product_backend_rating']}),
                 ('Product Source', {'fields': ['store', 'product_source', 'product_link', 'current_review_rating']}),
                 ('Product Info', {'fields': ['name', 'shopee_item_id',
                                              'description', 'product_thumbnail_image']}),
                 ('Price', {'fields': ['is_discount', 'is_free_ship', 'original_price', 'shipping_price',
                                       'discount_price', 'discount_rate', 'currency', 'stock']}),
                 ('Product Category', {'fields': ['category', 'sub_category', 'style', ]}),
                 ('Product Detail', {'fields': ['size', 'size_chart', 'color', 'pattern', 'extra_option']}),
                 ('Shopee Info', {'fields': ['shopee_category', 'shopee_color', 'shopee_size', ]}),
                 ('Post Info', {'fields': ['post', 'thumb_image_pk', ]}),
                 ]
    list_display_links = ['is_active', 'name', ]
    search_fields = ['store__insta_id', 'name']
    list_filter = [
        'is_active',
        'is_valid',
        'stock_available',
        'product_image_type',
        'sub_category',
        'product_source',
    ]
    actions = ['make_activate', 'make_deactivate',
               'categorize_bag', 'categorize_jewelry', 'categorize_shoes',
               'product_type_instagram',
               'product_pattern_print',
               'product_pattern_floral',
               'product_pattern_polka',
               'product_pattern_striped',
               'product_pattern_texture',
               'product_pattern_caro',
               ]

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

    def product_type_instagram(self, request, queryset):
        updated_count = queryset.update(product_source='INSTAGRAM')
        self.message_user(
            request, '{}건의 상품을 INSTAGRAM 분류'.format(updated_count))
    product_type_instagram.short_description = 'product source instagram'

    def product_pattern_print(self, request, queryset):
        print_pattern = models.ProductPattern.objects.get(name='print')
        updated_count = 0
        for obj in queryset.all():
            obj.pattern.add(print_pattern)
            obj.save()
            updated_count = updated_count + 1
        self.message_user(
            request, '{}건의 상품에 PRINT 패턴 추가'.format(updated_count))
    product_pattern_print.short_description = 'print 패턴 추가'

    def product_pattern_floral(self, request, queryset):
        floral_pattern = models.ProductPattern.objects.get(name='floral')
        updated_count = 0
        for obj in queryset.all():
            obj.pattern.add(floral_pattern)
            obj.save()
            updated_count = updated_count + 1
        self.message_user(
            request, '{}건의 상품에 floral 패턴 추가'.format(updated_count))
    product_pattern_floral.short_description = 'floral 패턴 추가'

    def product_pattern_polka(self, request, queryset):
        polka_pattern = models.ProductPattern.objects.get(name='polka')
        updated_count = 0
        for obj in queryset.all():
            obj.pattern.add(polka_pattern)
            obj.save()
            updated_count = updated_count + 1
        self.message_user(
            request, '{}건의 상품에 PRINT 패턴 추가'.format(updated_count))
    product_pattern_polka.short_description = 'polka 패턴 추가'

    def product_pattern_striped(self, request, queryset):
        striped_pattern = models.ProductPattern.objects.get(name='striped')
        updated_count = 0
        for obj in queryset.all():
            obj.pattern.add(striped_pattern)
            obj.save()
            updated_count = updated_count + 1
        self.message_user(
            request, '{}건의 상품에 PRINT 패턴 추가'.format(updated_count))
    product_pattern_striped.short_description = 'striped 패턴 추가'

    def product_pattern_texture(self, request, queryset):
        texture_pattern = models.ProductPattern.objects.get(name='texture')
        updated_count = 0
        for obj in queryset.all():
            obj.pattern.add(texture_pattern)
            obj.save()
            updated_count = updated_count + 1
        self.message_user(
            request, '{}건의 상품에 PRINT 패턴 추가'.format(updated_count))
    product_pattern_texture.short_description = 'texture 패턴 추가'

    def product_pattern_caro(self, request, queryset):
        caro_pattern = models.ProductPattern.objects.get(name='caro')
        updated_count = 0
        for obj in queryset.all():
            obj.pattern.add(caro_pattern)
            obj.save()
            updated_count = updated_count + 1
        self.message_user(
            request, '{}건의 상품에 PRINT 패턴 추가'.format(updated_count))
    product_pattern_caro.short_description = 'caro 패턴 추가'

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

    def get_product_link(self, obj):
        return format_html(
            '<a href="%s" target="_blank">%s</a>' % (
                obj.product_link, 'ProductLink')
        )
    get_product_link.short_description = "Link"
    get_product_link.allow_tags = True
