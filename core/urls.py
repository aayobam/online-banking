from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from core.settings import MEDIA_ROOT





schema_view = get_schema_view(
   openapi.Info(
      title="Internet Banking",
      default_version='v1',
      description="Iternet banking web app documentation",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
   authentication_classes=[]
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/users/', include('apps.users.urls')),
    path('api/v1/account_type/', include('apps.account_type.urls')),
    path('api/v1/bank_account/', include('apps.bank_account.urls')),
    path('api/v1/transaction/', include('apps.transaction.urls')),
    path('api/v1/transfer/', include('apps.transfer.urls')),

    # drf-yasg open api
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=MEDIA_ROOT)

admin.site.site_title = "Bank Admin"
admin.site.site_header ="Bank Administrator"
