from django.contrib import admin

from .models import Card


@admin.register(Card)
class AdminCards(admin.ModelAdmin):
    list_display = (
        "account",
        "card_type",
        "card_number",
        "cvv",
        "expiry_date",
        "is_active",
    )
    readonly_fields = ("id", "card_number", "cvv", "expiry_date", "is_active")
    search_fields = ("card_type", "account__account_no")
