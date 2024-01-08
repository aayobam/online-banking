from django.db import models

from apps.accounts.models import Account
from apps.common.models import TimeStampedModel


class Loan(TimeStampedModel):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    term = models.BigIntegerField(help_text="Number of months for the loan to be paid off")
    collateral = models.FileField(upload_to="loan/collateral")

    def __str__(self):
        return self.account
