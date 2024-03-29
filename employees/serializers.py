from rest_framework import serializers
from .models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['uuid', 'username', 'email', 'first_name', 'last_name', 'position', 'department', 'hire_date', 'date_of_termination', 'groups']
        read_only_fields = ['uuid', 'groups']
