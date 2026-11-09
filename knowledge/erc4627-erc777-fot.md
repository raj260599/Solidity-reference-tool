# Token and vault behaviour

- ERC4626 maxRedeem and maxDeposit can cap an operation below the recorded share balance.
- ERC-777 tokensToSend runs before the sender balance is decremented; tokensReceived
  runs after the recipient balance is incremented. Both allow reentry.
- Fee-on-transfer tokens deliver less than the requested amount; a settle() return
  value must be checked.