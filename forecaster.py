import json
import requests

MITRE_ENTERPRISE_URL = "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json"

def load_evidence(path="input-evidence.json"):
    """Load observed attacker evidence from JSON file."""
    with open(path, "r") as f:
        return json.load(f)


def load_transitions(path="data-transitions.json", live=False):
    """
    Load ATT&CK transitions.
    - If live=True, fetch MITRE's enterprise-attack.json bundle.
    - Otherwise, load from local JSON file.
    """
    if live:
        print(f"[INFO] Fetching MITRE ATT&CK enterprise dataset...")
        resp = requests.get(MITRE_ENTERPRISE_URL)
        resp.raise_for_status()
        data = resp.json()["objects"]

        transitions = {}

        # Build transitions using "relationship" objects
        for obj in data:
            if obj.get("type") == "relationship" and obj.get("relationship_type") == "uses":
                src = obj.get("source_ref", "")
                tgt = obj.get("target_ref", "")

                # Only keep technique-to-technique links
                if src.startswith("attack-pattern--") and tgt.startswith("attack-pattern--"):
                    transitions.setdefault(src, []).append(tgt)

        return transitions
    else:
        with open(path, "r") as f:
            return json.load(f)


def forecast(current_chain, transitions, top_k=3):
    """
    Given the current chain of techniques, suggest next likely techniques.
    """
    if not current_chain:
        return []

    last_step = current_chain[-1]
    candidates = transitions.get(last_step, [])

    results = []
    for i, c in enumerate(candidates[:top_k]):
        results.append({
            "technique_id": c,
            "weight": round(1.0 - (i * 0.1), 2)
        })
    return results
