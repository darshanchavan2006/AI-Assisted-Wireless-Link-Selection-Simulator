# Theory

## 1. Wireless link selection

A wireless link is the communication path between two nodes. When several candidate links exist, the transmitter needs a method to select one.

## 2. Path loss

As distance increases, received signal power generally decreases. A simplified log-distance model is:

PL(d) = PL(d0) + 10n log10(d/d0)

where:
- d = link distance
- d0 = reference distance
- n = path-loss exponent

## 3. RSSI

RSSI is a measure of received signal strength. More positive / less-negative values generally represent stronger received signals.

## 4. Noise

Noise is unwanted random energy present in the communication channel. Higher noise makes reliable reception harder.

## 5. Interference

Interference comes from unwanted signals occupying or affecting the same communication environment. It can reduce SNR and increase packet failures.

## 6. SNR

SNR compares useful received signal power with noise:

SNR(dB) = RSSI(dBm) - Noise(dBm)

Higher SNR normally indicates a cleaner link.

## 7. Time-varying channel

In mobile and IoT environments, wireless conditions change with time. The simulator changes distance, noise, interference and channel quality to represent this behavior.

## 8. Packet success

The simulator converts link quality into a packet-success probability. A random draw then determines whether a packet is received successfully.

This is a simulation model, not a physical-layer implementation.

## 9. Machine learning

A Random Forest classifier learns a relationship between channel features and link reliability. It uses multiple decision trees and combines their predictions.

Features:
- distance
- RSSI
- SNR
- noise
- interference
- recent success rate

Target:
- reliable_link

## 10. Age of Information

AoI measures information freshness at the receiver. Every time a packet is successfully delivered, the information age is reset. If transmissions fail, the age continues to increase.

Lower AoI means fresher information.

## 11. Why compare multiple strategies?

A good project should not only show that ML works. It should compare ML against simple baselines.

- Random: simplest baseline
- Distance: simple geometric heuristic
- RSSI/SNR: signal-quality heuristic
- ML: combines multiple features

This makes the experimental conclusion more meaningful.
