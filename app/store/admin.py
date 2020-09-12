from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.utils.translation import gettext as _
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.db.models.functions import TruncDay
import json
import requests
from store import models
from product.models import Product, ProductImage
from core.models import ExportCsvMixin
from .forms import ProductFormForInstagramPost, ProductInlineFormSet
from utils.helper.image_processing import create_presigned_url
from utils.helper.request_helper import get_user_agents


class ProductCreateInline(admin.StackedInline):
    model = Product
    form = ProductFormForInstagramPost
    formset = ProductInlineFormSet
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
    list_per_page = 50
    readonly_fields = (
        'view',
        'is_new_post',
        'current_ranking',
        'current_ranking_changed',
        'current_review_rating',
        'instagram_link',
        'profile_image_shot',
        'follower',
        'following',
        'post_num',
    )
    fieldsets = [
        (_("User Profile"), {'fields': ['is_new_post',
                                        'is_active',
                                        'view',
                                        'store_type',
                                        'current_ranking',
                                        'current_ranking_changed',
                                        'current_review_rating',
                                        'instagram_link',
                                        'profile_image',
                                        'profile_image_shot',
                                        'insta_id',
                                        'insta_url',
                                        'name',
                                        'description'
                                        ]}),
        (_("Url Infomation"),
         {'fields': (('phone', 'facebook_url', 'facebook_id',
                      'facebook_numeric_id', 'shopee_url',
                      'shopee_numeric_id', 'homepage_url', 'dosiin_url'),)}),
        (_("Instagram Numbers"), {'fields': (
            ('post_num', 'follower', 'following'),
        )}),
        (_("Tags"), {'fields': (
            ("category", 'product_category', 'age'),
            ("primary_style", "secondary_style"),
        )}),
        (_("Images"), {'fields': (
            ("recent_post_1", "recent_post_2",
             'recent_post_3'),
        )}),
    ]
    list_display = ["is_active",
                    'current_ranking',
                    'store_infomation',
                    'store_validation',
                    'need_to_update_num',
                    'product_num', ]
    list_display_links = ['store_infomation', 'store_validation']
    list_filter = ['is_active', 'store_type', 'primary_style', 'secondary_style']
    search_fields = ["insta_id",
                     "primary_style__name",
                     "secondary_style__name", ]
    actions = ['export_as_csv',
               'make_activate',
               'make_deactivate',
               'update_validation'
               ]

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
        if 'http' in str(obj.profile_image):
            url = obj.profile_image
        else:
            url = create_presigned_url('wachu', 'media/'+str(obj.profile_image), expiration=3000)
        return mark_safe('<img src="{url}" \
            width="200", height="200" />'.format(
            url=url
        ))

    def instagram_link(self, obj):
        return format_html(
            '<a href="%s" target="_blank">%s</a>' % (obj.insta_url, 'Insta')
        )

    def product_num(self, obj):
        product_num = obj.product_set.filter(is_active=True, stock_available=True).count()
        return format_html('<a href="http://dabivn.com/'
                           'admin/product/product/?q=%s&is_active__exact=1&stock_available__exact=1">%s</a>'
                           % (obj.insta_id, product_num)
                           )

    def need_to_update_num(self, obj):
        product_num = obj.product_set.filter(validation='R', stock_available=True).count()
        if product_num > 0:
            return format_html('<a href="http://dabivn.com/'
                               'admin/product/product/?q=%s&validation__exact=R'
                               '&stock_available__exact=1"><p style="color:red">%s</p></a>'
                               % (obj.insta_id, product_num)
                               )
        else:
            return product_num

    def profile_thumb(self, obj):
        if 'http' in str(obj.profile_image):
            url = obj.profile_image
        else:
            url = create_presigned_url('wachu', 'media/'+str(obj.profile_image), expiration=3000)
        return mark_safe('<img src="{url}" \
            width="50" height="50" border="1" />'.format(
            url=url
        ))

    def store_infomation(self, obj):
        if 'http' in str(obj.profile_image):
            profile_url = obj.profile_image
        else:
            profile_url = create_presigned_url('wachu', 'media/'+str(obj.profile_image), expiration=3000)
        style = "<style>\
                        h4 {color:black; margin-bottom:0px}\
                        p { color: black;font-size:10px;font-weight:400; margin-bottom:4px} \
                        p.light { font-weight:400; font-size:9px; color:grey}\
                        p.right { text-align:right}\
                        p.bold { font-weight:500; font-size:12px}\
                        span.False,p.False { color:grey; opacity:0.2 }\
                </style> "
        store_info = '<img src="{url}" width="50" height="50" border="1" style="padding:10px"/>\
                        <h4>{name}</h4>\
                        <p class="light">last update {updated_at}</p>\
                        <p class="">product source : {store_type}</p>\
                        <p class="{p_style} {s_style}">스타일 : {p_style} / {s_style}</p>'.format(
            name=obj.insta_id,
            url=profile_url,
            updated_at=obj.updated_at,
            store_type=obj.store_type,
            p_style=obj.primary_style,
            s_style=obj.secondary_style,
        )
        return mark_safe(style+'<div class="{status}">'.format(status=obj.is_active) +
                         store_info+'</div>')

    def store_validation(self, obj):
        insta_is_valid, facebook_is_valid, homepage_is_valid, shopee_is_valid = obj.validation_string.split('/')
        style = "<style>\
                        p.None { color:grey; font-weight:300; opacity:1;}\
                        p.True { color:green; font-weight:600; opacity:1;}\
                        p.False { color:red; font-weight:600; opacity:1;}\
                </style> "
        store_info = '<p class="">contact : {phone}</p>\
                        <p class="{insta_is_valid}">instagram link</p>\
                        <p class="{facebook_is_valid}">facebook link</p>\
                        <p class="{homepage_is_valid}">homepage link</p>\
                        <p class="{shopee_is_valid}">shopee link</p>'.format(
            phone=obj.phone,
            insta_is_valid=insta_is_valid,
            facebook_is_valid=facebook_is_valid,
            homepage_is_valid=homepage_is_valid,
            shopee_is_valid=shopee_is_valid,
        )
        return mark_safe(style+'<div class="{status}">'.format(status=obj.is_active) +
                         store_info+'</div>')

    def update_validation(self, request, queryset):
        for obj in queryset:
            # 인스타 200 체크
            if obj.insta_url is None:
                insta_is_valid = 'None'
            elif requests.get(obj.insta_url,
                              headers={'User-Agent': get_user_agents(),
                                       'X-Requested-With': 'XMLHttpRequest',
                                       'Referer': 'https://www.instagram.com'}).status_code == 200:
                insta_is_valid = 'True'
            else:
                insta_is_valid = 'False'

            if obj.facebook_url is None:
                facebook_is_valid = 'None'
            elif requests.get(obj.facebook_url,
                              headers={'User-Agent': get_user_agents(),
                                       'X-Requested-With': 'XMLHttpRequest'}).status_code == 200:
                facebook_is_valid = 'True'
            else:
                facebook_is_valid = 'False'

            if obj.homepage_url is None:
                homepage_is_valid = 'None'
            else:
                try:
                    if requests.get(obj.homepage_url,
                                    headers={'User-Agent': get_user_agents(),
                                             'X-Requested-With': 'XMLHttpRequest'}).status_code == 200:
                        homepage_is_valid = 'True'
                    else:
                        homepage_is_valid = 'False'
                except Exception as e:
                    print(e)
                    homepage_is_valid = 'False'

            if obj.shopee_url is None:
                shopee_is_valid = 'None'
            else:
                response_json = requests.get('https://shopee.vn/api/v2/search_items/?by=pop&limit=1&match_id'
                                             '={shopee_numeric_id}&newest=1&order=desc&page_type='
                                             'shop&shop_categoryids=&version=2'.format(
                                                 shopee_numeric_id=obj.shopee_numeric_id),
                                             headers={'User-Agent': get_user_agents(),
                                                      'X-Requested-With': 'XMLHttpRequest',
                                                      'Referer': 'https://shopee.vn/shop/{store_id}/'
                                                      'search?shopCollection='.format(store_id=obj.shopee_numeric_id),
                                                      },).json()
                if response_json['total_count'] == 0:
                    print('this')
                    shopee_is_valid = 'False'
                else:
                    shopee_is_valid = 'True'
            validation_string = insta_is_valid + '/'+facebook_is_valid+'/'+homepage_is_valid+'/'+shopee_is_valid
            obj.validation_string = validation_string
            obj.save()

    need_to_update_num.short_description = '업데이트 필요'
    product_num.short_description = '유효 상품'
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
    inlines = [ProductCreateInline, PostImageInline]
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

    def save_formset(self, request, form, formset, change):
        if formset.model != Product:
            return super(StorePostAdmin, self).save_formset(request, form, formset, change)
        product_list = formset.save(commit=False)
        for product_obj in product_list:
            print(product_obj.post)
            post_obj = product_obj.post
            product_obj.store = post_obj.store
            product_obj.description = post_obj.post_description
            product_obj.product_link = post_obj.post_url
            product_obj.currency = 'VND'
            product_obj.product_source = 'INSTAGRAM'
            product_obj.is_active = True
            product_obj.save()
            thumb_image_pk = product_obj.thumb_image_pk
            post_image_set = post_obj.post_image_set.all()
            image_count = post_image_set.count()
            print(image_count, thumb_image_pk, post_obj.post_type)
            if post_obj.post_type == 'V':
                product_obj.video_source = post_obj.video_source
                product_obj.product_thumbnail_image = post_obj.post_thumb_image
                product_image_obj, is_created = ProductImage.objects.get_or_create(
                    source_thumb=post_obj.post_thumb_image,
                    post_image_type='V',
                    source=post_obj.video_source, product=product_obj)
            else:
                product_obj.product_thumbnail_image = post_image_set[image_count - thumb_image_pk].source_thumb
                product_obj.product_image_type = post_obj.post_type
                product_obj.video_source = post_obj.video_source
                for i, post_image in enumerate(post_image_set):
                    product_image_obj, is_created = ProductImage.objects.get_or_create(
                        source_thumb=post_image.source_thumb,
                        post_image_type=post_image.post_image_type,
                        source=post_image.source, product=product_obj)
            product_obj.save()
        formset.save_m2m()


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
