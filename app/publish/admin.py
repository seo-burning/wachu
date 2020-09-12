from django.contrib import admin
from django.utils.safestring import mark_safe
from publish import models
# Register your models here.


# TODO Preview need to be fixed
class ProductInLine(admin.TabularInline):
    model = models.ProductGroup.product_list.through
    fields = ['product_link', 'product_thumb', 'product_name']
    readonly_fields = ['product_link', 'product_thumb', 'product_name']
    extra = 0

    def product_link(self, instance):
        return mark_safe('<a href="https://dabivn.com/admin/product/product/{}">product link</a>'.format(instance.product.pk))

    def product_thumb(self, instance):
        return mark_safe(instance.product)

    def product_name(self, instance):
        return instance.product.name


class ProductTagGroupInline(admin.StackedInline):
    model = models.ProductTagGroup
    show_change_link = True
    list_display = ['__str__', 'ordering', 'published_banner',
                    'category', 'sub_category', 'color',
                    'style', 'store', 'product_number']
    list_display_links = ['__str__', 'ordering', 'published_banner',
                          'category', 'sub_category', 'color',
                          'style', 'store', 'product_number']
    extra = 0
    max_num = 15
    ordering = ['ordering']

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(models.LinkingBanner)
class LinkingBannerAdmin(admin.ModelAdmin):
    fields = ['title', 'ordering', 'list_thumb_picture',
              'cover_picture_1',
              'cover_picture_2',
              'cover_picture_3',
              'cover_picture_4',
              'link_url',
              'published_banner',
              'banner_type',
              'coupon_code',
              'primary_color',
              'secondary_color', 'data']
    list_display = ['__str__', 'title',
                    'published_banner',
                    'banner_type',
                    ]
    list_display_links = ['__str__', 'title']
    extra = 0


class LinkingBannerInline(admin.StackedInline):
    model = models.LinkingBanner
    show_change_link = True
    fields = ['ordering', 'title', '__str__']
    readonly_fields = ['title', '__str__']
    extra = 0
    max_num = 15
    ordering = ['ordering']

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(models.ProductGroup)
class ProductGroupAdmin(admin.ModelAdmin):
    inlines = [ProductInLine]
    fields = ['title', 'ordering', 'cover_picture',
              'list_thumb_picture', 'published_banner',
              'published_magazine', 'product_list']
    list_display = ['__str__', 'published_banner',
                    'published_magazine', 'title', 'product_number']
    raw_id_fields = ['product_list', ]
    list_display_links = ['__str__', 'title']
    extra = 0

    def product_number(self, instance):
        return len(instance.product_list.all())


class ProductGroupInline(admin.StackedInline):
    model = models.ProductGroup
    show_change_link = True
    fields = ['ordering', 'title', '__str__']
    readonly_fields = ['title', '__str__']
    extra = 0
    max_num = 15
    ordering = ['ordering']

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(models.MainPagePublish)
class MainPagePublishAdmin(admin.ModelAdmin):
    inlines = [ProductTagGroupInline]
    fields = ['is_published', 'date', ]
    list_display = ['is_published', 'date']
    list_display_links = ['date']
    ordering = ['date']


@admin.register(models.BannerPublish)
class BannerPublishAdmin(admin.ModelAdmin):
    inlines = [ProductGroupInline, LinkingBannerInline]
    fields = ['is_published', 'date', ]
    list_display = ['is_published', 'date', 'product_group_number']
    list_display_links = ['date']
    ordering = ['date']

    def product_group_number(self, instance):
        return len(instance.productgroup_set.all())


@admin.register(models.MagazinePublish)
class MagazinePublishAdmin(admin.ModelAdmin):
    inlines = [ProductGroupInline, ]
    fields = ['is_published', 'date', ]
    list_display = ['is_published', 'date', 'product_group_number']
    list_display_links = ['date']
    ordering = ['date']

    def product_group_number(self, instance):
        return len(instance.productgroup_set.all())


@admin.register(models.ProductTagGroup)
class ProductTagGroupAdmin(admin.ModelAdmin):
    fields = ['ordering', 'is_active', 'published_banner', 'category',
              'sub_category', 'color',
              'style', 'pattern', 'store',
              'product_number']
    read_only_fields = ['preview', ]
    list_per_page = 50
    list_display = ['__str__',
                    'is_active',
                    'ordering',
                    'related_product_num',
                    'published_banner',
                    'category',
                    'sub_category',
                    'color',
                    'style',
                    'pattern',
                    'store',
                    'product_number',
                    'preview']
    ordering = ['-updated_at']
    list_display_links = ['__str__', 'is_active', 'ordering', 'published_banner',
                          'category', 'sub_category', 'color', 'pattern',
                          'style', 'store', 'product_number']
    raw_id_fields = ['store', ]
    actions = ['make_activate', 'make_deactivate', ]

    def make_activate(self, request, queryset):
        updated_count = queryset.update(is_active=True)
        self.message_user(
            request, '{}Activated 상태로 변경'.format(updated_count))
    make_activate.short_description = 'Activate 상태로 변경'

    def make_deactivate(self, request, queryset):
        updated_count = queryset.update(is_active=False)
        self.message_user(
            request, '{}Deavtivate 상태로 변경'.format(updated_count))
    make_deactivate.short_description = 'Deactivate 상태로 변경'
