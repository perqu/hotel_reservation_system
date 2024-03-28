from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Employee
from .serializers import EmployeeSerializer

class EmployeeListViewTests(APITestCase):
    def setUp(self):
        self.employee1 = Employee.objects.create(username='testuser1', position='Tester', department='Testing')
        self.employee2 = Employee.objects.create(username='testuser2', position='Developer', department='Development')

    def test_get_employee_list(self):
        url = reverse('employee-list')
        response = self.client.get(url)
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_employee(self):
        url = reverse('employee-list')
        data = {'username': 'newuser', 'position': 'New Position', 'department': 'New Department'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(), 3)

class EmployeeDetailViewTests(APITestCase):
    def setUp(self):
        self.employee = Employee.objects.create(username='testuser', position='Tester', department='Testing')

    def test_get_employee_detail(self):
        url = reverse('employee-detail', kwargs={'uuid': str(self.employee.uuid)})
        response = self.client.get(url)
        employee = Employee.objects.get(uuid=self.employee.uuid)
        serializer = EmployeeSerializer(employee)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_employee(self):
        url = reverse('employee-detail', kwargs={'uuid': str(self.employee.uuid)})
        data = {'username': 'updateduser', 'position': 'Updated Position', 'department': 'Updated Department'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_employee = Employee.objects.get(uuid=self.employee.uuid)
        self.assertEqual(updated_employee.username, 'updateduser')
        self.assertEqual(updated_employee.position, 'Updated Position')
        self.assertEqual(updated_employee.department, 'Updated Department')

    def test_delete_employee(self):
        url = reverse('employee-detail', kwargs={'uuid': str(self.employee.uuid)})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Employee.objects.filter(uuid=self.employee.uuid).exists())
