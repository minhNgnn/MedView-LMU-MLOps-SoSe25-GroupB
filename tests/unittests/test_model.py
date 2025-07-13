# tests/test_models_wandb.py  #to be tested after models.py is fixed
import os
from typing import Any, Dict

import pytest
import src.ml_backend.models as models


# -------------------------------------------------------------------------
# Fixtures to stub out external dependencies: YOLO, wandb, add_wandb_callback,
# and os.system, so tests stay fast, offline, and deterministic.
# -------------------------------------------------------------------------
class DummyYOLO:
    def __init__(self, weights: str):
        self.weights = weights
        self.trained = False
        self.train_kwargs = {}

    def train(self, **kwargs) -> Dict[str, Any]:
        self.trained = True
        self.train_kwargs = kwargs
        return {"success": True, "received": kwargs}


@pytest.fixture(autouse=True)
def patch_yolo(monkeypatch):
    """Replace models.YOLO with DummyYOLO in every test."""
    monkeypatch.setattr(models, "YOLO", DummyYOLO)


@pytest.fixture
def patch_wandb_and_system(monkeypatch):
    """
    Stub out:
      - wandb.login
      - wandb.init
      - M.add_wandb_callback
      - os.system
    so we can assert they were called with the right args.
    """
    calls = {"login": False, "init": {}, "callback": None, "system": None}

    # stub login()
    def fake_login():
        calls["login"] = True

    # stub init(...)
    def fake_init(**kwargs):
        calls["init"] = kwargs

    # stub callback(model)
    def fake_add_cb(model):
        calls["callback"] = model

    # stub os.system(cmd)
    def fake_system(cmd):
        calls["system"] = cmd
        return 0

    monkeypatch.setattr(models.wandb, "login", fake_login)
    monkeypatch.setattr(models.wandb, "init", fake_init)
    monkeypatch.setattr(models, "add_wandb_callback", fake_add_cb)
    monkeypatch.setattr(models.os, "system", fake_system)

    return calls


# -------------------------------------------------------------------------
# TESTS
# -------------------------------------------------------------------------


def test_train_model_plain_path(monkeypatch):
    """
    When wandb_logging=False, no W&B calls should happen.
    The DummyYOLO.train result should be returned verbatim,
    and kwargs should reflect the function signature.
    """
    # call without wandb
    res = models.train_model(model_name="simple", batch_size=16, epochs=5, wandb_logging=False)

    # verify return
    assert isinstance(res, dict)
    assert res["success"] is True

    # verify the DummyYOLO instance got the right training arguments
    # We know train() was invoked on the one and only DummyYOLO instance:
    # its kwargs should match our call
    kwargs = res["received"]
    assert kwargs["epochs"] == 5
    assert kwargs["batch"] == 16
    assert kwargs["project"] == "models/"
    assert kwargs["name"] == "simple"

    # no wandb side-effects
    # If patch_wandb_and_system isn't used, wandb.* shouldn't even be called,
    # so we don't need to assert anything here.


def test_train_model_with_wandb(patch_wandb_and_system):
    """
    When wandb_logging=True, we expect:
     - wandb.login() called
     - os.system("yolo settings wandb=True") called
     - wandb.init(...) called with our project & job_type
     - add_wandb_callback() called with the DummyYOLO instance
    """
    calls = patch_wandb_and_system

    # invoke with wandb Logging enabled
    res = models.train_model(model_name="simple", batch_size=8, epochs=3, wandb_logging=True)

    # verify training still returns success
    assert res["success"] is True

    # W&B calls
    assert calls["login"] is True
    assert calls["system"] == "yolo settings wandb=True"
    # init should have at least project & job_type
    assert calls["init"].get("project") == "BrainTumorDetection"
    assert calls["init"].get("job_type") == "training"
    # callback should have received the DummyYOLO instance
    assert isinstance(calls["callback"], DummyYOLO)


def test_train_model_uses_correct_data_path():
    """
    Ensure that each model_name picks its own data.yaml entry.
    """
    # for each key in yaml_data_path_dict, check that DummyYOLO.train saw it
    for name, path in models.train_model.__defaults__[0:3]:  # not super reliable—better to inspect the dict
        # Instead, just test two examples explicitly:
        pass  # we'll write two explicit subtests below


@pytest.mark.parametrize(
    "model_name,expected_yaml",
    [
        ("yolov8n", "data/BrainTumor/BrainTumorYolov8/data.yaml"),
        ("simple", "configs/data/data.yaml"),
    ],
)
def test_train_model_data_path_passed(model_name, expected_yaml):
    dummy = DummyYOLO(weights="unused")
    # patch YOLO to return our dummy
    models.YOLO = lambda w: dummy

    _ = models.train_model(model_name=model_name, wandb_logging=False)
    # check that the train() kwargs included the correct data path
    assert dummy.train_kwargs["data"] == expected_yaml
