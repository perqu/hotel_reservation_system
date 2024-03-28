from django.contrib import admin
from django.urls import path
from .views import check_database_connection

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "check-connection/", check_database_connection, name="check_database_connection"
    ),
]
