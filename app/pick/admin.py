from django.contrib import admin
from django.utils.translation import gettext as _

from pick import models


class ChuPickABInline(admin.StackedInline):
    model = models.ChuPickAB
    max_num = 50
    extra = 0
    fields = ('is_published', 'title',
              'store_a', 'outlink_a',
              'pick_image_a', 'chu_point_a',
              'store_b', 'outlink_b',
              'pick_image_b', 'chu_point_b',
              'pick_set')
    verbose_name = _('ChuPickAB')
    verbose_name_plural = _('ChuPickAB')


class ChuPickRatingInline(admin.StackedInline):
    model = models.ChuPickRating
    max_num = 50
    extra = 0
    fields = ('is_published', 'title', 'store', 'outlink',
              'pick_image', 'chu_point', 'pick_set')
    verbose_name = _('ChuPickRating')
    verbose_name_plural = _('ChuPickRating')


@admin.register(models.ChuPoint)
class ChuPointAdmin(admin.ModelAdmin):
    fields = ('product_category',
              'product_color',
              'primary_style',
              'secondary_style',
              'tpo',
              'age')
    list_display = (
        '__str__',
        'primary_style',
        'secondary_style',
        'tpo',
        'age')
    verbose_name = _('ChuPoint')
    verbose_name_plural = _('ChuPoint')


@admin.register(models.ChuPickRating)
class ChuPickRatingAdmin(admin.ModelAdmin):
    fields = ('is_published', 'title', 'store', 'outlink',
              'pick_image', 'chu_point', 'pick_set')
    list_display = ('is_published', 'title', 'pick_set')
    verbose_name = _('ChuPickRating')
    verbose_name_plural = _('ChuPickRating')


@admin.register(models.ChuPickAB)
class ChuPickABAdmin(admin.ModelAdmin):
    fields = ('is_published', 'title',
              'store_a', 'outlink_a', 'pick_image_a', 'chu_point_a',
              'store_b', 'outlink_b', 'pick_image_b', 'chu_point_b',
              'pick_set')
    list_display = ('is_published', 'title', 'pick_set')
    verbose_name = _('ChuPickAB')
    verbose_name_plural = _('ChuPickAB')


@admin.register(models.ChuPickSet)
class ChuPickSetAdmin(admin.ModelAdmin):
    inlines = (ChuPickABInline, ChuPickRatingInline)
    fields = ('is_published', 'date')
    list_display = ('is_published', 'date')
    verbose_name = _('ChuPickSet')
    verbose_name_plural = _('ChuPickSet')
