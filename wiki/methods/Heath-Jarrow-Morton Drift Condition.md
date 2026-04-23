---
title: Heath-Jarrow-Morton Drift Condition
type: method
status: seed
updated: 2026-04-22
tags:
  - method
  - quant-finance
  - fixed-income
  - hjm
domain: quant-finance
sources:
  - "[[Arbitrage Theory in Continuous Time]]"
  - "[[Arbitrage Theory in Continuous Time - Ch 22 Forward Rate Models]]"
  - "[[Term-Structure Models]]"
---
# Heath-Jarrow-Morton Drift Condition

## Summary

The HJM drift condition is the no-arbitrage restriction that ties the drift of the forward-rate curve to its volatility structure. In HJM, volatility can be specified more freely; drift is then forced.

## Core equations

If forward rates satisfy
$$
df(t,T)=\alpha(t,T)\,dt+\sigma(t,T)\,dW_t,
$$
then no-arbitrage implies
$$
\alpha(t,T)=\sigma(t,T)\int_t^T \sigma(t,s)^\prime ds-\sigma(t,T)\lambda(t).
$$

Under the martingale measure $Q$,
$$
\alpha^Q(t,T)=\sigma(t,T)\int_t^T \sigma(t,s)^\prime ds.
$$

## Main logic

The condition says a forward-rate model is not specified by an arbitrary pair $(\alpha,\sigma)$. Once the volatility family is chosen, the admissible drift is pinned down.

## Failure modes

- treating HJM as one model instead of a framework
- calibrating volatility while ignoring the implied drift restriction
- forgetting that forward-curve models are infinite-dimensional until parameterized

## Related notes

- [[Term-Structure Models]]
- [[LIBOR Market Models]]
- [[Change of Numeraire and Forward Measures]]

## Sources

- [[Arbitrage Theory in Continuous Time]]
- [[Arbitrage Theory in Continuous Time - Ch 22 Forward Rate Models]]
- [[Term-Structure Models]]

