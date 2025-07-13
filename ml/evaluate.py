import os
import argparse
import pandas as pd
from ultralytics import YOLO

# default data-yaml (you can override on the CLI)
DEFAULT_DATA_YAML = os.path.join(
    os.path.dirname(__file__),
    "configs", "data", "data.yaml"
)

def find_best_weights(model_name: str, project_dir: str = "models") -> str:
    """
    Look for the latest version folder under ml/models/{model_name}/
    and return the path to weights/best.pt
    """
    base = os.path.join(os.getcwd(), project_dir, model_name)
    if not os.path.isdir(base):
        raise FileNotFoundError(f"No folder found at {base}")
    # find subdirectories (versions)
    versions = [
        d for d in os.listdir(base)
        if os.path.isdir(os.path.join(base, d))
    ]
    if not versions:
        raise FileNotFoundError(f"No version subdirs in {base}")
    # pick latest (lexicographically)
    latest = sorted(versions)[-1]
    best_path = os.path.join(base, latest, "weights", "best.pt")
    if not os.path.isfile(best_path):
        raise FileNotFoundError(f"Could not find best.pt at {best_path}")
    return best_path


def evaluate_model(
    model_name: str,
    data_yaml: str,
    split: str,
) -> pd.DataFrame:
    """
    Loads best.pt for `model_name`, runs `val()`, and returns a DataFrame
    of the core detection metrics.
    """
    # 1) locate best.pt
    weights = find_best_weights(model_name)

    # 2) load model
    model = YOLO(weights)

    # 3) run validation
    metrics = model.val(data=data_yaml, split=split)

    # 4) build metrics dict just like in your notebook
    results_dict = {
        "Mean Precision": metrics.box.mp,
        "Mean Recall":    metrics.box.mr,
        "mAP@0.5":        metrics.box.map50,
        "mAP@0.5:0.95":   metrics.box.map,
    }

    # 5) DataFrame for easy viewing / CI
    df = pd.DataFrame(
        results_dict.items(),
        columns=["Metric", "Value"]
    )
    print(df)
    return df


if __name__ == "__main__":
    p = argparse.ArgumentParser(
        description="Evaluate a trained YOLO model and print mAP / precision / recall"
    )
    p.add_argument(
        "--model_name",
        type=str,
        default="simple",
        help="Subfolder under ml/models/ where your run lives",
    )
    p.add_argument(
        "--data_yaml",
        type=str,
        default=DEFAULT_DATA_YAML,
        help="Path to your data.yaml (no raw data folder needed)",
    )
    p.add_argument(
        "--split",
        type=str,
        default="val",
        help="Which split to evaluate (e.g. 'val' or 'test')",
    )
    args = p.parse_args()

    evaluate_model(
        model_name=args.model_name,
        data_yaml=args.data_yaml,
        split=args.split,
    )

