# Results Guide

After running:

```bash
python src/run_all.py
```

inspect:

- `results/model_metrics.csv`
- `results/strategy_comparison.csv`
- `results/figures/`

The main result should answer:

> Does ML-assisted link selection improve reliability and information freshness compared with simple selection strategies?

Use the generated CSV values in your report rather than manually typing performance numbers.

## Recommended figures

1. Strategy vs Packet Success Rate
2. Strategy vs Average Latency
3. Strategy vs Failed Transmissions
4. Strategy vs Average AoI
5. Strategy vs Selected-Link Reliability
6. RSSI vs Distance
7. SNR over Simulation Time

## How to write the conclusion

Use the actual generated values. A suitable structure is:

“Among the evaluated strategies, [best strategy] achieved the highest packet success rate of [value]%, while [best/other strategy] produced the lowest average AoI of [value] ms. The results indicate that considering multiple channel features can provide a more informed link-selection decision than a single heuristic. These results are limited to the assumptions of the simulation model.”
