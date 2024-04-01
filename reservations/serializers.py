from rest_framework import serializers
from .models import Reservation

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

class AvailableRoomsSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()