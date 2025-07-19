import os
from typing import Annotated, Any
<<<<<<< Updated upstream

import hydra
import typer

from models import train_model
from typing import Annotated
import typer
import hydra
=======

import hydra
import typer

from ml.models import train_model
>>>>>>> Stashed changes

from ml.models import train_model

app = typer.Typer()


@app.command()
def run_training_typer(
<<<<<<< Updated upstream
    model_name:    Annotated[str,  typer.Option("--model_name", "-m")] = "simple",
    batch_size:    Annotated[int,  typer.Option("--batch_size", "-b")] = -1,
    epochs:        Annotated[int,  typer.Option("--epochs")]           = 10,
    wandb_logging: Annotated[bool, typer.Option("--wandb", "-w")]      = False,
    num_workers:   Annotated[int,  typer.Option("--num-workers", "-n")] = -1,
) -> Any:
    """Run training via Typer CLI."""
    print("Starting training pipeline…")
    train_model(
        model_name,
        batch_size,
        epochs,
        wandb_logging,
        num_workers
    )
=======
    model_name: Annotated[str, typer.Option("--model_name", "-m")] = "simple",
    batch_size: Annotated[int, typer.Option("--batch_size", "-b")] = -1,
    epochs: Annotated[int, typer.Option("--epochs")] = 10,
    wandb_logging: Annotated[bool, typer.Option("--wandb", "-w")] = False,
) -> Any:
    print("Starting training pipeline...")

    train_model(model_name, batch_size, epochs, wandb_logging)

>>>>>>> Stashed changes
    print("Training pipeline completed.")


@hydra.main(version_base=None, config_name="config.yaml", config_path="configs/model")
def run_training_hydra(cfg) -> Any:
<<<<<<< Updated upstream
    """Run training via Hydra."""
    print("Starting training pipeline…")
    # Ensure we’re back in the project root (not Hydra’s run directory)
=======
    print("Starting training pipeline...")

>>>>>>> Stashed changes
    os.chdir(hydra.utils.get_original_cwd())
    train_model(
        cfg.hyperparameters.model_name,
        cfg.hyperparameters.batch_size,
        cfg.hyperparameters.epochs,
        cfg.hyperparameters.wandb_logging,
<<<<<<< Updated upstream
        cfg.hyperparameters.num_workers,
=======
>>>>>>> Stashed changes
    )

    print("Training pipeline completed.")


if __name__ == "__main__":
<<<<<<< Updated upstream
    # Default to Hydra entrypoint if called as a script
    run_training_hydra()

=======
    run_training_hydra()
>>>>>>> Stashed changes
