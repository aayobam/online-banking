from django.core.exceptions import ValidationError
from django.db import models

from apps.accounts.models import Account
from apps.cards import generate_card
from apps.common.choices import CARD_TYPES
from apps.common.models import TimeStampedModel


def validate_card_number(value):
    if len(value) < 12 or len(value) > 16:
        raise ValidationError("card value cannot be lesser than 12 or higher than 16.")
    elif type(value) != int:
        raise ValueError("value can only be a whole number")
    return value


def validate_cvv(value):
    if len(value) < 3 or len(value) > 7:
        raise ValidationError("value cannot be lesser than 3 or higher than 7")
    elif type(value) != int:
        raise ValueError("value can only be a whole number")
    return value


class Card(TimeStampedModel):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    card_type = models.CharField(max_length=50, choices=CARD_TYPES)
    card_number = models.CharField(max_length=16, unique=True, validators=[validate_card_number])
    cvv = models.CharField(max_length=7, blank=True, null=True, unique=True, validators=[validate_cvv])
    expiry_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.card_type

    def save(self, *args, **kwargs):
        self.card_number = generate_card.generate_card_number()
        self.cvv = generate_card.generate_cvv()
        self.expiry_date = generate_card.generate_expiry_date()
        super().save(*args, **kwargs)
