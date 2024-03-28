from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Client
from .serializers import ClientSerializer

class ClientListViewTests(APITestCase):
    def setUp(self):
        self.client1 = Client.objects.create(name='John Doe', email='john@example.com')
        self.client2 = Client.objects.create(name='Jane Smith', email='jane@example.com')

    def test_get_client_list(self):
        url = reverse('client-list')
        response = self.client.get(url)
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_client(self):
        url = reverse('client-list')
        data = {'name': 'Alice Wonderland', 'email': 'alice@example.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Client.objects.count(), 3)

class ClientDetailViewTests(APITestCase):
    def setUp(self):
        self.client1 = Client.objects.create(name='John Doe', email='john@example.com')

    def test_get_client_detail(self):
        url = reverse('client-detail', kwargs={'uuid': str(self.client1.uuid)})
        response = self.client.get(url)
        client = Client.objects.get(uuid=self.client1.uuid)
        serializer = ClientSerializer(client)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_client(self):
        url = reverse('client-detail', kwargs={'uuid': str(self.client1.uuid)})
        data = {'name': 'Updated Name', 'email': 'updated@example.com'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_client = Client.objects.get(uuid=self.client1.uuid)
        self.assertEqual(updated_client.name, 'Updated Name')
        self.assertEqual(updated_client.email, 'updated@example.com')

    def test_delete_client(self):
        url = reverse('client-detail', kwargs={'uuid': str(self.client1.uuid)})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Client.objects.filter(uuid=self.client1.uuid).exists())