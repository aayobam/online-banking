from uuid import uuid4
from django.db import models
from apps.common import choices
from django.urls import reverse
from apps.users.managers import CustomUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator



class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=100, unique=True)
    sex = models.CharField(default="male", choices=choices.SEX_CHOICE, max_length=10)
    role = models.CharField(default="admin", choices=choices.ROLE_CHOICE, max_length=50)
    phone_no = models.CharField(max_length=11)
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(null=True, max_length=7, validators=[MinLengthValidator(5)])
    country = models.CharField(default="nigeria", choices=choices.COUNTRY_CHOICE, max_length=100)
    profile_picture = models.ImageField(upload_to="profile_images", blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    class Meta:
        ordering = ("-date_created",)
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return self.get_full_name()

    def get_absolute_url(self):
       return reverse("user-detail", kwargs={"user_id": self.id})