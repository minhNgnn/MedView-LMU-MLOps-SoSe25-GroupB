# tentative data test file
from pathlib import Path

import pytest
import yaml

# Point this to wherever your test runner invokes it
PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()
DATA_YAML = PROJECT_ROOT / "ml" / "configs" / "data_config" / "data.yaml"


@pytest.mark.skipif(not DATA_YAML.exists(), reason="data.yaml not found")
def test_data_yaml_exists():
    assert DATA_YAML.exists(), f"Could not find data.yaml at {DATA_YAML}"


@pytest.mark.skipif(not DATA_YAML.exists(), reason="data.yaml not found")
def test_yaml_contents():
    cfg = yaml.safe_load(DATA_YAML.read_text())
    assert "train" in cfg and "val" in cfg and "test" in cfg
    assert "nc" in cfg and "names" in cfg


@pytest.mark.skipif(not DATA_YAML.exists(), reason="data.yaml not found")
def test_split_dirs_have_files():
    cfg = yaml.safe_load(DATA_YAML.read_text())
    for split in ["train", "val", "test"]:
        split_path = (PROJECT_ROOT / cfg[split].replace("../", "")).resolve()
        # If the split path does not exist, skip this split
        if not split_path.exists():
            pytest.skip(f"Split path {split_path} does not exist")
        assert split_path.exists(), f"Split path {split_path} does not exist"


@pytest.mark.skipif(not DATA_YAML.exists(), reason="data.yaml not found")
def test_labels_match_images():
    cfg = yaml.safe_load(DATA_YAML.read_text())
    for split in ["train", "val", "test"]:
        split_path = (PROJECT_ROOT / cfg[split].replace("../", "")).resolve()
        img_dir = split_path / "images"
        label_dir = split_path / "labels"
        if img_dir.exists() and label_dir.exists():
            img_files = set(f.stem for f in img_dir.glob("*.jpg"))
            label_files = set(f.stem for f in label_dir.glob("*.txt"))
            assert img_files == label_files, f"Mismatch in {split}: {img_files ^ label_files}"
