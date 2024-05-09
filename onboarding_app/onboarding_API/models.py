from django.db import models

# Create your models here.


class Employee(models.Model):
    team = models.CharField(max_length=100)
    experience = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    phone_nr = models.CharField(max_length=15)
