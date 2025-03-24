
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import AirQualitySensorData
from .serializers import AirQualitySensorDataSerializer
from rest_framework import status
from rest_framework.decorators import api_view


@api_view(['GET'])
def get_all_data(request):
    sensors_data = AirQualitySensorData.objects.all()
    serialized_sensors_data = AirQualitySensorDataSerializer(sensors_data, many=True).data
    return Response(serialized_sensors_data)
    
@api_view(['GET'])
def get_lastets(request):
    sensor_ids = ['sensor_1', 'sensor_2', 'sensor_3', 'sensor_4', 'sensor_5']
    
    latest_data = []
    for sensor_id in sensor_ids:
        latest_entry = AirQualitySensorData.objects.filter(sensor_id=sensor_id).order_by('-timestamp').first()
        if latest_entry:
            latest_data.append(AirQualitySensorDataSerializer(latest_entry).data)
        else:
            latest_data.append({"sensor_id": sensor_id, "message": "Brak danych"})

    return Response(latest_data)

@api_view(['POST'])   
def post_data(request):
    serializer = AirQualitySensorDataSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Dane zostały zapisane."}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)