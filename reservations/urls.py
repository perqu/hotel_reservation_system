from django.urls import path
from .views import ReservationListView, ReservationDetailView, AvailableRoomsView

urlpatterns = [
    path('', ReservationListView.as_view(), name='reservation-list'),
    path('/<uuid:uuid>', ReservationDetailView.as_view(), name='reservation-detail'),
    path('/available', AvailableRoomsView.as_view(), name='available-rooms')
]
