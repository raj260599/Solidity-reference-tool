# Oracle facts for this repo (pinned f6d0fb4)

- V4Oracle grace period after sequencer restart: 600 s (V4Oracle.sol:72).
- Deploy scripts use a 200 bps Chainlink-vs-TWAP tolerance and a 30-minute TWAP window.
- A feed round older than maxFeedAge reverts; a round older than the restart but
  within maxFeedAge still passes the staleness check.
- Recovery periods are per token. A gate that reads only the pool currencies
  does not see the vault asset's feed.
- Closing valuations (transform health checks) can revert on deviation even when
  the trigger gate passes. A revert there rolls back an action that already swapped.