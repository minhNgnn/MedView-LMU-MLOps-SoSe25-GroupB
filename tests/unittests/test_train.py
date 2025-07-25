# tests/test_train.py

import os
import sys
import types

import pytest
import wandb
from omegaconf import OmegaConf
from typer.testing import CliRunner

import ml.train as train_module
from ml.train import app

# --- Stub heavy dependencies before importing project modules ---
# Stub ultralytics module and YOLO class
ultra = types.ModuleType("ultralytics")
ultra.YOLO = lambda *args, **kwargs: None
sys.modules["ultralytics"] = ultra

# Stub wandb.integration.ultralytics for add_wandb_callback import
stub_integration = types.ModuleType("wandb.integration.ultralytics")
stub_integration.add_wandb_callback = lambda m: None
sys.modules["wandb.integration.ultralytics"] = stub_integration

# Stub PIL._imaging for ultralytics internals
sys.modules["PIL._imaging"] = types.ModuleType("PIL._imaging")
# Stub PIL.Image so PIL import succeeds
pil_img = types.ModuleType("PIL.Image")
pil_img.Image = object
sys.modules["PIL.Image"] = pil_img

runner = CliRunner()


# Fixture to stub train_model
@pytest.fixture(autouse=True)
def stub_train_model(monkeypatch):
    calls = {}

    def fake_train_model(model_name, batch_size, epochs, wandb_logging, connect_to_gcs=None, num_workers=None):
        calls["args"] = (model_name, batch_size, epochs, wandb_logging, connect_to_gcs, num_workers)
        return {"success": True, "received": {"epochs": epochs, "batch": batch_size, "project": "ml/models/"}}

    monkeypatch.setattr(train_module, "train_model", fake_train_model)
    return calls


def test_run_training_typer_defaults(stub_train_model):
    result = runner.invoke(app, [])
    assert result.exit_code == 0
    # The output uses a unicode ellipsis (U+2026)
    assert "Starting training pipeline…" in result.stdout
    assert stub_train_model["args"] == ("simple", -1, 10, False, False, -1)


def test_run_training_typer_with_flags(stub_train_model):
    args = ["--model_name", "foo", "-b", "4", "--epochs", "2", "--wandb"]
    result = runner.invoke(app, args)
    assert result.exit_code == 0
    assert "Training pipeline completed." in result.stdout
    assert stub_train_model["args"] == ("foo", 4, 2, True, False, -1)


def test_run_training_hydra(monkeypatch, tmp_path, stub_train_model):
    base_fn = train_module.run_training_hydra.__wrapped__
    monkeypatch.setattr(train_module.hydra.utils, "get_original_cwd", lambda: str(tmp_path))
    cfg = OmegaConf.create(
        {
            "hyperparameters": {
                "model_name": "bar",
                "batch_size": 7,
                "epochs": 3,
                "wandb_logging": True,
                "connect_to_gcs": False,
                # num_workers intentionally omitted to test default
            }
        }
    )
    base_fn(cfg)
    assert stub_train_model["args"] == ("bar", 7, 3, True, False, 2)
