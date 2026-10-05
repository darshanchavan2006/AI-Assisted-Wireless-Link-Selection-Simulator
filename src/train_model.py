import argparse
from pathlib import Path
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

FEATURES = [
    "distance_m", "rssi_dbm", "snr_db", "noise_dbm",
    "interference_db", "previous_success_rate", "latency_ms"
]
TARGET = "reliable_link"

def train(data_path, model_path, metrics_path):
    df = pd.read_csv(data_path)
    X = df[FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=250,
        max_depth=12,
        min_samples_leaf=3,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    pred = model.predict(X_test)

    metrics = pd.DataFrame([{
        "accuracy": accuracy_score(y_test, pred),
        "precision": precision_score(y_test, pred, zero_division=0),
        "recall": recall_score(y_test, pred, zero_division=0),
        "f1": f1_score(y_test, pred, zero_division=0)
    }])
    Path(metrics_path).parent.mkdir(parents=True, exist_ok=True)
    metrics.to_csv(metrics_path, index=False)

    cm = confusion_matrix(y_test, pred)
    pd.DataFrame(cm, index=["actual_0", "actual_1"],
                 columns=["pred_0", "pred_1"]).to_csv(
        Path(metrics_path).with_name("confusion_matrix.csv")
    )

    importance = pd.DataFrame({
        "feature": FEATURES,
        "importance": model.feature_importances_
    }).sort_values("importance", ascending=False)
    importance.to_csv(Path(metrics_path).with_name("feature_importance.csv"), index=False)

    figdir = Path(metrics_path).parent / "figures"
    figdir.mkdir(parents=True, exist_ok=True)

    fig = plt.figure(figsize=(7, 4.5))
    vals = metrics.iloc[0].values
    plt.bar(metrics.columns, vals)
    plt.ylim(0, 1.05)
    plt.ylabel("Score")
    plt.title("Random Forest Model Metrics")
    plt.grid(axis="y", alpha=0.25)
    plt.tight_layout()
    fig.savefig(figdir / "model_metrics.png", dpi=180)
    plt.close(fig)

    fig = plt.figure(figsize=(8, 4.8))
    plt.barh(importance["feature"][::-1], importance["importance"][::-1])
    plt.xlabel("Importance")
    plt.title("Random Forest Feature Importance")
    plt.tight_layout()
    fig.savefig(figdir / "feature_importance.png", dpi=180)
    plt.close(fig)

    fig = plt.figure(figsize=(5, 4))
    plt.imshow(cm)
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            plt.text(j, i, cm[i, j], ha="center", va="center")
    plt.tight_layout()
    fig.savefig(figdir / "confusion_matrix.png", dpi=180)
    plt.close(fig)

    Path(model_path).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_path)

    print(metrics.to_string(index=False))
    print(f"Saved model to {model_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="data/link_dataset.csv")
    parser.add_argument("--model", default="results/link_selector_rf.joblib")
    parser.add_argument("--metrics", default="results/model_metrics.csv")
    args = parser.parse_args()
    train(args.data, args.model, args.metrics)
