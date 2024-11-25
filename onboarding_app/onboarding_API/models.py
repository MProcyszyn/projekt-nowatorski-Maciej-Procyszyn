from django.db import models
from django.contrib.auth.models import User, Group
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta


class EmployeeGroup(models.Model):
    name = models.CharField(max_length=50, unique=True)
    group_id = models.IntegerField(unique=True)

    def __str__(self):
        return self.name


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    experience = models.CharField(max_length=100, blank=True, null=True)
    phone_nr = models.CharField(max_length=15, blank=True, null=True)
    employee_group = models.ForeignKey(EmployeeGroup, on_delete=models.SET_NULL, null=True, blank=True)
    hire_date = models.DateField(default=date.today)

    def __str__(self):
        return self.user.username


class Training(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    validity_period = models.PositiveIntegerField()     # In months

    def __str__(self):
        return self.name


class EmployeeTraining(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="trainings")
    training = models.ForeignKey(Training, on_delete=models.CASCADE, related_name="employees")
    completion_date = models.DateField()
    expiration_date = models.DateField()
    is_done = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.completion_date and self.training.validity_period:
            self.expiration_date = self.completion_date + relativedelta(months=self.training.validity_period)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee} - {self.training}"
