import argparse
from pathlib import Path
import numpy as np
import pandas as pd

def make_dataset(n_samples=12000, seed=42):
    rng = np.random.default_rng(seed)

    distance = rng.uniform(5, 150, n_samples)
    noise = rng.normal(-92, 3.5, n_samples)
    interference = np.clip(rng.gamma(shape=2.0, scale=5.0, size=n_samples), 0, 35)

    path_loss = 25 + 16 * np.log10(distance / 5)
    shadowing = rng.normal(0, 3.0, n_samples)
    rssi = -30 - path_loss + shadowing - 0.20 * interference

    snr = rssi - noise

    previous_success = np.clip(
        0.45
        + 0.010 * snr
        - 0.008 * distance
        - 0.010 * interference
        + rng.normal(0, 0.08, n_samples),
        0.02, 0.99
    )

    latency = (
        8
        + 0.10 * distance
        + 0.9 * interference
        + np.maximum(0, 15 - snr) * 1.4
        + rng.normal(0, 2.5, n_samples)
    )
    latency = np.clip(latency, 5, None)

    z = (0.12 * (snr - 5) - 0.025 * distance - 0.06 * interference
         + 2.0 * (previous_success - 0.5))
    reliability_probability = 1 / (1 + np.exp(-z))

    reliable = (reliability_probability >= 0.55).astype(int)

    return pd.DataFrame({
        "distance_m": distance.round(3),
        "rssi_dbm": rssi.round(3),
        "noise_dbm": noise.round(3),
        "snr_db": snr.round(3),
        "interference_db": interference.round(3),
        "previous_success_rate": previous_success.round(4),
        "latency_ms": latency.round(3),
        "reliable_link": reliable
    })

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples", type=int, default=12000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", default="data/link_dataset.csv")
    args = parser.parse_args()

    df = make_dataset(args.samples, args.seed)
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.output, index=False)
    print(f"Saved {len(df)} rows to {args.output}")
