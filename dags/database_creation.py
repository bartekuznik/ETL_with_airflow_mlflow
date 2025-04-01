from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator 

doc_md_DAG = """
### DAG for Creating a Sensor Data Table in PostgreSQL  

This DAG is designed to create a database table that stores data received from a sensor API.  
It runs only once (`@once`) and ensures the table exists before inserting any data.  
"""

default_args ={
    'owner': 'admin',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}


with DAG(
    dag_id='database_creation',
    default_args=default_args,
    start_date=datetime(2025, 3, 22),
    schedule_interval='@once',
    doc_md=doc_md_DAG
) as dag:
    task1 = SQLExecuteQueryOperator(
        task_id='database_creation_task',
        conn_id="sensors_local",
        sql="""
            create table if not exists sensor_data (
                id SERIAL PRIMARY KEY,
                sensor_id VARCHAR(100) NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                temperature DOUBLE PRECISION NULL,
                humidity DOUBLE PRECISION NULL,
                pm2_5 DOUBLE PRECISION NULL,
                pm10 DOUBLE PRECISION NULL,
                pressure DOUBLE PRECISION NULL
            )
        """
    )
    task1 

