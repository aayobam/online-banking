from django.forms import FloatField
import pytest
from apps.account_type.models import AccountType



@pytest.mark.django_db
def test_create_account_type_model(account_type):
    assert isinstance(account_type, AccountType)
    assert account_type.name == "savings"
    assert type(account_type.account_limit) == float