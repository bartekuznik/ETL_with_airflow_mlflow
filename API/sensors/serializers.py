from rest_framework import serializers
from .models import AirQualitySensorData

class AirQualitySensorDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirQualitySensorData
        fields = '__all__'