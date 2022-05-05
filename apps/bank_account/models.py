import random
from uuid import uuid4
from django.db import models
from apps.common import choices
from django.urls import reverse
from apps.users.models import CustomUser
from apps.account_type.models import AccountType
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _
from apps.common.custom_validator import file_validation



class BankAccount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    owner = models.OneToOneField(CustomUser, related_name='account', on_delete=models.CASCADE)
    account_type = models.ForeignKey(AccountType, related_name='accounts', on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    account_no = models.CharField(max_length=10, unique=True, blank=True, validators=[MinLengthValidator(10)])
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    transfer_limit = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    identity_verification = models.FileField(help_text=_("upload a legal document that truely identifies you for verification"), validators=[file_validation])
    verification_status = models.CharField(default="pending", choices=choices.BANK_VERIFICATION_STATUS, max_length=50)
    initial_deposit_date = models.DateField(null=True, blank=True)
    date_opened = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "bank account"
        verbose_name_plural = "bank accounts"

    def __str__(self):
        return f"{self.account_type} {self.account_no}"

    def get_absolute_url(self):
       return reverse("account_detail", kwargs={"account_id": self.id})

    
    def generate_account_number():
        account_number = random.randint(0000000000, 9999999999)
        return account_number

    def save(self, *args, **kwargs):
        if self.verification_status == "Pending" or self.verification_status == "Failed":
            self.account_no = "1234567890"
        self.account_no = self.generate_account_number()
        return super().save(*args, **kwargs)
            
