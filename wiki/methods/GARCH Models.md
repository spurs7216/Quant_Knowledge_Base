---
title: GARCH Models
type: method
status: seed
updated: 2026-04-20
tags:
  - method
  - time-series
  - volatility
  - garch
domain: quant-finance
sources:
  - "[[Applied Time Series Analysis and Forecasting with Python]]"
  - "[[Applied Time Series Analysis and Forecasting with Python - Ch 06 Financial Time Series and Related Models]]"
---
# GARCH Models

## Summary

GARCH models move dependence out of the conditional mean and into the conditional variance:

`X_t = sigma_t epsilon_t`

`sigma_t^2 = omega + sum alpha_i X_{t-i}^2 + sum beta_j sigma_{t-j}^2`

This is the classical way to model volatility clustering when returns are close to white noise in mean but not in second moments.

## Core logic

The method begins from a finance-specific fact:

- returns can be serially uncorrelated
- but their magnitudes or squares can still be strongly dependent

So the right question is not only whether `E(X_t | F_{t-1})` is predictable. It is whether `Var(X_t | F_{t-1})` is predictable.

## Load-bearing implications

- `E(X_t | F_{t-1}) = 0`
- `Var(X_t | F_{t-1}) = sigma_t^2`
- under standard stationarity conditions, squared returns behave like an ARMA-type process
- persistence in `sigma_t^2` produces volatility clustering

That is why GARCH can explain clustered turbulence even when the return series itself looks close to white noise.

## Practical workflow

1. Fit a mean model first if the observed series still has serial correlation.
2. Check residual squares or absolute residuals for dependence.
3. Fit a parsimonious ARCH/GARCH family to the residuals.
4. Test whether standardized residuals and their squares are now close to white noise.
5. If asymmetry matters, escalate to EGARCH, TGARCH, or related variants.

## What it is good for

- volatility forecasting
- risk and VaR pipelines
- stress and turbulence monitoring
- separating mean predictability from variance predictability

## Failure modes

- fitting GARCH directly to a series whose mean is still misspecified
- assuming volatility persistence means return predictability
- forcing Gaussian residuals on obviously heavy-tailed data
- ignoring asymmetry when downside shocks behave differently from upside shocks
- treating one successful sample fit as proof of regime robustness

## Quant relevance

For quant research, GARCH is a baseline volatility language. Even when later models become realized-volatility, state-space, or ML-based, the GARCH question remains:

- is the conditional variance persistent?
- does asymmetry matter?
- do standardized residuals actually look closer to noise after modeling?

## Related notes

- [[Time-Series Forecasting]]
- [[ARIMA and Box-Jenkins Modeling]]
- [[Applied Time Series Analysis and Forecasting with Python]]

## Sources

- [[Applied Time Series Analysis and Forecasting with Python]]
- [[Applied Time Series Analysis and Forecasting with Python - Ch 06 Financial Time Series and Related Models]]
