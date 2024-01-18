from django.contrib import admin
from apis.loans.models import Loan


@admin.register(Loan)
class AdminLoan(admin.ModelAdmin):
    list_display = ('account', 'amount', 'interest_rate', 'term', 'date_created', 'date_updated')
