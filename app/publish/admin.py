from django.contrib import admin
from django.utils.safestring import mark_safe
from publish import models
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


@admin.register(models.PostGroup)
class PostGroupAdmin(admin.ModelAdmin):
    inlines = [StorePostInline]
    fields = ['title', 'ordering', 'cover_picture',
              'list_thumb_picture',
              'published_page', 'published_banner',
              'published_magazine']
    list_display = ['published_page', 'published_banner',
                    'published_magazine', 'title', 'post_number']
    list_display_links = ['title']
    extra = 0

    def post_number(self, instance):
        return len(instance.post_list.all())


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
    inlines = [PostGroupInline, ]
    fields = ['is_published', 'date', ]
    list_display = ['is_published', 'date', 'post_group_number']
    list_display_links = ['date']
    ordering = ['date']

    def post_group_number(self, instance):
        return len(instance.postgroup_set.all())


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
