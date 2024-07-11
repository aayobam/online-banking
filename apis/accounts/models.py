from django.db import models
from django.urls import reverse
from apis.common import enums
from apis.users.models import CustomUser
from apis.common.enums import ACCOUNT_TYPE
from apis.common.models import BaseModel
from django.core.validators import MinValueValidator


class Account(BaseModel):
    owner = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    account_type = models.CharField(choices=ACCOUNT_TYPE, max_length=50)
    account_no = models.CharField(max_length=10, unique=True, blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    daily_transfer_limit = models.DecimalField(default=0, max_digits=12, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0.00)])
    verification_status = models.CharField(default="Pending", choices=enums.ACCOUNT_VERIFICATION_STATUS, max_length=50)

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"
        unique_together = (('owner', 'account_no'),)

    def __str__(self):
        return f"{self.account_type} {self.account_no}"

    def get_absolute_url(self):
        return reverse("account_detail", kwargs={"account_id": self.id})
