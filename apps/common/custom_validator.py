import mimetypes
from datetime import date, datetime
from django.core.files.storage import FileSystemStorage
from rest_framework.exceptions import ValidationError
from core.settings import base


def file_validation(file):

    file_types = ["image/png", "image/jpeg", "image/jpg"]

    if not file:
        raise ValidationError("No file selected.")

    if file.size > base.FILE_UPLOAD_MAX_MEMORY_SIZE:
        raise ValidationError("File shouldn't be larger than 10MB.")

    fs = FileSystemStorage()
    filename = fs.save(file.name, file)
    file_type = mimetypes.guess_type(filename)[0]
    if file_type not in file_types:
        raise ValidationError(
            "Invalid file, picture must be in clear png, jpeg \
            or jpg format, please try again..."
        )
    return file_type


def verify_date_of_birth(date_of_birth):
    if not date_of_birth:
        raise ValidationError("please provide your date of birth.")
    today = date.today()
    user_age = datetime.strptime(date_of_birth, "%Y-%m-%d").date()
    age_days = today - user_age
    age = age_days / 365.25
    age_obj = age.days

    if (user_age.year == today.year and user_age.day == today.day and user_age.month == today.month):
        return age_obj - 1
    return age_obj


def validate_bvn(bvn):
    if len(bvn) < 11 or len(bvn) > 11:
        raise ValidationError("value can not be higher or less than 11")
    elif type(bvn) != int:
        raise ValueError("value can only be a whole number")
    return bvn
