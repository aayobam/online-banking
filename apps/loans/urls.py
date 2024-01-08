from django.urls import path

from .views import create_user

urlpatterns = [path("register/", create_user, name="register")]
