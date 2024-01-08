from django.db import models
from apps.common import choices
from apps.common.models import TimeStampedModel
from apps.transactions.models import Transaction


class TransactionOtp(TimeStampedModel):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name="transactions")
    otp = models.CharField(max_length=255, default=None)
    expiry = models.DateTimeField(auto_now=True)
    description = models.CharField(choices=choices.TRANSACTION_OTP_DESCRIPTION)

    class Meta:
        verbose_name = "Transactionotp"
        verbose_name_plural="TransanctionOtps"
