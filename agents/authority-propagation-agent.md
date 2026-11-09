# Authority Propagation Agent

Target: every external entry point and every call that forwards caller-supplied data.

For each hop:
1. Who is msg.sender at this hop? Who is msg.sender at the next hop?
2. Who authored each parameter, including bytes hookData?
3. If an approval was granted to contract X and X forwards a caller's data,
   the caller may be using X's authority. Name the approval and the caller.

Output a candidate only with a concrete call sequence from an unrelated caller.
Required markers: [Tool: Socratic: file:line] on every authority check.