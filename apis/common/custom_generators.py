import random
from core import settings
from datetime import datetime, timedelta
from apis.authotps.models import AuthOtp


async def password_reset_otp_generator(user):
    code = None

    while True:
        code = random.randint(000000, 999999)
        if not await AuthOtp.objects.select_related("user").filter(code=code, user__email=user.email).exists():
            break
        
    auth_otp_object = {
        "user": user,
        "otp": code,
        "expiry": datetime.now() + timedelta(minutes=10),
        "description": "user account verification."
    }

    auth_object = await AuthOtp.objects.create(**auth_otp_object)
    auth_object.save()
    return auth_otp_object


async def account_verification_otp_generator(user):

    code = None

    while True:
        code = random.randint(000000, 999999)
        if not await AuthOtp.objects.select_related("user").filter(code=code, user__email=user.email).exists():
            break

    auth_otp_object = {
        "user": user,
        "otp": code,
        "expiry": datetime.now() + timedelta(minutes=10),
        "description": "user account verification."
    }

    auth_object = await AuthOtp.objects.create(**auth_otp_object)
    auth_object.save()
    auth_otp_object.otp = code
    return auth_otp_object
