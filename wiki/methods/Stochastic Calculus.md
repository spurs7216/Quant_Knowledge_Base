---
title: Stochastic Calculus
type: method
status: seed
updated: 2026-04-22
tags:
  - method
  - stochastic-calculus
  - mathematical-finance
  - continuous-time
domain: quant-finance
sources:
  - "[[Stochastic Calculus for Finance II]]"
  - "[[Arbitrage Theory in Continuous Time]]"
  - "[[Hull Options Futures and Other Derivatives]]"
  - "[[Monte Carlo Methods in Financial Engineering]]"
---
# Stochastic Calculus

## Summary

Stochastic calculus is the continuous-time mathematical framework for modeling noisy state dynamics, dynamic trading strategies, and contingent-claim values. In quant finance it is the common language behind diffusion models, martingale pricing, American exercise, term-structure models, and jump extensions.

## Core equations

Brownian quadratic variation is
$$[W,W](t)=t.$$

An Ito process has the form
$$dX(t)=\theta(t)\,dt+\Gamma(t)\,dW(t).$$

The Ito-Doeblin rule gives
$$df(t,X(t))=f_t\,dt+f_x\,dX(t)+\frac{1}{2}f_{xx}\,dX(t)\,dX(t).$$

Risk-neutral valuation writes a traded claim as
$$V(t)=\frac{1}{D(t)}\widetilde{\mathbb{E}}\bracket{D(T)V(T)\given\mathcal{F}(t)}.$$

With jumps, the calculus becomes
$$f(X(t))=f(X(0))+\int_0^t f'(X(s))\,dX^c(s)+\frac{1}{2}\int_0^t f''(X(s))\,d[X^c,X^c](s)+\sum_{0<s\le t}\bracket{f(X(s))-f(X(s-))}.$$

## What this method does

Stochastic calculus lets the researcher:

- specify continuous-time state laws under uncertainty
- transform those laws with the correct chain and product rules
- express traded-price dynamics in self-financing form
- switch measures and numeraires cleanly
- move between expectation, martingale, and PDE representations
- extend diffusion logic to jump models when continuity fails

## Source synthesis

- [[Stochastic Calculus for Finance II]] is the main bridge from filtration, Brownian motion, and Ito rules into risk-neutral pricing, American exercise, numeraire change, term-structure models, and jump processes.
- [[Arbitrage Theory in Continuous Time]] broadens the framework into general semimartingale asset-pricing structure, incompleteness, and deeper continuous-time finance theory.
- [[Hull Options Futures and Other Derivatives]] provides the market intuition and contract context that theorems alone do not supply.
- [[Monte Carlo Methods in Financial Engineering]] turns the continuous-time theory into usable numerical estimators and simulation schemes.

## Main branches

- [[Brownian Motion and Quadratic Variation]]
- [[Ito Calculus and Stochastic Differential Equations]]
- [[Risk-Neutral Pricing and Fundamental Theorems of Asset Pricing]]
- [[American Options and Optimal Stopping]]
- [[Change of Numeraire and Forward Measures]]
- [[Term-Structure Models]]
- [[Jump Processes and Compensators]]

## Workflow

1. Specify the filtration and state variables.
2. Decide whether the dynamics are diffusion, jump, or mixed.
3. Write the continuous-time law in differential form.
4. Choose the actual or pricing measure and the relevant numeraire.
5. Use Ito or jump calculus to derive the value, hedge, or state transformation.
6. Translate the result into a numerical method when no closed form exists.
7. Check whether the continuous-time assumptions survive discrete trading, costs, and calibration constraints.

## Failure modes

- using continuous-time elegance to hide weak economic assumptions
- confusing the pricing measure with the forecasting measure
- assuming replication or completeness in markets that are effectively incomplete
- applying diffusion-only formulas to jump or discretely monitored problems
- ignoring implementation frictions and calibration instability

## Quant use cases

- derivative pricing and Greeks
- dynamic hedging
- fixed-income and term-structure modeling
- filtering and state-space control in continuous time
- jump-risk modeling and event-driven valuation

## Related notes

- [[Derivatives Markets]]
- [[Martingales]]
- [[Diffusion Processes]]
- [[Brownian Motion and Quadratic Variation]]
- [[Ito Calculus and Stochastic Differential Equations]]
- [[Risk-Neutral Pricing and Fundamental Theorems of Asset Pricing]]
- [[Arbitrage Theory in Continuous Time]]
- [[Math Map]]
- [[Finance Map]]

## Sources

- [[Stochastic Calculus for Finance II]]
- [[Arbitrage Theory in Continuous Time]]
- [[Hull Options Futures and Other Derivatives]]
- [[Monte Carlo Methods in Financial Engineering]]
