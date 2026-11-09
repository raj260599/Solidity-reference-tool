#!/usr/bin/env python3
"""Recall over the benchmark: a benchmark item is hit if a PROVEN candidate
names its contract and one of its functions.
usage: recall.py output/candidates.json benchmark/accepted7.json
"""
import json, sys, pathlib

cands = [c for c in json.loads(pathlib.Path(sys.argv[1]).read_text()) if c.get("status") == "proven"]
bench = json.loads(pathlib.Path(sys.argv[2]).read_text())
hits = 0
for b in bench:
    ok = any(c["contract"] == b["contract"] and c["function"] in b["functions"] for c in cands)
    hits += ok
    print(("HIT  " if ok else "MISS ") + b["id"])
print(f"recall {hits}/{len(bench)}")



Run it after every prompt change: python3 tools/recall.py output/candidates.json benchmark/accepted7.json


Record the baseline first, with the old prompts, so you can see what each change adds. Expect recall to improve on the lifecycle and oracle-gate items first, then authority and time-window. A false-positive count matters too: track how many proven candidates the dedup step marks as duplicates of accepted items.