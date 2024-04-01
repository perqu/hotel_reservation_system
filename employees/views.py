from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Employee
from .serializers import EmployeeSerializer, LoginSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from utils.permissions import HasGroupPermission
from rest_framework.permissions import AllowAny


class LoginAPIView(APIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')

            user = authenticate(username=username, password=password)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key})
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeListView(APIView):
    serializer_class = EmployeeSerializer
    permission_classes = [HasGroupPermission]
    required_groups = ['IT']

    def get(self, request):
        employees = Employee.objects.all()
        serializer = self.serializer_class(employees, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmployeeDetailView(APIView):
    serializer_class = EmployeeSerializer
    permission_classes = [HasGroupPermission]
    required_groups = ['IT']

    def get_object(self, uuid):
        try:
            return Employee.objects.get(uuid=uuid)
        except Employee.DoesNotExist:
            return None

    def get(self, request, uuid):
        employee = self.get_object(uuid)
        if employee:
            serializer = self.serializer_class(employee)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, uuid):
        employee = self.get_object(uuid)
        if employee:
            serializer = self.serializer_class(employee, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, uuid):
        employee = self.get_object(uuid)
        if employee:
            employee.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
