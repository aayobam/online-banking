import pytest
from apps.account_type.models import AccountType
from apps.account_type.serializers import AccountTypeSerializer



@pytest.mark.django_db
def test_create_account_type(account_type):
    assert len(AccountType.objects.all()) == 1
    payload = {
        "name": "savings",
        "account_limit": 30000000.00,
        "maximum_daily_withdrawal_amount": 5000000.00
    }
    serializer = AccountTypeSerializer(data=payload)
    assert serializer.is_valid()
    assert serializer.save()
    assert len(AccountType.objects.all()) == 2
    assert serializer.errors == {}


@pytest.mark.django_db
def test_create_account_type_no_name(account_type):
    assert len(AccountType.objects.all()) == 1
    payload = {
        "account_limit": 30000000.00,
        "maximum_daily_withdrawal_amount": 5000000.00
    }
    serializer = AccountTypeSerializer(data=payload)
    assert not serializer.is_valid()
    assert len(AccountType.objects.all()) == 1
    assert serializer.errors != {}


@pytest.mark.django_db
def test_create_account_type_account_limit_length_longer_than_12_digits(account_type):
    assert len(AccountType.objects.all()) == 1
    payload = {
        "name": "savings",
        "account_limit": 300000000000.00,
        "maximum_daily_withdrawal_amount": 5000000.00
    }
    serializer = AccountTypeSerializer(data=payload)
    assert not serializer.is_valid()
    assert len(AccountType.objects.all()) == 1
    assert serializer.errors != {}