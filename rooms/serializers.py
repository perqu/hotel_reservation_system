from rest_framework import serializers
from .models import RoomStandard, Amenity, Room

class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = '__all__'

class RoomStandardSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomStandard
        fields = '__all__'

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
