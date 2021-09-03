from django.db import models

# Create your models here.
class Competition(models.Model):
    date = models.DateField()
    distance = models.IntegerField()