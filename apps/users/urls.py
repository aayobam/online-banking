from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from . import views


router = DefaultRouter()
router.register('users/', views.UserViewSet, basename="users")
# router.register('auth/', views.CustomTokenObtainPairView, basename="access_token")
# router.register('token/refresh/', TokenRefreshView.as_view(), basename="token_refresh")
urlpatterns = router.urls
