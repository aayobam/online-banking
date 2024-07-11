import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from apis.common import enums
from apis.common.custom_validator import file_validator
from apis.common.models import BaseModel
from apis.users.managers import CustomUserManager
from django.utils.crypto import get_random_string
from core import settings


class CustomUser(AbstractUser, BaseModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    gender = models.CharField(default="male", choices=enums.GENDER, max_length=10)
    role = models.CharField(default="admin", choices=enums.ROLE, max_length=50)
    phone_no = models.CharField(max_length=11)
    date_of_birth = models.DateField(blank=True, null=True)
    age = models.CharField(max_length=4, blank=True, null=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(default="nigeria", choices=enums.COUNTRY, max_length=100)
    profile_picture = models.ImageField("profile_images", validators=[file_validator], blank=True, null=True)

    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        ordering = ("-date_created",)
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.get_full_name()

    def get_absolute_url(self):
        return reverse("user_detail", kwargs={"id": self.id})
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_user_address(self):
        return f"{self.address.capitalize()}, {self.city.capitalize()}, {self.lga.capitalize()} {self.state.capitalize()}, {self.country.capitalize()}."
    

class Token(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, null=True)
    token_type = models.CharField(max_length=100, choices=enums.TOKEN_TYPE, default="ACCOUNT_VERIFICATION")

    def __str__(self):
        return f"{str(self.user)} {self.token}"

    def is_valid(self):
        lifespan_in_seconds = float(settings.TOKEN_LIFESPAN * 60 * 60)
        now = datetime.now(datetime.timezone.utc)
        time_diff = now - self.date_updated
        time_diff = time_diff.total_seconds()
        if time_diff >= lifespan_in_seconds:
            return False
        return True

    def verify_user(self):
        self.user.is_active = True
        self.user.save()

    def generate(self):
        if not self.token:
            self.token = get_random_string(120)
            self.save()

    def reset_user_password(self, password):
        self.user.set_password(password)
        self.user.save()
