import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib import admin

class UUIDModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True

class CustomGroup(UUIDModel):
    name = models.CharField(max_length=150, unique=True)

    class Meta:
        verbose_name = 'group'
        verbose_name_plural = 'groups'

    def __str__(self):
        return self.name

class CustomPermission(UUIDModel):
    name = models.CharField(max_length=255)
    codename = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'permission'
        verbose_name_plural = 'permissions'

    def __str__(self):
        return self.name

class Employee(AbstractUser, UUIDModel):
    position = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    hire_date = models.DateField(null=True, default=None)
    date_of_termination = models.DateField(blank=True, null=True)
    employee_groups = models.ManyToManyField(CustomGroup, related_name='employees', blank=True)
    employee_permissions = models.ManyToManyField(CustomPermission, related_name='employees', blank=True)

    class Meta:
        verbose_name = "Employee"
        verbose_name_plural = "Employees"

    def __str__(self):
        return self.username
