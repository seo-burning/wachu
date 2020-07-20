from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,\
    PermissionsMixin

import csv
from django.http import HttpResponse
from user.models import UserFavoriteProduct, UserProductView, UserStoreView
from product.models import Product, ProductStyle
from store.models import Store
from .abstract_models import TimeStampedModel, DispalyNameModel


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(
            meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field)
                             for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError("User must have an email address.")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """creates and saves new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class Region(TimeStampedModel, DispalyNameModel):
    def __str__(self):
        return self.display_name


GENDER_CHOICES_FIELD = [('female', 'female'), ('male', 'male'), ]
INFORMATION_CHOICES_FIELD = [('new', 'new'), ('basic', 'basic'), ('pick', 'pick'), ('done', 'done'), ('pass', 'pass')]


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    information_status = models.CharField(max_length=100, choices=INFORMATION_CHOICES_FIELD, default='new')

    age = models.IntegerField(null=True)
    gender = models.CharField(
        max_length=100, choices=GENDER_CHOICES_FIELD, blank=True, null=True)
    region = models.ForeignKey(Region,
                               on_delete=models.SET_NULL, blank=True, null=True)

    primary_style = models.ForeignKey(
        ProductStyle, on_delete=models.SET_NULL,
        related_name='user_on_primary_style',
        null=True, blank=True)
    secondary_style = models.ForeignKey(
        ProductStyle, on_delete=models.SET_NULL,
        related_name='user_on_secondary_style',
        null=True, blank=True)

    height = models.IntegerField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    profile_image = models.ImageField(
        blank=True, upload_to='profile/%Y/%m')
    favorite_products = models.ManyToManyField(
        Product,
        through=UserFavoriteProduct,
        related_name='favorite_users'
    )

    view_products = models.ManyToManyField(
        Product,
        through=UserProductView,
        related_name='view_users'
    )

    view_stores = models.ManyToManyField(
        Store,
        through=UserStoreView,
        related_name='view_users'
    )
    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.name


class UserPushToken(TimeStampedModel):
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    push_token = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.push_token


class Notice(TimeStampedModel):
    title = models.CharField(max_length=50, null=True)
    content = models.TextField(blank=True)
    date = models.DateField(null=True)

    def __str__(self):
        return self.title
