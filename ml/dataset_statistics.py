import glob
import os
from collections import Counter

import matplotlib.pyplot as plt
from google.cloud import storage
from PIL import Image


def get_image_shape(image_path):
    with Image.open(image_path) as img:
        return img.size, img.mode


def parse_label_file(label_path):
    # YOLO format: class x_center y_center width height (one object per line)
    with open(label_path, "r") as f:
        lines = f.readlines()
    classes = [int(line.split()[0]) for line in lines if line.strip()]
    return classes


def analyze_local_dataset(base_dir="data/BrainTumor/BrainTumorYolov8", out_dir="ml/data_changes"):
    os.makedirs(out_dir, exist_ok=True)
    for split in ["train", "valid", "test"]:
        images_dir = os.path.join(base_dir, split, "images")
        labels_dir = os.path.join(base_dir, split, "labels")
        image_files = glob.glob(os.path.join(images_dir, "*.jpg"))
        label_files = glob.glob(os.path.join(labels_dir, "*.txt"))
        print(f"\n{split.capitalize()} set (local):")
        print(f"Number of images: {len(image_files)}")
        if image_files:
            shape, mode = get_image_shape(image_files[0])
            print(f"Image shape: {shape}, mode: {mode}")
        else:
            print("No images found.")
        all_classes = []
        for label_file in label_files:
            all_classes.extend(parse_label_file(label_file))
        class_counts = Counter(all_classes)
        print(f"Label distribution: {dict(class_counts)}")
        if class_counts:
            plt.bar(class_counts.keys(), class_counts.values())
            plt.title(f"Local {split.capitalize()} Label Distribution")
            plt.xlabel("Class")
            plt.ylabel("Count")
            plt.savefig(os.path.join(out_dir, f"local_{split}_label_distribution.png"))
            plt.close()


def download_gcs_files(bucket, prefix, local_dir):
    os.makedirs(local_dir, exist_ok=True)
    blobs = list(bucket.list_blobs(prefix=prefix))
    local_files = []
    for blob in blobs:
        if not blob.name.endswith("/"):
            local_path = os.path.join(local_dir, os.path.basename(blob.name))
            blob.download_to_filename(local_path)
            local_files.append(local_path)
    return local_files


def dataset_statistics_gcs(bucket_name="brain-tumor-data", base_prefix="BrainTumorYolov8", out_dir="ml/data_changes"):
    os.makedirs(out_dir, exist_ok=True)
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    for split in ["train", "valid", "test"]:
        image_prefix = f"{base_prefix}/{split}/images/"
        label_prefix = f"{base_prefix}/{split}/labels/"
        local_images = os.path.join(out_dir, f"gcs_{split}_images")
        local_labels = os.path.join(out_dir, f"gcs_{split}_labels")
        image_files = download_gcs_files(bucket, image_prefix, local_images)
        label_files = download_gcs_files(bucket, label_prefix, local_labels)
        print(f"\n{split.capitalize()} set (GCS):")
        print(f"Number of images: {len(image_files)}")
        if image_files:
            shape, mode = get_image_shape(image_files[0])
            print(f"Image shape: {shape}, mode: {mode}")
        else:
            print("No images found.")
        all_classes = []
        for label_file in label_files:
            all_classes.extend(parse_label_file(label_file))
        class_counts = Counter(all_classes)
        print(f"Label distribution: {dict(class_counts)}")
        if class_counts:
            plt.bar(class_counts.keys(), class_counts.values())
            plt.title(f"GCS {split.capitalize()} Label Distribution")
            plt.xlabel("Class")
            plt.ylabel("Count")
            plt.savefig(os.path.join(out_dir, f"gcs_{split}_label_distribution.png"))
            plt.close()


if __name__ == "__main__":
    local_base = "data/BrainTumor/BrainTumorYolov8"
    if os.path.exists(local_base) and any(
        os.path.exists(os.path.join(local_base, split, "images")) for split in ["train", "valid", "test"]
    ):
        print("Local data found. Using local dataset for statistics.")
        analyze_local_dataset(base_dir=local_base)
    else:
        print("Local data not found. Downloading and analyzing from GCS.")
        dataset_statistics_gcs()
