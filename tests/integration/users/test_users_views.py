import pytest
from apps.users.models import CustomUser
from rest_framework.test import APIClient
from rest_framework.reverse import reverse



@pytest.mark.django_db
def test_create_user_view():
    api_client = APIClient()
    assert len(CustomUser.objects.all()) == 0
    payload = {
        "email": "testuser@gmail.com",
        "username": "testuser",
        "first_name": "test",
        "last_name": "user",
        "password": "notreal01",
        "phone_no": "74536483538",
        "country": "nigeria"
    }
    url = reverse("create_user")
    response = api_client.post(url, data=payload)
    assert response.status_code == 201
    assert len(CustomUser.objects.all()) == 1
    assert response.data["email"] == "testuser@gmail.com"
    assert response.data["username"] == "testuser"


@pytest.mark.django_db
def test_create_user_no_email_view():
    api_client = APIClient()
    assert len(CustomUser.objects.all()) == 0
    payload = {
        "username": "testuser",
        "first_name": "test",
        "last_name": "user",
        "password": "notreal01",
        "phone_no": "74536483538",
        "country": "nigeria"
    }
    url = reverse("create_user")
    response = api_client.post(url, data=payload, format="json")
    assert response.status_code == 400
    assert len(CustomUser.objects.all()) == 0
    print("RESPONSE ERROR = ", response.json()["email"])
    assert response.json()["email"] == ['This field is required.']


@pytest.mark.django_db
def test_create_user_short_password_view():
    api_client = APIClient()
    assert len(CustomUser.objects.all()) == 0
    payload = {
        "email": "testuser@gmail.com",
        "username": "testuser",
        "first_name": "test",
        "last_name": "user",
        "password": "notreal",
        "phone_no": "74536483538",
        "country": "nigeria"
    }
    url = reverse("create_user")
    response = api_client.post(url, data=payload)
    assert response.status_code == 400
    assert len(CustomUser.objects.all()) == 0
    assert response.data["password"] == ["Ensure this field has at least 8 characters."]


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
    assert response.data["detail"] == "You do not have permission to perform this action."


@pytest.mark.django_db
def test_superuser_can_view_all_users_details_view(regularuser, superuser, authenticated_superuser):
    url = reverse("user_detail", kwargs={"user_id": regularuser.id})
    response = authenticated_superuser.get(url)
    assert response.status_code == 200
    assert len(CustomUser.objects.all()) == 2


@pytest.mark.django_db
def test_regularuser_cannnot_view_other_users_details_view(regularuser, superuser, authenticated_superuser, authenticated_regularuser):
    url = reverse("user_detail", kwargs={"user_id": superuser.id})
    response = authenticated_regularuser.get(url)
    assert response.status_code == 403
    assert len(CustomUser.objects.all()) == 2
    assert response.data["detail"] == "You do not have permission to perform this action."


@pytest.mark.django_db
def test_regularuser_detail_view(regularuser, superuser, authenticated_superuser, authenticated_regularuser):
    url = reverse("user_detail", kwargs={"user_id": regularuser.id})
    response = authenticated_regularuser.get(url)
    assert response.status_code == 200
    assert len(CustomUser.objects.all()) == 2
    assert response.data["id"] == str(regularuser.id)
    assert response.data["username"] == "regularuser"
    assert response.data["email"] == "regularuser@gmail.com"


@pytest.mark.django_db
def test_superuser_can_update_all_users_detail_view(regularuser, superuser, authenticated_superuser):
    assert len(CustomUser.objects.all()) == 2
    payload = {
        "email": "testuser2@gmail.com",
        "username": "testuser2",
        "first_name": "test",
        "last_name": "user2",
        "password": "notreal01",
        "phone_no": "74536483538",
        "role": "customer",
        "address": "51 church street",
        "city": "illinoi",
        "state": "chicago",
        "zipcode": "100020",
        "country": "nigeria",
        "is_active": True,
        "is_staff": True,
        "is_superuser": False
    }
    url = reverse("update_user", kwargs={"user_id": regularuser.id})
    response = authenticated_superuser.put(url, data=payload)
    assert response.status_code == 200
    assert len(CustomUser.objects.all()) == 2
    assert response.data["username"] == "testuser2"
    assert response.data["last_name"] == "user2"
    assert response.data["email"] == "testuser2@gmail.com"


@pytest.mark.django_db
def test_regularuser_cannot_update_other_users_detail_view(regularuser, superuser, authenticated_regularuser):
    assert len(CustomUser.objects.all()) == 2
    payload = {
        "email": "superuser@gmail.com",
        "username": "superuser",
        "first_name": "super",
        "last_name": "user",
        "password": "notreal01",
        "phone_no": "74536483538",
        "role": "customer",
        "address": "51 church street",
        "city": "illinoi",
        "state": "chicago",
        "zipcode": "100020",
        "country": "nigeria",
        "is_active": True,
        "is_staff": True,
        "is_superuser": True
    }
    url = reverse("update_user", kwargs={"user_id": superuser.id})
    response = authenticated_regularuser.put(url, data=payload)
    assert response.status_code == 403
    assert len(CustomUser.objects.all()) == 2
    assert response.data["detail"] == "You do not have permission to perform this action."


@pytest.mark.django_db
def test_regularuser_cannot_update_view(regularuser, superuser, authenticated_regularuser):
    payload = {
        "email": "testuser@gmail.com",
        "username": "testuser",
        "first_name": "test",
        "last_name": "user",
        "password": "notreal01",
        "phone_no": "74536483538",
        "country": "nigeria",
        "role": "customer",
        "address": "51 church street",
        "city": "illinoi",
        "state": "chicago",
        "zipcode": "100020",
        "country": "nigeria",
        "is_active": True,
        "is_staff": False,
        "is_superuser": False
    }
    url = reverse("update_user", kwargs={"user_id": regularuser.id})
    response = authenticated_regularuser.put(url, data=payload)
    assert response.status_code == 403
    assert len(CustomUser.objects.all()) == 2
    assert response.data["detail"] == "You do not have permission to perform this action."


@pytest.mark.django_db
def test_superuser_can_delete_users_view(regularuser, superuser, authenticated_superuser, authenticated_regularuser):
    assert len(CustomUser.objects.all()) == 2
    url = reverse("delete_user", kwargs={"user_id": regularuser.id})
    response = authenticated_superuser.delete(url)
    assert response.status_code == 204
    assert len(CustomUser.objects.all()) == 1


@pytest.mark.django_db
def test_regularuser_cannot_delete_other_users_view(regularuser, superuser, authenticated_superuser, authenticated_regularuser):
    assert len(CustomUser.objects.all()) == 2
    url = reverse("delete_user", kwargs={"user_id": superuser.id})
    response = authenticated_regularuser.delete(url)
    assert response.status_code == 403
    assert len(CustomUser.objects.all()) == 2
    assert response.data["detail"] == "You do not have permission to perform this action."


@pytest.mark.django_db
def test_regularuser_cannot_delete_own_account_view(regularuser, superuser, authenticated_superuser, authenticated_regularuser):
    assert len(CustomUser.objects.all()) == 2
    url = reverse("delete_user", kwargs={"user_id": regularuser.id})
    response = authenticated_regularuser.delete(url)
    assert response.status_code == 403
    assert len(CustomUser.objects.all()) == 2
    assert response.data["detail"] == "You do not have permission to perform this action."