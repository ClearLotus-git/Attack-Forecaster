# Attack Path Forecaster

A lightweight Python tool that forecasts the **next likely adversary techniques** based on MITRE ATT&CK® transition mappings.

Given observed attacker techniques (from alerts, logs, or manual input), it predicts possible next steps in the attack chain and outputs the top candidate techniques with confidence weights.

---

## Features
- Ingests observed attacker techniques (`input-evidence.json`)
- Uses weighted transitions (`data-transitions.json`) or live MITRE data
- Forecasts **top 3 likely next ATT&CK techniques**
- Supports offline (local JSON) and online (`--live-mitre`) modes
- Dependency-light (just Python + `requests`)

---

## Installation
Clone the repo:
```bash
git clone https://github.com/ClearLotus-git/Attack-Forecaster.git
cd Attack-Forecaster
pip install -r requirements.txt
```
## Usage

### Run with local data:

```
$ python3 run_forecaster.py
```
### Run with live MITRE ATT&CK data:

```
$ python3 run_forecaster.py --live-mitre
```

## Example

### Input (input-evidence.json)

```
{
  "observed": [
    {"technique_id": "T1566.001", "source": "email_gateway"},
    {"technique_id": "T1059.001", "source": "sysmon"}
  ]
}
```

### Output

```
{
  "current_chain": ["T1566.001", "T1059.001"],
  "top_predictions": [
    {"technique_id": "T1027", "weight": 0.8},
    {"technique_id": "T1105", "weight": 0.7}
  ]
}

```

## License

Released under the MIT License.
© 2025 ClearLotus

---

<sub>⚠️ Note: Live MITRE integration is still experimental. Current predictions are based on local transition data. Future updates may expand live data support.</sub>
