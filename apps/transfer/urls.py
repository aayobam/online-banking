from django.urls import path
from apps.transfer.views import make_transfer


urlpatterns = [
    path('transfer/', make_transfer, name="make_transfer")
]
