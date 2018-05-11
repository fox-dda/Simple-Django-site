from django.db import models

class GNSSData(models.Model):
    time = models.CharField(max_length=8)
    coordinate = models.CharField(max_length=50)
    date = models.CharField(max_length=15)
    satellitesCount = models.CharField(max_length=2)
    dataFlag = models.CharField(max_length=15)


class DriverStatus(models.Model):
    status = models.CharField(max_length=100)