from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.utils.translation import gettext as _

from store import models
from publish.models import PostGroup
from core.models import ExportCsvMixin


class PostImageInline(admin.StackedInline):
    model = models.PostImage
    fields = ['post_image_shot', ]
    readonly_fields = ['post_image_shot', ]
    extra = 0

    def post_image_shot(self, obj):
        return mark_safe('<img src="{url}" \
            width="300" height="300" border="1" />'.format(
            url=obj.source_thumb
        ))


class PostGroupInline(admin.TabularInline):
    model = PostGroup.post_list.through
    extra = 1


class StorePostInline(admin.StackedInline):
    model = models.StorePost
    show_change_link = True
    readonly_fields = ('post_taken_at_timestamp', 'post_type')
    fields = ['post_taken_at_timestamp', 'post_type']
    extra = 0
    max_num = 50
    ordering = ['-post_taken_at_timestamp']

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


# class StoreSurveyInline(admin.StackedInline):
#     model = models.StoreSurvey
#     readonly_fields = ['updated_at']
#     fields = ['title', 'updated_at',
#               'contact_status', 'reaction_rate', 'content']
#     extra = 0


class StoreRankingInline(admin.StackedInline):
    model = models.StoreRanking
    readonly_fields = ['follower', 'following', 'post_num', 'store_score',
                       'post_total_score', 'date', 'ranking',
                       'ranking_changed']
    fields = ['ranking', 'ranking_changed',
              'store_score', 'post_total_score']
    extra = 0
    max_num = 3

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

# https://medium.com/@hakibenita/things-you-must-know-about-django-admin-as-your-app-gets-bigger-6be0b0ee9614
@admin.register(models.Store)
class StoreAdmin(admin.ModelAdmin, ExportCsvMixin):
    inlines = [StoreRankingInline, StorePostInline, ]
    readonly_fields = (
        'insta_id',
        'insta_url',
        'current_ranking',
        'current_ranking_changed',
        'instagram_link',
        'profile_image',
        'profile_image_shot',
        'name',
        'follower',
        'following',
        'post_num',
        'description',)
    fieldsets = [
        (_("User Profile"), {'fields': [
            'is_active',
            'is_updated',
            'current_ranking',
            'current_ranking_changed',
            'instagram_link',
            'profile_image_shot',
            'insta_id',
            'insta_url',
            'name',
            'description'
        ]}),
        (_("Url Infomation"), {'fields': (('facebook_url', 'shopee_url'),)}),
        (_("Instagram Numbers"), {'fields': (
            ('post_num', 'follower', 'following'),
        )}),
        (_("Images"), {'fields': (
            ("category", "region", 'age'),
            ("primary_style", "secondary_style"),
        )}),
    ]
    list_display = ["instagram_link",
                    'current_ranking',
                    'current_ranking_changed',
                    "insta_id", 'profile_thumb', 'follower',
                    "primary_style", "secondary_style", "age"]
    list_filter = ['is_active', 'is_updated']
    list_editable = ["primary_style", "secondary_style", "age"]
    list_display_links = ["insta_id"]
    list_select_related = (
        'primary_style', 'secondary_style', 'age'
    )
    search_fields = ["insta_id", "region__name",
                     "primary_style__name", "secondary_style__name", ]

    actions = ['export_as_csv', 'make_activate',
               'make_deactivate', 'make_deactivate_under_5000']

    def make_deactivate_under_5000(self, request, queryset):
        num = 0
        for q in queryset:
            if (int(q.follower) < 5000):
                num = num+1
                q.is_active = False
                q.save()
        self.message_user(
            request, '5000 follower 이하인 {}의 계정을 deactivate로 변경'.format(num))

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


@admin.register(models.StorePost)
class StorePostAdmin(admin.ModelAdmin):
    inlines = [PostImageInline, PostGroupInline]
    model = models.StorePost
    readonly_fields = ('post_like', 'post_score',
                       'post_description',
                       'post_taken_at_timestamp',
                       'post_url')
    fields = ['is_active', 'post_score', 'post_description',
              'post_url']
    ordering = ['post_taken_at_timestamp']
    actions = ['make_activate',
               'make_deactivate']
    list_per_page = 1000

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


@admin.register(models.Age)
class AgeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )
