---
title: Gradient Descent and Preconditioning
type: method
status: seed
updated: 2026-04-22
tags:
  - method
  - optimization
  - linear-algebra
domain: mathematics
sources:
  - "[[Linear Algebra for Data Science, Machine Learning, and Signal Processing]]"
  - "[[Linear Algebra for Data Science, Machine Learning, and Signal Processing - Ch 09 Optimization Basics and Logistic Regression]]"
  - "[[Convex Optimization]]"
  - "[[Convex Optimization - Ch 09 Unconstrained Minimization]]"
---
# Gradient Descent and Preconditioning

## Summary

Gradient descent solves smooth optimization problems by repeated movement in the negative-gradient direction:
$$x_{k+1}=x_k-\alpha_k \nabla f(x_k).$$

Preconditioning replaces scalar scaling by geometry-aware matrix scaling:
$$x_{k+1}=x_k-P\nabla f(x_k),$$
or more generally $x_{k+1}=x_k-\alpha_k P\nabla f(x_k)$ with $P \succ 0$.

The durable point is that slow first-order optimization is usually a conditioning problem, not an algorithmic mystery.

## Least-squares case

For
$$f(x)=\frac{1}{2}\norm{Ax-y}_2^2,$$
the gradient is
$$\nabla f(x)=A^\trans(Ax-y).$$

Classical fixed-step gradient descent converges when
$$0<\alpha<\frac{2}{\lambda_{\max}(A^\trans A)}=\frac{2}{\norm{A}_2^2}.$$

The ideal preconditioner would be
$$P=(A^\trans A)^{-1},$$
which exactly neutralizes the quadratic curvature when it is available and well behaved. Practical preconditioners are approximations to that idea.

## Smooth convex extension

For functions with $L$-Lipschitz gradient, suitable fixed-step or line-search gradient descent gives sublinear decrease of objective error. For strongly convex objectives, the convergence rate depends on the condition number of the effective curvature.

That is the real geometric meaning of preconditioning: reduce anisotropy so the algorithm does not waste iterations zigzagging across long narrow level sets.

## Line search and conditioning

- exact or backtracking line search decides whether a descent direction becomes a credible update
- poor conditioning produces slow progress even when every step is valid
- a good change of variables can matter as much as the nominal algorithm family

## Newton comparison

Gradient descent and Newton's method solve different problems:

- gradient descent uses only first-order information and pays in iteration count when curvature is badly scaled
- Newton uses local curvature through $\nabla^2 f(x)^{-1} \nabla f(x)$
- preconditioning is the practical middle ground: inject some curvature information without paying full Newton cost

## Logistic regression link

Logistic regression is a useful bridge example because the objective is smooth and convex but usually has no closed-form minimizer. First-order methods are therefore natural, and conditioning of the feature geometry matters directly for training speed.

## Failure modes

- choosing a step size that violates curvature limits
- using no line-search discipline when scaling is poor
- ignoring conditioning and blaming the method
- using a diagonal preconditioner that does not match the actual geometry
- treating optimization success as a substitute for model validation

## Quant relevance

This note matters for scalable regression, classification, penalized fitting, and large optimization problems where exact factorizations are too expensive to update repeatedly.

## Related notes

- [[Convex Optimization Methods]]
- [[Interior-Point Methods]]
- [[Least Squares and Pseudoinverse]]
- [[Low-Rank Approximation]]
- [[Singular Value Decomposition]]

## Sources

- [[Linear Algebra for Data Science, Machine Learning, and Signal Processing]]
- [[Linear Algebra for Data Science, Machine Learning, and Signal Processing - Ch 09 Optimization Basics and Logistic Regression]]
- [[Convex Optimization]]
- [[Convex Optimization - Ch 09 Unconstrained Minimization]]
