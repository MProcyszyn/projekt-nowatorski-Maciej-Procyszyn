from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    experience = models.CharField(max_length=100)
    phone_nr = models.CharField(max_length=15)
    EMPLOYEE_GROUP_CHOICES = (
        ('IT', 'IT'),
        ('HR', 'Human Resources'),
        ('MT', 'Maintenance'),
    )
    employee_group = models.CharField(max_length=20, choices=EMPLOYEE_GROUP_CHOICES, default='MT')

    def __str__(self):
        return self.user.username
