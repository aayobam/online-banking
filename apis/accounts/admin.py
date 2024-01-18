from django.contrib import admin

from apis.accounts.models import Account


@admin.register(Account)
class AdminAccount(admin.ModelAdmin):
    list_display = (
        "owner",
        "account_no",
        "balance",
        "account_type",
        "daily_transfer_limit",
        "verification_status",
    )
    readonly_fields = ("id", "account_no", "balance",
                       "daily_transfer_limit", "verification_status")
