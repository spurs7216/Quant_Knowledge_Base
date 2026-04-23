---
title: Convex Duality and KKT Conditions
type: method
status: seed
updated: 2026-04-22
tags:
  - method
  - optimization
  - convex-optimization
  - duality
domain: mathematics
sources:
  - "[[Convex Optimization]]"
  - "[[Convex Optimization - Ch 05 Duality]]"
  - "[[Convex Optimization - Ch 10 Equality Constrained Minimization]]"
---
# Convex Duality and KKT Conditions

## Summary

Convex duality turns a constrained optimization problem into a certificate problem. KKT conditions are the operational system that ties primal feasibility, dual feasibility, complementarity, and stationarity together.

## Core equations

For
$$\begin{aligned}
\min_x \quad & f_0(x) \\
\text{subject to} \quad & f_i(x)\le 0,\quad i=1,\dots,m \\
& Ax=b,
\end{aligned}$$
the Lagrangian is
$$L(x,\lambda,\nu)=f_0(x)+\sum_{i=1}^m \lambda_i f_i(x)+\nu^\trans(Ax-b),$$
and the dual function is
$$g(\lambda,\nu)=\inf_x L(x,\lambda,\nu).$$

For every dual-feasible $(\lambda,\nu)$ with $\lambda \succeq 0$,
$$g(\lambda,\nu)\le p^\star.$$

## Main logic

### 1. The dual function creates lower bounds

The dual problem does not guess a better primal point. It produces certified lower bounds on the primal optimum.

### 2. Strong duality makes those bounds exact

Under Slater-style regularity for convex problems,
$$d^\star=p^\star.$$

Then the dual variables are not only formal multipliers. They become exact optimality certificates.

### 3. Complementary slackness identifies the active constraints

At optimum,
$$\lambda_i^\star f_i(x^\star)=0,\qquad i=1,\dots,m.$$

So a positive multiplier can only sit on a binding constraint.

### 4. KKT is the usable optimality system

For differentiable convex problems, the KKT system is
$$f_i(x^\star)\le 0,\qquad Ax^\star=b,\qquad \lambda^\star \succeq 0,$$
$$\lambda_i^\star f_i(x^\star)=0,\qquad i=1,\dots,m,$$
$$\nabla f_0(x^\star)+\sum_{i=1}^m \lambda_i^\star \nabla f_i(x^\star)+A^\trans \nu^\star = 0.$$

When convexity and regularity hold, satisfying this system is sufficient for optimality.

## KKT system as a certificate

The most practical suboptimality certificate is
$$f_0(x)-g(\lambda,\nu),$$
for any primal-feasible $x$ and dual-feasible $(\lambda,\nu)$.

That is why duality is central to solver diagnostics: it gives a quantity that must vanish at optimum and is interpretable before optimum.

## Strong-duality condition to remember

A clean sufficient condition is Slater's condition: there exists a feasible point satisfying all nonlinear inequalities strictly,
$$f_i(x)<0,\qquad i=1,\dots,m,\qquad Ax=b.$$

For convex problems this typically yields zero duality gap and dual attainment.

## Why this note matters

Duality explains:

- why solver gaps mean something
- which constraints are actually shaping the optimum
- how shadow prices arise
- why interior-point methods are built around perturbed KKT systems

## Failure modes

- applying KKT mechanically without checking convexity or regularity
- interpreting multipliers economically when the model is weak or misspecified
- confusing a low duality gap with a good research question
- forgetting that weak duality gives a bound, not automatically an exact certificate

## Quant relevance

This note matters for:

- constrained portfolio problems with meaningful shadow prices
- sensitivity analysis of leverage, exposure, or turnover limits
- auditing solver output
- understanding whether a penalty term behaves like a priced constraint

## Related notes

- [[Convex Optimization Methods]]
- [[Interior-Point Methods]]
- [[Regularization and Robust Approximation]]
- [[Portfolio Optimization]]
- [[Convex Optimization]]

## Sources

- [[Convex Optimization]]
- [[Convex Optimization - Ch 05 Duality]]
- [[Convex Optimization - Ch 10 Equality Constrained Minimization]]
