import json
from collections import defaultdict

DECAY = 0.7  # weight decay for two-hop lookahead

def load_transitions(path="data-transitions.json"):
    """Load technique transition graph from JSON."""
    with open(path, "r", encoding="utf-8") as f:
        edges = json.load(f)

    graph = defaultdict(list)
    for e in edges:
        graph[e["from"]].append({
            "to": e["to"],
            "weight": float(e["weight"]),
            "note": e.get("note", "")
        })
    return graph


def one_hop_scores(graph, last_tid):
    """Direct predictions from last technique."""
    scores = defaultdict(float)
    for edge in graph.get(last_tid, []):
        scores[edge["to"]] = max(scores[edge["to"]], edge["weight"])
    return scores


def two_hop_scores(graph, last_tid):
    """Indirect predictions (neighbors of neighbors)."""
    scores = defaultdict(float)
    for edge in graph.get(last_tid, []):
        mid = edge["to"]
        for edge2 in graph.get(mid, []):
            scores[edge2["to"]] = max(
                scores[edge2["to"]],
                edge["weight"] * edge2["weight"] * DECAY
            )
    return scores


def normalize(scores):
    """Scale scores 0–1 relative to max."""
    if not scores:
        return {}
    maxv = max(scores.values())
    if maxv == 0:
        return dict(scores)
    return {k: round(v / maxv, 2) for k, v in scores.items()}


def forecast(evidence_path="input-evidence.json",
             transitions_path="data-transitions.json"):
    """Main forecasting function."""
    # Load evidence
    with open(evidence_path, "r", encoding="utf-8") as f:
        evidence = json.load(f)

    chain = [e["technique_id"] for e in evidence.get("observed", [])]
    last = chain[-1] if chain else None
    if not last:
        return {"error": "No observed techniques provided."}

    # Load transitions graph
    graph = load_transitions(transitions_path)

    # One-hop + two-hop scores
    s1 = one_hop_scores(graph, last)
    s2 = two_hop_scores(graph, last)

    combined = defaultdict(float)
    for k, v in s1.items():
        combined[k] = max(combined[k], v)
    for k, v in s2.items():
        combined[k] = max(combined[k], v)

    # Drop already-seen techniques
    for tid in chain:
        combined.pop(tid, None)

    # Normalize + rank
    combined = normalize(combined)
    top = sorted(combined.items(), key=lambda x: x[1], reverse=True)[:3]

    return {
        "current_chain": chain,
        "top_predictions": [
            {"technique_id": k, "score": v} for k, v in top
        ]
    }


if __name__ == "__main__":
    result = forecast()
    print(json.dumps(result, indent=2))
