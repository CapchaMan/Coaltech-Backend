from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.http import HttpResponse

# --- Swagger/OpenAPI Setup ---
schema_view = get_schema_view(
    openapi.Info(
        title="Coaltech API Documentation",
        default_version='v1',
        description="Live API documentation for Coaltech backend",
        contact=openapi.Contact(email="support@coaltech.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# --- Root/Homepage Views ---
def home(request):
    return HttpResponse("Welcome to Coaltech API")

# Optional: redirect root to Swagger UI instead of plain text
# def redirect_to_swagger(request):
#     return redirect('schema-swagger-ui')

urlpatterns = [
    # Root URL
    path('', home),  # <-- Shows "Welcome to Coaltech API" at /

    # Django Admin
    path('admin/', admin.site.urls),

    # Accounts (Vendor & Rider Registration + Auth)
    path('accounts/', include('accounts.urls')),  # <-- for registration forms
    path('api/auth/', include('accounts.urls')),  # <-- optional future API endpoints

    # Categories app API
    path('api/categories/', include('categories.urls')),

    # Swagger Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# --- Media & Static Files ---
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
