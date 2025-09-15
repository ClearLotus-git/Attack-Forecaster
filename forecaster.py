import json
import argparse
import requests
from stix2 import MemoryStore

# Default transition file
DEFAULT_TRANSITIONS_FILE = "data-transitions.json"

# MITRE CTI ATT&CK dataset (enterprise)
MITRE_URL = "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json"


def load_transitions(local=True):
    if local:
        with open(DEFAULT_TRANSITIONS_FILE, "r") as f:
            return json.load(f)
    else:
        print("[*] Fetching MITRE ATT&CK dataset...")
        data = requests.get(MITRE_URL).json()
        ms = MemoryStore(stix_data=data["objects"])

        # Build transitions dynamically
        transitions = {}
        for rel in ms.query(["relationship"]):
            if rel["relationship_type"] == "uses":
                src = rel.get("source_ref", "")
                tgt = rel.get("target_ref", "")
                transitions.setdefault(src, []).append(tgt)

        return transitions


def forecast(current_chain, transitions, top_n=3):
    last_step = current_chain[-1]
    candidates = transitions.get(last_step, [])

    results = []
    for c in candidates:
        results.append({"technique_id": c, "score": 1.0})  # Placeholder score

    return results[:top_n]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--live-mitre", action="store_true", help="Use live MITRE ATT&CK dataset")
    args = parser.parse_args()

    transitions = load_transitions(local=not args.live_mitre)

    # Load example evidence
    with open("input-evidence.json") as f:
        evidence = json.load(f)

    chain = [obs["technique_id"] for obs in evidence["observed"]]

    predictions = forecast(chain, transitions)

    print("=== Attack Path Forecast ===")
    print(json.dumps({
        "current_chain": chain,
        "top_predictions": predictions
    }, indent=2))
