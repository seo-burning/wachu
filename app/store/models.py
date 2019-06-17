from django.db import models
from django.utils.safestring import mark_safe

from django.utils.translation import ugettext_lazy as _
from product.models import SlidingBannerSection, MainSection


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

    # Ranking Info
    current_ranking = models.IntegerField(null=True)
    current_ranking_changed = models.IntegerField(null=True)

    def __str__(self):
        return self.name


class StoreRanking(TimeStampedModel):
    class Meta(object):
        unique_together = (('date', 'store'))

    date = models.DateField(db_index=True)
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE, related_name='store_ranking_set',
        default=None)
    post_total_score = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    store_score = models.DecimalField(
        max_digits=12, decimal_places=2, default=0)
    follower = models.IntegerField(_("Instagram Follower"), null=True)
    following = models.IntegerField(_("Instagram Following"), null=True)
    post_num = models.IntegerField(_("Instagram Number of posts"), null=True)
    ranking = models.IntegerField(null=True)
    ranking_changed = models.IntegerField(null=True)

    def __str__(self):
        return ("{}, {}".format(self.date, self.store))


class StorePost(TimeStampedModel):
    is_active = models.BooleanField(default=True)
    name = models.CharField(
        _("Post Name"), max_length=255, blank=True, null=True)
    ordering_keyword = models.IntegerField(null=True, default=True)
    post_score = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE,
        related_name='store_post_set', default=None)
    post_like = models.IntegerField(_("Post Like"), null=True)
    post_comment = models.IntegerField(_("Post Comment"), null=True)
    post_taken_at_timestamp = models.IntegerField(
        _("Taken_at_timestamp"), null=True)
    post_description = models.TextField(
        _("Post Description"), blank=True, null=True)
    post_image = models.URLField(
        _("Post Image"),  blank=True, null=True, max_length=255)
    sliding_section_published = models.ForeignKey(
        SlidingBannerSection,
        related_name='sliding_banner_post_set',
        on_delete=models.SET_NULL,
        null=True,
        blank=True)
    main_section_published = models.ForeignKey(
        MainSection,
        related_name='main_banner_post_set',
        on_delete=models.SET_NULL,
        null=True,
        blank=True)

    def __str__(self):
        return mark_safe('<center><img src="{url}" \
            width="200" height="200" border="1" alt="image 1" />\
            </center><br />'.format(
            url=self.post_image,
        )
        )


CONTACT_STATUS_CHOICES = (
    ('NONE', _('연락안함')),
    ('DM', _('DM 보냄, 답장대기중')),
    ('CM', _('연락중')),
)

REACT_RATE_CHOICES = (
    (1, '매우 부정적'),
    (2, '부정적'),
    (3, '의견 없음'),
    (4, '긍정적'),
    (5, '매우 긍정적'),
)


class StoreSurvey(TimeStampedModel):
    title = models.CharField(max_length=25)
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE, related_name='store_survey',
        default=None)
    contact_status = models.CharField(
        max_length=25, choices=CONTACT_STATUS_CHOICES)
    content = models.TextField(
        _("Survey Content"), blank=True, null=True)
    reaction_rate = models.IntegerField(
        choices=REACT_RATE_CHOICES, blank=True, null=True)

    def __str__(self):
        return self.title
