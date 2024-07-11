from django.db import models
from apis.common import enums
from apis.common.models import BaseModel
from apis.transactions.models import Transaction


class TransactionOtp(BaseModel):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name="transactions")
    otp = models.CharField(max_length=255, default=None)
    expiry = models.DateTimeField(auto_now=True)
    description = models.CharField(choices=enums.TRANSACTION_OTP_DESCRIPTION)

    class Meta:
        verbose_name = "Transactionotp"
        verbose_name_plural="TransanctionOtps"
