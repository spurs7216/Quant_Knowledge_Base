---
title: Term-Structure Models
type: method
status: seed
updated: 2026-04-22
tags:
  - method
  - quant-finance
  - fixed-income
  - term-structure
domain: quant-finance
sources:
  - "[[Stochastic Calculus for Finance II]]"
  - "[[Stochastic Calculus for Finance II - Ch 10 Term-Structure Models]]"
  - "[[Change of Numeraire and Forward Measures]]"
  - "[[Arbitrage Theory in Continuous Time - Ch 19 Bonds and Interest Rates]]"
  - "[[Arbitrage Theory in Continuous Time - Ch 21 Martingale Models for the Short Rate]]"
  - "[[Arbitrage Theory in Continuous Time - Ch 22 Forward Rate Models]]"
  - "[[Arbitrage Theory in Continuous Time - Ch 23 LIBOR Market Models]]"
---
# Term-Structure Models

## Summary

Term-structure models describe the joint evolution of zero-coupon bond prices, short rates, forward rates, and forward LIBOR rates. Their central difficulty is not only fitting one yield. It is preserving no-arbitrage across the entire maturity curve.

## Core equations

The short rate is
$$R(t)=f(t,t).$$

Zero-coupon bond prices and the forward curve are related by
$$B(t,T)=\exp\paren{-\int_t^T f(t,u)\,du}.$$

In HJM form, the forward curve evolves under the risk-neutral measure as
$$df(t,T)=\sigma(t,T)\sigma^\star(t,T)\,dt+\sigma(t,T)\,d\widetilde{W}(t),$$
where
$$\sigma^\star(t,T)=\int_t^T \sigma(t,u)\,du.$$

Zero-coupon bond prices then satisfy
$$dB(t,T)=R(t)B(t,T)\,dt-\sigma^\star(t,T)B(t,T)\,d\widetilde{W}(t).$$

Forward LIBOR is defined by
$$L(t,T)=\frac{1}{\delta}\paren{\frac{B(t,T)}{B(t,T+\delta)}-1}.$$

In affine short-rate models, bond prices often take the form
$$B(t,T)=A(t,T)e^{-B(t,T)R(t)}.$$

## Main logic

### 1. No-arbitrage ties drift to volatility

In curve models, volatility can often be chosen more freely than drift. The drift is then forced by the no-arbitrage restriction.

### 2. Different model families choose different state variables

- short-rate models choose $R(t)$ or a factor state
- HJM chooses the whole forward curve
- forward-LIBOR models choose market-observed discrete forward rates

### 3. Calibration convenience and tractability are part of the design problem

Affine-yield models, HJM, and market models solve different tradeoffs between parsimony, fit, and payoff alignment.

## Failure modes

- calibrating curve levels without enforcing no-arbitrage dynamics
- using a state variable whose payoff mapping is awkward for the product being priced
- forgetting that term-structure models are curve models, not single-maturity models

## Quant relevance

This method matters for:

- fixed-income derivatives
- discount-curve and forward-curve modeling
- caplet and swaption pricing
- rates risk decomposition and scenario generation

## Related notes

- [[Change of Numeraire and Forward Measures]]
- [[Risk-Neutral Pricing and Fundamental Theorems of Asset Pricing]]
- [[Derivatives Markets]]
- [[Stochastic Calculus]]

## Sources

- [[Stochastic Calculus for Finance II]]
- [[Stochastic Calculus for Finance II - Ch 10 Term-Structure Models]]
- [[Change of Numeraire and Forward Measures]]
- [[Arbitrage Theory in Continuous Time - Ch 19 Bonds and Interest Rates]]
- [[Arbitrage Theory in Continuous Time - Ch 21 Martingale Models for the Short Rate]]
- [[Arbitrage Theory in Continuous Time - Ch 22 Forward Rate Models]]
- [[Arbitrage Theory in Continuous Time - Ch 23 LIBOR Market Models]]
