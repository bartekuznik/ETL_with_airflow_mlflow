# Dungeon Crawler Game with Dynamic Soundtrack Generation

## Table of Contents

1. [Project Overview](#project-overview)
2. [Technologies](#technologies)
3. [Installation Instructions](#installation-instructions)


## Project Overview

This project is a data pipeline designed to automate the process of collecting data from an external API and later analyzing it. The first part of the project focuses on ensuring data is available for further analysis:

- Implementing an API using Django Rest Framework, simulating an external source collecting logs from air quality sensors.

- Implementing a log generator that can run at a chosen frequency.

The second part involves implementing three DAGs using Apache Airflow:

- DAG database_creation: A one-time task to create a database for storing logs.

- DAG get_data_from_api: A task that fetches data from the API at a chosen frequency and stores it in the previously created database.

- DAG etl_dag: A task that performs data preprocessing, trains a model, and uses MLflow to identify the parameters for which the model made predictions with the lowest Mean Absolute Error.

## Technologies

- Python 3.12.1
- Mlflow 2.20.1
- Apache Airflow 2.10.5
- Django 5.0
- pandas 2.2.3
- scikit-learn 1.6.1

## Installation

To run the project locally, you need to have an environment with Apache Airflow. Instructions for setting it up can be found at this link:

```
https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html
```

Once you've set up the Docker environment, follow these steps:

1. Clone the repository:

```
git clone https://github.com/bartekuznik/ETL_with_airflow_mlflow.git
```

2. Start the Docker containers:

```
docker-compose up -d
```

3. Run sensor API (Django server):

```
python manage.py runserver
```

4. Run the sensor logs generator:

```
python generator.py
```

