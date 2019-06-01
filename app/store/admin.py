from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.html import format_html

from store import models

import csv
from django.http import HttpResponse


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(
            meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field)
                            for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


class StorePostInline(admin.StackedInline):
    model = models.StorePost
    readonly_fields = ('post_image', 'post_like',
                       'post_description', 'post_taken_at_timestamp')
    fields = ['is_active']
    extra = 0
    ordering = ['post_taken_at_timestamp']
    verbose_name = 'Post'
    verbose_name_plural = 'Post'

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(models.Store)
class StoreAdmin(admin.ModelAdmin, ExportCsvMixin):
    inlines = [StorePostInline]
    readonly_fields = (
        'insta_id',
        'insta_url',
        'instagram_link',
        'profile_image',
        'profile_image_shot',
        'name',
        'follower',
        'following',
        'post_num',
        'description',)
    fieldsets = [
        ("User Profile", {'fields': [
            'is_active',
            'is_updated',
            'instagram_link',
            'profile_image_shot',
            'insta_id',
            'insta_url',
            'name',
            'description'
        ]}),
        ("Instagram Images", {'fields': (
            ('post_num', 'follower', 'following'),
        )}),
        ("images", {'fields': (
            ("category", "region"),
            ("primary_style", "secondary_style", "tpo"),
        )}),
    ]
    list_display = ["instagram_link", "insta_id", 'profile_thumb',
                    "category",
                    "primary_style", "secondary_style", "tpo"]
    list_filter = ['is_active', 'is_updated']
    list_editable = ["category",
                     "primary_style", "secondary_style", "tpo"]
    list_display_links = ["insta_id"]
    search_fields = ["insta_id", "category__name", "region__name",
                     "primary_style__name", "secondary_style__name",
                     "tpo__name"]

    actions = ['export_as_csv', 'make_activate',
               'make_deactivate', 'make_deactivate_under_1000']

    def make_deactivate_under_1000(self, request, queryset):
        num = 0
        for q in queryset:
            if (int(q.follower) < 1000):
                num = num+1
                q.is_active = False
                q.save()
        self.message_user(
            request, '1000 follower 이하인 {}의 계정을 deactivate>로 변경'.format(num))

    def make_activate(self, request, queryset):
        updated_count = queryset.update(is_active=True)
        self.message_user(
            request, '{}건의 포스팅을 Activated 상태로 변경'.format(updated_count))
    make_activate.short_description = '지정 스토어를 Activate 상태로 변경'

    def make_deactivate(self, request, queryset):
        updated_count = queryset.update(is_active=False)
        self.message_user(
            request, '{}건의 포스팅을 Deavtivate 상태로 변경'.format(updated_count))
    make_deactivate.short_description = '지정 스토어를 Deactivate 상태로 변경'

    def profile_image_shot(self, obj):
        return mark_safe('<img src="{url}" \
            width="300", height="300" />'.format(
            url=obj.profile_image
        ))

    def profile_thumb(self, obj):
        return mark_safe('<img src="{url}" \
            width="50" height="50" border="1" />'.format(
            url=obj.profile_image
        ))

    def instagram_link(self, obj):
        return format_html(
            '<a href="%s" target="_blank">%s</a>' % (obj.insta_url, 'Insta')
        )
    instagram_link.short_description = "Link"
    instagram_link.allow_tags = True


@admin.register(models.Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )


@admin.register(models.Primary_Style)
class Primary_StyleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )


@admin.register(models.Secondary_Style)
class Secondary_StyleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )


@admin.register(models.Tpo)
class TpoAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )


admin.site.register(models.StorePost)
