import glob
import os
from collections import Counter

import matplotlib.pyplot as plt
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


def dataset_statistics_local(out_dir="ml/data_changes", splits=["train", "valid", "test"]):
    os.makedirs(out_dir, exist_ok=True)
    for split in splits:
        local_images = os.path.join(out_dir, f"gcs_{split}_images")
        local_labels = os.path.join(out_dir, f"gcs_{split}_labels")
        image_files = glob.glob(os.path.join(local_images, "*.jpg"))
        label_files = glob.glob(os.path.join(local_labels, "*.txt"))
        print(f"\n{split.capitalize()} set:")
        print(f"Number of images: {len(image_files)}")
        if image_files:
            shape, mode = get_image_shape(image_files[0])
            print(f"Image shape: {shape}, mode: {mode}")
        else:
            print("No images found.")
        # Gather label distribution
        all_classes = []
        for label_file in label_files:
            all_classes.extend(parse_label_file(label_file))
        class_counts = Counter(all_classes)
        print(f"Label distribution: {dict(class_counts)}")
        # Plot label distribution
        if class_counts:
            plt.bar(class_counts.keys(), class_counts.values())
            plt.title(f"GCS {split.capitalize()} Label Distribution")
            plt.xlabel("Class")
            plt.ylabel("Count")
            plt.savefig(os.path.join(out_dir, f"gcs_{split}_label_distribution.png"))
            plt.close()


if __name__ == "__main__":
    dataset_statistics_local()
