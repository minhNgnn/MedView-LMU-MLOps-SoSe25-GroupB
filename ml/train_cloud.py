import os
from typing import Annotated, Any

import hydra
import typer
from models import train_model

app = typer.Typer()


@app.command()
def run_training_typer(
    model_name: Annotated[str, typer.Option("--model_name", "-m")] = "simple",
    batch_size: Annotated[int, typer.Option("--batch_size", "-b")] = -1,
    epochs: Annotated[int, typer.Option("--epochs")] = 10,
    wandb_logging: Annotated[bool, typer.Option("--wandb")] = False,
    connect_to_gcs: Annotated[bool, typer.Option("--gcs")] = True,
    num_workers: Annotated[int, typer.Option("--num-workers", "-n")] = -1,
) -> Any:
    print("Starting training pipeline...")

    train_model(model_name, batch_size, epochs, wandb_logging, connect_to_gcs)

    print("Training pipeline completed.")


@hydra.main(version_base=None, config_name="config_cloud.yaml", config_path=f"configs/model")
def run_training_hydra(cfg) -> Any:
    print("Starting training pipeline...")

    os.chdir(hydra.utils.get_original_cwd())
    train_model(
        cfg.hyperparameters.model_name,
        cfg.hyperparameters.batch_size,
        cfg.hyperparameters.epochs,
        cfg.hyperparameters.wandb_logging,
        cfg.hyperparameters.connect_to_gcs,
        cfg.hyperparameters.num_workers,
    )

    print("Training pipeline completed.")


if __name__ == "__main__":
    run_training_hydra()
