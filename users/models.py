from django.contrib.auth.models import User, Permission
from django.db import models


# Create your models here.
class Module(models.Model):
    module = models.CharField(max_length=100)


class Location(models.Model):
    location_data = models.CharField(max_length=100)


class DataRecord(models.Model):
    data = models.CharField(max_length=100)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
