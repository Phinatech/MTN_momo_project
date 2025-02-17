from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404, handler500, handler403, handler400
from api.views import error_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('userauths.urls')),
    path('', include("api.urls")),
]

if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
else:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
handler404 = lambda request, exception: error_view(request, exception, status=404)
handler500 = lambda request: error_view(request, status=500)
handler403 = lambda request, exception: error_view(request, exception, status=403)
handler400 = lambda request, exception: error_view(request, exception, status=400)
