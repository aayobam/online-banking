import pytest
from apps.users.models import CustomUser



@pytest.mark.django_db
def test_create_user(superuser):
    assert isinstance(superuser, CustomUser)
    assert superuser.email == "superuser@gmail.com"
    assert superuser.first_name == "super"
    assert superuser.last_name == "user"
    assert superuser.username == "superuser"
    assert superuser.role == "Admin"
    assert superuser.country == "Nigeria"