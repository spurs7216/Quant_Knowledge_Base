---
title: Stochastic Optimal Control and Hamilton-Jacobi-Bellman Equation
type: method
status: seed
updated: 2026-04-22
tags:
  - method
  - stochastic-control
  - hjb
  - quant
domain: quant-research
sources:
  - "[[Arbitrage Theory in Continuous Time]]"
  - "[[Arbitrage Theory in Continuous Time - Ch 25 Stochastic Optimal Control]]"
  - "[[Arbitrage Theory in Continuous Time - Ch 26 Optimal Consumption and Investment]]"
  - "[[Arbitrage Theory in Continuous Time - Ch 36 The Cox-Ingersoll-Ross Factor Model]]"
---
# Stochastic Optimal Control and Hamilton-Jacobi-Bellman Equation

## Summary

Stochastic optimal control solves dynamic decision problems where actions affect a stochastic state process. The HJB equation is the infinitesimal optimality condition implied by Bellman time consistency.

## Core equations

For a controlled diffusion
$$
dX_t=b(t,X_t,u_t)\,dt+\sigma(t,X_t,u_t)\,dW_t,
$$
the value function is
$$
V(t,x)=\sup_u \E_{t,x}\bracket{\int_t^T F(s,X_s,u_s)\,ds+\Phi(X_T)}.
$$

The formal HJB equation is
$$
0=V_t+\sup_u\bracket{F+\mathcal{L}^u V},
$$
with terminal condition $V(T,x)=\Phi(x)$.

## Workflow

1. Specify state dynamics, controls, and admissibility.
2. Define the value function for the family of subproblems.
3. Use Bellman time consistency to derive the HJB equation.
4. Solve for a candidate value function and feedback control.
5. Prove a verification theorem rather than stopping at formal derivation.

## Failure modes

- deriving HJB formally and skipping verification
- assuming time consistency in a problem that is actually path dependent or constrained differently
- confusing a candidate feedback law with a proven optimizer

## Related notes

- [[Martingale Methods for Portfolio Optimization]]
- [[American Options and Optimal Stopping]]
- [[Dynamic Equilibrium Asset Pricing]]

## Sources

- [[Arbitrage Theory in Continuous Time]]
- [[Arbitrage Theory in Continuous Time - Ch 25 Stochastic Optimal Control]]
- [[Arbitrage Theory in Continuous Time - Ch 26 Optimal Consumption and Investment]]
- [[Arbitrage Theory in Continuous Time - Ch 36 The Cox-Ingersoll-Ross Factor Model]]

