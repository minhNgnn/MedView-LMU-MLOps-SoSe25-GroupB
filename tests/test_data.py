# tentative data test file
import yaml
from pathlib import Path

# Point this to wherever your test runner invokes it
PROJECT_ROOT = Path(__file__).parent.parent
DATA_YAML    = PROJECT_ROOT / "ml" / "configs" / "data_config" / "data.yaml"

def test_data_yaml_exists():
    assert DATA_YAML.exists(), f"Could not find data.yaml at {DATA_YAML}"

def test_yaml_contents():
    cfg = yaml.safe_load(DATA_YAML.read_text())
    # should have keys: 'train', 'val', 'nc', 'names'
    for key in ("train", "val", "nc", "names"):
        assert key in cfg, f"Missing '{key}' in data.yaml"
    # basic sanity
    assert isinstance(cfg["names"], list) and len(cfg["names"]) == cfg["nc"]

def test_split_dirs_have_files():
    cfg = yaml.safe_load(DATA_YAML.read_text())
    for split in ("train", "val"):
        #img_dir = PROJECT_ROOT / cfg[split]
        img_dir = PROJECT_ROOT / cfg[split].replace("../", "")
        assert img_dir.exists(), f"{split} dir {img_dir} not found"
        images = list(img_dir.glob("images/*.jpg")) + list(img_dir.glob("images/*.png"))
        assert len(images) > 0, f"No images found in {img_dir}/images"

def test_labels_match_images():
    cfg = yaml.safe_load(DATA_YAML.read_text())
    for split in ("train", "val"):
        img_dir   = PROJECT_ROOT / cfg[split].replace("../", "") / "images"
        label_dir = PROJECT_ROOT / cfg[split].replace("../", "") / "labels"
        for img in img_dir.iterdir():
            lbl = label_dir / f"{img.stem}.txt"
            assert lbl.exists(), f"Label missing for image {img.name}"
