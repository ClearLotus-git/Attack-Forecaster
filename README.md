# Attack Path Forecaster

A lightweight Python tool that forecasts the **next likely adversary techniques** based on MITRE ATT&CK transition mappings.

Given observed techniques from alerts/logs, it predicts possible next steps in the attack chain and outputs the top candidates with confidence scores.

```
ingest (alerts/logs) → technique resolver → attack-graph forecaster → recommendations
                                             ↑
                                  ATT&CK transitions + weights
```

---

## Features
- Ingests observed attacker techniques (`input-evidence.json`)
- Uses weighted transitions (`data-transitions.json`) to forecast likely next techniques
- Provides top 3 predictions with normalized scores
- Simple, dependency-light (just Python built-ins)

---
## Run
```
$ python run_forecaster.py
```
---


## Example

### Input (`input-evidence.json`)
```json
{
  "observed": [
    {"technique_id": "T1566.001", "source": "email_gateway"},
    {"technique_id": "T1059.001", "source": "sysmon"}
  ]
}
```

## Output

```
=== Attack Path Forecast ===
{
  "current_chain": [
    "T1566.001",
    "T1059.001"
  ],
  "top_predictions": [
    {
      "technique_id": "T1027",
      "score": 1.0
    },
    {
      "technique_id": "T1105",
      "score": 0.91
    },
    {
      "technique_id": "T1003.001",
      "score": 0.82
    }
  ]
}
```

## License

This project is released under the MIT License.  
You are free to use, modify, and distribute it with attribution.

© 2025 ClearLotus









