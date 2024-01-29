from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from . import views


router = DefaultRouter()

router.register('', views.UserViewSet, basename="users")

urlpatterns = [
    path('token/refresh', TokenRefreshView.as_view(), name="token_refresh"),
    path('auth', views.CustomTokenObtainPairView.as_view(), name="access_token"),
    path('', include(router.urls))
]
