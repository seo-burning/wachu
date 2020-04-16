from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.utils.translation import gettext as _
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.db.models.functions import TruncDay
import json

from store import models
from product.models import Product
from publish.models import PostGroup
from core.models import ExportCsvMixin


class ProductInline(admin.StackedInline):
    model = Product
    fields = [
        'store',
        'category',
        'sub_category',
        'thumb_image_pk',
        'style',
        'color',
        'price',
        'size'
    ]
    raw_id_fields = ['store']
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)
    extra = 1


@admin.register(models.UserFavoritePost)
class FavoritePost(admin.ModelAdmin):
    model = models.UserFavoritePost
    list_display = ['store_post', 'user']
    list_filter = ['user']
    actions = ['export_as_csv']


@admin.register(models.UserFavoriteStore)
class FavoriteStoreAdmin(admin.ModelAdmin, ExportCsvMixin):
    model = models.UserFavoriteStore
    list_display = ['store', 'user']
    list_filter = ['user']
    actions = ['export_as_csv']


@admin.register(models.PostImage)
class PostImageAdmin(admin.ModelAdmin):
    model = models.PostImage
    search_fields = ["store_post__store__insta_id", 'source_thumb']


class StoreCategoryInline(admin.TabularInline):
    model = models.Store.category.through
    extra = 0
    max_num = 200


class PostImageInline(admin.StackedInline):
    model = models.PostImage
    fields = ['post_image_shot', 'post_image_type']
    readonly_fields = ['post_image_shot', ]
    extra = 0
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)

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
    readonly_fields = ('post_taken_at_timestamp',
                       'post_type', 'post_thumb_image')
    fields = ['post_taken_at_timestamp', 'post_type',
              'post_thumb_image']
    extra = 0
    max_num = 50
    ordering = ['-post_taken_at_timestamp']

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class StoreRankingInline(admin.StackedInline):
    model = models.StoreRanking
    readonly_fields = ['follower', 'following', 'post_num',
                       'store_score',
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


@admin.register(models.StoreAddress)
class StoreAddressAdmin(admin.ModelAdmin):
    model = models.StoreAddress


class StoreAddressInline(admin.StackedInline):
    model = models.StoreAddress
    fields = ['address',
              'google_map_url', 'region', 'X_axis', 'Y_axis', 'contact']
    extra = 1

# https://medium.com/@hakibenita/things-you-must-know-about-django-admin-as-your-app-gets-bigger-6be0b0ee9614
@admin.register(models.Store)
class StoreAdmin(admin.ModelAdmin, ExportCsvMixin):
    inlines = [StoreAddressInline]  # StorePostInline,
    readonly_fields = (
        'is_new_post',
        'insta_url',
        'current_ranking',
        'current_ranking_changed',
        'current_review_rating',
        'instagram_link',
        'profile_image',
        'profile_image_shot',
        'name',
        'follower',
        'following',
        'post_num',
        'description',)
    fieldsets = [
        (_("User Profile"), {'fields': ['is_new_post',
                                        'is_active',
                                        'is_updated',
                                        'store_type',
                                        'current_ranking',
                                        'current_ranking_changed',
                                        'current_review_rating',
                                        'instagram_link',
                                        'profile_image_shot',
                                        'insta_id',
                                        'insta_url',
                                        'name',
                                        'description'
                                        ]}),
        (_("Url Infomation"),
         {'fields': (('facebook_url', 'facebook_id',
                      'facebook_numeric_id', 'shopee_url', 'homepage_url'),)}),
        (_("Instagram Numbers"), {'fields': (
            ('post_num', 'follower', 'following'),
        )}),
        (_("Tags"), {'fields': (
            ("category", 'age'),
            ("primary_style", "secondary_style"),
        )}),
        (_("Images"), {'fields': (
            ("recent_post_1", "recent_post_2",
             'recent_post_3'),
        )}),
    ]
    list_display = ["instagram_link",
                    "store_type",
                    'current_ranking',
                    "insta_id", 'profile_thumb',
                    'follower', 'post_num',
                    'post_product_num', 'need_to_update', ]
    list_filter = ['is_active', 'is_updated', 'store_type']
    list_display_links = ["insta_id"]
    search_fields = ["insta_id",
                     "primary_style__name", "secondary_style__name", ]
    actions = ['export_as_csv', 'make_activate',
               'make_deactivate', 'make_deactivate_under_5000',
               'make_is_updated', 'make_is_not_updated',
               'make_deactivate_not_categorized']

    def make_deactivate_not_categorized(self, request, queryset):
        num = 0
        for q in queryset:
            if (len(q.category.all()) == 0):
                print(q.insta_id)
                num = num + 1
                q.is_active = False
                q.save()
        self.message_user(
            request, '분류되지 않은 {}의 계정을 deactivate로 변경'.format(num))

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

    def make_is_updated(self, request, queryset):
        updated_count = queryset.update(is_updated=True)
        self.message_user(
            request, '{}건의 포스팅을 Updated 상태로 변경'.format(updated_count))
    make_is_updated.short_description = '지정 스토어를 Updated 상태로 변경'

    def make_is_not_updated(self, request, queryset):
        updated_count = queryset.update(is_updated=False)
        self.message_user(
            request, '{}건의 포스팅을 Not Updated 상태로 변경'.format(updated_count))
    make_is_not_updated.short_description = '지정 스토어를 Not Updated 상태로 변경'

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

    def post_product_num(self, obj):
        product_num = obj.store_post_set.all().filter(product__gte=1).count()
        return format_html('<a href="http://dabivn.com/'
                           'admin/product/product/?q=%s">%s</a>'
                           % (obj.insta_id, product_num)
                           )

    def need_to_update(self, obj):
        product_num = obj.store_post_set.all().filter(
            product__isnull=True, is_product='P').count()
        return format_html(
            '<a style="color: red" href="'
            'http://dabivn.com/admin/store/'
            'storepost/?is_product__exact=P'
            '&is_active=1'
            '&product=related_product_not_exist'
            '&q=%s">%s</a>'
            % (obj.insta_id, product_num)
        )

    instagram_link.short_description = "Link"
    instagram_link.allow_tags = True


class PostRankingFilter(admin.SimpleListFilter):
    title = 'Ranking Filter'
    parameter_name = 'store__current_ranking'

    def lookups(self, request, model_admin):
        return(
            ('store__current_ranking <= 200', 'store__current_ranking <= 200'),
            ('store__current_ranking <= 400', 'store__current_ranking <= 400'),
            ('store__current_ranking <= 600', 'store__current_ranking <= 600'),
            ('store__current_ranking <= 800', 'store__current_ranking <= 800'),
            ('store__current_ranking <= 1000',
             'store__current_ranking <= 1000'),

        )

    def queryset(self, request, queryset):
        if self.value() == 'store__current_ranking <= 200':
            return queryset.filter(store__current_ranking__lte=200)
        elif self.value() == 'store__current_ranking <= 400':
            return queryset.filter(store__current_ranking__lte=400)
        elif self.value() == 'store__current_ranking <= 600':
            return queryset.filter(store__current_ranking__lte=600)
        elif self.value() == 'store__current_ranking <= 800':
            return queryset.filter(store__current_ranking__lte=800)
        elif self.value() == 'store__current_ranking <= 1000':
            return queryset.filter(store__current_ranking__lte=1000)


class PostRelatedProductFilter(admin.SimpleListFilter):
    title = 'Ranking Filter'
    parameter_name = 'product'

    def lookups(self, request, model_admin):
        return(
            ('related_product_not_exist', 'related_product_not_exist'),
            ('related_product exist', 'related_product exist'),

        )

    def queryset(self, request, queryset):
        if self.value() == 'related_product exist':
            return queryset.filter(product__gt=0)
        elif self.value() == 'related_product_not_exist':
            return queryset.filter(product__isnull=True)


@admin.register(models.StorePost)
class StorePostAdmin(admin.ModelAdmin):
    inlines = [ProductInline, PostImageInline, PostGroupInline]
    model = models.StorePost
    readonly_fields = ('post_like', 'post_score',
                       'post_description',
                       'post_taken_at_timestamp',
                       'post_url', 'store', 'get_store_pk',
                       'get_store_category_style')
    fieldsets = [(_('status'), {'fields': ['is_active', 'is_product']}),
                 (_('Post Info'), {'fields': ['post_score',
                                              'post_like',
                                              'post_description',
                                              'post_taken_at_timestamp',
                                              'post_url', ]}),
                 (_('Store Info'), {'fields': ['store', 'get_store_pk',
                                               'get_store_category_style']}), ]
    ordering = ['-post_taken_at_timestamp', 'store', ]
    actions = ['make_activate',
               'make_deactivate', 'categorize_not_product',
               'categorize_product_etc']
    list_filter = (PostRelatedProductFilter, 'is_active', 'is_product')
    list_display = ['store', '__str__',
                    'related_product',
                    'is_active',
                    'is_product',
                    ]
    list_display_links = ['store', '__str__',
                          'is_active',
                          'is_product',
                          ]
    search_fields = ('store__insta_id',)
    list_per_page = 30

    def make_activate(self, request, queryset):
        updated_count = queryset.update(is_active=True)
        self.message_user(
            request, '{}건의 포스팅을 Activated 상태로 변경'.format(updated_count))
    make_activate.short_description = 'Activate 상태로 변경'

    def make_deactivate(self, request, queryset):
        updated_count = queryset.update(is_active=False)
        self.message_user(
            request, '{}건의 포스팅을 Deavtivate 상태로 변경'.format(updated_count))
    make_deactivate.short_description = 'Deactivate 상태로 변경'

    def categorize_not_product(self, request, queryset):
        updated_count = queryset.update(is_product='N')
        self.message_user(
            request, '{}건의 포스팅을 Not Product 로 분류'.format(updated_count))
    categorize_not_product.short_description = 'Not Product 로 분류'

    def categorize_product_etc(self, request, queryset):
        updated_count = queryset.update(is_product='E')
        self.message_user(
            request, '{}건의 포스팅을 Product ETC 로 분류'.format(updated_count))
    categorize_product_etc.short_description = 'Product ETC 로 분류'

    def get_store_pk(self, obj):
        return obj.store.pk

    def get_store_category_style(self, obj):
        category = ''
        primary_style = ''
        secondary_style = ''
        if obj.store.category:
            category = obj.store.category.name
        if obj.store.primary_style:
            primary_style = obj.store.primary_style.name
        if obj.store.secondary_style:
            secondary_style = obj.store.secondary_style.name
        return "category: {} /////// style: {} & {}"\
            .format(category, primary_style, secondary_style)

    def related_product(self, obj):
        return obj.product_set.all().count()

    def changelist_view(self, request, extra_context=None):
        # Aggregate new subscribers per day
        chart_data = (
            models.StorePost.objects.annotate(date=TruncDay("created_at"))
            .values("date")
            .annotate(y=Count("id"))
            .order_by("-date")
        )

        # Serialize and attach the chart data to the template context
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data": as_json}

        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(models.Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [StoreCategoryInline, ]
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
