from django.db import models
from apis.accounts.models import Account
from apis.common.models import BaseModel
from apis.common.choices import TRANSACTION_CHANNELS, TRANSACTION_TYPES


class Transaction(BaseModel):
    transaction_channel = models.CharField(max_length=50, choices=TRANSACTION_CHANNELS, default="deposit")
    transaction_type = models.CharField(max_length=50, choices=TRANSACTION_TYPES, default="debit")
    from_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="from_account")
    to_account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True, related_name="to_account")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)

    class Meta:
        ordering = ("-date_created",)
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"

    def __str__(self) -> str:
        return self.amount
