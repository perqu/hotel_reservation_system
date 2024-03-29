import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import Group

class Employee(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    position = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    hire_date = models.DateField(null=True, default=None)
    date_of_termination = models.DateField(blank=True, null=True)
    groups = models.ManyToManyField(Group, related_name='employees', blank=True)
    password = models.CharField(max_length=128, blank=False)

    class Meta:
        verbose_name = "Employee"
        verbose_name_plural = "Employees"

    def __str__(self):
        return self.username
