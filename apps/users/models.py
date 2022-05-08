from uuid import uuid4
from django.db import models
from apps.common import choices
from django.urls import reverse
from apps.users.managers import CustomUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, MaxLengthValidator
from apps.common.models import TimeStampedModel



class CustomUser(AbstractUser, TimeStampedModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=100, unique=True)
    sex = models.CharField(default="male", choices=choices.SEX_CHOICE, max_length=10)
    role = models.CharField(default="admin", choices=choices.ROLE_CHOICE, max_length=50)
    phone_no = models.CharField(max_length=11)
    birth_date = models.DateField(blank=False, null=True)
    age = models.CharField(max_length=10, blank=True, null=True)
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(null=True, max_length=7)
    country = models.CharField(default="nigeria", choices=choices.COUNTRY_CHOICE, max_length=100)
    profile_picture = models.ImageField(upload_to="profile_images", blank=False)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    class Meta:
        ordering = ("-date_created",)
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.get_full_name()

    def get_absolute_url(self):
       return reverse("user_detail", kwargs={"user_id": self.id})