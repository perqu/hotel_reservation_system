from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Reservation
from .serializers import ReservationSerializer, AvailableRoomsSerializer
from utils.permissions import HasGroupPermission
from rooms.models import Room
from rooms.serializers import RoomSerializer
from utils.paginators import SmallResultsSetPagination
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

class ReservationListView(APIView):
    """
    A view to list all reservations or create a new reservation.
    """
    serializer_class = ReservationSerializer
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
        Get a list of paginated reservations.

        Example:
        http://localhost:8000/reservations?page=2&page_size=20
        """
        reservations = Reservation.objects.all().order_by('start_date')

        paginator = self.pagination_class()
        paginated_reservations = paginator.paginate_queryset(reservations, request)
        
        serializer = self.serializer_class(paginated_reservations, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        """
        Create a new reservation.

        Required parameters in the request:
        - client: The UUID of the client for the reservation (string).
        - room: The UUID of the room for the reservation (string).
        - start_date: The start date and time of the reservation (datetime, format: YYYY-MM-DDThh:mm:ss).
        - end_date: The end date and time of the reservation (datetime, format: YYYY-MM-DDThh:mm:ss).
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReservationDetailView(APIView):
    """
    A view to retrieve, update or delete a reservation instance.
    """
    serializer_class = ReservationSerializer
    permission_classes = [HasGroupPermission]
    required_groups = ['IT']

    def get_object(self, uuid):
        """
        Retrieve a reservation object by its UUID.

        parameters:
         - uuid: The UUID of the reservation to retrieve (string).

        return: Reservation object if found, None otherwise.
        """
        try:
            return Reservation.objects.get(uuid=uuid)
        except Reservation.DoesNotExist:
            return None

    def get(self, request, uuid):
        """
        Retrieve details of a reservation by UUID.

        Required parameter in the URL:
        - uuid: The UUID of the reservation to retrieve (string).
        """
        reservation = self.get_object(uuid)
        if reservation:
            serializer = self.serializer_class(reservation)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, uuid):
        """
        Update a reservation instance partially.

        Possible parameters in the request:
        - client: The UUID of the client (string).
        - room: The UUID of the room (string).
        - start_date: The start date and time of the reservation (datetime).
        - end_date: The end date and time of the reservation (datetime).
        """
        reservation = self.get_object(uuid)
        if reservation:
            serializer = self.serializer_class(reservation, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, uuid):
        """
        Delete a reservation by UUID.

        Required parameter in the URL:
        - uuid: The UUID of the reservation to delete (string).
        """
        reservation = self.get_object(uuid)
        if reservation:
            reservation.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
    
class AvailableRoomsView(APIView):
    """
    A view to retrieve available rooms for a given date range.
    """
    serializer_class = AvailableRoomsSerializer
    permission_classes = [HasGroupPermission]
    required_groups = ['IT']

    def post(self, request):
        """
        Retrieve available rooms for a given date range.

        Required parameters in the request:
        - start_date: The start date of the date range (datetime).
        - end_date: The end date of the date range (datetime).
        - room_standard: The standard of the room to filter available rooms(UUID).
        """
        available_rooms_serializer = self.serializer_class(data=request.data)
        if not available_rooms_serializer.is_valid():
            return Response(available_rooms_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        start_date = available_rooms_serializer.validated_data['start_date']
        end_date = available_rooms_serializer.validated_data['end_date']
        room_standard = available_rooms_serializer.validated_data['room_standard']

        available_rooms = self.get_available_rooms(start_date, end_date, room_standard)
        return Response({'available_rooms': available_rooms}, status=status.HTTP_200_OK)

    def get_available_rooms(self, start_date, end_date, room_standard):
        """
        Retrieve available rooms for a given date range.

        This method queries the database to retrieve available rooms for the specified date range
        and room standard.

        Args:
            start_date: The start date of the date range.
            end_date: The end date of the date range.
            room_standard: The standard of the room to filter available rooms.

        Returns:
            A list of available rooms and their details.
        """
        conflicting_reservations = Reservation.objects.filter(start_date__lte=end_date, end_date__gte=start_date)

        all_rooms = Room.objects.all().filter(room_standard = room_standard, is_available=True)
        occupied_rooms = [reservation.room for reservation in conflicting_reservations]
        available_rooms = [room for room in all_rooms if room not in occupied_rooms]
        room_serializer = RoomSerializer(available_rooms, many=True)
        serialized_rooms = room_serializer.data

        return serialized_rooms
