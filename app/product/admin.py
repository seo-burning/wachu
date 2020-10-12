from django.contrib import admin
from product import models
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.db.models.functions import TruncDay
import json
from pick.models import Pick
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
    list_display = ['is_active', 'ordering', 'name', 'display_name',
                    'product_active_num', 'product_num']
    list_editable = ['ordering', ]
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
    list_display = ['is_active', 'ordering', 'name', 'display_name', 'product_active_num', 'product_num', 'category']
    list_editable = ['ordering', ]
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
        width="400" height="400" border="1" /><p>{category} - {subcategory}</p>'.format(
            url=instance.product.product_thumbnail_image,
            category=instance.product.category,
            subcategory=instance.product.sub_category
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


class SourceExtraOptionThroughInline(admin.TabularInline):
    model = models.Product.source_extra_option.through
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
    list_display = ['name', 'display_name', 'product_num', 'created_at', 'ordering']
    list_editable = ['ordering', ]
    list_filter = ['name']
    # inlines = [ProductSizeThroughInline, ]

    def product_num(self, obj):
        product_num = obj.product_set.all().filter(size=obj).count()
        return product_num


@admin.register(models.ProductColor)
class ProductColorAdmin(admin.ModelAdmin):
    fields = ['display_name', 'name', ]
    list_display = ['name', 'display_name', 'product_num', 'created_at', 'ordering']
    list_editable = ['ordering', ]
    search_fields = ['display_name']
    # list_filter = ['name']

    def product_num(self, obj):
        product_num = obj.product_set.all().filter(color=obj).count()
        return product_num


@admin.register(models.ProductStyle)
class ProductStyleAdmin(admin.ModelAdmin):
    fields = ['name', 'pk']
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
    list_filter = ['category', 'sub_category', 'no_sub', 'is_valid']
    search_fields = ['display_name', ]
    inlines = [ProductShopeeCategoryThroughInline, ]
    actions = ['make_related_product_review_state', ]

    def product_num(self, obj):
        product_num = obj.product_set.all().filter(shopee_category=obj).count()
        return product_num

    def make_related_product_review_state(self, request, queryset):
        for obj in queryset.all():
            for po in obj.product_set.all():
                po.validation = 'R'
                po.is_active = False
                po.save()
            obj.is_valid = False
            obj.category = None
            obj.sub_cateogry = None
            obj.save()


@admin.register(models.ShopeeSize)
class ShopeeSizeAdmin(admin.ModelAdmin):
    list_display = ['is_valid', 'display_name', 'size', 'product_num']
    list_editable = ['size', ]
    list_filter = ['is_valid', ]
    search_fields = ['display_name', ]
    inlines = [ProductShopeeSizeThroughInline, ]

    def product_num(self, obj):
        product_num = obj.product_set.all().filter(shopee_size=obj).count()
        return product_num


@admin.register(models.ShopeeColor)
class ShopeeColorAdmin(admin.ModelAdmin):
    list_display = ['is_valid', 'display_name', 'color', 'product_num']
    list_editable = ['color', ]
    list_filter = ['is_valid', ]
    search_fields = ['display_name', ]
    inlines = [ProductShopeeColorThroughInline, ]

    def product_num(self, obj):
        product_num = obj.product_set.all().filter(shopee_color=obj).count()
        return product_num


@admin.register(models.SourceExtraOption)
class SourceExtraOptionAdmin(admin.ModelAdmin):
    list_display = ['name', 'product_num', 'variation_group']
    inlines = [SourceExtraOptionThroughInline, ]

    def product_num(self, obj):
        product_num = obj.product_set.all().filter(source_extra_option=obj).count()
        return product_num


@admin.register(models.ProductExtraOption)
class ProductExtraOptionAdmin(admin.ModelAdmin):
    list_display = ['name', 'product_num']
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
    list_display = ['is_active', 'name', 'original_price', 'discount_price', 'stock', 'product', 'created_at']


class ProductOptionInline(admin.StackedInline):
    model = models.ProductOption
    fields = ['is_active', 'name', 'original_price',
              'discount_price', 'stock', 'size', 'color', 'extra_option']
    readonly_fields = ['name', ]
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
class ProductAdmin(admin.ModelAdmin):
    inlines = [ShopeeRatingInline, ProductImageInline, ProductOptionInline]
    list_per_page = 25
    raw_id_fields = ['store', 'post', 'shopee_category', ]
    list_display = [
        'product_summary',
        'option_summary',
        'is_active',
        'validation',
        'store',
        'get_product_link'
    ]
    fieldsets = [('Status', {'fields': ['is_active',
                                        'validation',
                                        'stock_available',
                                        'view',
                                        'sold',
                                        'current_product_backend_rating']}),
                 ('Preorder', {'fields': ['is_preorder', 'preorder_campaign']}),
                 ('Product Source', {'fields': ['store', 'product_source', 'product_link', 'current_review_rating']}),
                 ('Product Info', {'fields': ['name', 'shopee_item_id',
                                              'description', 'product_thumbnail_image']}),
                 ('Price', {'fields': ['is_discount', 'is_free_ship', 'original_price', 'shipping_price',
                                       'discount_price', 'discount_rate', 'currency', 'stock']}),
                 ('Product Category', {'fields': ['category', 'sub_category', 'style', ]}),
                 ('Product Detail', {'fields': ['size', 'size_chart', 'size_chart_url',
                                                'color', 'pattern', 'extra_option']}),
                 ('Shopee Info', {'fields': ['shopee_category', 'shopee_color', 'shopee_size', ]}),
                 ('Post Info', {'fields': ['post', 'thumb_image_pk', ]}),
                 ]
    list_display_links = ['product_summary', ]
    search_fields = ['store__insta_id', 'name', 'pk']
    list_select_related = ('category', 'sub_category',
                           'preorder_campaign', 'store', 'style',
                           'post', 'shopee_rating')
    list_prefetch_related = ('size', 'color', 'pick_set')
    list_filter = [
        'is_active',
        'is_discount',
        'validation',
        'stock_available',
        'sub_category',
        'product_source',
        'style'
    ]
    actions = ['make_activate', 'make_deactivate',
               'make_valid_and_active',
               'make_valid', 'make_not_valid', 'make_need_to_review',
               'categorize_bag', 'categorize_jewelry', 'categorize_shoes',
               'product_pattern_print',
               'product_pattern_floral',
               'product_pattern_tiedye',
               'product_pattern_polka',
               'product_pattern_striped',
               'product_pattern_texture',
               'product_pattern_caro',
               'product_style_simple',
               'product_style_lovely',
               'product_style_sexy',
               'product_style_vintage',
               'product_style_street',
               'product_style_feminine',
               'make_name_to_option',
               'product_category_dam_kieu',
               'product_category_ao_somi',
               'product_set_vest',
               'make_it_to_pick_object'
               ]

    def make_it_to_pick_object(self, request, queryset):
        for product_object in queryset.all():
            pick_obj, is_created = Pick.objects.get_or_create(product=product_object)
            if is_created:
                pick_obj.image_outlink = product_object.product_thumbnail_image
                # pick_obj.outlink = product_object.product_link
                pick_obj.product_category.add(product_object.category)
                pick_obj.product_sub_category.add(product_object.sub_category)
                for product_color in product_object.color.all():
                    pick_obj.product_color.add(product_color)
                pick_obj.primary_style = product_object.style
                pick_obj.age = product_object.store.age
                pick_obj.save()
                pass
            self.message_user(
                request,
                mark_safe('<a herf="https://dabivn.com/admin/pick/pick/{pk}">https://dabivn.com/admin/pick/pick/{pk}</a>'.format(pk=pick_obj.pk)))
    make_it_to_pick_object.short_description = '[pick] Make a pick objects from selected products'

    def make_activate(self, request, queryset):
        updated_count = queryset.update(is_active=True)
        self.message_user(
            request, '{}건의 상품을 Activated 상태로 변경'.format(updated_count))
    make_activate.short_description = '[is_active] Make is_active status to Actived'

    def make_deactivate(self, request, queryset):
        updated_count = queryset.update(is_active=False)
        self.message_user(
            request, '{}건의 상품을 Deavtivate 상태로 변경'.format(updated_count))
    make_deactivate.short_description = '[is_active] Make is_active status to Deactived'

    def make_valid_and_active(self, request, queryset):
        updated_count = queryset.update(validation='V', is_active=True)
        self.message_user(
            request, '{}건의 상품을 확인 완료 & Active로 변경'.format(updated_count))
    make_valid_and_active.short_description = '[is_active] 지정 상품을 확인 완료 후 Active'

    def make_valid(self, request, queryset):
        updated_count = queryset.update(validation='V')
        self.message_user(
            request, '{}건의 상품을 확인 완료 상태로 변경'.format(updated_count))
    make_valid.short_description = '[validation] Mark product validation as Validated (확인완료)'

    def make_not_valid(self, request, queryset):
        updated_count = queryset.update(validation='N')
        self.message_user(
            request, '{}건의 상품을 비정상상품 상태로 변경'.format(updated_count))
    make_not_valid.short_description = '[validation] Mark product validation as Unqualified (비정상)'

    def make_need_to_review(self, request, queryset):
        updated_count = queryset.update(validation='V')
        self.message_user(
            request, '{}건의 상품을 리뷰 필요 상태로 변경'.format(updated_count))
    make_need_to_review.short_description = '[validation] Mark product validation as Need to Review (확인필요)'

    def categorize_bag(self, request, queryset):
        category_bag = models.ProductCategory.objects.get(name='bag')
        updated_count = queryset.update(category=category_bag)
        self.message_user(
            request, '{}건의 상품을 Bag으로 분류'.format(updated_count))
    categorize_bag.short_description = '[Category] Categorize product as bag'

    def categorize_jewelry(self, request, queryset):
        category_jewelry = models.ProductCategory.objects.get(name='jewelry')
        updated_count = queryset.update(category=category_jewelry)
        self.message_user(
            request, '{}건의 상품을 jewelry으로 분류'.format(updated_count))
    categorize_jewelry.short_description = '[Category] Categorize product as jewelry'

    def categorize_shoes(self, request, queryset):
        category_shoes = models.ProductCategory.objects.get(name='shoes')
        updated_count = queryset.update(category=category_shoes)
        self.message_user(
            request, '{}건의 상품을 shoes으로 분류'.format(updated_count))
    categorize_shoes.short_description = '[Category] Categorize product as shoes'

    def product_category_dam_kieu(self, request, queryset):
        sub_categroy_dam = models.ProductSubCategory.objects.get(name='dam_kieu')
        updated_count = queryset.update(sub_category=sub_categroy_dam, category=sub_categroy_dam.category)
        self.message_user(
            request, '{}건의 상품 분류'.format(updated_count))
    product_category_dam_kieu.short_description = '[Category] Categorize product as Dam kieu'

    def product_category_ao_somi(self, request, queryset):
        sub_categroy_dam = models.ProductSubCategory.objects.get(name='shirts')
        updated_count = queryset.update(sub_category=sub_categroy_dam, category=sub_categroy_dam.category)
        self.message_user(
            request, '{}건의 상품 분류'.format(updated_count))
    product_category_ao_somi.short_description = '[Category] Categorize product as Ao somi'

    def product_set_vest(self, request, queryset):
        vest_sub_category = models.ProductSubCategory.objects.get(pk=73)
        updated_count = queryset.update(sub_category=vest_sub_category, category=vest_sub_category.category)
        self.message_user(
            request, '{}건의 상품 분류'.format(updated_count))
    product_set_vest.short_description = '[Category] Categorize product as - Set / Vest'

    def product_pattern_print(self, request, queryset):
        print_pattern = models.ProductPattern.objects.get(name='print')
        updated_count = 0
        for obj in queryset.all():
            obj.pattern.add(print_pattern)
            obj.save()
            updated_count = updated_count + 1
        self.message_user(
            request, '{}건의 상품에 PRINT 패턴 추가'.format(updated_count))
    product_pattern_print.short_description = '[Pattern] Add print pattern on product'

    def product_pattern_floral(self, request, queryset):
        floral_pattern = models.ProductPattern.objects.get(name='floral')
        updated_count = 0
        for obj in queryset.all():
            obj.pattern.add(floral_pattern)
            obj.save()
            updated_count = updated_count + 1
        self.message_user(
            request, '{}건의 상품에 floral 패턴 추가'.format(updated_count))
    product_pattern_floral.short_description = '[Pattern] Add floral pattern on product'

    def product_pattern_tiedye(self, request, queryset):
        tiedye_pattern = models.ProductPattern.objects.get(name='tiedye')
        updated_count = 0
        for obj in queryset.all():
            obj.pattern.add(tiedye_pattern)
            obj.save()
            updated_count = updated_count + 1
        self.message_user(
            request, '{}건의 상품에 tiedye 패턴 추가'.format(updated_count))
    product_pattern_tiedye.short_description = '[Pattern] Add tiedye pattern on product'

    def product_pattern_polka(self, request, queryset):
        polka_pattern = models.ProductPattern.objects.get(name='polka')
        updated_count = 0
        for obj in queryset.all():
            obj.pattern.add(polka_pattern)
            obj.save()
            updated_count = updated_count + 1
        self.message_user(
            request, '{}건의 상품에 PRINT 패턴 추가'.format(updated_count))
    product_pattern_polka.short_description = '[Pattern] Add polka pattern on product'

    def product_pattern_striped(self, request, queryset):
        striped_pattern = models.ProductPattern.objects.get(name='striped')
        updated_count = 0
        for obj in queryset.all():
            obj.pattern.add(striped_pattern)
            obj.save()
            updated_count = updated_count + 1
        self.message_user(
            request, '{}건의 상품에 PRINT 패턴 추가'.format(updated_count))
    product_pattern_striped.short_description = '[Pattern] Add striped pattern on product'

    def product_pattern_texture(self, request, queryset):
        texture_pattern = models.ProductPattern.objects.get(name='texture')
        updated_count = 0
        for obj in queryset.all():
            obj.pattern.add(texture_pattern)
            obj.save()
            updated_count = updated_count + 1
        self.message_user(
            request, '{}건의 상품에 PRINT 패턴 추가'.format(updated_count))
    product_pattern_texture.short_description = '[Pattern] Add texture pattern on product'

    def product_pattern_caro(self, request, queryset):
        caro_pattern = models.ProductPattern.objects.get(name='caro')
        updated_count = 0
        for obj in queryset.all():
            obj.pattern.add(caro_pattern)
            obj.save()
            updated_count = updated_count + 1
        self.message_user(
            request, '{}건의 상품에 PRINT 패턴 추가'.format(updated_count))
    product_pattern_caro.short_description = '[Pattern] Add caro pattern on product'

    def product_style_simple(self, request, queryset):
        simple_style = models.ProductStyle.objects.get(name='simple')
        updated_count = 0
        for obj in queryset.all():
            obj.style = simple_style
            obj.save()
            updated_count = updated_count + 1
        self.message_user(
            request, '{}건의 상품에 simple 스타일 분류'.format(updated_count))
    product_style_simple.short_description = '[style] Mark product style as simple'

    def product_style_lovely(self, request, queryset):
        lovely_style = models.ProductStyle.objects.get(name='lovely')
        updated_count = 0
        for obj in queryset.all():
            obj.style = lovely_style
            obj.save()
            updated_count = updated_count + 1
        self.message_user(
            request, '{}건의 상품에 lovely 스타일 분류'.format(updated_count))
    product_style_lovely.short_description = '[style] Mark product style as lovely'

    def product_style_street(self, request, queryset):
        street_style = models.ProductStyle.objects.get(name='street')
        updated_count = 0
        for obj in queryset.all():
            obj.style = street_style
            obj.save()
            updated_count = updated_count + 1
        self.message_user(
            request, '{}건의 상품에 street 스타일 분류'.format(updated_count))
    product_style_street.short_description = '[style] Mark product style as street'

    def product_style_feminine(self, request, queryset):
        feminine_style = models.ProductStyle.objects.get(name='feminine')
        updated_count = 0
        for obj in queryset.all():
            obj.style = feminine_style
            obj.save()
            updated_count = updated_count + 1
        self.message_user(
            request, '{}건의 상품에 feminine 스타일 분류'.format(updated_count))
    product_style_feminine.short_description = '[style] Mark product style as feminine'

    def product_style_sexy(self, request, queryset):
        sexy_style = models.ProductStyle.objects.get(name='sexy')
        updated_count = 0
        for obj in queryset.all():
            obj.style = sexy_style
            obj.save()
            updated_count = updated_count + 1
        self.message_user(
            request, '{}건의 상품에 sexy 스타일 분류'.format(updated_count))
    product_style_sexy.short_description = '[style] Mark product style as sexy'

    def product_style_vintage(self, request, queryset):
        vintage_style = models.ProductStyle.objects.get(name='vintage')
        updated_count = 0
        for obj in queryset.all():
            obj.style = vintage_style
            obj.save()
            updated_count = updated_count + 1
        self.message_user(
            request, '{}건의 상품에 vintage 스타일 분류'.format(updated_count))
    product_style_vintage.short_description = '[style] Mark product style as vintage'

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

    def get_product_link(self, obj):
        return format_html(
            '<a href="%s" target="_blank">%s</a>' % (
                obj.product_link, 'ProductLink')
        )
    get_product_link.short_description = "Link"
    get_product_link.allow_tags = True

    def product_summary(self, obj):
        style = "<style>\
                        h4 {color:black; margin-bottom:0px}\
                        p { color: black;font-size:10px;font-weight:400; margin-bottom:4px} \
                        p.light { font-weight:400; font-size:9px; color:grey}\
                        p.right { text-align:right}\
                        p.bold { font-weight:500; font-size:12px}\
                        p.None { color:red; font-weight:600; opacity:1; background-color:pink}\
                        span.False,p.False { color:grey; opacity:0.2 }\
                        div.review { background-color : rgba(245, 223, 223,0.3) }\
                        div.not-valid { background-color : rgba(245, 100, 100,0.8) }\
                        div.no-stock { background-color : rgba(0, 0, 0,0.1)}\
                        div.not-active { background-color : rgba(251, 255, 193, 0.3) }\
                        div.active { background-color : rgba(223, 245, 223,0.3) }\
                </style> "
        stock_is_null = 'False' if obj.stock == 0 else ''
        pick_set_exist = obj.pick_set.exists()
        # TODO pick_set_style 변경
        product_info = '<img src="{url}" width="200" height="200" border="1" style="padding:10px"/>\
                        <p class="bold {subcategory}">{category} > {subcategory}</p>\
                        <h4>{name}</h4>\
                        <p class="{pick_set_exist}"> Pick exists : {pick_set_exist}</p>\
                        <p class="light right">{created_at}</p>\
                        <p class="{style}">Style : {style}</p>\
                        <p>Price :{original_price} VND \
                            <span class={is_discount}>/ Discount Price :{discount_price} VND ({discount_rate}%)</span>\
                        </p>\
                        <p class={stock_is_null}>Stock : {stock}</p>'.format(
            url=obj.product_thumbnail_image,
            pick_set_exist=pick_set_exist,
            category=obj.category,
            subcategory=obj.sub_category,
            created_at=obj.created_at,
            name=obj.name,
            style=obj.style,
            stock=obj.stock,
            stock_is_null=stock_is_null,
            is_discount=obj.is_discount,
            original_price=obj.original_price,
            discount_price=obj.discount_price,
            discount_rate=obj.discount_rate
        )

        if obj.stock_available is False:
            status = 'no-stock'
        elif obj.validation == 'R':
            status = 'review'
        elif obj.validation == 'N':
            status = 'not-valid'
        elif obj.is_active is False:
            status = 'not-active'
        elif obj.is_active is True:
            status = 'active'
        return mark_safe(style+'<div class="{status}">'.format(status=status) +
                         product_info+'</div>')

    def option_summary(self, obj):
        style = "<style>\
                h4 {color:black}\
                th, td { padding-left:10px; \
                    margin:0px; font-size:10px; color:black;font-weight:400}\
                td.False {color: grey; opacity:0.2}\
                td.no-stock {color: red; font-weight:600; }\
                td.null {color: red; font-weight:600; opacity:1; background-color:pink}\
                        div.review { background-color : rgba(245, 223, 223,0.3) }\
                        div.not-valid { background-color : rgba(245, 100, 100,0.8) }\
                        div.no-stock { background-color : rgba(0, 0, 0,0.1)}\
                div.not-active { background-color : rgba(251, 255, 193, 0.3) }\
                div.active { background-color : rgba(223, 245, 223,0.3) }\
        </style> "
        pattern_list = obj.pattern.all()
        pattern_info = '<h4>Pattern ({len}) : </h4><p>'.format(len=len(pattern_list))
        for pattern_obj in pattern_list:
            pattern_info += '{pattern}, '.format(pattern=pattern_obj)
        pattern_info += '</p>'

        size_list = obj.size.all()
        shopee_size_list = obj.shopee_size.all()
        size_info = '<h4>Size ({len} / src {source_len}): </h4><p>'.format(
            len=len(size_list), source_len=len(shopee_size_list))
        for size_obj in size_list:
            size_info += '{size}, '.format(size=size_obj)
        size_info += '</p>'

        color_list = obj.color.all()
        shopee_color_list = obj.shopee_color.all()
        color_info = '<h4>Color ({len} / src {source_len}) : </h4><p>'.format(
            len=len(color_list), source_len=len(shopee_color_list))
        for color_obj in color_list:
            color_info += '{color}, '.format(color=color_obj)
        color_info += '</p>'

        extra_option_list = obj.extra_option.all()
        source_extra_option_list = obj.source_extra_option.all()
        extra_option_info = '<h4>Extra_option ({len} / src {source_len}) : </h4><p>'.format(
            len=len(extra_option_list), source_len=len(source_extra_option_list))
        for extra_option_obj in extra_option_list:
            extra_option_info += '{extra_option}, '.format(extra_option=extra_option_obj)
        extra_option_info += '</p>'

        option_list = obj.product_options.all()
        option_info = '<h4>Options ({len}) : </h4>\
            <table>\
                <tr>\
                    <td>No</td>\
                    <td>name</td>\
                    <td>size</td>\
                    <td>color</td>\
                    <td>extra</td>\
                    <td>stock</td>\
                </tr>'.format(len=len(option_list))
        for i, option_obj in enumerate(option_list):
            size_is_null = 'null' if option_obj.size is None else ''
            color_is_null = 'null' if option_obj.color is None else ''
            extra_is_null = 'False' if option_obj.extra_option is None else ''
            stock_is_null = 'no-stock' if option_obj.stock == 0 else ''
            option_info += '<tr>\
                                <td class="{is_active}">{i} </td>\
                                <td class="{is_active}">{name} </td>\
                                <td class="{is_active} {size_is_null}">{size}</td>\
                                <td class="{is_active} {color_is_null}">{color} </td>\
                                <td class="{is_active} {extra_is_null}">{extra}</td>\
                                <td class="{is_active} {stock_is_null}">{stock}</td>\
                            </tr>'.format(is_active=option_obj.is_active, i=i, name=option_obj.name,
                                          size=option_obj.size, size_is_null=size_is_null,
                                          color=option_obj.color, color_is_null=color_is_null,
                                          extra=option_obj.extra_option, extra_is_null=extra_is_null,
                                          stock=option_obj.stock, stock_is_null=stock_is_null)
        option_info += '</table>'
        if obj.stock_available is False:
            status = 'no-stock'
        elif obj.validation == 'R':
            status = 'review'
        elif obj.validation == 'N':
            status = 'not-valid'
        elif obj.is_active is False:
            status = 'not-active'
        elif obj.is_active is True:
            status = 'active'
        return mark_safe(style+'<div class="{status}">'.format(status=status) +
                         pattern_info +
                         size_info +
                         color_info +
                         extra_option_info +
                         option_info + '</div>')

    def make_name_to_option(self, request, queryset):
        u_color = models.ProductColor.objects.get(name='undefined')
        u_size = models.ProductSize.objects.get(name='undefined')
        for obj in queryset.all():
            option_list = obj.product_options
            for option_obj in option_list.all():
                option_obj.extra_option = option_obj.name
                option_obj.color = u_color
                option_obj.size = u_size
                option_obj.save()
    make_name_to_option.short_description = '[Option] Make Product Option from option name'
