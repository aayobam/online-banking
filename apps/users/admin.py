from .models import CustomUser
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.users.forms import CustomUserChangeForm, CustomUserCreationForm


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
                    "username",
                    "phone_no",
                    "birth_date",
                    "age",
                    "password1",
                    "password2",
                    "role",
                    "address",
                    "city",
                    "state",
                    "zipcode",
                    "country",
                    "profile_picture",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "user_permissions",
                    "date_joined",
                    "date_created",
                    "date_updated"
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
                    "username",
                    "phone_no",
                    "birth_date",
                    "age",
                    "role",
                    "address",
                    "city",
                    "state",
                    "zipcode",
                    "country",
                    "profile_picture",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "password",
                    "user_permissions",
                    "date_joined",
                    "date_created",
                    "date_updated"
                ),
            },
        ),
    )
    
    list_display = ("id", 'username', 'email', 'first_name', 'last_name', 'birth_date', 'age',  'is_active', 'is_superuser')
    readonly_fields = ("id", 'date_joined', 'date_created', 'date_updated')