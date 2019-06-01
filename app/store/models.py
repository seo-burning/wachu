from django.db import models
from django.utils.safestring import mark_safe

from django.utils.translation import ugettext_lazy as _


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Region(models.Model):
    name = models.CharField('Region Name', max_length=100)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField('Category Name', max_length=100)

    def __str__(self):
        return self.name


class Primary_Style(models.Model):
    name = models.CharField('Primary Style', max_length=100)

    def __str__(self):
        return self.name


class Secondary_Style(models.Model):
    name = models.CharField('Secondary Style', max_length=100)

    def __str__(self):
        return self.name


class Tpo(models.Model):
    name = models.CharField('Tpo', max_length=100)

    def __str__(self):
        return self.name


class Age(models.Model):
    name = models.CharField('Age', max_length=100)

    def __str__(self):
        return self.name


class Store(TimeStampedModel):
    """Store object"""
    is_active = models.BooleanField(default=False)
    is_updated = models.BooleanField(default=False)

    insta_id = models.CharField(_("Instagram ID"), max_length=255)
    insta_url = models.URLField(
        _("Instagram URL"), null=True, blank=True, max_length=500)
    profile_image = models.URLField(
        _("Instagram Profile Image"), null=True, blank=True, max_length=500)
    name = models.CharField(_("Instagram Name"), max_length=255)

    store_score = models.DecimalField(
        max_digits=5, decimal_places=2, default=0)
    last_score = models.DecimalField(
        max_digits=5, decimal_places=2, default=0)
    ranking_changed = models.IntegerField(null=True)
    ranking = models.IntegerField(null=True)

    # Cannot be changed in Admin site ( updated by crwaler )
    follower = models.IntegerField(_("Instagram Follower"), null=True)
    following = models.IntegerField(_("Instagram Following"), null=True)
    post_num = models.IntegerField(_("Instagram Number of posts"), null=True)
    description = models.TextField(
        _("Instagram Description"), blank=True, null=True)
    phone = models.CharField(max_length=255)
    email = models.CharField(max_length=255)

    # Categorizing Fields ( updated by admin user )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True)
    region = models.ManyToManyField(
        Region, blank=True, symmetrical=False, related_name="regions_set")

    primary_style = models.ForeignKey(
        Primary_Style, on_delete=models.CASCADE, null=True, blank=True)
    secondary_style = models.ForeignKey(
        Secondary_Style, on_delete=models.CASCADE, null=True, blank=True)
    tpo = models.ForeignKey(
        Tpo, on_delete=models.CASCADE, null=True, blank=True)
    age = models.ForeignKey(
        Age, on_delete=models.CASCADE, null=True, blank=True)

    # Additional Information Fields ( updated by admin user )
    facebook_url = models.URLField(null=True, blank=True, max_length=500)
    shopee_url = models.URLField(null=True, blank=True, max_length=500)

    def __str__(self):
        return self.name


class StorePost(TimeStampedModel):
    is_active = models.BooleanField(default=True)
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE, related_name='store', default=None)
    post_like = models.IntegerField(_("Post Like"), null=True)
    post_comment = models.IntegerField(_("Post Comment"), null=True)
    post_taken_at_timestamp = models.IntegerField(
        _("Taken_at_timestamp"), null=True)
    post_description = models.TextField(
        _("Post Description"), blank=True, null=True)
    post_image = models.URLField(
        _("Post Image"),  blank=True, null=True, max_length=255)

    def __str__(self):
        return mark_safe('<center><img src="{url}" \
            width="200" height="200" border="1" alt="image 1" />\
            </center><br />'.format(
            url=self.post_image,
        )
        )
