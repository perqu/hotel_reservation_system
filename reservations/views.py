from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Reservation
from .serializers import ReservationSerializer, AvailableRoomsSerializer
from utils.permissions import HasGroupPermission
from rooms.models import Room
from rooms.serializers import RoomSerializer

class ReservationListView(APIView):
    serializer_class = ReservationSerializer
    permission_classes = [HasGroupPermission]
    required_groups = ['IT']

    def get(self, request):
        reservations = Reservation.objects.all()
        serializer = self.serializer_class(reservations, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReservationDetailView(APIView):
    serializer_class = ReservationSerializer
    permission_classes = [HasGroupPermission]
    required_groups = ['IT']

    def get_object(self, uuid):
        try:
            return Reservation.objects.get(uuid=uuid)
        except Reservation.DoesNotExist:
            return None

    def get(self, request, uuid):
        reservation = self.get_object(uuid)
        if reservation:
            serializer = self.serializer_class(reservation)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, uuid):
        reservation = self.get_object(uuid)
        if reservation:
            serializer = self.serializer_class(reservation, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, uuid):
        reservation = self.get_object(uuid)
        if reservation:
            reservation.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
    
class AvailableRoomsView(APIView):
    serializer_class = AvailableRoomsSerializer
    permission_classes = [HasGroupPermission]
    required_groups = ['IT']

    def post(self, request):
        available_rooms_serializer = self.serializer_class(data=request.data)
        if not available_rooms_serializer.is_valid():
            return Response(available_rooms_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        start_date = available_rooms_serializer.validated_data['start_date']
        end_date = available_rooms_serializer.validated_data['end_date']

        available_rooms = self.get_available_rooms(start_date, end_date)
        return Response({'available_rooms': available_rooms}, status=status.HTTP_200_OK)

    def get_available_rooms(self, start_date, end_date):
        conflicting_reservations = Reservation.objects.filter(start_date__lte=end_date, end_date__gte=start_date)

        all_rooms = Room.objects.all()
        occupied_rooms = [reservation.room for reservation in conflicting_reservations]
        available_rooms = [room for room in all_rooms if room not in occupied_rooms]
        room_serializer = RoomSerializer(available_rooms, many=True)
        serialized_rooms = room_serializer.data

        return serialized_rooms
