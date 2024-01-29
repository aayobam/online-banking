from django.urls import path, include
from apis.accounts import views

from rest_framework.routers import DefaultRouter


routers = DefaultRouter()

routers.register('', views.AccountViewSet, basename="accounts")

urlpatterns = [
    path('', include(routers.urls))
]
