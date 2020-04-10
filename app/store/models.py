from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe

from django.utils.translation import ugettext_lazy as _


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserFavoriteStore(TimeStampedModel):
    store = models.ForeignKey('Store', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)


class UserFavoritePost(TimeStampedModel):
    store_post = models.ForeignKey('StorePost', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)


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


class Age(models.Model):
    name = models.CharField('Age', max_length=100)

    def __str__(self):
        return self.name


STORE_TYPE = (('IF', _('-')),
              ('IF(P)', _('INS w/P')),
              ('IPFH', _('INS w/P HP')),
              ('IH', _('HP')),
              ('IS', _('Shopee')),
              ('IS(P)', _('Shopee w/P')),
              ('IFSH', _('Shopee HP')),
              ('IF(P)SH', _('INS w/P SH')),
              )


class Store(TimeStampedModel):
    class Meta:
        ordering = ('current_ranking',)
    store_type = models.CharField(
        max_length=25, choices=STORE_TYPE, default='IF', null=True)
    """Store object"""
    is_active = models.BooleanField(default=False)
    is_updated = models.BooleanField(default=False)
    is_new_post = models.BooleanField(default=False)

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
    category = models.ManyToManyField(
        Category, blank=True, symmetrical=False, related_name="categorys_set")

    primary_style = models.ForeignKey(
        Primary_Style, on_delete=models.SET_NULL, null=True, blank=True)
    secondary_style = models.ForeignKey(
        Secondary_Style, on_delete=models.SET_NULL, null=True, blank=True)
    age = models.ForeignKey(
        Age, on_delete=models.SET_NULL, null=True, blank=True)

    # Additional Information Fields ( updated by admin user )
    facebook_url = models.URLField(null=True, blank=True, max_length=500)
    facebook_id = models.CharField(max_length=255, blank=True)
    facebook_numeric_id = models.CharField(max_length=255, blank=True)
    shopee_url = models.URLField(null=True, blank=True, max_length=500)
    homepage_url = models.URLField(null=True, blank=True, max_length=500)

    # Ranking Info
    current_ranking = models.IntegerField(null=True)
    current_review_rating = models.DecimalField(
        max_digits=8, decimal_places=2, default=0)
    current_ranking_changed = models.IntegerField(null=True)

    # Favorite info
    favorite_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='UserFavoriteStore',
        related_name='favorite_stores'
    )

    # Recent Post
    recent_post_1 = models.URLField(null=True, blank=True, max_length=500)
    recent_post_2 = models.URLField(null=True, blank=True, max_length=500)
    recent_post_3 = models.URLField(null=True, blank=True, max_length=500)

    def __str__(self):
        return self.insta_id


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
    review_rating = models.DecimalField(
        max_digits=8, decimal_places=2, default=0)

    store_view_count = models.IntegerField(
        _("Store View Count of the day"), null=True)

    ranking = models.IntegerField(null=True)
    ranking_changed = models.IntegerField(null=True)

    def __str__(self):
        return ("{}, {}".format(self.date, self.store))


POST_IMAGE_TYPE = (('P', _('Picture')), ('V', _('Video')))


class StoreAddress(TimeStampedModel):
    address = models.CharField(
        max_length=250, null=True)
    store = models.ForeignKey(
        'Store', on_delete=models.CASCADE, related_name='store_address_set')
    google_map_url = models.CharField(
        max_length=250, null=True, blank=True)
    contact = models.CharField(
        max_length=250, null=True, blank=True)
    region = models.ForeignKey(
        Region, on_delete=models.CASCADE, related_name="store_address_set")
    X_axis = models.CharField(max_length=250)
    Y_axis = models.CharField(max_length=250)

    def __str__(self):
        return self.address


class StoreReview(TimeStampedModel):
    review = models.CharField(
        max_length=500, null=True)
    store = models.ForeignKey(
        'Store', on_delete=models.CASCADE, related_name='store_review_set')
    rating = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    def __str__(self):
        return self.review


class PostImage(TimeStampedModel):
    post_image_type = models.CharField(
        max_length=25, choices=POST_IMAGE_TYPE, null=True)
    source = models.CharField(_('URL Source'), max_length=1024, null=True)
    source_thumb = models.CharField(
        _('Thumb Small Link'), max_length=1024, null=True)
    store_post = models.ForeignKey(
        'StorePost', on_delete=models.CASCADE, related_name='post_image_set')

    def __str__(self):
        return self.source_thumb


POST_TYPE = (('SP', _('Single Picture')),
             ('MP', _('Multiple Picture')), ('V', _('Video')))

PRODUCT_TYPE = (('P', _('Product')),
                ('E', _('Prodcut Etc')), ('N', _('NOT Product')))


class StorePost(TimeStampedModel):
    is_active = models.BooleanField(default=True)
    is_product = models.CharField(
        max_length=25, choices=PRODUCT_TYPE, default='P')

    post_id = models.CharField(max_length=25)
    post_type = models.CharField(max_length=25, choices=POST_TYPE, null=True)
    post_url = models.URLField(null=True, blank=True, max_length=500)
    post_taken_at_timestamp = models.IntegerField(
        _("Taken_at_timestamp"), null=True)
    post_description = models.TextField(
        _("Post Description"), blank=True, null=True)

    store = models.ForeignKey(
        Store, on_delete=models.CASCADE,
        related_name='store_post_set', default=None)
    post_thumb_image = models.CharField(
        _('Post Thumb Image'), null=True, max_length=1024)

    video_source = models.CharField(
        _('URL Source'), null=True, max_length=1024)

    view_count = models.IntegerField(_("Video View Count"), null=True)
    post_like = models.IntegerField(_("Post Like"), null=True)
    post_comment = models.IntegerField(_("Post Comment"), null=True)
    post_score = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    ordering_keyword = models.IntegerField(null=True, default=True)

    # Favorite info
    favorite_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='UserFavoritePost',
        related_name='favorite_posts'
    )

    def __str__(self):
        return mark_safe('<img src="{url}" \
        width="300" height="300" border="1" />'.format(
            url=self.post_thumb_image
        ))
