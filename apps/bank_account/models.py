import random
from django.db import models
from apps.common import choices
from django.urls import reverse
from apps.users.models import CustomUser
from apps.common.models import TimeStampedModel
from apps.account_type.models import AccountType
from django.utils.translation import gettext_lazy as _
from apps.common.custom_validator import file_validation




class BankAccount(TimeStampedModel):
    owner = models.OneToOneField(CustomUser, related_name='account', on_delete=models.CASCADE)
    account_type = models.ForeignKey(AccountType, related_name='accounts', on_delete=models.CASCADE)
    account_no = models.CharField(max_length=10, unique=True, blank=True, null=True)
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    transfer_limit = models.DecimalField(default=0, max_digits=12, decimal_places=2, null=True, blank=True)
    identity_verification = models.FileField(help_text=_("upload a legal document that truely identifies you for verification"), unique=True, validators=[file_validation])
    verification_status = models.CharField(default="Pending", choices=choices.BANK_VERIFICATION_STATUS, max_length=50)

    class Meta:
        verbose_name = "Bank account"
        verbose_name_plural = "Bank accounts"

    def __str__(self):
        return f"{self.account_type} {self.account_no}"

    def get_absolute_url(self):
       return reverse("account_detail", kwargs={"account_id": self.id})

    def generate_account_no(self):
        account_no = random.randint(0000000000,9999999999)
        return account_no

    def verify_account_status(self, value):
        if not value == "success":
            self.transfer_limit = None
            self.account_no = None
        
        if self.account_type == "savings":
            self.transfer_limit = 5000000.00
            return self.transfer_limit

        elif self.account_type == "current":
            self.transfer_limit = 1000000.00
            self.account_no = self.generate_account_no()

    def save(self, *args, **kwargs):
        selected_file = self.identity_verification
        file_validation(value=selected_file)
        self.verify_account_status(value=self.verification_status)
        return super().save(*args, **kwargs)