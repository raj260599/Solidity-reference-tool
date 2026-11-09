# Shared Scan Rules

## Bundle contents

Your bundle is four concatenated files: all in-scope source code, the SOP (HOW to think), your specialty agent (WHAT to look for), and these shared rules (output format, dedup tags, AND mandatory mental tool protocol).

Read the whole bundle once at the start. The bundle contains all in-scope source. Use Read/Grep only for cross-file searches or out-of-scope context (interfaces/, lib/, mocks/, test/) — do not re-read in-scope files for the initial scan.

**The protocol below applies continuously during source reading — not just before it.** The "read source" phase does not turn off the protocol; every trigger condition fires the moment it occurs, throughout your entire review.

When matching function names, check both `functionName` and `_functionName` (Solidity convention).

## Mental tool protocol — MANDATORY

The three tools in `senior-auditor-sop.md` are NOT optional. Each tool has a specific trigger. **When the trigger fires, you MUST emit the corresponding marker in your output stream BEFORE continuing.** No skipping. The markers live in your working text — they do NOT go into the FINDING/LEAD output blocks.

### Triggers → required markers

| Trigger (the condition) | Marker (required immediately, literal `[Tool: ...]` syntax) | Content |
|---|---|---|
| You open a new function or contract to read | `[Feynman: <name>]` | Explain what it does in plain English — no Solidity jargon, no `mload`/`assembly`/`mstore`/`safeTransfer`/etc. Use as many sentences as you need until the explanation is solid. If your wording slips back to jargon, you're papering over an assumption — keep going. Wherever your plain-English explanation gets fuzzy or you have to reach for a Solidity term to keep it accurate, mark that spot — that is where bugs hide. |
| You stop on a line whose purpose isn't immediately clear | `[Socratic: <file:line> — why?]` | A one-line question that drills past "because that's how it's written." If your first answer is a restatement of the code, ask again. Stop when the answer exposes the implicit belief the code rests on — don't pad with extra steps just to hit a quota. |
| A code path reads as clean / a check looks sufficient / a guard looks correct | `[Inversion: <function>]` | Three concrete attacker moves that attempt to defeat the path. Specific addresses/values/states, not abstractions. |

### Rules

1. **Triggers are not optional.** If the condition fires, the marker follows. Always. No skipping.
2. **Use the literal `[Tool: ...]` syntax.** The orchestrator greps your output for these tags after the run.
3. **You may emit a marker without a trigger.** Extra Feynman / Inversion markers are fine. You may NOT skip a marker after its trigger fired.
4. **The protocol applies to reasoning depth, not output volume.** Heavy use of these tools is what produces the audit work. Skipping them = surface-level scanning, which is the failure mode of every junior auditor.

The orchestrator verifies marker counts after every run. Skipped markers downgrade the value of your findings and are recorded as workflow violations.

## Cross-contract patterns

When you find a bug in one contract, **weaponize that pattern across every other contract in the bundle.** Search by function name AND by code pattern. Finding native/ERC20 confusion in `ContractA.onRevert` means you check every other contract's `onRevert` — missing a repeat instance is an audit failure.

After scanning: escalate every finding to its worst exploitable variant (DoS may hide fund theft). Then revisit every function where you found something and attack the other branches.

## Do not report

- Pure admin actions with no configuration-induced violation.
- Standard tradeoffs that the repo's accepted list already names (check accepted.json first).
- Anything without a proof test. It goes to the notes file, not the candidates.

## Output

Write `output/candidates.json`: a JSON array. A candidate may only have
status "candidate" until the proof loop runs. Every field is required.

```json
[
  {
    "id": "M02-pace",
    "contract": "HookLeaseController",
    "function": "_addPending",
    "bug_class": "mutable-state-at-accrual",
    "preconditions": [
      {"kind": "public | config-owner | token-trust | market-move", "realistic": true, "note": "..."}
    ],
    "invariant": {"text": "one horizon of rent at the accrual price", "source": "docs/audit-handoff.md:205"},
    "path": ["caller", "function", "state change", "impact"],
    "poc_solidity": "<full Foundry test file>",
    "proof_test": "test_name_attack",
    "control_test": "test_name_control",
    "fix_patch": "<unified diff, or empty>",
    "fix": "one sentence",
    "assumption_violated": "accepted tag this violates, or empty"
  }
]
```

Rules:
- Use `[Tool: Feynman]`, `[Tool: Socratic: file:line]` and `[Tool: Inversion: function]` exactly.
  The old file mixed `[Feynman: <n>]` and `[Tool: ...]`; use only the second form.
- Do not drop a candidate because its precondition is configuration. Grade the
  precondition in `preconditions` instead.
- Every candidate needs `poc_solidity` with an attack test and a control test.