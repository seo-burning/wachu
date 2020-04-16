from django.contrib import admin

from user import models


@admin.register(models.StoreReview)
class StoreReviewAdmin(admin.ModelAdmin):
    list_display = (
        '__str__', 'store', 'user'
    )


@admin.register(models.UserFavoriteProduct)
class UserFavoriteProductAdmin(admin.ModelAdmin):
    list_display = (
        'product', 'user',
    )
