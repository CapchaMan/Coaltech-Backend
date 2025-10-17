from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static

def home(request):
    return JsonResponse({'message':'Varse Commerce API'})

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/categories/', include('categories.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
