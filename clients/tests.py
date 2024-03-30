from rest_framework.test import APITestCase
from rest_framework import status
from clients.models import Client
from employees.models import Employee
from django.contrib.auth.models import Group
from django.urls import reverse

class ClientListViewTests(APITestCase):
    def setUp(self):
        self.url = reverse('client-list')

        group = Group.objects.create(name='IT')

        self.employee = Employee.objects.create_user(username='test_employee', password='test_password')
        self.employee.groups.add(group)

        data = {'username': 'test_employee', 'password': 'test_password'}
        response = self.client.post(reverse('login'), data, format='json')
        self.token = response.data.get('token', '')

    def test_list_clients_authenticated(self):
        headers = {'Authorization': f'Token {self.token}'}
        response = self.client.get(self.url, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_clients_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_client_authenticated(self):
        data = {'name': 'New Client', 'email': 'newclient@example.com'}
        headers = {'Authorization': f'Token {self.token}'}
        response = self.client.post(self.url, data, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_client_unauthenticated(self):
        data = {'name': 'New Client', 'email': 'newclient@example.com'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class ClientDetailViewTests(APITestCase):
    def setUp(self):
        group = Group.objects.create(name='IT')

        self.employee = Employee.objects.create_user(username='test_employee', password='test_password')
        self.employee.groups.add(group)

        data = {'username': 'test_employee', 'password': 'test_password'}
        response = self.client.post(reverse('login'), data, format='json')
        self.token = response.data.get('token', '')

        # Creating a client for testing
        self.client_obj = Client.objects.create(name='Test Client', email='testclient@example.com')
        self.url = reverse('client-detail', args=[self.client_obj.uuid])

    def test_retrieve_client_authenticated(self):
        headers = {'Authorization': f'Token {self.token}'}
        response = self.client.get(self.url, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_client_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_client_authenticated(self):
        data = {'name': 'Updated Client'}
        headers = {'Authorization': f'Token {self.token}'}
        response = self.client.patch(self.url, data, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_client_unauthenticated(self):
        data = {'name': 'Updated Client'}
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_client_authenticated(self):
        headers = {'Authorization': f'Token {self.token}'}
        response = self.client.delete(self.url, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_client_unauthenticated(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
