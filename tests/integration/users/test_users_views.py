import pytest
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from apps.users.models import CustomUser



@pytest.mark.django_db
def test_create_user_view():
    api_client = APIClient()
    assert len(CustomUser.objects.all()) == 0
    payload = {
        "first_name": "test",
        "last_name": "user",
        "phone_no": "74536483538",
        "email": "testuser@gmail.com",
        "username": "testuser",
        "password": "notreal01",
        "role": "Customer",
        "country": "Nigeria",
        "is_active": True,
        "is_staff": False,
        "is_superuser": False
    }
    url = reverse("create")
    response = api_client.post(url, data=payload)
    assert response.status_code == 201
    assert len(CustomUser.objects.all()) == 1
    assert response.data["email"] == "testuser@gmail.com"
    assert response.data["username"] == "testuser"


@pytest.mark.django_db
def test_create_user_email_and_username_exist_view(regularuser):
    api_client = APIClient()
    assert len(CustomUser.objects.all()) == 1
    payload = {
        "first_name": "regular",
        "last_name": "user",
        "phone_no": "74536483538",
        "email": "regularuser@gmail.com",
        "username": "regularuser",
        "password": "notreal01",
        "role": "Customer",
        "country": "Nigeria",
        "is_active": True,
        "is_staff": False,
        "is_superuser": False
    }
    url = reverse("create")
    response = api_client.post(url, data=payload)
    assert response.status_code == 400
    assert len(CustomUser.objects.all()) == 1


@pytest.mark.django_db
def test_create_user_no_email_view():
    api_client = APIClient()
    assert len(CustomUser.objects.all()) == 0
    payload = {
        "first_name": "test",
        "last_name": "user",
        "phone_no": "74536483538",
        "username": "testuser",
        "password": "notreal01",
        "role": "Customer",
        "country": "Nigeria",
    }
    url = reverse("create")
    response = api_client.post(url, data=payload)
    assert response.status_code == 400
    assert len(CustomUser.objects.all()) == 0


@pytest.mark.django_db
def test_create_user_short_password_view():
    api_client = APIClient()
    assert len(CustomUser.objects.all()) == 0
    payload = {
        "first_name": "test",
        "last_name": "user",
        "phone_no": "74536483538",
        "email": "testuser@gmail.com",
        "username": "testuser",
        "password": "notreal",
        "role": "Customer",
        "country": "Nigeria",
    }
    url = reverse("create")
    response = api_client.post(url, data=payload)
    assert response.status_code == 400
    assert len(CustomUser.objects.all()) == 0


@pytest.fixture(scope="function")
def authenticated_user(superuser):
    api_client = APIClient()
    payload = {
        "email": superuser.email,
        "password": superuser.password
    }
    url = reverse("create_user")
    response = api_client.post(url, data=payload)
    assert response.status_code == 200
    token = response.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return api_client


@pytest.mark.django_db
def test_superuser_can_view_users_list_view(regularuser, superuser, authenticated_superuser):
    url = reverse("user_list")
    response = authenticated_superuser.get(url)
    assert response.status_code == 200
    assert len(CustomUser.objects.all()) == 2


@pytest.mark.django_db
def test_regularuser_cannot_view_users_list_view(regularuser, superuser, authenticated_regularuser):
    url = reverse("user_list")
    response = authenticated_regularuser.get(url)
    assert response.status_code == 403
    assert len(CustomUser.objects.all()) == 2


@pytest.mark.django_db
def test_superuser_can_view_all_users_details_view(regularuser, superuser, authenticated_superuser):
    url = reverse("user_detail", kwargs={"user_id":regularuser.id})
    response = authenticated_superuser.get(url)
    assert response.status_code == 200
    assert len(CustomUser.objects.all()) == 2


@pytest.mark.django_db
def test_regularuser_cannnot_view_other_users_details_view(regularuser, superuser, authenticated_superuser, authenticated_regularuser):
    url = reverse("user_detail", kwargs={"user_id":superuser.id})
    response = authenticated_regularuser.get(url)
    assert response.status_code == 403
    assert len(CustomUser.objects.all()) == 2


@pytest.mark.django_db
def test_regularuser_detail_view(regularuser, superuser, authenticated_superuser, authenticated_regularuser):
    url = reverse("user_detail", kwargs={"user_id":regularuser.id})
    response = authenticated_regularuser.get(url)
    assert response.status_code == 200
    assert len(CustomUser.objects.all()) == 2


@pytest.mark.django_db
def test_superuser_can_update_all_users_detail_view(regularuser, superuser, authenticated_superuser):
    payload = {
        "first_name": "regular",
        "last_name": "user",
        "phone_no": "74536483538",
        "email": "regularuser@gmail.com",
        "username": "regularuser",
        "password": "notreal01",
        "role": "Teller",
        "country": "Nigeria",
        "is_active": True,
        "is_staff": False,
        "is_superuser": False
    }
    url = reverse("update_user", kwargs={"user_id":regularuser.id})
    response = authenticated_superuser.put(url, data=payload)
    assert response.status_code == 200
    assert len(CustomUser.objects.all()) == 2


@pytest.mark.django_db
def test_regularuser_cannot_update_other_users_detail_view(regularuser, superuser, authenticated_regularuser):
    payload = {
        "first_name": "super",
        "last_name": "user",
        "phone_no": "74536483538",
        "email": "superuserruser@gmail.com",
        "username": "superuseruser",
        "password": "notreal01",
        "role": "Teller",
        "country": "Nigeria",
        "is_active": True,
        "is_staff": True,
        "is_superuser": True
    }
    url = reverse("update_user", kwargs={"user_id":superuser.id})
    response = authenticated_regularuser.put(url, data=payload)
    assert response.status_code == 403
    assert len(CustomUser.objects.all()) == 2


@pytest.mark.django_db
def test_regularuser_update_view(regularuser, superuser, authenticated_regularuser):
    payload = {
        "first_name": "regular",
        "last_name": "user",
        "phone_no": "74536483538",
        "email": "regularuser@gmail.com",
        "username": "regularuser",
        "password": "notreal01",
        "country": "Ghana",
        "is_active": True,
        "is_staff": False,
        "is_superuser": False
    }
    url = reverse("update_user", kwargs={"user_id":regularuser.id})
    response = authenticated_regularuser.put(url, data=payload)
    assert response.status_code == 200
    assert len(CustomUser.objects.all()) == 2


@pytest.mark.django_db
def test_superuser_can_delete_users_view(regularuser, superuser, authenticated_superuser, authenticated_regularuser):
    assert len(CustomUser.objects.all()) == 2
    url = reverse("delete_user", kwargs={"user_id":regularuser.id})
    response = authenticated_superuser.delete(url)
    assert response.status_code == 204
    assert len(CustomUser.objects.all()) == 1


@pytest.mark.django_db
def test_regularuser_cannot_delete_other_users_view(regularuser, superuser, authenticated_superuser, authenticated_regularuser):
    assert len(CustomUser.objects.all()) == 2
    url = reverse("delete_user", kwargs={"user_id":superuser.id})
    response = authenticated_regularuser.delete(url)
    assert response.status_code == 403
    assert len(CustomUser.objects.all()) == 2


@pytest.mark.django_db
def test_regularuser_delete_account_view(regularuser, superuser, authenticated_superuser, authenticated_regularuser):
    assert len(CustomUser.objects.all()) == 2
    url = reverse("delete_user", kwargs={"user_id":regularuser.id})
    response = authenticated_regularuser.delete(url)
    assert response.status_code == 204
    assert len(CustomUser.objects.all()) == 1