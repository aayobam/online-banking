import random
from uuid import uuid4
from django.db import models
from apps.common import choices
from django.urls import reverse
from apps.users.models import CustomUser
from apps.common.models import TimeStampedModel
from apps.account_type.models import AccountType
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _
from apps.common.custom_validator import file_validation



class BankAccount(TimeStampedModel):
    owner = models.OneToOneField(CustomUser, related_name='account', on_delete=models.CASCADE)
    account_type = models.ForeignKey(AccountType, related_name='accounts', on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    account_no = models.CharField(max_length=10, unique=True, blank=True, validators=[MinLengthValidator(10)])
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    transfer_limit = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    identity_verification = models.FileField(help_text=_("upload a legal document that truely identifies you for verification"), validators=[file_validation])
    verification_status = models.CharField(default="pending", choices=choices.BANK_VERIFICATION_STATUS, max_length=50)

    class Meta:
        verbose_name = "Bank account"
        verbose_name_plural = "Bank accounts"

    def __str__(self):
        return f"{self.account_type} {self.account_no}"

    def get_absolute_url(self):
       return reverse("account_detail", kwargs={"account_id": self.id})
