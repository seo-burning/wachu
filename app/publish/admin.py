from django.contrib import admin

from publish import models
# Register your models here.


# TODO Preview need to be fixed
class StorePostInline(admin.TabularInline):
    model = models.PostGroup.post_list.through


@admin.register(models.PostGroup)
class PostGroupAdmin(admin.ModelAdmin):
    inlines = [StorePostInline]
    fields = ['title']
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
