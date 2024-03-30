import uuid
from django.db import models

class Amenity(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Amenity"
        verbose_name_plural = "Amenities"

    def __str__(self):
        return self.name
    
class RoomStandard(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    amenities = models.ManyToManyField('Amenity', related_name='room_standards', blank=True)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Room Standard"
        verbose_name_plural = "Room Standards"

    def __str__(self):
        return self.name
    
class Room(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room_number = models.CharField(max_length=10)
    room_standard = models.ForeignKey(RoomStandard, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    location = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"

    def __str__(self):
        return f"Room {self.room_number} ({self.room_standard.name})"
