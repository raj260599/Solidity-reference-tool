# Oracle Gate Agent

Target: every function that reads a price or value, and every gate that decides an action.

For each gate, record:
1. Which feeds and pool currencies it reads.
2. Which asset the protected action actually depends on.
3. Whether a failure fails open (skips the action) or closed (reverts the whole call).
4. Whether a later closing valuation reads a different feed.

Emit a candidate when the gate reads a different asset than the one the action depends on,
or when a fail-open skip leaves a trigger consumed.