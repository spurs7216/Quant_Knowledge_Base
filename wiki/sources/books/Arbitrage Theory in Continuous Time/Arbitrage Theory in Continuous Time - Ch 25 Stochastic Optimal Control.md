---
title: Arbitrage Theory in Continuous Time - Ch 25 Stochastic Optimal Control
type: source
status: chapter_ingested
updated: 2026-04-22
tags:
  - source
  - stochastic-control
  - chapter-digest
  - mathematical-finance
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: toc_scan_plus_utf8_text_extraction_and_targeted_rendered_theorem_pages
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 25 Stochastic Optimal Control
parent_source: "[[Arbitrage Theory in Continuous Time]]"
sources:
  - "[[Arbitrage Theory in Continuous Time]]"
  - "[[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]"
---
# Arbitrage Theory in Continuous Time - Ch 25 Stochastic Optimal Control

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed.
- Pass 2: theorem-level extraction completed for time consistency, the Bellman principle, HJB derivation, verification logic, and the linear-regulator benchmark.

## Deepening Targets

- If the vault later builds a control shelf, deepen the verification step and state-constraint caveats beyond the current theorem spine.

## Deepened Subparts

- `25.3` embedding the problem
- `25.4` time consistency and the Bellman principle
- `25.5` deriving the HJB equation
- `25.6` handling the HJB equation

## Role of the chapter

This chapter opens the dynamic optimization branch. It moves from pricing claims to choosing actions over time when actions affect state evolution.

## Core mathematical objects

- controlled state dynamics
  $$
  dX_t=b(t,X_t,u_t)\,dt+\sigma(t,X_t,u_t)\,dW_t
  $$
- value function
  $$
  V(t,x)=\sup_u \E_{t,x}\bracket{\int_t^T F(s,X_s,u_s)\,ds+\Phi(X_T)}
  $$
- HJB equation
  $$
  0=V_t+\sup_u\bracket{F+\mathcal{L}^u V}
  $$

## Structural map of the chapter

- formulate the control problem
- embed it into a family of subproblems
- prove time consistency via the Bellman principle
- derive the HJB equation and discuss verification

## Theorem and derivation spine

### Bellman optimality gives time consistency

The rendered theorem page states the Bellman principle: an optimal control law for the original problem remains optimal on every later subinterval once the realized state is taken as the new starting point.

That is what makes dynamic programming possible.

### HJB is the infinitesimal optimality condition

Once Bellman time consistency is accepted, the value function must satisfy an equation of the form
$$
0=V_t+\sup_u\bracket{F+\mathcal{L}^u V},
$$
subject to terminal conditions.

### Verification is as important as derivation

The chapter keeps emphasizing that solving the formal HJB is not enough. One must still verify that the candidate value function and control law are admissible and actually attain the optimum.

## Failure modes and misuse points

- deriving HJB formally and skipping the verification step
- assuming time consistency in problems that are not actually dynamically consistent
- confusing a candidate feedback law with a proven optimizer

## Quant research relevance

This chapter is reusable far beyond finance derivatives:

- optimal execution
- portfolio choice
- consumption and investment
- reinforcement-learning interpretations of continuous-time control

## What should be promoted out of this source note

- [[Stochastic Optimal Control and Hamilton-Jacobi-Bellman Equation]]

## Related notes

- [[Stochastic Optimal Control and Hamilton-Jacobi-Bellman Equation]]
- [[Martingale Methods for Portfolio Optimization]]
- [[American Options and Optimal Stopping]]

## Sources

- [[Arbitrage Theory in Continuous Time]]
- [[raw/math_statistics/Björk - Arbitrage theory in continuous time (2020).pdf]]

