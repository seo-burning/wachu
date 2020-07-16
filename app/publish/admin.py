from django.contrib import admin
from django.utils.safestring import mark_safe
from publish import models
from django.utils.safestring import mark_safe

from product.models import Product
# Register your models here.


# TODO Preview need to be fixed
class StorePostInline(admin.TabularInline):
    model = models.PostGroup.post_list.through
    fields = ['post_name', ]
    readonly_fields = ['post_name', ]
    extra = 0

    def post_name(self, instance):
        return mark_safe('<img src="{url}" \
        width="200" height="200" border="1" />'.format(
            url=instance.storepost.post_thumb_image
        ))


class PostTagGroupInline(admin.StackedInline):
    model = models.PostTagGroup
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
              'secondary_color']
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


@admin.register(models.PostGroup)
class PostGroupAdmin(admin.ModelAdmin):
    inlines = [StorePostInline]
    fields = ['title', 'ordering', 'cover_picture',
              'list_thumb_picture', 'published_banner',
              'published_magazine']
    list_display = ['__str__', 'published_banner',
                    'published_magazine', 'title', 'post_number']
    list_display_links = ['__str__', 'title']
    extra = 0

    def post_number(self, instance):
        return len(instance.post_list.all())


class PostGroupInline(admin.StackedInline):
    model = models.PostGroup
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
    inlines = [PostTagGroupInline]
    fields = ['is_published', 'date', ]
    list_display = ['is_published', 'date']
    list_display_links = ['date']
    ordering = ['date']


@admin.register(models.BannerPublish)
class BannerPublishAdmin(admin.ModelAdmin):
    inlines = [PostGroupInline, LinkingBannerInline]
    fields = ['is_published', 'date', ]
    list_display = ['is_published', 'date', 'post_group_number']
    list_display_links = ['date']
    ordering = ['date']

    def post_group_number(self, instance):
        return len(instance.postgroup_set.all())


@admin.register(models.MagazinePublish)
class MagazinePublishAdmin(admin.ModelAdmin):
    inlines = [PostGroupInline, ]
    fields = ['is_published', 'date', ]
    list_display = ['is_published', 'date', 'post_group_number']
    list_display_links = ['date']
    ordering = ['date']

    def post_group_number(self, instance):
        return len(instance.postgroup_set.all())


@admin.register(models.PostTagGroup)
class PostTagGroupAdmin(admin.ModelAdmin):
    fields = ['ordering', 'published_banner', 'category',
              'sub_category', 'color',
              'style', 'pattern', 'store', 'product_number', 'preview']
    list_display = ['__str__',
                    'ordering',
                    'related_product_num',
                    'published_banner',
                    'category',
                    'sub_category',
                    'color',
                    'style',
                    'pattern',
                    'store',
                    'product_number']
    list_display_links = ['__str__', 'ordering', 'published_banner',
                          'category', 'sub_category', 'color', 'pattern',
                          'style', 'store', 'product_number']
    raw_id_fields = ['store', ]

    def get_queryset(self, obj):
        queryset = Product.objects.filter(is_active=True)
        if (obj.category):
            queryset = queryset.filter(category=obj.category)
        sub_category = obj.sub_category
        if (sub_category):
            queryset = queryset.filter(sub_category=sub_category)
        color = obj.color
        if (color):
            queryset = queryset.filter(color=color)
        style = obj.style
        if (style):
            queryset = queryset.filter(style=style)
        pattern = obj.pattern
        if (pattern):
            queryset = queryset.filter(pattern=pattern)
        store = obj.store
        if (store):
            queryset = queryset.filter(store=store)
        return queryset

    def related_product_num(self, obj):
        queryset = self.get_queryset()
        return queryset.count()

    def preview(self, obj):
        image_string = ''
        for obj in queryset.all():
            image_string += str(obj)
        return mark_safe(image_string)
