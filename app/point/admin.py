from django.contrib import admin

# Register your models here.
from .models import Point, PointLog


@admin.register(Point)
class PointAdmin(admin.ModelAdmin):
    pass


@admin.register(PointLog)
class PointLogAdmin(admin.ModelAdmin):
    pass
