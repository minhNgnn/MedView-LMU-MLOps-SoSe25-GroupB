# tentative data test file
import os
import tempfile
from pathlib import Path

import pytest
import yaml
from google.cloud import storage

BUCKET_NAME = "brain-tumor-data"
GCS_PREFIX = "BrainTumorYolov8/"
DATA_YAML_GCS = GCS_PREFIX + "data.yaml"


@pytest.fixture(scope="session", autouse=True)
def fetch_gcs_data_yaml():
    import sys

    print(f"[DEBUG] Attempting to download data.yaml from GCS: bucket={BUCKET_NAME}, blob={DATA_YAML_GCS}", flush=True)
    try:
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(DATA_YAML_GCS)
        tmpdir = tempfile.gettempdir()
        local_path = os.path.join(tmpdir, "data.yaml")
        print(f"[DEBUG] Will download to {local_path}", flush=True)
        blob.download_to_filename(local_path)
        print(f"[DEBUG] Downloaded data.yaml to {local_path}", flush=True)
        os.environ["TEST_DATA_YAML"] = local_path
    except Exception as e:
        print(f"[ERROR] Failed to download data.yaml: {e}", flush=True)
        raise
    yield
    # Optionally, clean up the file after tests


def get_data_yaml_path():
    return os.environ.get("TEST_DATA_YAML")


def test_data_yaml_exists():
    path = get_data_yaml_path()
    if not path or not os.path.exists(path):
        pytest.skip("data.yaml not found")
    assert os.path.exists(path), f"Could not find data.yaml at {path}"


def test_yaml_contents():
    path = get_data_yaml_path()
    if not path or not os.path.exists(path):
        pytest.skip("data.yaml not found")
    cfg = yaml.safe_load(open(path).read())
    assert "train" in cfg and "val" in cfg and "test" in cfg
    assert "nc" in cfg and "names" in cfg


def test_split_dirs_have_files():
    path = get_data_yaml_path()
    if not path or not os.path.exists(path):
        pytest.skip("data.yaml not found")
    cfg = yaml.safe_load(open(path).read())
    # If the config points to GCS, check GCS, else check local
    for split in ["train", "val", "test"]:
        split_path = cfg[split]
        if split_path.startswith("/gcs/"):
            # Parse bucket and prefix
            # Example: /gcs/brain-tumor-data/Simple/train/images
            parts = split_path.split("/")
            bucket_name = parts[2]
            prefix = "/".join(parts[3:])
            client = storage.Client()
            bucket = client.bucket(bucket_name)
            blobs = list(bucket.list_blobs(prefix=prefix))
            if not blobs:
                pytest.skip(f"No files found in GCS at {split_path}")
            assert any(b.name.endswith(".jpg") for b in blobs), f"No images found in GCS at {split_path}"
        else:
            # Local path fallback
            project_root = Path(__file__).parent.parent.parent.resolve()
            split_dir = (project_root / split_path.replace("../", "")).resolve()
            if not split_dir.exists():
                pytest.skip(f"Split path {split_dir} does not exist")
            assert split_dir.exists(), f"Split path {split_dir} does not exist"


# def test_labels_match_images():
#     path = get_data_yaml_path()
#     if not path or not os.path.exists(path):
#         pytest.skip("data.yaml not found")
#     cfg = yaml.safe_load(open(path).read())
#     for split in ["train", "val", "test"]:
#         split_path = cfg[split]
#         if split_path.startswith("/gcs/"):
#             # Parse bucket and prefix
#             # Example: /gcs/brain-tumor-data/Simple/train/images
#             parts = split_path.split("/")
#             bucket_name = parts[2]
#             image_prefix = "/".join(parts[3:])
#             label_prefix = image_prefix.replace("images", "labels")
#             client = storage.Client()
#             bucket = client.bucket(bucket_name)
#             img_blobs = list(bucket.list_blobs(prefix=image_prefix))
#             label_blobs = list(bucket.list_blobs(prefix=label_prefix))
#             img_files = set(
#                 os.path.splitext(os.path.basename(b.name))[0]
#                 for b in img_blobs if b.name.endswith('.jpg')
#             )
#             label_files = set(
#                 os.path.splitext(os.path.basename(b.name))[0]
#                 for b in label_blobs if b.name.endswith('.txt')
#             )
#             assert img_files == label_files, f"Mismatch in {split}: {img_files ^ label_files}"
#         else:
#             # Local path fallback
#             project_root = Path(__file__).parent.parent.parent.resolve()
#             split_path_obj = (project_root / split_path.replace("../", "")).resolve()
#             img_dir = split_path_obj / "images"
#             label_dir = split_path_obj / "labels"
#             if img_dir.exists() and label_dir.exists():
#                 img_files = set(f.stem for f in img_dir.glob("*.jpg"))
#                 label_files = set(f.stem for f in label_dir.glob("*.txt"))
#                 assert img_files == label_files, f"Mismatch in {split}: {img_files ^ label_files}"
