import pytest
from apps.users.models import CustomUser
from rest_framework.test import APIClient
from apps.users.serializers import UserRegisterationSerializer, UserSerializer



api_client = APIClient()


@pytest.mark.django_db
def test_create_superuser_serializer():
    assert len(CustomUser.objects.all()) == 0
    payload = {
        "first_name": "test",
        "last_name": "user",
        "email": "testuser@gmail.com",
        "username": "testuser",
        "phone_no": "74536483538",
        "password": "notreal01",
        "country": "nigeria",
        "is_active": True,
        "is_staff": True,
        "is_superuser": True
    }
    serializer = UserRegisterationSerializer(data=payload)
    assert serializer.is_valid()
    serializer.save(role="Admin")
    assert len(CustomUser.objects.all()) == 1
    assert serializer.errors == {}


@pytest.mark.django_db
def test_create_regularuser_serializer():
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
    serializer = UserRegisterationSerializer(data=payload)
    assert serializer.is_valid()
    serializer.save(role="Customer")
    assert len(CustomUser.objects.all()) == 1
    assert serializer.errors == {}


@pytest.mark.django_db
def test_create_user_no_email_serializer():
    assert len(CustomUser.objects.all()) == 0
    payload = {
        "first_name": "test",
        "last_name": "user",
        "phone_no": "74536483538",
        "username": "testuser",
        "password": "notreal01",
        "address": "51 church street",
        "city": "illinoi",
        "state": "chicago",
        "zipcode": "100010",
        "country": "nigeria",
        "is_active": True,
        "is_staff": False,
        "is_superuser": False  
    }
    serializer = UserRegisterationSerializer(data=payload)
    assert not serializer.is_valid()
    assert len(CustomUser.objects.all()) == 0
    assert serializer.errors != {}