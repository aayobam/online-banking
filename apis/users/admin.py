from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apis.users.forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "gender"
                    "phone_no",
                    "date_of_birth",
                    "age",
                    "password1",
                    "password2",
                    "role",
                    "address",
                    "city",
                    "state",
                    "country",
                    "profile_picture",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "user_permissions",
                    "groups",
                    "date_joined",
                    "date_created",
                    "date_updated",
                ),
            },
        ),
    )
    form = CustomUserChangeForm
    fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "id",
                    "first_name",
                    "last_name",
                    "email",
                    "gender",
                    "phone_no",
                    "date_of_birth",
                    "age",
                    "role",
                    "address",
                    "city",
                    "state",
                    "country",
                    "profile_picture",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "password",
                    "user_permissions",
                    "groups",
                    "date_joined",
                    "date_created",
                    "date_updated",
                ),
            },
        ),
    )

    list_display = (
        "email",
        "first_name",
        "last_name",
        "gender",
        "date_of_birth",
        "age",
        "is_active",
        "is_staff",
        "is_superuser",
    )
    readonly_fields = ("id", "age", "date_joined", "date_created", "date_updated")
