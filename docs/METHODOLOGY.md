# Methodology

## Step 1 — Create network

Create a set of virtual nodes representing IoT devices, vehicles, or roadside units.

## Step 2 — Generate candidate links

For each source node, create several candidate destination links.

## Step 3 — Simulate wireless conditions

For each link calculate:
- distance
- path loss
- RSSI
- noise
- SNR
- interference
- previous success rate

## Step 4 — Generate ML dataset

The simulator creates repeated channel observations and labels a link as reliable when its underlying communication probability is sufficiently high.

## Step 5 — Train model

Split the generated data into training and testing sets. Train a Random Forest classifier and calculate accuracy, precision, recall and F1-score.

## Step 6 — Select links

For every transmission:
- Random strategy chooses randomly.
- Distance strategy chooses the shortest candidate.
- RSSI/SNR strategy chooses the strongest channel-quality candidate.
- ML strategy uses predicted reliability probability and current channel quality.

## Step 7 — Simulate packets

Transmit a fixed number of packets under time-varying conditions.

## Step 8 — Evaluate

Calculate:
- packet success rate
- average latency
- failed transmissions
- average AoI
- average selected-link reliability

## Step 9 — Visualize

Generate comparison charts for the four strategies.
