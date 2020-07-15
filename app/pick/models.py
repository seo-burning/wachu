from django.db import models
from django.utils.translation import ugettext_lazy as _

from core.models import TimeStampedModel, User
from product.models import ProductCategory, ProductColor
from store.models import Store, Primary_Style, Secondary_Style, Age


class PickPointModel(models.Model):
    class Meta:
        abstract = True
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


class PickAB(TimeStampedModel):
    class Meta:
        verbose_name = _('Pick AB / AB 픽')
        verbose_name_plural = _('Pick AB / AB 픽')
    title = models.CharField(max_length=255, blank=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return "{}".format(self.title)


class PickABResult(TimeStampedModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, default=None)
    pick_AB = models.ForeignKey(
        PickAB,
        on_delete=models.CASCADE,
        default=None)
    selection = models.CharField(max_length=2, choices=(
        ('A', 'A'), ('B', 'B')), null=True)

    def __str__(self):
        return "{} - rating : {}".format(self.user, self.pick_rating)


class Pick(TimeStampedModel, PickPointModel):
    class Meta:
        verbose_name = _('Pick / 픽')
        verbose_name_plural = _('Pick / 픽')

    image = models.ImageField(blank=True, upload_to='pick/%Y/%m')
    outlink = models.URLField(null=True, blank=True, max_length=500)
    ab_pick_set = models.ForeignKey(
        PickAB, related_name='picks', on_delete=models.SET_NULL,
        default=None, null=True, blank=True)
