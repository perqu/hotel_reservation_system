from rest_framework import serializers
from .models import Employee, CustomGroup, CustomPermission

class CustomGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomGroup
        fields = ['uuid', 'name']

class CustomPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomPermission
        fields = ['uuid', 'name', 'codename']

class EmployeeSerializer(serializers.ModelSerializer):
    employee_groups = CustomGroupSerializer(many=True, read_only=True)
    employee_permissions = CustomPermissionSerializer(many=True, read_only=True)

    class Meta:
        model = Employee
        fields = ['uuid', 'username', 'email', 'first_name', 'last_name', 'position', 'department', 'hire_date', 'date_of_termination', 'employee_groups', 'employee_permissions']
