from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Client
from .serializers import ClientSerializer
from utils.permissions import HasGroupPermission


class ClientListView(APIView):
    serializer_class = ClientSerializer
    permission_classes = [HasGroupPermission]
    required_groups = ['IT']

    def get(self, request):
        clients = Client.objects.all()
        serializer = self.serializer_class(clients, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClientDetailView(APIView):
    serializer_class = ClientSerializer
    permission_classes = [HasGroupPermission]
    required_groups = ['IT']

    def get_object(self, uuid):
        try:
            return Client.objects.get(uuid=uuid)
        except Client.DoesNotExist:
            return None

    def get(self, request, uuid):
        client = self.get_object(uuid)
        if client:
            serializer = self.serializer_class(client)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, uuid):
        client = self.get_object(uuid)
        if client:
            serializer = self.serializer_class(client, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, uuid):
        client = self.get_object(uuid)
        if client:
            client.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
