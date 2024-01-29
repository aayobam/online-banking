from django.db import models
from apis.common.models import TimeStampedModel
from apis.users.models import CustomUser
from apis.common import choices


class AuthOtp(TimeStampedModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    otp = models.CharField(max_length=255, default=None)
    expiry = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=255, choices=choices.AUTH_OTP_DESCRIPTION)

    class Meta:
        verbose_name = "AuthOtp"
        verbose_name_plural = "AuthOtps"

    def __str__(self):
        return self.otp
