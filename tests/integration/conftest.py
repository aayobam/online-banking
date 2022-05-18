import pytest
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from apps.users.models import CustomUser
from apps.account_type.models import AccountType



@pytest.fixture(scope="function")
def superuser():
    return CustomUser.objects.create_user(
        first_name="super",
        last_name="user",
        phone_no= "03647394756",
        email="superuser@gmail.com",
        username= "superuser",
        sex="Female",
        role="Admin",
        password= "notreal01",
        address="51 church street",
        city="illinoi",
        state="chicago",
        zipcode="100010",
        country = "Nigeria",
        is_active=True,
        is_staff=True,
        is_superuser=True,
        profile_picture=None
    )


@pytest.fixture(scope="function")
def authenticated_superuser(superuser):
    api_client = APIClient()
    payload = {
        "email": "superuser@gmail.com",
        "password": "notreal01"
    }
    url = reverse("access_token")
    response = api_client.post(url, data=payload, format="json")
    assert response.status_code == 201
    token = response.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return api_client


@pytest.fixture(scope="function")
def regularuser():
    return CustomUser.objects.create_user(
        first_name="regular",
        last_name="user",
        phone_no= "47304638404",
        email="regularuser@gmail.com",
        username= "regularuser",
        sex="Male",
        role="Customer",
        password= "notreal01",
        address="51 church street",
        city="illinoi",
        state="chicago",
        zipcode="100010",
        country = "Nigeria",
        is_active=True,
        is_staff=False,
        is_superuser=False,
        profile_picture=None
    )


@pytest.fixture(scope="function")
def authenticated_regularuser(regularuser):
    api_client = APIClient()
    payload = {
        "email": "regularuser@gmail.com",
        "password": "notreal01"
    }
    url = reverse("access_token")
    response = api_client.post(url, data=payload, format="json")
    assert response.status_code == 201
    token = response.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return api_client


@pytest.fixture(scope="function")
def account_type(superuser):
    account_type_obj = AccountType.objects.create(
        name="savings",
        account_limit=30000000.00,
        maximum_daily_withdrawal_amount=5000000.00
    )
    return account_type_obj