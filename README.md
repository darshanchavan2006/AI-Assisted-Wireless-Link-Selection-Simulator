# AI-Assisted-Wireless-Link-Selection-Simulator

# AI-Assisted Wireless Link Selection Simulator for Reliable IoT and V2X Networks

A Python-based wireless-network simulator that models IoT/V2X nodes, wireless links, path loss, noise, interference, and time-varying channel conditions. It compares four link-selection strategies:

1. Random selection
2. Distance-based selection
3. RSSI/SNR-based selection
4. Machine-learning-assisted selection

The project evaluates packet success rate, latency, failed transmissions, link reliability, and Age of Information (AoI).

> **Important:** This is a software-only simulation project. No physical RF hardware is required.

## Project idea

When multiple wireless links are available, choosing a link only from distance or randomly may not give the most reliable communication. This project simulates changing wireless conditions and uses ML to select a link expected to perform well.

### Main pipeline

```text
Virtual IoT/V2X nodes
        ↓
Wireless channel simulation
        ↓
Distance + path loss
        ↓
Noise + interference
        ↓
RSSI + SNR
        ↓
Candidate links
        ↓
Random / Distance / RSSI-SNR / ML selection
        ↓
Packet transmission simulation
        ↓
Success rate + latency + failed packets + AoI
        ↓
Comparison plots and CSV results
```

## Repository structure

```text
AI-Wireless-Link-Selection-Simulator/
├── data/
│   ├── link_dataset.csv
│   └── README.md
├── docs/
│   ├── THEORY.md
│   ├── METHODOLOGY.md
│   └── RESULTS.md
├── results/
│   ├── model_metrics.csv
│   ├── strategy_comparison.csv
│   └── figures/
├── src/
│   ├── generate_dataset.py
│   ├── train_model.py
│   ├── simulate_network.py
│   └── run_all.py
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

## Installation

```bash
git clone <your-repository-url>
cd AI-Wireless-Link-Selection-Simulator
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the complete project

```bash
python src/run_all.py
```

This will:
- generate a synthetic wireless-link dataset
- train the ML model
- evaluate the model
- run the network simulation
- compare all four strategies
- save CSV results
- save plots inside `results/figures/`

## ML model

The baseline implementation uses a Random Forest classifier from scikit-learn.

Example features:

- distance_m
- rssi_dbm
- snr_db
- noise_dbm
- interference_db
- previous_success_rate

Target:

- reliable_link

The model predicts whether a candidate link is likely to be reliable. During link selection, the simulator scores available links using the predicted reliability probability and current channel quality.

## Metrics

### Packet Success Rate

PSR = successful packets / transmitted packets × 100

### Packet Failure Rate

Failure Rate = failed packets / transmitted packets × 100

### Average Latency

Mean simulated end-to-end transmission delay.

### Age of Information

AoI represents how old the latest successfully delivered information is at the receiver. Lower AoI is better.

### Link Reliability

A link's reliability is represented by its successful transmission probability over repeated simulations.

## Expected result

The project is designed to test whether ML-assisted selection can outperform simple baselines under changing channel conditions. Do not claim a specific percentage improvement until you run the simulator and use the generated result files.

## Resume description

**AI-Assisted Wireless Link Selection Simulator for Reliable IoT and V2X Networks**
- Developed a Python-based wireless-network simulator modeling IoT/V2X nodes, path loss, noise, interference and time-varying channel conditions.
- Compared random, distance-based, RSSI/SNR-based and Random-Forest-assisted link-selection strategies using NumPy, Pandas, Matplotlib and scikit-learn.
- Evaluated packet success rate, latency, failed transmissions, link reliability and Age of Information with automated result generation and visualization.

## Interview summary

“I built a software-only wireless-network simulator for IoT and V2X scenarios. The simulator creates multiple candidate wireless links and models distance, path loss, noise, interference and time-varying channel conditions. I compared random, distance-based, RSSI/SNR-based and ML-assisted link selection. A Random Forest model predicts link reliability from channel features, and the final strategies are compared using packet success rate, latency, failed transmissions and Age of Information.”

## Disclaimer

This project is a simulation and research/learning prototype. It does not represent a certified real-world wireless channel model or a production V2X communication stack.
