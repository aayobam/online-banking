from django.db import models
from apps.common.models import TimeStampedModel
from apps.users.models import CustomUser
from apps.common import choices


class AuthOtp(TimeStampedModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    otp = models.CharField(max_length=255, default=None)
    expiry = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=255, choices=choices.AUTH_OTP_DESCRIPTION)

    class Meta:
        verbose_name = "AuthOtp"
        verbose_name_plural = "AuthOtps"
