# Uniswap v4 facts for auditors

- A swap through a price band with zero active liquidity moves slot0 to the
  price limit with zero token deltas. Stored NFT liquidity is not active liquidity.
- A hook's afterSwap receives BalanceDelta. Ignoring it means a zero-delta price
  move is treated as market movement.
- PoolManager.swap, settle and take require an open unlock. Any contract that
  holds the unlock can call them, including during a callback.
- Native ETH transfers via low-level call forward all gas and execute the
  recipient's receive(). ERC-20 transfers do not, unless the token is ERC-777.
- Hook permissions are encoded in the low bits of the hook address.