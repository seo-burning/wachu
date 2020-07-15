from django.contrib import admin
from django.utils.translation import gettext as _

from pick import models


@admin.register(models.Pick)
class PickAdmin(admin.ModelAdmin):
    pass


@admin.register(models.PickABResult)
class PickABResultAdmin(admin.ModelAdmin):
    pass


class PickInline(admin.StackedInline):
    model = models.Pick
    max_num = 50
    extra = 0
    fields = ('image', 'outlink', 'product_category', 'product_color', 'primary_style', 'secondary_style', 'age')
    verbose_name = _('PickAB')
    verbose_name_plural = _('PickAB')


@admin.register(models.PickAB)
class PickABAdmin(admin.ModelAdmin):
    list_display = ('is_published', 'title', )
    verbose_name = _('PickAB')
    verbose_name_plural = _('PickAB')
