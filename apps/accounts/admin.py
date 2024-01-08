from django.contrib import admin

from apps.accounts.models import Account


@admin.register(Account)
class AdminAccount(admin.ModelAdmin):
    list_display = (
        "owner",
        "account_no",
        "bvn",
        "balance",
        "account_type",
        "daily_transfer_limit",
        "verification_status",
    )
    readonly_fields = ("id", "account_no", "balance", "daily_transfer_limit", "verification_status")
