"""Export synthetic model evidence without account identifiers or machine paths."""
import argparse
import hashlib
import json
from pathlib import Path


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def export(directory):
    preflight = json.loads((directory / "preflight.json").read_text())
    plan = preflight["plan"]
    plan["issue"] = 4968
    rows = []
    for cell in preflight["cells"]:
        root = directory / cell["id"]
        result = json.loads((root / "result.json").read_text())
        trace = [json.loads(line) for line in (root / "rpc.jsonl").read_text().splitlines()]
        rows.append({
            "cell": cell,
            "returncode": result["returncode"],
            "stop_reason": result["stop_reason"],
            "duration_seconds": result["duration_seconds"],
            "output_bytes": result["output_bytes"],
            "score": result["score"],
            "trace": [{key: value for key, value in event.items() if key != "at"} for event in trace],
            "final_state": json.loads((root / "state.json").read_text()),
            "raw_sha256": {name: digest(root / name) for name in ("stdout.jsonl", "stderr.txt", "rpc.jsonl", "state.json", "result.json")},
        })
    return {
        "plan": plan,
        "source_hashes": preflight["source_hashes"],
        "auth": preflight["auth"],
        "client_versions": preflight["client_versions"],
        "raw_sha256": {name: digest(directory / name) for name in ("preflight.json", "ledger.jsonl")},
        "predecessor_ledger_sha256": list(preflight.get("prior_ledgers", {}).values()),
        "attempts_reserved": len((directory / "ledger.jsonl").read_text().splitlines()),
        "publication_normalization": "Issue URL represented by issue number; machine paths and timestamps omitted. Original raw artifact hashes retained. Task success remains ungraded by this exporter; see manual-review.json.",
        "results": rows,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.write_text(json.dumps(export(args.directory), indent=2, sort_keys=True) + "\n")
