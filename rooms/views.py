from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Amenity, RoomStandard, Room
from .serializers import AmenitySerializer, RoomStandardSerializer, RoomSerializer
from utils.permissions import HasGroupPermission
from utils.paginators import SmallResultsSetPagination
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

class AmenityListView(APIView):
    """
    A view to list all amenities or create a new amenity.
    """
    serializer_class = AmenitySerializer
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
        Get a list of paginated amenities.

        Example:
        http://localhost:8000/amenities?page=2&page_size=20
        """
        amenities = Amenity.objects.all().order_by('name')

        paginator = self.pagination_class()
        paginated_amenities = paginator.paginate_queryset(amenities, request)

        serializer = self.serializer_class(paginated_amenities, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        """
        Create a new amenity.

        Required parameters in the request:
        - name: The name of the amenity (string).
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AmenityDetailView(APIView):
    """
    A view to retrieve, update or delete an amenity instance.
    """
    serializer_class = AmenitySerializer
    permission_classes = [HasGroupPermission]
    required_groups = ['IT']
    
    def get_object(self, uuid):
        """
        Retrieve an amenity object by its UUID.

        parameters:
         - uuid: The UUID of the amenity to retrieve (string).

        return: Amenity object if found, None otherwise.
        """
        try:
            return Amenity.objects.get(uuid=uuid)
        except Amenity.DoesNotExist:
            return None

    def get(self, request, uuid):
        """
        Retrieve details of an amenity by UUID.

        Required parameter in the URL:
        - uuid: The UUID of the amenity to retrieve (string).
        """
        amenity = self.get_object(uuid)
        if amenity:
            serializer = self.serializer_class(amenity)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, uuid):
        """
        Update an amenity instance partially.

        Possible parameters in the request:
        - name: The name of the amenity (string).
        """
        amenity = self.get_object(uuid)
        if amenity:
            serializer = self.serializer_class(amenity, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, uuid):
        """
        Delete an amenity by UUID.

        Required parameter in the URL:
        - uuid: The UUID of the amenity to delete (string).
        """
        amenity = self.get_object(uuid)
        if amenity:
            amenity.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

class RoomStandardListView(APIView):
    """
    A view to list all room standards or create a new room standard.
    """
    serializer_class = RoomStandardSerializer
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
        Get a list of paginated room standards.

        Example:
        http://localhost:8000/room-standards?page=2&page_size=20
        """
        room_standards = RoomStandard.objects.all().order_by('name')

        paginator = self.pagination_class()
        paginated_room_standards = paginator.paginate_queryset(room_standards, request)

        serializer = self.serializer_class(paginated_room_standards, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        """
        Create a new room standard.

        Required parameters in the request:
        - name: The name of the room standard (string).
        - description: The description of the room standard (string).
        - amenities: List of amenities associated with the room standard (list of strings).
        - price_per_night: The price per night for the room standard (float).
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RoomStandardDetailView(APIView):
    """
    A view to retrieve, update or delete a room standard instance.
    """
    serializer_class = RoomStandardSerializer
    permission_classes = [HasGroupPermission]
    required_groups = ['IT']
    
    def get_object(self, uuid):
        """
        Retrieve a room standard object by its UUID.

        parameters:
         - uuid: The UUID of the room standard to retrieve (string).

        return: RoomStandard object if found, None otherwise.
        """
        try:
            return RoomStandard.objects.get(uuid=uuid)
        except RoomStandard.DoesNotExist:
            return None

    def get(self, request, uuid):
        """
        Retrieve details of a room standard by UUID.

        Required parameter in the URL:
        - uuid: The UUID of the room standard to retrieve (string).
        """
        room_standard = self.get_object(uuid)
        if room_standard:
            serializer = self.serializer_class(room_standard)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, uuid):
        """
        Update a room standard instance partially.

        Possible parameters in the request:
        - name: The name of the room standard (string).
        - description: The description of the room standard (string).
        - amenities: List of amenities associated with the room standard (list of strings).
        - price_per_night: The price per night for the room standard (float).
        """
        room_standard = self.get_object(uuid)
        if room_standard:
            serializer = self.serializer_class(room_standard, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, uuid):
        """
        Delete a room standard by UUID.

        Required parameter in the URL:
        - uuid: The UUID of the room standard to delete (string).
        """
        room_standard = self.get_object(uuid)
        if room_standard:
            room_standard.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

class RoomListView(APIView):
    """
    A view to list all rooms or create a new room.
    """
    serializer_class = RoomSerializer
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
        Get a list of paginated rooms.

        Example:
        http://localhost:8000/rooms?page=2&page_size=20
        """
        rooms = Room.objects.all().order_by('room_number')

        paginator = self.pagination_class()
        paginated_rooms = paginator.paginate_queryset(rooms, request)

        serializer = self.serializer_class(paginated_rooms, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        """
        Create a new room.

        Required parameters in the request:
        - room_number: The room number (string).
        - room_standard: The UUID of the room standard associated with the room (string).
        - is_available: Availability status of the room (boolean).
        - location: The location description of the room (string).
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RoomDetailView(APIView):
    """
    A view to retrieve, update or delete a room instance.
    """
    serializer_class = RoomSerializer
    permission_classes = [HasGroupPermission]
    required_groups = ['IT']
    
    def get_object(self, uuid):
        """
        Retrieve a room object by its UUID.

        parameters:
         - uuid: The UUID of the room to retrieve (string).

        return: Room object if found, None otherwise.
        """
        try:
            return Room.objects.get(uuid=uuid)
        except Room.DoesNotExist:
            return None

    def get(self, request, uuid):
        """
        Retrieve details of a room by UUID.

        Required parameter in the URL:
        - uuid: The UUID of the room to retrieve (string).
        """
        room = self.get_object(uuid)
        if room:
            serializer = self.serializer_class(room)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, uuid):
        """
        Update a room instance partially.

        Possible parameters in the request:
        - room_number: The room number (string).
        - room_standard: The UUID of the room standard associated with the room (string).
        - is_available: Availability status of the room (boolean).
        - location: The location description of the room (string).
        """
        room = self.get_object(uuid)
        if room:
            serializer = self.serializer_class(room, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, uuid):
        """
        Delete a room by UUID.

        Required parameter in the URL:
        - uuid: The UUID of the room to delete (string).
        """
        room = self.get_object(uuid)
        if room:
            room.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
