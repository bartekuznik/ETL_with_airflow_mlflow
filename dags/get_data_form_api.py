from datetime import datetime, timedelta
import requests
from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook

doc_md_DAG =""""
### DAG: Fetch and Save Sensor Data from API

    This DAG automates the process of fetching the latest sensor data from an API and storing it in a PostgreSQL database.

    **Workflow:**
    1. **Fetch Data** - Calls an external API (`http://host.docker.internal:8000/api/last/`) to retrieve the latest sensor readings.
    2. **Save Data** - Inserts the retrieved sensor data into the `sensor_data` table in a PostgreSQL database.

    **Schedule:** Runs daily (`@daily`).
"""

default_args ={
    'owner': 'admin',
    'retries': 1,
    'retry_delay': timedelta(minutes=2)
}

@dag(dag_id='get_data_form_api',
    default_args=default_args,
    start_date=datetime(2025, 3, 22),
    schedule_interval='@daily',
    doc_md = doc_md_DAG)
def get_and_save_data():
    
    @task()
    def fetch_data():
        response = requests.get('http://host.docker.internal:8000/api/last/')
        print(response.json())    
        data = response.json()
        for entry in data:
            print(entry['sensor_id'])
            print(entry['timestamp'])
        return data
    
    @task()
    def save_in_database(data):
        pg_hook = PostgresHook(postgres_conn_id='sensors_local')
        conn = pg_hook.get_conn()
        cursor = conn.cursor()

        for entry in data:
            sensor_id = entry['sensor_id']
            timestamp = entry['timestamp']
            temperature = entry['temperature']
            humidity = entry['humidity']
            pm2_5 = entry['pm2_5']
            pm10 = entry['pm10']
            pressure = entry['pressure']

            query = """
            INSERT INTO sensor_data (sensor_id, timestamp, temperature, humidity, pm2_5, pm10, pressure)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (sensor_id, timestamp, temperature, humidity,pm2_5, pm10, pressure))

        conn.commit()
        cursor.close()
        conn.close()

    data = fetch_data()
    save_in_database(data=data)


new_dag = get_and_save_data()
