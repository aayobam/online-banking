import pytest
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from apps.users.models import CustomUser



@pytest.fixture(scope="function")
def superuser():
    return CustomUser.objects.create_superuser(
        first_name="super",
        last_name="user",
        phone_no= "03647394756",
        email="superuser@gmail.com",
        username= "superuser",
        password= "notreal01",
        role="Admin",
        country = "Nigeria",
        is_active=True,
        is_staff=True,
        is_superuser=True
    )


@pytest.fixture(scope="function")
def authenticated_superuser(superuser):
    api_client = APIClient()
    payload = {
        "email": "superuser@gmail.com",
        "password": "notreal01"
    }
    url = reverse("access_token")
    response = api_client.post(url, data=payload)
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
        username= "regularuserr",
        password= "notreal01",
        role="Customer",
        country = "Nigeria",
        is_active=True,
        is_staff=False,
        is_superuser=False
    )


@pytest.fixture(scope="function")
def authenticated_regularuser(regularuser):
    api_client = APIClient()
    payload = {
        "email": "regularuser@gmail.com",
        "password": "notreal01"
    }
    url = reverse("access_token")
    response = api_client.post(url, data=payload)
    assert response.status_code == 201
    token = response.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")