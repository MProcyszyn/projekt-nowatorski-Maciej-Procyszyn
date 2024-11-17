from django.db import models
from django.contrib.auth.models import User, Group


class EmployeeGroup(models.Model):
    name = models.CharField(max_length=50, unique=True)
    group_id = models.IntegerField(unique=True)

    def __str__(self):
        return self.name


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    experience = models.CharField(max_length=100, blank=True, null=True)
    phone_nr = models.CharField(max_length=15, blank=True, null=True)
    employee_group = models.ForeignKey(EmployeeGroup, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username
