from django.contrib import admin
from django.urls import path, include
from .views import check_database_connection

urlpatterns = [
    path("admin", admin.site.urls),
    path('clients', include('clients.urls')),
    path(
        "check-connection", check_database_connection, name="check_database_connection"
    ),
]
