from django.http import HttpResponse
from django.db import connection


def check_database_connection(request):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        return HttpResponse("DB works")
    except Exception as e:
        return HttpResponse(f"Error: {e}", status=500)
