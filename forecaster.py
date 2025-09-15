import json
import requests

def load_evidence(path="input-evidence.json"):
    """Load observed attacker techniques + context from JSON file."""
    with open(path, "r") as f:
        return json.load(f)

def load_transitions(path="data-transitions.json", live=False):
    """
    Load ATT&CK technique transitions.
    - Local: from JSON file in repo
    - Live: from MITRE CTI GitHub (attack-pattern.json)
    """
    if live:
        url = "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/attack-pattern/attack-pattern.json"
        print(f"[INFO] Fetching MITRE ATT&CK data from {url}")
        resp = requests.get(url)
        resp.raise_for_status()
        data = resp.json()
        transitions = {}

        # Build a simple mapping: technique_id -> related technique_ids
        for obj in data.get("objects", []):
            if obj.get("type") == "attack-pattern":
                tid = obj.get("external_references", [{}])[0].get("external_id")
                if tid:
                    # For demo, we’ll just map to same ID to avoid empty dict
                    transitions[tid] = [tid]
        return transitions
    else:
        with open(path, "r") as f:
            return json.load(f)

def forecast(current_chain, transitions, top_k=3):
    """
    Predict next likely techniques based on current chain + transitions.
    """
    if not current_chain:
        return []

    last_step = current_chain[-1]
    candidates = transitions.get(last_step, [])

    # Weighting: simple decreasing scores
    results = []
    for i, c in enumerate(candidates[:top_k]):
        results.append({
            "technique_id": c,
            "weight": round(1.0 - (i * 0.1), 2)
        })
    return results
