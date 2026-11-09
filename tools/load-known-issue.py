#!/usr/bin/env python3
"""Collect every AUDIT-ACCEPTED-*, HOMEPAGE-OOS-* and V4LE-* tag with its line.
usage: load_known_issues.py <path-to-KNOWN_ISSUES_ALL_SOURCES.md> <out.json>
"""
import json, re, sys, pathlib

src = pathlib.Path(sys.argv[1]).read_text().splitlines()
out = sys.argv[2]
tag = re.compile(r"((?:AUDIT-ACCEPTED|HOMEPAGE-OOS|V4LE)-[A-Z0-9-]+)")
seen = {}
for n, line in enumerate(src, 1):
    for t in tag.findall(line):
        seen.setdefault(t, {"tag": t, "line": n, "excerpt": line.strip()[:300],
                            "functions": [], "invariant": ""})
pathlib.Path(out).write_text(json.dumps(list(seen.values()), indent=2))
print(f"{len(seen)} tags written to {out}")


Run it: python3 tools/load_known_issues.py path/to/KNOWN_ISSUES_ALL_SOURCES.md knowledge/accepted.json

Then open knowledge/accepted.json and fill functions (list of function names the tag covers) and invariant (one sentence) for each entry that matters. The script finds the tags; you supply the scope. This is the manual part, and it is worth doing.