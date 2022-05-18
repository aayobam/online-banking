
from django.db import models
from apps.common.models import TimeStampedModel
from apps.users.models import CustomUser
from apps.bank_account.models import BankAccount
from django.core.validators import MinValueValidator
from apps.common.choices import TRANSACTION_TYPES_CHOICE





class Transaction(TimeStampedModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=50, default="Deposit", choices=TRANSACTION_TYPES_CHOICE)
    amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(100)])
    comment = models.TextField()

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = "Transactions"