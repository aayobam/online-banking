import mimetypes
from datetime import date, datetime
from rest_framework.exceptions import ValidationError
from core.settings import FILE_UPLOAD_MAX_MEMORY_SIZE
from django.core.files.storage import FileSystemStorage


def file_validation(value):
    file_types = ["image/png", "image/jpeg", "image/jpg", "application/pdf"]

    if not value:
        raise ValidationError("No file selected.")

    if value.size > FILE_UPLOAD_MAX_MEMORY_SIZE:
        raise ValidationError("File shouldn't be larger than 10MB.")

    fs = FileSystemStorage()
    filename = fs.save(value.name, value)
    file_type = mimetypes.guess_type(filename)[0]
    if file_type not in file_types:
        raise ValidationError("Invalid file, please upload a clearer image or pdf file that shows your full name, picture and date of birth.")


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
    return age_obj

    
