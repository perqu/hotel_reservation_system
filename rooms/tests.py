from rest_framework.test import APITestCase
from rest_framework import status
from rooms.models import Amenity, RoomStandard, Room
from employees.models import Employee
from django.contrib.auth.models import Group
from django.urls import reverse


class AmenityListViewTests(APITestCase):
    def setUp(self):
        self.url = reverse('amenity-list')

        group = Group.objects.create(name='IT')

        self.employee = Employee.objects.create_user(username='test_employee', password='test_password')
        self.employee.groups.add(group)

        data = {'username': 'test_employee', 'password': 'test_password'}
        response = self.client.post(reverse('login'), data, format='json')

        self.token = response.data.get('token', '')

    def test_list_amenities_authenticated(self):
        headers = {'Authorization': f'Token {self.token}'}
        response = self.client.get(self.url, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_amenities_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_amenity_authenticated(self):
        data = {'name': 'New Amenity'}
        headers = {'Authorization': f'Token {self.token}'}
        response = self.client.post(self.url, data, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_amenity_unauthenticated(self):
        data = {'name': 'New Amenity'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class AmenityDetailViewTests(APITestCase):
    def setUp(self):
        group = Group.objects.create(name='IT')

        self.employee = Employee.objects.create_user(username='test_employee', password='test_password')
        self.employee.groups.add(group)

        data = {'username': 'test_employee', 'password': 'test_password'}
        response = self.client.post(reverse('login'), data, format='json')

        self.token = response.data.get('token', '')
        self.amenity = Amenity.objects.create(name='Test Amenity')

        self.url = reverse('amenity-detail', args=[self.amenity.uuid])

    def test_retrieve_amenity_authenticated(self):
        headers = {'Authorization': f'Token {self.token}'}
        response = self.client.get(self.url, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_amenity_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_amenity_authenticated(self):
        data = {'name': 'Updated Amenity'}
        headers = {'Authorization': f'Token {self.token}'}
        response = self.client.patch(self.url, data, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_amenity_unauthenticated(self):
        data = {'name': 'Updated Amenity'}
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_amenity_authenticated(self):
        headers = {'Authorization': f'Token {self.token}'}
        response = self.client.delete(self.url, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_amenity_unauthenticated(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class RoomStandardListViewTests(APITestCase):
    def setUp(self):
        self.url = reverse('room-standard-list')
        self.group = Group.objects.create(name='IT')
        self.employee = Employee.objects.create_user(username='test_employee', password='test_password')
        self.employee.groups.add(self.group)

        data = {'username': 'test_employee', 'password': 'test_password'}
        response = self.client.post(reverse('login'), data, format='json')
        self.token = response.data.get('token', '')

        self.amenity = Amenity.objects.create(name='Test Amenity')
        self.room_standard = RoomStandard.objects.create(name='Test Room Standard', price_per_night='100.00')

    def test_list_room_standards_authenticated(self):
        headers = {'Authorization': f'Token {self.token}'}
        response = self.client.get(self.url, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_room_standards_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_room_standard_authenticated(self):
        data_amenity = {'name': 'New Amenity'}
        headers = {'Authorization': f'Token {self.token}'}
        response_amenity = self.client.post(reverse('amenity-list'), data_amenity, headers=headers, format='json')
        self.assertEqual(response_amenity.status_code, status.HTTP_201_CREATED)

        new_amenity_id = response_amenity.data.get('uuid')

        data = {'name': 'New Room Standard', 'price_per_night': '200.00', 'amenities': [new_amenity_id]}
        headers = {'Authorization': f'Token {self.token}'}
        response = self.client.post(self.url, data, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_room_standard_unauthenticated(self):
        data = {'name': 'New Room Standard', 'price_per_night': '200.00'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class RoomStandardDetailViewTests(APITestCase):
    def setUp(self):
        self.group = Group.objects.create(name='IT')
        self.employee = Employee.objects.create_user(username='test_employee', password='test_password')
        self.employee.groups.add(self.group)

        data = {'username': 'test_employee', 'password': 'test_password'}
        response = self.client.post(reverse('login'), data, format='json')
        self.token = response.data.get('token', '')

        self.amenity = Amenity.objects.create(name='Test Amenity')
        self.room_standard = RoomStandard.objects.create(name='Test Room Standard', price_per_night='100.00')

        self.url = reverse('room-standard-detail', args=[self.room_standard.uuid])

    def test_retrieve_room_standard_authenticated(self):
        headers = {'Authorization': f'Token {self.token}'}
        response = self.client.get(self.url, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_room_standard_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_room_standard_authenticated(self):
        data = {'name': 'Updated Room Standard'}
        headers = {'Authorization': f'Token {self.token}'}
        response = self.client.patch(self.url, data, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_room_standard_unauthenticated(self):
        data = {'name': 'Updated Room Standard'}
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_room_standard_authenticated(self):
        headers = {'Authorization': f'Token {self.token}'}
        response = self.client.delete(self.url, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_room_standard_unauthenticated(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class RoomListViewTests(APITestCase):
    def setUp(self):
        self.url = reverse('room-list')

        self.group = Group.objects.create(name='IT')
        self.employee = Employee.objects.create_user(username='test_employee', password='test_password')
        self.employee.groups.add(self.group)

        data = {'username': 'test_employee', 'password': 'test_password'}
        response = self.client.post(reverse('login'), data, format='json')
        self.token = response.data.get('token', '')

        self.room_standard = RoomStandard.objects.create(name='Test Room Standard', price_per_night='100.00')
        self.room = Room.objects.create(room_number='101', room_standard=self.room_standard)

    def test_list_rooms_authenticated(self):
        headers = {'Authorization': f'Token {self.token}'}
        response = self.client.get(self.url, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_rooms_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_room_authenticated(self):
        # Tworzenie nowego standardu pokoju
        data_standard = {'name': 'New Room Standard', 'price_per_night': '200.00'}
        headers = {'Authorization': f'Token {self.token}'}
        response_standard = self.client.post(reverse('room-standard-list'), data_standard, headers=headers, format='json')
        self.assertEqual(response_standard.status_code, status.HTTP_201_CREATED)

        # Pobranie identyfikatora nowego standardu pokoju
        new_room_standard_id = response_standard.data.get('uuid')

        # Tworzenie pokoju z nowym standardem pokoju
        data_room = {'room_number': '102', 'location': 'Poland', 'room_standard': new_room_standard_id}
        response_room = self.client.post(self.url, data_room, headers=headers, format='json')
        self.assertEqual(response_room.status_code, status.HTTP_201_CREATED)

    def test_create_room_unauthenticated(self):
        data = {'room_number': '102'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class RoomDetailViewTests(APITestCase):
    def setUp(self):
        self.group = Group.objects.create(name='IT')
        self.employee = Employee.objects.create_user(username='test_employee', password='test_password')
        self.employee.groups.add(self.group)

        data = {'username': 'test_employee', 'password': 'test_password'}
        response = self.client.post(reverse('login'), data, format='json')
        self.token = response.data.get('token', '')

        self.room_standard = RoomStandard.objects.create(name='Test Room Standard', price_per_night='100.00')
        self.room = Room.objects.create(room_number='101', room_standard=self.room_standard)

        self.url = reverse('room-detail', args=[self.room.uuid])

    def test_retrieve_room_authenticated(self):
        headers = {'Authorization': f'Token {self.token}'}
        response = self.client.get(self.url, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_room_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_room_authenticated(self):
        data = {'room_number': '102'}
        headers = {'Authorization': f'Token {self.token}'}
        response = self.client.patch(self.url, data, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_room_unauthenticated(self):
        data = {'room_number': '102'}
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_room_authenticated(self):
        headers = {'Authorization': f'Token {self.token}'}
        response = self.client.delete(self.url, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_room_unauthenticated(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
