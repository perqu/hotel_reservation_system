from django.urls import path
from .views import EmployeeDetailView, EmployeeListView

urlpatterns = [
    path('', EmployeeListView.as_view(), name='employee-list'),
    path('/<uuid:uuid>', EmployeeDetailView.as_view(), name='employee-detail'),
]
