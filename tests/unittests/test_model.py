# tests/test_model.py

import os
import sys
import types

import numpy as np
import pytest
import wandb

import ml.models as models
import ml.predict as predict

# --- Stub external heavy deps to avoid import-time errors ---
# Stub ultralytics package entirely, including YOLO
ultra = types.ModuleType("ultralytics")


class DummyYOLOBase:
    def __init__(self, *args, **kwargs):
        pass


ultra.YOLO = DummyYOLOBase
sys.modules["ultralytics"] = ultra

# Stub wandb.integration.ultralytics for add_wandb_callback import
stub_integration = types.ModuleType("wandb.integration.ultralytics")
stub_integration.add_wandb_callback = lambda m: None
sys.modules["wandb.integration.ultralytics"] = stub_integration

# Stub PIL modules to satisfy any PIL imports
sys.modules["PIL"] = types.ModuleType("PIL")
sys.modules["PIL._imaging"] = types.ModuleType("PIL._imaging")
sys.modules["PIL.Image"] = types.ModuleType("PIL.Image")
sys.modules["PIL.Image"].Image = object

# Stub onnxruntime so import succeeds and provide a dummy InferenceSession
stub_ort = types.ModuleType("onnxruntime")
stub_ort.InferenceSession = lambda *args, **kwargs: None
sys.modules["onnxruntime"] = stub_ort


# -------------------------------------------------------------------------
# Fixtures for train_model: stub out YOLO, wandb, add_wandb_callback, os.system
# -------------------------------------------------------------------------
class DummyYOLOTrain:
    def __init__(self, weights: str):
        self.weights = weights
        self.train_kwargs = {}

    def train(self, **kwargs):
        self.train_kwargs = kwargs
        return {"success": True, "received": kwargs}


@pytest.fixture(autouse=True)
def patch_yolo(monkeypatch):
    """Replace models.YOLO with DummyYOLO in every test."""
    monkeypatch.setattr(models, "YOLO", DummyYOLOBase)


@pytest.fixture
def patch_train(monkeypatch):
    dummy_cls = DummyYOLOTrain
    calls = {"login": False, "init": {}, "callback": None, "system": None}

    def fake_login():
        calls["login"] = True

    def fake_init(**kwargs):
        calls["init"] = kwargs

    def fake_add_cb(model):
        calls["callback"] = model

    def fake_system(cmd):
        calls["system"] = cmd
        return 0

    monkeypatch.setattr(models.wandb, "login", fake_login)
    monkeypatch.setattr(models.wandb, "init", fake_init)
    monkeypatch.setattr(models, "add_wandb_callback", fake_add_cb)
    monkeypatch.setattr(models.os, "system", fake_system)
    monkeypatch.setattr(models, "YOLO", dummy_cls)

    return dummy_cls, calls


# -------------------------------------------------------------------------
# Tests for train_model
# -------------------------------------------------------------------------
def test_train_model_without_wandb(patch_train):
    dummy, calls = patch_train
    res = models.train_model(model_name="simple", batch_size=16, epochs=5, wandb_logging=False)
    assert isinstance(res, dict) and res["success"] is True
    assert res["received"]["epochs"] == 5
    assert res["received"]["batch"] == 16
    assert res["received"]["project"] == "ml/models/"
    assert res["received"]["name"] == "simple"
    assert calls["login"] is False
    assert calls["system"] is None
    assert calls["init"] == {}
    assert calls["callback"] is None


def test_train_model_with_wandb(patch_train):
    dummy, calls = patch_train
    res = models.train_model(model_name="simple", batch_size=8, epochs=3, wandb_logging=True)
    assert res["success"] is True
    assert calls["login"] is True
    assert calls["system"] == "yolo settings wandb=True"
    assert calls["init"]["project"] == "BrainTumorDetection"
    assert calls["init"]["job_type"] == "training"
    assert isinstance(calls["callback"], DummyYOLOTrain)


# -------------------------------------------------------------------------
# Tests for helper functions
# -------------------------------------------------------------------------


def test_normalize_image():
    img = np.array([[[0, 128, 255]]], dtype=np.uint8)
    norm = models.normalize_image(img)
    assert np.allclose(norm, img / 255.0)


def test_resize_image():
    img = np.zeros((10, 10, 3), dtype=np.uint8)
    resized = models.resize_image(img, size=(5, 5))
    assert resized.shape == (5, 5, 3)


# -------------------------------------------------------------------------
# Tests for get_prediction_from_array
# -------------------------------------------------------------------------
class DummyRes:
    def __init__(self):
        self._plot = np.zeros((640, 640, 3), dtype=np.uint8)

    def plot(self):
        return self._plot


class DummyYOLOPred:
    def __init__(self, path):
        self.path = path

    def predict(self, source, imgsz, conf):
        return [DummyRes()]


@pytest.fixture(autouse=True)
def patch_yolo_predict(monkeypatch):
    monkeypatch.setattr(models, "YOLO", lambda path: DummyYOLOPred(path))


def test_get_prediction_from_array_none():
    ann = predict.get_prediction_from_array(None)
    assert ann is None


def test_get_prediction_from_array_valid():
    img = np.ones((100, 200, 3), dtype=np.uint8)
    float_img = img.astype(np.float32) / 255.0
    ann = predict.get_prediction_from_array(float_img)
    assert isinstance(ann, np.ndarray)
    assert ann.shape == (640, 640, 3)
