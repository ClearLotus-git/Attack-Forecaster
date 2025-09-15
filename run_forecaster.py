import json
import argparse
from forecaster import forecast, load_transitions, load_evidence

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--live-mitre", action="store_true", help="Pull latest ATT&CK data from MITRE CTI repo")
    args = parser.parse_args()

    # Load input evidence
    evidence = load_evidence("input-evidence.json")
    current_chain = [item["technique_id"] for item in evidence["observed"]]

    # Load transitions (local or live)
    if args.live_mitre:
        transitions = load_transitions(live=True)
    else:
        transitions = load_transitions("data-transitions.json")

    # Forecast next techniques
    predictions = forecast(current_chain, transitions)

    # Pretty print results
    result = {
        "current_chain": current_chain,
        "top_predictions": predictions
    }

    print("=== Attack Path Forecast ===")
    print(json.dumps(result, indent=2))
