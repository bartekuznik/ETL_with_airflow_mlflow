from datetime import datetime, timedelta
from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import mlflow
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
from sklearn.linear_model import Ridge

default_args ={
    'owner': 'admin',
    'retries': 1,
    'retry_delay': timedelta(minutes=2)
}

@dag(dag_id='etl_dag',
    default_args=default_args,
    start_date=datetime(2025, 3, 22),
    schedule_interval='@daily')
def etl():
    
    @task()
    def extract():
        pg_hook = PostgresHook(postgres_conn_id='sensors_local')
        conn = pg_hook.get_conn()
        query = "SELECT * FROM sensor_data"
        df = pd.read_sql(query, conn, index_col='id')
        conn.close()
        return df
    
    @task()
    def preprocesing(data):
        data = data.dropna()
        data.drop(columns=['timestamp'], inplace=True, axis=1)
        print(data.isnull().sum())
        encoded_data = pd.get_dummies(data['sensor_id']).astype(int)
        data.drop(columns=['sensor_id'], inplace=True, axis=1)
        data_encoded = pd.concat([data, encoded_data], axis=1)
        print(data_encoded)
        return data_encoded


    @task()
    def model_evaluation(data):
        X = data.drop(columns=['temperature'])
        y = data['temperature']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        experiment_name = f"experiment_{current_time}"
        exp = mlflow.set_experiment(experiment_name=experiment_name)

        alpha_values = [0.1, 1.0, 10.0, 100.0]

        for alpha in alpha_values:
            with mlflow.start_run(experiment_id=exp.experiment_id):
                model = Ridge(alpha=alpha)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)

                mae = mean_absolute_error(y_test, y_pred)
                r2 = r2_score(y_test, y_pred)

                print("MAE: ", mae)
                print("R2: ", r2)
                
                mlflow.log_param("alpha", alpha)
                mlflow.log_metric("mae", mae)
                mlflow.log_metric("r2_score", r2)
                mlflow.sklearn.log_model(model, "Ridge"+f'_{alpha}')

    @task()
    def find_best_run():
        experiments = mlflow.search_experiments()
        experiment_ids = [exp.experiment_id for exp in experiments]
        all_runs = mlflow.search_runs(experiment_ids=experiment_ids, order_by=["metrics.mae ASC"])
        best_run = all_runs.iloc[0]
        print(f"Najlepszy model: {best_run['params.alpha']} alpha, MAE={best_run['metrics.mae']}")

    data = extract()
    transformed_data = preprocesing(data)
    model_evaluation(transformed_data) >> find_best_run()
    

    

new_dag = etl()
