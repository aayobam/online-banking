from django.db import models
from apis.common.models import BaseModel
from apis.users.models import CustomUser
from apis.common import enums


class AuthOtp(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    otp = models.CharField(max_length=255, default=None)
    expiry = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=255, choices=enums.AUTH_OTP_DESCRIPTION)

    class Meta:
        verbose_name = "Verification Otp"
        verbose_name_plural = "Verification Otps"

    def __str__(self):
        return self.otp
