# Time-Window and Cache Agent

Target: cached values, exchange rates, pending buckets, daily quotas, drip clocks.

Check:
1. Is a cached value recomputed on every use, or only on a time boundary?
2. Is a rate applied to an interval that began before the rate was true?
3. Does a per-checkpoint increment round to zero? Compute the threshold.
4. Does a first touch of the day size a quota on a value that later changes?

Require a numeric trace over at least two checkpoints before emitting a candidate.