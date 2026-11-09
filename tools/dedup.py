#!/usr/bin/env python3
"""Classify each candidate as new, duplicate, or accepted-assumption-violated.
This is a heuristic. A human reviews every result before submission.
usage: dedup.py output/candidates.json knowledge/accepted.json
"""
import json, sys, pathlib

cands = json.loads(pathlib.Path(sys.argv[1]).read_text())
accepted = json.loads(pathlib.Path(sys.argv[2]).read_text())

for c in cands:
    if c.get("assumption_violated"):
        c["dedup"] = f"accepted-assumption-violated:{c['assumption_violated']}"
        continue
    hits = [a for a in accepted if c["function"] in a.get("functions", [])]
    if not hits:
        c["dedup"] = "new"
    elif any(a.get("invariant") and a["invariant"] in c.get("invariant", {}).get("text", "") for a in hits):
        c["dedup"] = f"duplicate-of:{hits[0]['tag']}"
    else:
        c["dedup"] = "same-function-review:" + ",".join(a["tag"] for a in hits)

pathlib.Path(sys.argv[1]).write_text(json.dumps(cands, indent=2))
for c in cands:
    print(f"{c['id']}: {c['dedup']}")