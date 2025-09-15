import json
import argparse
from forecaster import forecast, load_transitions, load_evidence

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--live-mitre", action="store_true", help="Use MITRE ATT&CK enterprise dataset")
    args = parser.parse_args()

    # Load evidence
    evidence = load_evidence("input-evidence.json")
    current_chain = [item["technique_id"] for item in evidence["observed"]]

    # Load transitions (local or live MITRE)
    transitions = load_transitions(live=args.live_mitre)

    # Run forecast
    predictions = forecast(current_chain, transitions)

    result = {
        "current_chain": current_chain,
        "top_predictions": predictions
    }

    print("=== Attack Path Forecast ===")
    print(json.dumps(result, indent=2))
