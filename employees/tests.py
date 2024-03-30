from rest_framework.test import APITestCase
from rest_framework import status
from employees.models import Employee
from django.contrib.auth.models import Group
from django.urls import reverse

class EmployeeLoginTests(APITestCase):
    def setUp(self):
        self.url = reverse('login')

        self.employee = Employee.objects.create_user(username='test_employee', password='test_password')

    def test_login_with_valid_credentials(self):
        data = {'username': 'test_employee', 'password': 'test_password'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)

    def test_login_with_invalid_credentials(self):
        data = {'username': 'invalid_employee', 'password': 'invalid_password'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue('error' in response.data)

class EmployeeListViewTests(APITestCase):
    def setUp(self):
        self.url_list = reverse('employee-list')

        group = Group.objects.create(name='IT')

        self.employee = Employee.objects.create_user(username='test_employee', password='test_password')
        self.employee.groups.add(group)

        data = {'username': 'test_employee', 'password': 'test_password'}
        response = self.client.post(reverse('login'), data, format='json')
        self.token = response.data.get('token', '')

    def test_list_employees_authenticated(self):
        headers = {'Authorization': f'Token {self.token}'}
        response = self.client.get(self.url_list, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_employees_unauthenticated(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_employee_authenticated(self):
        data = {'username': 'new_employee', 'password': 'new_password', 'position': 'Developer', 'department': 'Engineering', 'hire_date': '2023-01-15'}
        headers = {'Authorization': f'Token {self.token}'}
        response = self.client.post(self.url_list, data, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_employee_unauthenticated(self):
        data = {'username': 'new_employee', 'password': 'new_password'}
        response = self.client.post(self.url_list, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class EmployeeDetailViewTests(APITestCase):
    def setUp(self):
        group = Group.objects.create(name='IT')

        self.employee = Employee.objects.create_user(username='test_employee', password='test_password')
        self.employee.groups.add(group)

        data = {'username': 'test_employee', 'password': 'test_password'}
        response = self.client.post(reverse('login'), data, format='json')
        self.token = response.data.get('token', '')

        self.url = reverse('employee-detail', args=[self.employee.uuid])

    def test_retrieve_employee_authenticated(self):
        headers = {'Authorization': f'Token {self.token}'}
        response = self.client.get(self.url, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_employee_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_employee_authenticated(self):
        data = {'username': 'new_employee', 'department': 'Engineering'}
        headers = {'Authorization': f'Token {self.token}'}
        response = self.client.patch(self.url, data, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_employee_unauthenticated(self):
        data = {'username': 'updated_employee'}
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_employee_authenticated(self):
        headers = {'Authorization': f'Token {self.token}'}
        response = self.client.delete(self.url, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_employee_unauthenticated(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
