from rest_framework.test import APITestCase
from rest_framework import status
from clients.models import Client
from reservations.models import Reservation
from rooms.models import Room
from employees.models import Employee
from rooms.models import RoomStandard
from django.contrib.auth.models import Group
from django.urls import reverse
from django.shortcuts import get_object_or_404
import warnings

warnings.filterwarnings('ignore', message="DateTimeField Reservation.start_date received a naive datetime")
warnings.filterwarnings('ignore', message="DateTimeField Reservation.end_date received a naive datetime")

class ReservationListViewTests(APITestCase):
    def setUp(self):
        self.url = reverse('reservation-list')

        group = Group.objects.create(name='IT')

        self.employee = Employee.objects.create_user(username='test_employee', password='test_password')
        self.employee.groups.add(group)

        # Employee
        data_employee = {'username': 'test_employee', 'password': 'test_password'}
        response_employee = self.client.post(reverse('login'), data_employee, format='json')
        self.token = response_employee.data.get('token', '')

        # Room standard
        data_standard = {'name': 'New Room Standard', 'price_per_night': '200.00'}
        headers = {'Authorization': f'Token {self.token}'}
        response_standard = self.client.post(reverse('room-standard-list'), data_standard, headers=headers, format='json')
        room_standard_uuid = response_standard.data.get('uuid')

        # Room
        data_room = {'room_number': '102', 'location': 'Poland', 'room_standard': room_standard_uuid}
        response_room = self.client.post(reverse('room-list'), data_room, headers=headers, format='json')
        self.room_uuid = response_room.data.get('uuid')

        # Client
        data_client = {'name': 'New Client', 'email': 'newclient@example.com'}
        headers = {'Authorization': f'Token {self.token}'}
        response_client = self.client.post(reverse('client-list'), data_client, headers=headers, format='json')
        self.client_uuid = response_client.data.get('uuid')

    def test_list_reservations_authenticated(self):
        headers = {'Authorization': f'Token {self.token}'}
        response = self.client.get(self.url, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_reservations_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_reservation_authenticated(self):
        data = {'client': self.client_uuid, 'room': self.room_uuid, 'start_date': '2024-03-01 12:00:00', 'end_date': '2024-03-07 11:00:00'}
        headers = {'Authorization': f'Token {self.token}'}
        response = self.client.post(self.url, data, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_reservation_unauthenticated(self):
        data = {'client': self.client_uuid, 'room': self.room_uuid, 'start_date': '2024-03-01 12:00:00', 'end_date': '2024-03-07 11:00:00'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class ReservationDetailViewTests(APITestCase):
    def setUp(self):
        group = Group.objects.create(name='IT')

        self.employee = Employee.objects.create_user(username='test_employee', password='test_password')
        self.employee.groups.add(group)

        # Employee
        data_employee = {'username': 'test_employee', 'password': 'test_password'}
        response_employee = self.client.post(reverse('login'), data_employee, format='json')
        self.token = response_employee.data.get('token', '')

        # Room standard
        data_standard = {'name': 'New Room Standard', 'price_per_night': '200.00'}
        headers = {'Authorization': f'Token {self.token}'}
        response_standard = self.client.post(reverse('room-standard-list'), data_standard, headers=headers, format='json')
        room_standard_uuid = response_standard.data.get('uuid')

        # Room
        data_room = {'room_number': '102', 'location': 'Poland', 'room_standard': room_standard_uuid}
        response_room = self.client.post(reverse('room-list'), data_room, headers=headers, format='json')
        room_uuid = response_room.data.get('uuid')
        self.room = get_object_or_404(Room, uuid=room_uuid)

        # Client
        data_client = {'name': 'New Client', 'email': 'newclient@example.com'}
        headers = {'Authorization': f'Token {self.token}'}
        response_client = self.client.post(reverse('client-list'), data_client, headers=headers, format='json')
        client_uuid = response_client.data.get('uuid')
        self.client_object = get_object_or_404(Client, uuid=client_uuid)

        self.reservation = Reservation.objects.create(client=self.client_object, room=self.room, start_date='2024-03-01 12:00:00', end_date='2024-03-08 11:00:00')
        self.url = reverse('reservation-detail', args=[self.reservation.uuid])

    def test_retrieve_reservation_authenticated(self):
        headers = {'Authorization': f'Token {self.token}'}
        response = self.client.get(self.url, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_reservation_unauthenticated(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_reservation_authenticated(self):
        data = {'name': 'Updated Client'}
        headers = {'Authorization': f'Token {self.token}'}
        response = self.client.patch(self.url, data, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_reservation_unauthenticated(self):
        data = {'name': 'Updated Client'}
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_reservation_authenticated(self):
        headers = {'Authorization': f'Token {self.token}'}
        response = self.client.delete(self.url, headers=headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_reservation_unauthenticated(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class AvailableRoomsViewTests(APITestCase):
    def setUp(self):
        # Creating a test user and assigning it to the 'IT' group
        self.employee = Employee.objects.create_user(username='test_employee', password='test_password')
        group = Group.objects.create(name='IT')
        self.employee.groups.add(group)

        # Authenticating the test user and getting the token
        data = {'username': 'test_employee', 'password': 'test_password'}
        response = self.client.post(reverse('login'), data=data, format='json')
        self.token = response.data.get('token', '')

        # Creating a room standard
        room_standard_data = {'name': 'Test Standard', 'price_per_night': '100.00'}
        headers = {'Authorization': f'Token {self.token}'}
        response_standard = self.client.post(reverse('room-standard-list'), data=room_standard_data, headers=headers, format='json')
        self.room_standard_uuid = response_standard.data.get('uuid')

        # Creating a room
        room_data = {'room_number': '101', 'location': 'Test Location', 'room_standard': self.room_standard_uuid, 'is_available': True}
        response_room = self.client.post(reverse('room-list'), data=room_data, headers=headers, format='json')
        self.room_uuid = response_room.data.get('uuid')

        # Creating a client
        client_data = {'name': 'Test Client', 'email': 'test@example.com'}
        response_client = self.client.post(reverse('client-list'), data=client_data, headers=headers, format='json')
        self.client_uuid = response_client.data.get('uuid')

        # Creating a reservation
        reservation_data = {'client': self.client_uuid, 'room': self.room_uuid, 'start_date': '2024-04-01 12:00:00', 'end_date': '2024-04-05 11:00:00'}
        response_reservation = self.client.post(reverse('reservation-list'), data=reservation_data, headers=headers, format='json')

    def test_retrieve_available_rooms_authenticated(self):
        data = {'start_date': '2024-04-02', 'end_date': '2024-04-03', 'room_standard': self.room_standard_uuid}
        headers = {'Authorization': f'Token {self.token}'}
        url = reverse('available-rooms')
        response = self.client.post(url, data=data, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_available_rooms_unauthenticated(self):
        data = {'start_date': '2024-04-02', 'end_date': '2024-04-03', 'room_standard': self.room_standard_uuid}
        url = reverse('available-rooms')
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_available_rooms_with_reservation(self):
        data = {'start_date': '2024-04-02', 'end_date': '2024-04-03', 'room_standard': self.room_standard_uuid}
        headers = {'Authorization': f'Token {self.token}'}
        url = reverse('available-rooms')

        response = self.client.post(url, data=data, headers=headers, format='json')
        available_rooms = response.data['available_rooms']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(any(room['uuid'] == str(self.room_uuid) for room in available_rooms))

    def test_retrieve_available_rooms_without_reservation(self):
        data = {'start_date': '2024-04-06', 'end_date': '2024-04-09', 'room_standard': self.room_standard_uuid}
        headers = {'Authorization': f'Token {self.token}'}
        url = reverse('available-rooms')

        response = self.client.post(url, data=data, headers=headers, format='json')
        available_rooms = response.data['available_rooms']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(room['uuid'] == str(self.room_uuid) for room in available_rooms))

