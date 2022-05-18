from django.contrib import admin
from apps.account_type.models import AccountType


@admin.register(AccountType)
class AdminAccountType(admin.ModelAdmin):
    list_display = ('id', 'name', 'account_limit', 'maximum_daily_withdrawal_amount')
