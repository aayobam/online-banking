import pytest
from django.urls import resolve
from rest_framework.reverse import reverse
from apps.account_type import views



@pytest.mark.django_db
def test_create_account_type_url_is_resolved():
    url = reverse("create_type")
    assert resolve(url).func.view_class == views.CreateAccountTypeApiView


@pytest.mark.django_db
def test_account_type_list_url_is_resolved():
    url = reverse("list_type")
    assert resolve(url).func.view_class == views.AccountTypeListApiView


@pytest.mark.django_db
def test_account_type_detail_url_is_resolved(account_type):
    url = reverse("detail_type", kwargs={"type_id":account_type.id})
    assert resolve(url).func.view_class == views.AccountTypeDetailApiView


@pytest.mark.django_db
def test_account_type_update_url_is_resolved(account_type):
    url = reverse("update_type", kwargs={"type_id": account_type.id})
    assert resolve(url).func.view_class == views.AccountTypeUpdateApiView


@pytest.mark.django_db
def test_account_type_delete_url_is_resolved(account_type):
    url = reverse("delete_type", kwargs={"type_id": account_type.id})
    assert resolve(url).func.view_class == views.AccountTypeDeleteApiView