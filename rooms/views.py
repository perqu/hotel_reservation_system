from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Amenity, RoomStandard, Room
from .serializers import AmenitySerializer, RoomStandardSerializer, RoomSerializer
from utils.permissions import HasGroupPermission

class AmenityListView(APIView):
    permission_classes = [HasGroupPermission]
    required_groups = ['IT']

    def get(self, request):
        amenities = Amenity.objects.all()
        serializer = AmenitySerializer(amenities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AmenityDetailView(APIView):
    permission_classes = [HasGroupPermission]
    required_groups = ['IT']
    
    def get_object(self, uuid):
        try:
            return Amenity.objects.get(uuid=uuid)
        except Amenity.DoesNotExist:
            return None

    def get(self, request, uuid):
        amenity = self.get_object(uuid)
        if amenity:
            serializer = AmenitySerializer(amenity)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, uuid):
        amenity = self.get_object(uuid)
        if amenity:
            serializer = AmenitySerializer(amenity, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, uuid):
        amenity = self.get_object(uuid)
        if amenity:
            amenity.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

class RoomStandardListView(APIView):
    permission_classes = [HasGroupPermission]
    required_groups = ['IT']

    def get(self, request):
        room_standards = RoomStandard.objects.all()
        serializer = RoomStandardSerializer(room_standards, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RoomStandardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RoomStandardDetailView(APIView):
    permission_classes = [HasGroupPermission]
    required_groups = ['IT']
    
    def get_object(self, uuid):
        try:
            return RoomStandard.objects.get(uuid=uuid)
        except RoomStandard.DoesNotExist:
            return None

    def get(self, request, uuid):
        room_standard = self.get_object(uuid)
        if room_standard:
            serializer = RoomStandardSerializer(room_standard)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, uuid):
        room_standard = self.get_object(uuid)
        if room_standard:
            serializer = RoomStandardSerializer(room_standard, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, uuid):
        room_standard = self.get_object(uuid)
        if room_standard:
            room_standard.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
    
class RoomListView(APIView):
    permission_classes = [HasGroupPermission]
    required_groups = ['IT']

    def get(self, request):
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RoomDetailView(APIView):
    permission_classes = [HasGroupPermission]
    required_groups = ['IT']
    
    def get_object(self, uuid):
        try:
            return Room.objects.get(uuid=uuid)
        except Room.DoesNotExist:
            return None

    def get(self, request, uuid):
        room = self.get_object(uuid)
        if room:
            serializer = RoomSerializer(room)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, uuid):
        room = self.get_object(uuid)
        if room:
            serializer = RoomSerializer(room, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, uuid):
        room = self.get_object(uuid)
        if room:
            room.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)