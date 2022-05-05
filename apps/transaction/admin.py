from django.contrib import admin
from apps.transaction.models import Transaction


@admin.register(Transaction)
class AdminTransaction(admin.ModelAdmin):
    list_display = ('id', 'user', 'account', 'transaction_type', 'amount', 'comment')
