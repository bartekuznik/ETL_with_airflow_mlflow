from rest_framework import serializers
from .models import AirQualitySensorData

class AirQualitySensorDataSerializer(serializers.ModelSerializer):
    """
    Serializer for the AirQualitySensorData model.
    """
    class Meta:
        model = AirQualitySensorData
        fields = '__all__'