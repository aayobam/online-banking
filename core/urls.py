from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

routers = DefaultRouter()


schema_view = get_schema_view(
    openapi.Info(
        title="Swift Bank Internet Banking",
        default_version="v1",
        description="Api created by Abayomi Olowu",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="aayobam@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny]
)
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("users/api/", include("apis.users.urls")),
    path("accounts/api/", include("apis.accounts.urls")),
    path("transaction/api/", include("apis.transactions.urls")),

    # Drf-yasg open api docs.
    path("swagger", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("swagger.json", schema_view.without_ui(cache_timeout=0), name="schema-json"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_title = "Swift Bank Admin"
admin.site.site_header = "Swift Bank Administrator"
