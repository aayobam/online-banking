from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from . import views


router = DefaultRouter()

router.register("", views.UserViewSet, basename="users")
router.register("", views.LogoutView)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.CustomObtainTokenPairView.as_view(), name='token_obtain_pair'),
]

