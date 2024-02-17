from django.db import models


class Airport(models.Model):
    name = models.CharField(max_length=100)
    closest_big_city = models.CharField(max_length=255)


class AirplaneType(models.Model):
    name = models.CharField(max_length=255)
