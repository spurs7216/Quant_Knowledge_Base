---
title: Change of Numeraire and Forward Measures
type: method
status: seed
updated: 2026-04-22
tags:
  - method
  - quant-finance
  - numeraire
  - forward-measure
domain: quant-finance
sources:
  - "[[Stochastic Calculus for Finance II]]"
  - "[[Stochastic Calculus for Finance II - Ch 09 Change of Numeraire]]"
  - "[[Stochastic Calculus for Finance II - Ch 10 Term-Structure Models]]"
  - "[[Arbitrage Theory in Continuous Time - Ch 15 Change of Numeraire]]"
  - "[[Arbitrage Theory in Continuous Time - Ch 22 Forward Rate Models]]"
  - "[[Arbitrage Theory in Continuous Time - Ch 23 LIBOR Market Models]]"
---
# Change of Numeraire and Forward Measures

## Summary

Change of numeraire is the method of valuing claims by dividing all prices by a positive traded benchmark and then switching to the measure under which those normalized prices are martingales. Forward measures are the most important practical instance, using a zero-coupon bond as numeraire.

## Core equations

If $N(t)$ is the numeraire, then the normalized asset price is
$$S^{(N)}(t)=\frac{S(t)}{N(t)}.$$

The invariance lemma says self-financing is preserved by normalization:
$$dV_t^S=h_t\,dS_t \iff dV_t^Z=h_t\,dZ_t.$$

The associated pricing identity is
$$V(t)=N(t)\,\mathbb{E}^N\bracket{\frac{V(T)}{N(T)}\given\mathcal{F}(t)}.$$

For a zero-coupon bond,
$$B(t,T)=\frac{1}{D(t)}\widetilde{\mathbb{E}}\bracket{D(T)\given\mathcal{F}(t)}.$$

The time-$t$ forward price for delivery at $T$ is
$$\operatorname{Fwd}_S(t,T)=\frac{S(t)}{B(t,T)}.$$

## Main logic

### 1. There is no single universal risk-neutral measure

The measure depends on the numeraire. What remains invariant is no-arbitrage pricing, not the drift specification under a chosen benchmark.

### 2. Pick the benchmark that simplifies the payoff

For forwards, bond options, caplets, FX claims, and some Asians, the right numeraire can collapse awkward discount factors or state variables.

### 3. Forward measures linearize rates products

Using $B(t,T)$ or $B(t,T+\delta)$ as numeraire aligns the pricing measure with the maturity structure of the claim.

## Workflow

1. Identify a positive traded asset natural for the payoff.
2. Divide prices by that numeraire.
3. Change to the corresponding measure.
4. Re-express the payoff in numeraire units.
5. Price by conditional expectation under the new measure.

## Failure modes

- speaking about "risk-neutral drift" without saying which numeraire is in force
- using a forward measure for a payoff tied to the wrong maturity bucket
- forgetting that the benchmark itself must be traded and strictly positive

## Quant relevance

This method matters for:

- FX options
- forwards and futures
- bond options, caplets, and swap-related pricing
- simplifying path-dependent or rates payoffs

## Related notes

- [[Risk-Neutral Pricing and Fundamental Theorems of Asset Pricing]]
- [[Term-Structure Models]]
- [[American Options and Optimal Stopping]]
- [[Derivatives Markets]]

## Sources

- [[Stochastic Calculus for Finance II]]
- [[Stochastic Calculus for Finance II - Ch 09 Change of Numeraire]]
- [[Stochastic Calculus for Finance II - Ch 10 Term-Structure Models]]
- [[Arbitrage Theory in Continuous Time - Ch 15 Change of Numeraire]]
- [[Arbitrage Theory in Continuous Time - Ch 22 Forward Rate Models]]
- [[Arbitrage Theory in Continuous Time - Ch 23 LIBOR Market Models]]
