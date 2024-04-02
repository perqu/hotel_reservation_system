from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Employee
from .serializers import EmployeeSerializer, AuthSerializer
from utils.permissions import HasGroupPermission
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from utils.paginators import SmallResultsSetPagination
from knox.views import LoginView as KnoxLoginView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import login
from utils.scheme import KnoxTokenScheme
        
class LoginAPIView(KnoxLoginView):
    """
    A view to handle user authentication and token generation.
    """

    serializer_class = AuthSerializer
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        """
        Authenticate user and generate a token.

        Required parameters in the request:
        - username: The username of the user (string).
        - password: The password of the user (string).
        """
        serializer = AuthTokenSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPIView, self).post(request, format=None)

class EmployeeListView(APIView):
    """
    A view to list all employees or create a new employee.
    """
    serializer_class = EmployeeSerializer
    permission_classes = [HasGroupPermission]
    required_groups = ['IT']
    pagination_class = SmallResultsSetPagination

    @extend_schema(
        parameters=[
            OpenApiParameter(name="page_size", type=OpenApiTypes.INT, description='Page Size for pagination.', required=False),
            OpenApiParameter(name="page", type=OpenApiTypes.INT, description='Page number for pagination.', required=False),
        ],
    )
    def get(self, request):
        """
        Get a list of paginated employees.

        Example:
        http://localhost:8000/employees?page=2&page_size=20
        """
        employees = Employee.objects.all().order_by('username')

        paginator = self.pagination_class()
        paginated_employees = paginator.paginate_queryset(employees, request)

        serializer = self.serializer_class(paginated_employees, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        """
        Create a new employee.

        Required parameters in the request:
        - username: The username of the employee (string).
        - email: The email of the employee (string).
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmployeeDetailView(APIView):
    """
    A view to retrieve, update or delete an employee instance.
    """
    serializer_class = EmployeeSerializer
    permission_classes = [HasGroupPermission]
    required_groups = ['IT']

    def get_object(self, uuid):
        """
        Retrieve an employee object by its UUID.

        parameters:
         - uuid: The UUID of the employee to retrieve (string).

        return: Employee object if found, None otherwise.
        """
        try:
            return Employee.objects.get(uuid=uuid)
        except Employee.DoesNotExist:
            return None

    def get(self, request, uuid):
        """
        Retrieve details of an employee by UUID.

        Required parameter in the URL:
        - uuid: The UUID of the employee to retrieve (string).
        """
        employee = self.get_object(uuid)
        if employee:
            serializer = self.serializer_class(employee)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, uuid):
        """
        Update an employee instance partially.

        Possible parameters in the request:
        - username: The username of the employee (string).
        - email: The email of the employee (string).
        """
        employee = self.get_object(uuid)
        if employee:
            serializer = self.serializer_class(employee, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, uuid):
        """
        Delete an employee by UUID.

        Required parameter in the URL:
        - uuid: The UUID of the employee to delete (string).
        """
        employee = self.get_object(uuid)
        if employee:
            employee.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
