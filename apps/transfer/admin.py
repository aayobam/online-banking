from django.contrib import admin
from apps.transfer.models import Transfer


@admin.register(Transfer)
class AdminTransfer(admin.ModelAdmin):
    list_display = ('id', 'from_account', 'receiver_account', 'receiver_name', 'amount', 'status')
