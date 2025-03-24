import random
from apscheduler.schedulers.background import BackgroundScheduler
import requests


def generate_air_quality_data():
    print("Generating air quality data...")
    def maybe_none(value, chance=0.02):
        value = random.random()
        if value > chance:
            return value
        else:
            return None

    sensor_ids = ['sensor_1', 'sensor_2', 'sensor_3', 'sensor_4', 'sensor_5']

    for sensor_id in sensor_ids:
        new_data = {
            'sensor_id':sensor_id,
            'temperature':maybe_none(random.uniform(10.0, 30.0)),
            'humidity':maybe_none(random.uniform(30.0, 80.0)),
            'pm2_5':maybe_none(random.uniform(5.0, 50.0)),
            'pm10':maybe_none(random.uniform(10.0, 100.0)),
            'pressure':maybe_none(random.uniform(980, 1050)),
        }
            
        print(f"Generated data for {sensor_id}: {new_data}")

        response = requests.post("http://localhost:8000/api/add/", json=new_data)
        
        if response.status_code == 201:
            print(f"Dane dla {sensor_id} zostały zapisane.")
        else:
            print(f"Błąd podczas zapisywania danych dla {sensor_id}: {response.text}")

scheduler = BackgroundScheduler()
scheduler.add_job(generate_air_quality_data, 'interval', minutes=1)
scheduler.start()
scheduler._thread.join()