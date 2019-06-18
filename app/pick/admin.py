from django.contrib import admin
from django.utils.translation import gettext as _

from pick import models


class ChuPickABInline(admin.StackedInline):
    model = models.ChuPickAB
    max_num = 50
    extra = 0
    fields = ('is_published', 'store', 'pick_image_a', 'pick_image_b',)
    verbose_name = _('ChuPickAB')
    verbose_name_plural = _('ChuPickAB')


class ChuPickRatingInline(admin.StackedInline):
    model = models.ChuPickRating
    max_num = 50
    extra = 0
    fields = ('is_published', 'store', 'pick_image',)
    verbose_name = _('ChuPickRating')
    verbose_name_plural = _('ChuPickRating')


@admin.register(models.ChuPickRating)
class ChuPickRatingAdmin(admin.ModelAdmin):
    fields = ('is_published', 'store', 'pick_image', 'pick_set')
    list_display = ('is_published', 'store', 'pick_image', 'pick_set')
    verbose_name = _('ChuPickRating')
    verbose_name_plural = _('ChuPickRating')


@admin.register(models.ChuPickAB)
class ChuPickABAdmin(admin.ModelAdmin):
    fields = ('is_published', 'store', 'pick_image_a',
              'pick_image_b', 'pick_set')
    list_display = ('is_published', 'store', 'pick_image_a',
                    'pick_image_b',  'pick_set')
    verbose_name = _('ChuPickAB')
    verbose_name_plural = _('ChuPickAB')


@admin.register(models.ChuPickSet)
class ChuPickSetAdmin(admin.ModelAdmin):
    inlines = (ChuPickABInline, ChuPickRatingInline)
    fields = ('is_published', 'date')
    list_display = ('is_published', 'date')
    verbose_name = _('ChuPickSet')
    verbose_name_plural = _('ChuPickSet')
