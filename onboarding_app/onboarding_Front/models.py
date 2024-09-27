from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class EmployeeUser(models.Model):
    employee = models.OneToOneField(User, on_delete=models.CASCADE)
    EMPLOYEE_GROUP_CHOICES = (
        ('IT', 'IT'),
        ('HR', 'Human Resources'),
        ('MT', 'Maintenance'),
    )
    employee_group = models.CharField(max_length=20, choices=EMPLOYEE_GROUP_CHOICES, default='MT')

    def __str__(self):
        return self.employee.username
