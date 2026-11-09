# Lifecycle and Trigger Agent

Target: any try/catch, consume-before-dispatch, restore path, or rollback.

For each swallowed failure (catch {} or failed-action event):
1. List which state is committed and which is rolled back.
2. Check whether the trigger or node is consumed before the failing call.
3. Name the attacker-controlled input (token donation, amount, price move)
   that makes the failure deterministic.
4. If the failure is deterministic and the position loses protection, emit a candidate.

Required markers: [Tool: Feynman] on every new function; [Tool: Inversion] on every guard.