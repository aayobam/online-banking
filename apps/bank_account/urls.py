from django.urls import path
from apps.bank_account import views



urlpatterns = [
    path('verify-account/', views.GetBankAccountNumberApiView.as_view(), name="generate_account_number"),
    path('all/', views.BankAccountListApiView.as_view(), name="account_list"),
    path('detail/<uuid:account_id>', views.BankccountDetailApiView.as_view(), name="account_detail"),
    path('update/<uuid:account_id>/', views.BankAccountUpdateApiView.as_view(), name="account_update"),
    path('delete/<uuid:account_id>/', views.DeleteBankAccountApiView.as_view(), name="delete_account")
]
