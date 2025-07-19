import os
from typing import Annotated, Any

import hydra
import typer
from models import train_model

from ml.models import train_model

app = typer.Typer()


@app.command()
def run_training_typer(
    model_name: Annotated[str, typer.Option("--model_name", "-m")] = "simple",
    batch_size: Annotated[int, typer.Option("--batch_size", "-b")] = -1,
    epochs: Annotated[int, typer.Option("--epochs")] = 10,
    wandb_logging: Annotated[bool, typer.Option("--wandb", "-w")] = False,
    connect_to_gcs: Annotated[bool, typer.Option("--gcs")] = False,
    num_workers: Annotated[int, typer.Option("--num-workers", "-n")] = -1,
) -> Any:
    """Run training via Typer CLI."""
    print("Starting training pipeline…")
    train_model(model_name, batch_size, epochs, wandb_logging, connect_to_gcs, num_workers)
    print("Training pipeline completed.")


@hydra.main(version_base=None, config_name="config.yaml", config_path="configs/model")
def run_training_hydra(cfg) -> Any:
    """Run training via Hydra."""
    print("Starting training pipeline…")
    # Ensure we’re back in the project root (not Hydra’s run directory)
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
    # Default to Hydra entrypoint if called as a script
    run_training_typer()
