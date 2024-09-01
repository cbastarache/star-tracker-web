from django.db import models

class Satellite(models.Model):
    catNo = models.IntegerField("Catalog Number", primary_key=True)
    name = models.CharField("Name", max_length=30)
    tle1 = models.CharField("TLE Line 1", max_length=70)
    tle2 = models.CharField("TLE Line 2", max_length=70)
    uplink = models.DecimalField("Radio Uplink Frequency", max_digits=10, decimal_places=5)
    downlink = models.DecimalField("Radio Downlink Frequency", max_digits=10, decimal_places=5)
    classification = models.CharField("Classification", max_length=30)
