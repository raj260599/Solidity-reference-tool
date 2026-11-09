#!/usr/bin/env python3
"""Proof loop. A candidate is "proven" only if:
  1. its attack test and control test PASS on the pinned commit, and
  2. with fix_patch applied, the attack test FAILS and the control test PASSES.
Compile errors are reported separately so a repair round can fix them.

usage: prove.py <repo> <pinned-commit> <candidates.json> <out.json>
"""
import json, pathlib, re, subprocess, sys

repo, commit, cand_path, out_path = sys.argv[1:5]
repo = pathlib.Path(repo).resolve()
work = pathlib.Path("/tmp/audit-tree")
patches = pathlib.Path("/tmp/audit-patches"); patches.mkdir(exist_ok=True)
RESULT = re.compile(r"\[(PASS|FAIL)[^\]]*\]\s+(\w+)\(")

def sh(args, cwd, timeout=1800):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=timeout)

def forge(rel, names):
    p = sh(["forge", "test", "--offline", "--match-path", rel,
            "--match-test", names, "-vv"], work)
    text = p.stdout + p.stderr
    results = {m.group(2): m.group(1) for m in RESULT.finditer(text)}
    compiled = "Compiler run failed" not in text and "Error:" not in text
    return results, compiled, text

def reset(rel):
    sh(["git", "checkout", "--", "."], work)
    (work / rel).unlink(missing_ok=True)

if not work.exists():
    r = sh(["git", "-C", str(repo), "worktree", "add", "--detach", str(work), commit], repo)
    if r.returncode != 0:
        sys.exit(f"worktree failed: {r.stderr}")

cands = json.loads(pathlib.Path(cand_path).read_text())
results = []
for c in cands:
    rel = f"test/agent/{c['id']}.t.sol"
    (work / rel).parent.mkdir(parents=True, exist_ok=True)
    (work / rel).write_text(c["poc_solidity"])
    names = f"{c['proof_test']}|{c['control_test']}"
    status, detail = "unproven", ""
    try:
        res, compiled, text = forge(rel, names)
        if not compiled:
            status, detail = "compile-error", text[-2000:]
        elif res.get(c["proof_test"]) == "PASS" and res.get(c["control_test"]) == "PASS":
            status = "reproduced"
            if c.get("fix_patch"):
                patch = patches / f"{c['id']}.patch"
                patch.write_text(c["fix_patch"])
                applied = sh(["git", "apply", str(patch)], work)
                if applied.returncode != 0:
                    status, detail = "patch-does-not-apply", applied.stderr[-1000:]
                else:
                    res2, _, text2 = forge(rel, names)
                    if res2.get(c["proof_test"]) == "FAIL" and res2.get(c["control_test"]) == "PASS":
                        status = "proven"
                    else:
                        status, detail = "fix-not-refuted", text2[-2000:]
                reset(rel)
        else:
            detail = text[-2000:]
    finally:
        reset(rel)
    results.append({"id": c["id"], "status": status, "detail": detail})
    c["status"] = status
    print(f"{c['id']}: {status}")

pathlib.Path(cand_path).write_text(json.dumps(cands, indent=2))
pathlib.Path(out_path).write_text(json.dumps(results, indent=2))

Two notes:

The first run builds the Foundry project, which takes minutes. Later runs reuse the worktree.
If a candidate has compile-error, feed the detail text back to the agent for one repair round, then rerun the proof loop. Do not promote it on the first failure.