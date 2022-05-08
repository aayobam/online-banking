from datetime import date, datetime
from django.utils import timezone, timesince
from rest_framework.exceptions import ValidationError
from core.settings import FILE_UPLOAD_MAX_MEMORY_SIZE



def file_validation(value):

    if not value:
        raise ValidationError("No file selected.")

    if value.size > FILE_UPLOAD_MAX_MEMORY_SIZE:
        raise ValidationError("File shouldn't be larger than 10MB.")


def verify_date_of_birth(value):

    if not value:
        raise ValidationError("please provide your date of birth.")

    today = date.today()
    user_age = datetime.strptime(value, '%Y-%m-%d').date()
    age_days = today - user_age
    age = age_days / 365.25
    age_obj = age.days

    if user_age.year == today.year and user_age.day < today.day and user_age.month < today.month:
        return age_obj - 1

    # if user_age.year == today.year and user_age.day >= today.day and user_age.month >= today.month:
    #     return age_obj

    return age_obj
    
