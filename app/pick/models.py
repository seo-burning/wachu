from django.db import models
import sys
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

from django.utils.safestring import mark_safe

from django.utils.translation import ugettext_lazy as _

from core.models import TimeStampedModel, User
from product.models import ProductCategory, ProductColor, ProductStyle, Product
from store.models import Age
from utils.helper.image_processing import create_presigned_url


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
        User, on_delete=models.CASCADE, related_name='pickAB_results', default=None)
    pick_AB = models.ForeignKey(
        PickAB,
        on_delete=models.CASCADE,
        default=None)
    selection = models.CharField(max_length=2, choices=(
        (0, 0), (1, 1), (2, 2)), null=True)

    def __str__(self):
        return "{} - {} => {}".format(self.user, self.pick_AB, self.selection)


class PickPointModel(models.Model):
    class Meta:
        abstract = True
    # Categorizing Fields ( updated by admin user )
    product_category = models.ManyToManyField(
        ProductCategory,
        blank=True,
        symmetrical=False)
    product_color = models.ManyToManyField(
        ProductColor,
        blank=True,
        symmetrical=False)
    primary_style = models.ForeignKey(
        ProductStyle, on_delete=models.SET_NULL,
        related_name='picks_on_primary_style',
        null=True, blank=True)
    secondary_style = models.ForeignKey(
        ProductStyle, on_delete=models.SET_NULL,
        related_name='picks_on_secondary_style',
        null=True, blank=True)
    age = models.ForeignKey(
        Age, on_delete=models.SET_NULL, null=True, blank=True)


class Pick(TimeStampedModel, PickPointModel):
    class Meta:
        verbose_name = _('Pick / 픽')
        verbose_name_plural = _('Pick / 픽')

    image = models.ImageField(blank=True, upload_to='pick/%Y/%m')
    outlink = models.URLField(null=True, blank=True, max_length=500)
    product = models.ForeignKey(Product, blank=True, null=True,
                                on_delete=models.SET_NULL)
    ab_pick_set = models.ForeignKey(
        PickAB, related_name='picks', on_delete=models.SET_NULL,
        default=None, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.image = self.compressImage(self.image)
        super(Pick, self).save(*args, **kwargs)

    def compressImage(self, image):
        imageTemproary = Image.open(image)
        if imageTemproary.mode != 'RGB':
            imageTemproary = imageTemproary.convert('RGB')
        if image.width > 500:
            compress_ratio = image.width / 500
            imageTemproary = imageTemproary.resize((500, int(image.height/compress_ratio)))
        outputIoStream = BytesIO()
        imageTemproary.save(outputIoStream, format='JPEG', quality=95)
        outputIoStream.seek(0)
        uploadedImage = InMemoryUploadedFile(outputIoStream, 'ImageField',
                                             "%s.jpg" % image.name.split('.')[0],
                                             'image/jpeg', sys.getsizeof(outputIoStream), None)
        return uploadedImage

    def __str__(self):
        if self.image:
            thumb_image = create_presigned_url('wachu', 'media/'+str(self.image), expiration=3000)
        else:
            thumb_image = "http://dabivn.comm"

        return mark_safe('<img src="{url}" \
        width="250" height="250" border="1" />'.format(
            url=thumb_image
        ))
