from django.urls import path
from .views import RoomListView, RoomDetailView, RoomStandardListView, RoomStandardDetailView, AmenityListView, AmenityDetailView

urlpatterns = [
    path('', RoomListView.as_view(), name='room-list'),
    path('/<uuid:uuid>', RoomDetailView.as_view(), name='room-detail'),
    path('room-standards', RoomStandardListView.as_view(), name='room-standard-list'),
    path('room-standards/<uuid:uuid>', RoomStandardDetailView.as_view(), name='room-standard-detail'),
    path('amenities', AmenityListView.as_view(), name='amenity-list'),
    path('amenities/<uuid:uuid>', AmenityDetailView.as_view(), name='amenity-detail'),
]
