---
title: LIBOR Market Models
type: method
status: seed
updated: 2026-04-22
tags:
  - method
  - quant-finance
  - fixed-income
  - libor
domain: quant-finance
sources:
  - "[[Arbitrage Theory in Continuous Time]]"
  - "[[Arbitrage Theory in Continuous Time - Ch 23 LIBOR Market Models]]"
  - "[[Change of Numeraire and Forward Measures]]"
---
# LIBOR Market Models

## Summary

LIBOR market models price rates derivatives by modeling discrete forward LIBOR rates directly under their natural forward measures. The attraction is practical: the modeled rates match market quoting conventions more closely than many short-rate or full-curve models.

## Core equations

Under the relevant forward measure, a forward LIBOR rate follows
$$
dL_i(t)=L_i(t)\sigma_i(t)\,dW_i(t).
$$

That gives Black-type caplet prices:
$$
\mathrm{Capl}_i(t)=\alpha_i p_i(t)\bracket{L_i(t)N(d_1)-RN(d_2)}.
$$

## Main logic

- choose the maturity-specific forward measure
- model the quoted forward rate as a lognormal martingale under that measure
- price caplets and related claims in Black-style closed form when the volatility structure is tractable

## Failure modes

- using the wrong measure for the tenor bucket
- forgetting that existence and consistency constraints still matter
- treating calibration convenience as equivalent to structural realism

## Related notes

- [[Term-Structure Models]]
- [[Heath-Jarrow-Morton Drift Condition]]
- [[Change of Numeraire and Forward Measures]]

## Sources

- [[Arbitrage Theory in Continuous Time]]
- [[Arbitrage Theory in Continuous Time - Ch 23 LIBOR Market Models]]
- [[Change of Numeraire and Forward Measures]]

