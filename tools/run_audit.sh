#!/usr/bin/env bash
set -euo pipefail
REPO="$1"            # path to the pinned v4lend clone
COMMIT="$2"          # f6d0fb41b7487f60ce64e011312a956e184e2a75
KNOWN="$3"           # path to KNOWN_ISSUES_ALL_SOURCES.md

python3 tools/load_known_issues.py "$KNOWN" knowledge/accepted.json

# Your harness: run each agent over $REPO with knowledge/ and the agents/ prompts.
# It must write output/raw/<agent>.txt and output/candidates.json.
# Example placeholder:  your-harness run --repo "$REPO" --out output/

python3 tools/check_markers.py output/raw
python3 tools/prove.py "$REPO" "$COMMIT" output/candidates.json output/proof.json
python3 tools/dedup.py output/candidates.json knowledge/accepted.json

echo "Done. Review output/candidates.json: only status=proven and dedup=new go to a human."

Make it executable with chmod +x tools/run_audit.sh.