import argparse
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

FEATURES = [
    'distance_m','rssi_dbm','snr_db','noise_dbm',
    'interference_db','previous_success_rate','latency_ms'
]


def make_candidates(rng, n_steps, n_links=5):
    distance = rng.uniform(5, 150, (n_steps, n_links))
    noise = rng.normal(-92, 3.5, (n_steps, n_links))
    interference = np.clip(rng.gamma(2.0, 5.0, (n_steps, n_links)), 0, 35)
    path_loss = 25 + 16 * np.log10(distance / 5)
    shadowing = rng.normal(0, 3.0, (n_steps, n_links))
    rssi = -30 - path_loss + shadowing - 0.20 * interference
    snr = rssi - noise
    previous_success = np.clip(
        0.45 + 0.010 * snr - 0.008 * distance - 0.010 * interference
        + rng.normal(0, 0.06, (n_steps, n_links)), 0.02, 0.99
    )
    latency = np.clip(
        8 + 0.10 * distance + 0.9 * interference
        + np.maximum(0, 15 - snr) * 1.4
        + rng.normal(0, 2.0, (n_steps, n_links)), 5, None
    )
    z = (0.12 * (snr - 5) - 0.025 * distance - 0.06 * interference
         + 2.0 * (previous_success - 0.5))
    probability = 1 / (1 + np.exp(-z))
    return {
        'distance_m': distance, 'rssi_dbm': rssi, 'noise_dbm': noise,
        'snr_db': snr, 'interference_db': interference,
        'previous_success_rate': previous_success, 'latency_ms': latency,
        'true_probability': probability
    }


def select_indices(data, strategy, model):
    n_steps, n_links = data['distance_m'].shape
    if strategy == 'Random':
        return np.random.default_rng(123).integers(0, n_links, n_steps)
    if strategy == 'Distance':
        return np.argmin(data['distance_m'], axis=1)
    if strategy == 'RSSI-SNR':
        score = 0.55 * data['snr_db'] + 0.30 * data['rssi_dbm'] - 0.15 * data['interference_db']
        return np.argmax(score, axis=1)
    if strategy == 'ML':
        flat = pd.DataFrame({k: data[k].ravel() for k in FEATURES})
        p = model.predict_proba(flat)[:, 1].reshape(n_steps, n_links)
        score = p + 0.01 * np.clip(data['snr_db'], -20, 40)
        return np.argmax(score, axis=1)
    raise ValueError(strategy)


def run_simulation(model_path, output_csv, figure_dir, steps=2000, seed=7):
    model = joblib.load(model_path)
    strategies = ['Random', 'Distance', 'RSSI-SNR', 'ML']
    records = []

    for strategy in strategies:
        rng = np.random.default_rng(seed)
        data = make_candidates(rng, steps, 5)
        idx = select_indices(data, strategy, model)
        rows = np.arange(steps)
        prob = data['true_probability'][rows, idx]
        latency = data['latency_ms'][rows, idx]
        success = rng.random(steps) < prob

        aoi = np.empty(steps)
        current = 0.0
        for i in range(steps):
            if success[i]:
                current = latency[i]
            else:
                current += latency[i]
            aoi[i] = current

        records.append({
            'strategy': strategy,
            'packets': steps,
            'successful_packets': int(success.sum()),
            'failed_transmissions': int((~success).sum()),
            'packet_success_rate_pct': 100 * success.mean(),
            'average_latency_ms_successful': latency[success].mean() if success.any() else 0,
            'average_aoi_ms': aoi.mean(),
            'average_selected_link_reliability': prob.mean()
        })

    result = pd.DataFrame(records)
    Path(output_csv).parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(output_csv, index=False)
    figdir = Path(figure_dir); figdir.mkdir(parents=True, exist_ok=True)

    plot_bar(result, 'packet_success_rate_pct', 'Packet Success Rate (%)', 'Packet Success Rate by Strategy', figdir/'packet_success_rate.png')
    plot_bar(result, 'average_latency_ms_successful', 'Average Latency (ms)', 'Average Latency by Strategy', figdir/'latency.png')
    plot_bar(result, 'failed_transmissions', 'Failed Transmissions', 'Failed Transmissions by Strategy', figdir/'failed_transmissions.png')
    plot_bar(result, 'average_aoi_ms', 'Average AoI (ms)', 'Average Age of Information by Strategy', figdir/'aoi.png')
    plot_bar(result, 'average_selected_link_reliability', 'Reliability Probability', 'Selected-Link Reliability by Strategy', figdir/'reliability.png')

    rng2 = np.random.default_rng(seed + 100)
    sample = make_candidates(rng2, 500, 1)
    fig = plt.figure(figsize=(8, 5))
    plt.scatter(sample['distance_m'].ravel(), sample['rssi_dbm'].ravel(), s=12)
    plt.xlabel('Distance (m)'); plt.ylabel('RSSI (dBm)'); plt.title('RSSI vs Distance')
    plt.grid(alpha=0.25); plt.tight_layout(); fig.savefig(figdir/'rssi_vs_distance.png', dpi=180); plt.close(fig)
    print(result.to_string(index=False))


def plot_bar(df, column, ylabel, title, output):
    fig = plt.figure(figsize=(8, 5))
    plt.bar(df['strategy'], df[column])
    plt.ylabel(ylabel); plt.title(title); plt.grid(axis='y', alpha=0.25)
    plt.tight_layout(); fig.savefig(output, dpi=180); plt.close(fig)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', default='results/link_selector_rf.joblib')
    parser.add_argument('--output', default='results/strategy_comparison.csv')
    parser.add_argument('--figures', default='results/figures')
    parser.add_argument('--steps', type=int, default=2000)
    args = parser.parse_args()
    run_simulation(args.model, args.output, args.figures, args.steps)
