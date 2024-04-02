from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Client
from .serializers import ClientSerializer
from utils.permissions import HasGroupPermission
from utils.paginators import SmallResultsSetPagination
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

class ClientListView(APIView):
    """
    A view to list all clients or create a new client.
    """
    serializer_class = ClientSerializer
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
        Get a list of paginated clients.

        Example:
        http://localhost:8000/clients?page=2&page_size=20
        """
        clients = Client.objects.all().order_by('name')
        
        paginator = self.pagination_class()
        paginated_clients = paginator.paginate_queryset(clients, request)
        
        serializer = self.serializer_class(paginated_clients, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        """
        Create a new client.

        Required parameters in the request:
        - name: The name of the client (string).
        - email: The email of the client (string).
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClientDetailView(APIView):
    """
    A view to retrieve, update or delete a client instance.
    """
    serializer_class = ClientSerializer
    permission_classes = [HasGroupPermission]
    required_groups = ['IT']

    def get_object(self, uuid):
        """
        Retrieve a client object by its UUID.

        parameters:
         - uuid: The UUID of the client to retrieve (string).

        return: Client object if found, None otherwise.
        """
        try:
            return Client.objects.get(uuid=uuid)
        except Client.DoesNotExist:
            return None

    def get(self, request, uuid):
        """
        Retrieve details of a client by UUID.

        Required parameter in the URL:
        - uuid: The UUID of the client to retrieve (string).
        """
        client = self.get_object(uuid)
        if client:
            serializer = self.serializer_class(client)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, uuid):
        """
        Update a client instance partially.

        Possible parameters in the request:
        - name: The name of the client (string).
        - email: The email of the client (string).
        """
        client = self.get_object(uuid)
        if client:
            serializer = self.serializer_class(client, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, uuid):
        """
        Delete a client by UUID.

        Required parameter in the URL:
        - uuid: The UUID of the client to delete (string).
        """
        client = self.get_object(uuid)
        if client:
            client.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
