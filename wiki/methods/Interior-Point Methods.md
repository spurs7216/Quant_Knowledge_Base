---
title: Interior-Point Methods
type: method
status: seed
updated: 2026-04-22
tags:
  - method
  - optimization
  - convex-optimization
  - interior-point
domain: mathematics
sources:
  - "[[Convex Optimization]]"
  - "[[Convex Optimization - Ch 11 Interior-Point Methods]]"
  - "[[Convex Duality and KKT Conditions]]"
---
# Interior-Point Methods

## Summary

Interior-point methods solve constrained convex programs by staying in the strict interior, solving barrier or perturbed-KKT systems, and shrinking the duality gap in a controlled way.

## Core equations

For inequalities $f_i(x)\le 0$, the logarithmic barrier is
$$\phi(x)=-\sum_{i=1}^m \log\paren{-f_i(x)}.$$

The barrier subproblem is
$$\min_x \; t f_0(x)+\phi(x) \quad \text{s.t.} \quad Ax=b.$$

The central-path conditions are
$$Ax=b,\qquad f_i(x)<0,\qquad \lambda_i \ge 0,$$
$$\nabla f_0(x)+\sum_{i=1}^m \lambda_i \nabla f_i(x)+A^\trans \nu = 0,$$
$$-\lambda_i f_i(x)=\frac{1}{t},\qquad i=1,\dots,m.$$

The standard primal-dual residual blocks are
$$r_{\mathrm{dual}}=\nabla f_0(x)+Df(x)^\trans \lambda + A^\trans \nu,$$
$$r_{\mathrm{pri}}=Ax-b,$$
$$r_{\mathrm{cent}}=-\diag(\lambda) f(x)-\frac{1}{t}\ones.$$

## Core logic

### 1. Barriers replace hard boundaries with smooth interior geometry

The barrier grows to $+\infty$ at the feasible boundary, so the iterates remain strictly feasible while still being pulled toward the constrained optimum.

### 2. The central path organizes the trajectory

Interior-point methods are not generic local searches. The family $x(t)$ traces a structured path whose duality gap is explicit:
$$f_0(x(t))-p^\star \le \frac{m}{t}.$$

### 3. Primal-dual variants solve perturbed KKT systems directly

The methods update primal and dual variables together instead of solving each barrier problem in isolation. That is usually the most efficient route in serious solvers.

### 4. Residuals and duality gap provide the stopping logic

Progress is judged by primal feasibility, dual feasibility, and complementarity, not by raw objective decrease alone.

## When this method is the right tool

- the problem is convex and constrained
- high accuracy matters
- dual variables or active constraints are economically meaningful
- first-order methods are too slow because of conditioning or accuracy demands

## Failure modes

- using interior-point methods on a bad model and blaming the solver for weak economics
- ignoring the linear algebra burden of repeated KKT solves
- failing to scale the problem and then treating the method as unstable
- assuming low gap implies good out-of-sample decisions

## Quant relevance

This note matters for:

- constrained portfolio programs
- high-accuracy estimation under equality and inequality structure
- conic and barrier-style reformulations where dual interpretation matters

## Related notes

- [[Convex Optimization Methods]]
- [[Convex Duality and KKT Conditions]]
- [[Regularization and Robust Approximation]]
- [[Gradient Descent and Preconditioning]]
- [[Portfolio Optimization]]
- [[Convex Optimization]]

## Sources

- [[Convex Optimization]]
- [[Convex Optimization - Ch 11 Interior-Point Methods]]
- [[Convex Duality and KKT Conditions]]
