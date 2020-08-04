from django.contrib import admin
from django.utils.translation import gettext as _

from pick import models


class PickInline(admin.StackedInline):
    model = models.Pick
    max_num = 50
    extra = 0
    fields = ('image', 'image_outlink', 'outlink', 'product_category',
              'product_sub_category', 'product_color', 'primary_style', 'secondary_style', 'age', 'product')
    raw_id_fields = ('product',)

    verbose_name = _('PickAB')
    verbose_name_plural = _('PickAB')


@admin.register(models.Pick)
class PickAdmin(admin.ModelAdmin):
    list_display = ('is_active', '__str__', 'ab_pick_set', 'product',
                    'primary_style', 'secondary_style', 'age')
    raw_id_fields = ('product',)


@admin.register(models.PickAB)
class PickABAdmin(admin.ModelAdmin):
    inlines = [PickInline, ]
    list_display = ('is_published', 'title', 'pick_num')

    def pick_num(self, obj):
        pick_num = obj.picks.all().count()
        return pick_num


@admin.register(models.PickABResult)
class PickABResultAdmin(admin.ModelAdmin):
    raw_id_fields = ('pick_AB', 'pick_A', 'pick_B')
