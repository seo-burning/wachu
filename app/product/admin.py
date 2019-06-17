from django.contrib import admin
from django.utils.translation import gettext as _

from store.models import StorePost
from product import models
# Register your models here.


class StorePostInline(admin.StackedInline):
    model = StorePost
    readonly_fields = ('post_image', 'post_description')
    fields = ['ordering_keyword', 'name', 'post_description']
    extra = 0
    max_num = 50
    ordering = ['post_taken_at_timestamp']
    verbose_name = _('Post')
    verbose_name_plural = _('Post')

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(models.SlidingBannerSection)
class SlidingBannerSectionAdmin(admin.ModelAdmin):
    inlines = [StorePostInline]
    fields = ['is_published', 'title_head',
              'title_colored_keyword', 'title_foot', 'date']


@admin.register(models.MainSection)
class MainSectionAdmin(admin.ModelAdmin):
    inlines = [StorePostInline]
    fields = ['is_published', 'date']
