from rest_framework import serializers
from .models import RoomStandard, Amenity, Room

class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = '__all__'

class RoomStandardSerializer(serializers.ModelSerializer):
    amenities = AmenitySerializer(many=True, read_only=True)

    class Meta:
        model = RoomStandard
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    room_standard = RoomStandardSerializer()

    class Meta:
        model = Room
        fields = '__all__'
