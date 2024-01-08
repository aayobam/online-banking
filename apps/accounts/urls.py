from django.urls import path

from apps.accounts import views

urlpatterns = [
    path(
        "verify-account/",
        views.GetAccountNumberApiView.as_view(),
        name="generate_account_number",
    ),
    path("all/", views.AccountListApiView.as_view(), name="account_list"),
    path(
        "detail/<uuid:account_id>",
        views.AccountDetailApiView.as_view(),
        name="account_detail",
    ),
    path(
        "update/<uuid:account_id>/",
        views.AccountUpdateApiView.as_view(),
        name="account_update",
    ),
    path(
        "delete/<uuid:account_id>/",
        views.DeleteAccountApiView.as_view(),
        name="delete_account",
    ),
]
