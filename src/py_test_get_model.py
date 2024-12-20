from mlflow.client import MlflowClient
# Create an MLflow client
client = MlflowClient(tracking_uri="file:mlruns")
# Get the last model version of an experiment
experiment_name = "Velib"
experiment = client.get_experiment_by_name(experiment_name)
latest_run = client.search_runs(experiment_ids=[experiment.experiment_id], order_by=["start_time DESC"], max_results=1)[0]
model_uri = f"runs:/{latest_run.info.run_id}/model"
print(f"Model URI: {model_uri}")