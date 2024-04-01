from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularRedocView, SpectacularSwaggerView, SpectacularAPIView

urlpatterns = [
    path("admin", admin.site.urls),
    path('clients', include('clients.urls')),
    path('employees', include('employees.urls')),
    path('rooms', include('rooms.urls')),
    path('reservations', include('reservations.urls')),

    path('docs', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/schema', SpectacularAPIView.as_view(), name='schema'),
]
