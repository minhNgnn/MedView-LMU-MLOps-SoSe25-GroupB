from typing import Annotated

import typer
from features import engineer_features, select_features

from data import clean_data, load_raw_data, split_data
from models import save_model, train_model

app = typer.Typer()


@app.command()
def run_training_pipeline(
    model_name: Annotated[str, typer.Option("--model_name", "-m")] = "yolov8n",
    epoch: Annotated[int, typer.Option("--epoch")] = 10,
):
    print("Starting training pipeline...")

    # 1. Load Data
    # raw_data = load_raw_data(data_path)
    # cleaned_data = clean_data(raw_data)

    # 2. Feature Engineering
    # features = engineer_features(cleaned_data)
    # X = select_features(features) # Assuming select_features returns X_train for simplicity
    # y = features['Outcome'] # Placeholder for target data

    ## 2-1. Split Data
    # X_train , X_test , y_train , y_test = split_data(X, y, test_size=0.3, random_state=random_state)

    # 3. Model Training
    # model_params = {"learning_rate": 0.01, "n_estimators": 100}
    trained_model = train_model(model_name, epoch)

    # 4. Save Model
    # save_model(trained_model, model_output_path)

    print("Training pipeline completed.")


if __name__ == "__main__":
    # MODEL_NAME = "yolov8n"
    # EPOCH = 5
    # run_training_pipeline(MODEL_NAME, EPOCH)
    app()
