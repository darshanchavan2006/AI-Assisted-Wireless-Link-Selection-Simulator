# Experiment Summary

The current generated experiment uses 5,000 simulated packet-transmission steps per strategy.

## Current run

| Strategy | Packet Success Rate | Avg. Latency (ms) | Avg. AoI (ms) | Selected-Link Reliability |
|---|---:|---:|---:|---:|
| Random | 25.80% | 19.29 | 104.51 | 0.2553 |
| Distance | 63.10% | 17.89 | 31.86 | 0.6286 |
| RSSI/SNR | 63.86% | 17.27 | 29.03 | 0.6361 |
| ML | **65.24%** | 17.41 | **28.81** | **0.6505** |

## ML model

Random Forest test metrics from this run:

- Accuracy: 98.73%
- Precision: 95.64%
- Recall: 98.40%
- F1-score: 96.998%

These numbers are from the synthetic simulation dataset and should be presented as simulation results, not real-world RF performance.

## Interpretation

The ML strategy selected links with the highest average simulated reliability and achieved the highest packet success rate in this run. RSSI/SNR was close behind. Random selection performed substantially worse because it does not use channel information.
