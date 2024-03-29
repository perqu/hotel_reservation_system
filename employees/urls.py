from django.urls import path
from .views import EmployeeDetailView, EmployeeListView, LoginAPIView

urlpatterns = [
    path('/login', LoginAPIView.as_view(), name='login'),  # URL do widoku logowania
    path('', EmployeeListView.as_view(), name='employee-list'),
    path('/<uuid:uuid>', EmployeeDetailView.as_view(), name='employee-detail'),
]
