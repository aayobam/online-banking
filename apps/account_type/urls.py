from django.urls import path
from apps.account_type import views



urlpatterns = [
    path('create/', views.CreateAccountTypeApiView.as_view(), name="create_type"),
    path('all/', views.AccountTypeListApiView.as_view(), name="list_type"),
    path('detail/<uuid:type_id>/', views.AccountTypeDetailApiView.as_view(), name="detail_type"),
    path('update/<uuid:type_id>/', views.AccountTypeUpdateApiView.as_view(), name="update_type"),
    path('delete/<uuid:type_id>/', views.AccountTypeDeleteApiView.as_view(), name="delete_type"),
]
