from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    CustomTokenObtainPairView,
    RegisterUserApiView,
    UserListApiView,
    UserDetailApiView,
    UserUpdateApiView,
    UserDeleteApiView
)


urlpatterns = [
    path('auth/', CustomTokenObtainPairView.as_view(), name="access-token"),
    path('token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
    path('register/', RegisterUserApiView.as_view(), name="register"),
    path('all/', UserListApiView.as_view(), name="user-list"),
    path('detail/<uuid:user_id>/', UserDetailApiView.as_view(), name="user-detail"),
    path('update/<uuid:user_id>/', UserUpdateApiView.as_view(), name="update-user"),
    path('delete/<uuid:user_id>/', UserDeleteApiView.as_view(), name="delete-user"),
]