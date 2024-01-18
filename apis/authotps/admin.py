from django.contrib import admin

from apis.authotps.models import AuthOtp



@admin.register(AuthOtp)
class AdminAuthOtp(admin.ModelAdmin):
    list_display = ('user', 'otp', 'expiry', 'description', 'date_created', 'date_updated')
