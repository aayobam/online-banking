import random
from django.db import models
from django.urls import reverse
from apps.common import choices
from apps.common.custom_validator import validate_bvn
from apps.users.models import CustomUser
from apps.common.choices import ACCOUNT_TYPE
from apps.common.models import TimeStampedModel
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


class Account(TimeStampedModel):
    owner = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    account_type = models.CharField(choices=ACCOUNT_TYPE, max_length=50)
    account_no = models.CharField(max_length=10, unique=True, blank=True, null=True)
    bvn = models.CharField(max_length=10, blank=True,
                           null=True, validators=[validate_bvn])
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    daily_transfer_limit = models.DecimalField(
        default=0, max_digits=12, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0.00)])
    verification_status = models.CharField(
        default="Pending", choices=choices.ACCOUNT_VERIFICATION_STATUS, max_length=50)

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"
        unique_together = (('owner', 'account_no'),)

    def __str__(self):
        return f"{self.account_type} {self.account_no}"

    def get_absolute_url(self):
        return reverse("account_detail", kwargs={"account_id": self.id})

    def generate_account_no(self):
        account_no = random.randint(0000000000, 9999999999)
        return account_no

    def save(self, *args, **kwargs):
        if self.verification_status == "success":
            if self.account_type == "basic":
                self.account_no = self.generate_account_no()
                self.daily_transfer_limit = 1000000

            if self.account_type == "premium":
                self.account_no = self.generate_account_no()
                self.daily_transfer_limit = 25000000

        elif (self.verification_status == "pending" or self.verification_status == "failed"):
            self.daily_transfer_limit = None
            self.account_no = None
        return super().save(*args, **kwargs)
