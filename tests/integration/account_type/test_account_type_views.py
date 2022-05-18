from collections import OrderedDict
import pytest
from apps.account_type.models import AccountType
from rest_framework.reverse import reverse



@pytest.mark.django_db
def test_create_account_type_view(account_type, authenticated_superuser):
    assert len(AccountType.objects.all()) == 1
    payload = {
        "name": "savings",
        "account_limit": 30000000.00,
        "maximum_daily_withdrawal_amount": 5000000.00
    }
    url = reverse("create_type")
    response = authenticated_superuser.post(url, data=payload)
    assert response.status_code == 201
    assert len(AccountType.objects.all()) == 2


@pytest.mark.django_db
def test_create_account_type_no_name_view(account_type, authenticated_superuser):
    assert len(AccountType.objects.all()) == 1
    payload = {
        "account_limit": 30000000.00,
        "maximum_daily_withdrawal_amount": 5000000.00
    }
    url = reverse("create_type")
    response = authenticated_superuser.post(url, data=payload)
    assert response.status_code == 400
    assert len(AccountType.objects.all()) == 1
    assert response.json()["name"] == ["This field is required."]


@pytest.mark.django_db
def test_create_account_type_account_limit_length_longer_than_12_digits_view(account_type, authenticated_superuser):
    assert len(AccountType.objects.all()) == 1
    payload = {
        "name": "savings",
        "account_limit": 300000000000.00,
        "maximum_daily_withdrawal_amount": 5000000.00
    }
    url = reverse("create_type")
    response = authenticated_superuser.post(url, data=payload)
    assert response.status_code == 400
    assert len(AccountType.objects.all()) == 1
    assert response.data["account_limit"] == ["Ensure that there are no more than 12 digits in total."]


@pytest.mark.django_db
def test_superuser_can_view_account_type_list_view(account_type, authenticated_superuser):
    assert len(AccountType.objects.all()) == 1
    url = reverse("list_type")
    response = authenticated_superuser.get(url)
    assert response.status_code == 200
    assert len(AccountType.objects.all()) == 1
    assert type(response.data) == OrderedDict


@pytest.mark.django_db
def test_superuser_can_view_account_type_details_view(account_type, authenticated_superuser):
    assert len(AccountType.objects.all()) == 1
    url = reverse("detail_type", kwargs={"type_id": account_type.id})
    response = authenticated_superuser.get(url)
    assert response.status_code == 200
    assert len(AccountType.objects.all()) == 1
    assert response.data["name"] == "savings"


@pytest.mark.django_db
def test_superuser_can_update_account_type_view(account_type, authenticated_superuser):
    assert len(AccountType.objects.all()) == 1
    payload = {
        "name": "saving",
        "account_limit": 30000000.00,
        "maximum_daily_withdrawal_amount": 5000000.00
    }
    url = reverse("update_type", kwargs={"type_id": account_type.id})
    response = authenticated_superuser.patch(url, data=payload)
    assert response.status_code == 200
    assert len(AccountType.objects.all()) == 1
    assert response.data["name"] == "saving"


@pytest.mark.django_db
def test_superuser_can_delete_account_type_view(account_type, authenticated_superuser):
    assert len(AccountType.objects.all()) == 1
    url = reverse("delete_type", kwargs={"type_id": account_type.id})
    response = authenticated_superuser.delete(url)
    assert response.status_code == 204
    assert len(AccountType.objects.all()) == 0


@pytest.mark.django_db
def test_regularuser_cannot_create_account_type_view(account_type, authenticated_regularuser):
    assert len(AccountType.objects.all()) == 1
    payload = {
        "name": "savings",
        "account_limit": 30000000.00,
        "maximum_daily_withdrawal_amount": 5000000.00
    }
    url = reverse("create_type")
    response = authenticated_regularuser.post(url, data=payload)
    assert response.status_code == 403
    assert len(AccountType.objects.all()) == 1
    assert response.data["detail"] == "You do not have permission to perform this action." 


@pytest.mark.django_db
def test_regularuser_cannot_fetch_account_type_list_view(account_type, authenticated_regularuser):
    assert len(AccountType.objects.all()) == 1
    url = reverse("list_type")
    response = authenticated_regularuser.get(url)
    assert response.status_code == 403
    assert len(AccountType.objects.all()) == 1
    assert response.data["detail"] == "You do not have permission to perform this action."



@pytest.mark.django_db
def test_regularuser_cannot_fetch_account_type_detail_view(account_type, authenticated_regularuser):
    assert len(AccountType.objects.all()) == 1
    url = reverse("detail_type", kwargs={"type_id": account_type.id})
    response = authenticated_regularuser.get(url)
    assert response.status_code == 403
    assert len(AccountType.objects.all()) == 1
    assert response.data["detail"] == "You do not have permission to perform this action."


@pytest.mark.django_db
def test_regularuser_cannot_update_account_type_view( account_type, authenticated_regularuser):
    assert len(AccountType.objects.all()) == 1
    payload = {
        "name": "saving",
        "account_limit": 30000000.00,
        "maximum_daily_withdrawal_amount": 5000000.00
    }
    url = reverse("update_type", kwargs={"type_id": account_type.id})
    response = authenticated_regularuser.put(url, data=payload)
    assert response.status_code == 403
    assert len(AccountType.objects.all()) == 1
    assert response.data["detail"] == "You do not have permission to perform this action." 


@pytest.mark.django_db
def test_regularuser_cannot_d_account_type_detail_view(account_type, authenticated_regularuser):
    assert len(AccountType.objects.all()) == 1
    url = reverse("delete_type", kwargs={"type_id": account_type.id})
    response = authenticated_regularuser.get(url)
    assert response.status_code == 403
    assert len(AccountType.objects.all()) == 1
    assert response.data["detail"] == "You do not have permission to perform this action."