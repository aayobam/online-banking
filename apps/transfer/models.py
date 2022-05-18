from uuid import uuid4
from apps.common import choices
from django.db import models
from apps.common.models import TimeStampedModel
from apps.bank_account.models import BankAccount



class Transfer(TimeStampedModel):
    from_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    receiver_account = models.CharField(max_length=10)
    receiver_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=choices.BANK_VERIFICATION_STATUS)

    def __str__(self):
       return f"{self.amount} to {self.receiver_account} - {self.receiver_name}"
   