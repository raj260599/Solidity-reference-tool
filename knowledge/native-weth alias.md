# WETH / native ETH alias

- In a pool containing native ETH and WETH, a resolver that matches literal currency
  addresses before the alias can select the wrong leg (RevertHookActionBase._lendCurrency).
- Direct wrapping of native ETH to WETH is 1:1. A swap between them is never required
  for repayment and only adds fee and price impact.