from uuid import uuid4
from django.db import models
from django.urls import reverse
from apps.common.models import TimeStampedModel
from django.core.validators import MinValueValidator



class AccountType(TimeStampedModel):
    name = models.CharField(max_length=100)
    account_limit = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    maximum_daily_withdrawal_amount = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    
    class Meta:
        verbose_name = "account type"
        verbose_name_plural = "account types"
        ordering = ('date_created',)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("type_detail", kwargs={"type_id": self.id})
    
