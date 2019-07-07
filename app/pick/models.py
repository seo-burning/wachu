from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import TimeStampedModel
from product.models import ProductCategory, ProductColor
from store.models import Store, Primary_Style, Secondary_Style, Age


class ChuPoint(TimeStampedModel):
    # Categorizing Fields ( updated by admin user )
    product_category = models.ManyToManyField(
        ProductCategory,
        blank=True,
        symmetrical=False,
        related_name="product_category_set")
    product_color = models.ManyToManyField(
        ProductColor,
        blank=True,
        symmetrical=False,
        related_name="product_color_set")
    primary_style = models.ForeignKey(
        Primary_Style, on_delete=models.CASCADE, null=True, blank=True)
    secondary_style = models.ForeignKey(
        Secondary_Style, on_delete=models.CASCADE, null=True, blank=True)
    age = models.ForeignKey(
        Age, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return ' {} {} {} {} {} {}'.format(''.join(
            obj.name for obj in self.product_category.all()),
            ''.join(
            obj.name for obj in self.product_color.all()),
            self.primary_style,
            self.secondary_style,
            self.age)


class ChuPickSet(TimeStampedModel):
    is_published = models.BooleanField(default=False)
    date = models.DateField(_('Section Published Date'), max_length=30)

    def __str__(self):
        return "{}".format(self.date)


class ChuPickRating(TimeStampedModel):
    title = models.CharField(max_length=255, blank=True)
    is_published = models.BooleanField(default=False)
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE,
        related_name='chu_pick_rating_set',
        default=None, blank=True)
    outlink = models.URLField(null=True, blank=True, max_length=500)
    pick_image = models.ImageField(blank=True, upload_to='pick/%Y/%m')
    chu_point = models.ForeignKey(
        ChuPoint, on_delete=models.SET_NULL, null=True, blank=True)
    pick_set = models.ForeignKey(
        ChuPickSet, on_delete=models.SET_NULL,
        related_name='chu_pick_rating_set',
        default=None, null=True, blank=True)

    def __str__(self):
        return "{}".format(self.title)


class ChuPickAB(TimeStampedModel):
    title = models.CharField(max_length=255, blank=True)
    is_published = models.BooleanField(default=False)
    store_a = models.ForeignKey(
        Store, on_delete=models.CASCADE,
        related_name='chu_pick_AB_a_set', default=None, blank=True, null=True)
    store_b = models.ForeignKey(
        Store, on_delete=models.CASCADE,
        related_name='chu_pick_AB_b_set', default=None, blank=True, null=True)
    outlink_a = models.URLField(null=True, blank=True, max_length=500)
    outlink_b = models.URLField(null=True, blank=True, max_length=500)

    pick_image_a = models.ImageField(blank=True, upload_to='pick/%Y/%m')
    pick_image_b = models.ImageField(blank=True, upload_to='pick/%Y/%m')
    chu_point_a = models.ForeignKey(
        ChuPoint, related_name='chu_point_AB_a_set',
        on_delete=models.SET_NULL, null=True, blank=True)
    chu_point_b = models.ForeignKey(
        ChuPoint, related_name='chu_point_AB_b_set',
        on_delete=models.SET_NULL, null=True, blank=True)
    pick_set = models.ForeignKey(
        ChuPickSet, on_delete=models.SET_NULL,
        related_name='chu_pick_AB_set', default=None, null=True, blank=True)

    def __str__(self):
        return "{}".format(self.title)
