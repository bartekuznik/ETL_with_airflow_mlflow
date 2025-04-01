from django.db import models

class AirQualitySensorData(models.Model):
    """
    Model representing air quality sensor data.
    """
    sensor_id = models.CharField(max_length=100) 
    timestamp = models.DateTimeField(auto_now_add=True)
    temperature = models.FloatField(null=True, blank=True) 
    humidity = models.FloatField(null=True, blank=True) 
    pm2_5 = models.FloatField(null=True, blank=True)  
    pm10 = models.FloatField(null=True, blank=True) 
    pressure = models.FloatField(null=True, blank=True) 