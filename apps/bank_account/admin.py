from django.contrib import admin
from apps.bank_account.models import BankAccount



@admin.register(BankAccount)
class AdminBankAccount(admin.ModelAdmin):
    list_display = ('id', 'owner', 'account_type', 'account_no', 'balance', 'transfer_limit', 'verification_status')
