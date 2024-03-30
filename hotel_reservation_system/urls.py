from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin", admin.site.urls),
    path('clients', include('clients.urls')),
    path('employees', include('employees.urls')),
    path('rooms', include('rooms.urls')),
    path('reservations', include('reservations.urls')),
]
