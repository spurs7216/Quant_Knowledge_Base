---
title: Ruin Asymptotics with Small and Large Claims
type: method
status: seed
updated: 2026-04-22
tags:
  - method
  - risk
  - ruin
  - heavy-tails
  - insurance
domain: statistics
sources:
  - "[[Modelling Extremal Events for insurance and finance]]"
  - "[[Modelling Extremal Events for insurance and finance - Ch 01 Risk Theory]]"
  - "[[Modelling Extremal Events for insurance and finance - Ch 08 Special Topics]]"
---
# Ruin Asymptotics with Small and Large Claims

## Summary

Ruin asymptotics split into two genuinely different regimes. In the small-claim regime, ruin is exponentially rare and is caused by a build-up of unfavorable increments. In the large-claim regime, ruin is caused by one catastrophic jump and is governed by the integrated tail.

## Core equations

Write the reserve process as
$$U(t)=u+ct-S(t), \qquad \psi(u)=\Prob\!\paren{\inf_{t\ge 0} U(t)<0},$$
with safety loading
$$\rho=\frac{c}{\lambda\mu}-1>0.$$

Let
$$F_I(x)=\frac{1}{\mu}\int_0^x \bar F(y)\,\mathrm{d}y.$$

In the Cramer-Lundberg regime, if there exists $\nu>0$ such that
$$\int_0^\infty e^{\nu x}\,\mathrm{d}F_I(x)=1+\rho,$$
then
$$\psi(u)\le e^{-\nu u}, \qquad e^{\nu u}\psi(u)\to C.$$

In the heavy-tail regime, if $F_I$ is subexponential,
$$\psi(u)\sim \frac{1}{\rho}\,\bar F_I(u).$$

## Main logic

### 1. Small-claim ruin is a tilted random-walk story

The path to ruin behaves like an Esscher-tilted process with positive local drift. Ruin is a build-up phenomenon.

### 2. Large-claim ruin is a one-big-jump story

The reserve process behaves typically until one exceptional claim causes ruin. The integrated tail, not an adjustment coefficient, controls the asymptotic.

### 3. Finite-time ruin depends on the same regime split

The same small-claim versus large-claim distinction persists when the horizon is finite. Pathwise interpretation matters, not just the final scalar probability.

## Failure modes

- applying Cramer-Lundberg formulas when the claim tail is too heavy
- using one-big-jump ruin logic for light-tailed claims
- ignoring the integrated tail and looking only at the claim tail itself

## Quant relevance

This method matters for:

- solvency and insurance-capital modeling
- catastrophe-like loss processes
- stress scenarios where one jump can break the balance sheet
- deciding whether exponential adjustment logic is defensible

## Related notes

- [[Regular Variation and Heavy-Tailed Distributions]]
- [[Point Process Methods for Extremes]]
- [[Extreme Value Theory for Maxima and Threshold Exceedances]]

## Sources

- [[Modelling Extremal Events for insurance and finance]]
- [[Modelling Extremal Events for insurance and finance - Ch 01 Risk Theory]]
- [[Modelling Extremal Events for insurance and finance - Ch 08 Special Topics]]
