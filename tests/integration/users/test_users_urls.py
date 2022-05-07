import pytest
from django.urls import resolve
from rest_framework.reverse import reverse
from apps.users.views import (
    RegisterUserApiView,
    UserListApiView,
    UserDetailApiView,
    UserUpdateApiView,
    UserDeleteApiView,
    CustomTokenObtainPairView
)



@pytest.mark.django_db
def test_create_user_url_is_resolved():
    url = reverse("create_user")
    assert resolve(url).func.view_class == RegisterUserApiView


@pytest.mark.django_db
def test_user_list_url_is_resolved():
    url = reverse("user_list")
    assert resolve(url).func.view_class == UserListApiView


@pytest.mark.django_db
def test_user_detail_url_is_resolved(regularuser):
    url = reverse("user_detail", kwargs={"user_id": regularuser.id})
    assert resolve(url).func.view_class == UserDetailApiView


@pytest.mark.django_db
def test_update_user_detail_url_is_resolved(regularuser):
    url = reverse("update_user", kwargs={"user_id": regularuser.id})
    assert resolve(url).func.view_class == UserUpdateApiView


@pytest.mark.django_db
def test_delete_user_url_is_resolved(regularuser):
    url = reverse("delete_user", kwargs={"user_id": regularuser.id})
    assert resolve(url).func.view_class == UserDeleteApiView


@pytest.mark.django_db
def test_access_token_for_user_url_is_resolved():
    url = reverse("access_token")
    assert resolve(url).func.view_class == CustomTokenObtainPairView