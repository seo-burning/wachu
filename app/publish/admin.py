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
    fields = ['title', 'ordering']
    extra = 0


class PostGroupInline(admin.TabularInline):
    model = models.MainPagePublish.main_section_post_group_list.through
    extra = 0
    max_num = 50

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(models.MainPagePublish)
class MainPagePublishAdmin(admin.ModelAdmin):
    inlines = [PostGroupInline, ]
    fields = ['is_published', 'date', 'top_section_post_group']
