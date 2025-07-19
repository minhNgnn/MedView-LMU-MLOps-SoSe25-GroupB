#!/usr/bin/env python
import os
from typing import Any

import hydra
import torch
import torch.distributed as dist
import torch.multiprocessing as mp
from hydra.utils import get_original_cwd

from ml.models import train_model


def init_distributed(rank: int, world_size: int, backend: str = "gloo") -> None:
    """
    Initialize the default process group for DDP.
    """
    os.environ["MASTER_ADDR"] = "127.0.0.1"
    os.environ["MASTER_PORT"] = "29500"
    dist.init_process_group(backend=backend, rank=rank, world_size=world_size)
    torch.manual_seed(42)
    if torch.cuda.is_available():
        torch.cuda.set_device(rank % torch.cuda.device_count())


def worker(rank: int, world_size: int, cfg: Any, root_dir: str) -> None:
    """
    Entry point for each DDP worker process.
    """
    # 1) Initialize the process group
    init_distributed(rank, world_size, backend=cfg.distributed.backend)

    # 2) Return to project root (Hydra changes cwd)
    os.chdir(root_dir)

    # 3) Call the shared train_model (no rank/world_size args needed)
    train_model(
        cfg.hyperparameters.model_name,
        cfg.hyperparameters.batch_size,
        cfg.hyperparameters.epochs,
        cfg.hyperparameters.wandb_logging,
        cfg.hyperparameters.num_workers,
    )

    # 4) Clean up
    dist.destroy_process_group()


@hydra.main(version_base=None, config_name="config.yaml", config_path="configs/model")
def main(cfg: Any) -> None:
    """
    Hydra-powered entrypoint to spawn DDP workers.
    """
    # Capture the original working directory
    root_dir = get_original_cwd()

    # Number of processes = number of replicas
    world_size = cfg.distributed.world_size

    # Spawn worker processes
    mp.spawn(worker, args=(world_size, cfg, root_dir), nprocs=world_size, join=True)


if __name__ == "__main__":
    main()
