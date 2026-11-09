#!/usr/bin/env python3
"""Fail the run if an agent skipped its required markers.
usage: check_markers.py output/raw
"""
import pathlib, re, sys

bad = False
for f in sorted(pathlib.Path(sys.argv[1]).glob("*.txt")):
    t = f.read_text()
    feyn = len(re.findall(r"\[Tool: Feynman\]", t))
    inv = len(re.findall(r"\[Tool: Inversion:", t))
    if feyn == 0 or inv == 0:
        print(f"FAIL {f.name}: feynman={feyn} inversion={inv}")
        bad = True
    else:
        print(f"ok   {f.name}: feynman={feyn} inversion={inv}")
sys.exit(1 if bad else 0)

Markers do not prove the reasoning was done, but missing ones are a cheap signal that the agent skipped the pass.