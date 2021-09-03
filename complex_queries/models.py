from django.db import models

# Create your models here.
from django.utils.timezone import now


class Competition(models.Model):
    date = models.DateField()
    datetime = models.DateTimeField(default=now)
    distance = models.IntegerField()
    is_win = models.BooleanField(default=False)
    score = models.DecimalField(max_digits=3, decimal_places=2, default=0)