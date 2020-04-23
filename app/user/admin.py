from django.contrib import admin
from user import models


class ReviewImageInline(admin.StackedInline):
    model = models.ReviewImage
    extra = 0


@admin.register(models.ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    inlines = [ReviewImageInline, ]
    list_display = (
        '__str__', 'store', 'user', 'product'
    )


@admin.register(models.UserFavoriteProduct)
class UserFavoriteProductAdmin(admin.ModelAdmin):
    list_display = (
        'product', 'user',
    )


@admin.register(models.ReviewImage)
class ReviewImageAdmin(admin.ModelAdmin):
    pass
