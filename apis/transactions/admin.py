from django.contrib import admin

from apis.transactions.models import Transaction


@admin.register(Transaction)
class AdminTransaction(admin.ModelAdmin):
    list_display = (
        "from_account",
        "to_account",
        "transaction_type",
        "amount",
        "date_created",
        "date_updated"
    )
    readonly_fields = ("id", "date_created", "date_updated")
    search_fields = ("from_account", "to_account")
