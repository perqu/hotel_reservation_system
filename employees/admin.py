from django.contrib import admin
from .models import CustomGroup, CustomPermission, Employee

@admin.register(CustomGroup)
class CustomGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'uuid']
    search_fields = ['name']
    # Dodaj dodatkowe pola, jeśli chcesz filtrować lub sortować

@admin.register(CustomPermission)
class CustomPermissionAdmin(admin.ModelAdmin):
    list_display = ['name', 'codename', 'uuid']
    search_fields = ['name', 'codename']
    # Dodaj dodatkowe pola, jeśli chcesz filtrować lub sortować

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'position', 'department', 'hire_date', 'date_of_termination']
    search_fields = ['username', 'email', 'position', 'department']
    filter_horizontal = ['employee_groups', 'employee_permissions']
    # Dodaj dodatkowe pola, jeśli chcesz filtrować lub sortować
