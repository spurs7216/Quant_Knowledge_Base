---
title: All of Statistics - Ch 08 The Bootstrap
type: source
status: chapter_ingested
updated: 2026-04-19
tags:
  - source
  - statistics
  - bootstrap
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: full_source
extraction_basis: full_text
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 08 The Bootstrap
parent_source: "[[All of Statistics]]"
sources:
  - "[[All of Statistics]]"
  - "[[raw/math_statistics/2004 - wasserman - all of statistics.pdf]]"
---
# All of Statistics - Ch 08 The Bootstrap

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed against the raw source.
- Pass 2: the chapter was rewritten around the bootstrap principle, variance estimation, interval constructions, percentile-interval justification, and the jackknife appendix.

## Deepening Targets

- If bootstrap-based uncertainty becomes a main working tool in the vault, add a durable follow-up note on dependent-data bootstrap methods and another on bootstrap failure modes for nonsmooth or boundary estimators.

## Deepened Subparts

- Whole chapter reworked at theorem-oriented depth.

## Role of the chapter

This chapter is the computational continuation of Chapter 7.

Chapter 7 says:

- estimate `F` by `hat F_n`

Chapter 8 says:

- if the sampling law of an estimator depends on unknown `F`, replace `F` by `hat F_n` and simulate that sampling law

So the bootstrap is not an isolated trick. It is a second-order plug-in principle.

## Core mathematical objects

- statistic `T_n = g(X_1, ..., X_n)`
- unknown variance `V_F(T_n)`
- empirical law `hat F_n`
- bootstrap sample `X_1^*, ..., X_n^* ~ hat F_n`
- bootstrap statistic `T_n^* = g(X_1^*, ..., X_n^*)`
- bootstrap variance estimate `v_boot`
- interval methods:
  - Normal
  - pivotal
  - percentile

The chapter's object of estimation is not only a parameter. It is often the sampling distribution of an estimator.

## Structural map of the chapter

The chapter has four main blocks:

1. simulation as expectation approximation
2. bootstrap variance estimation
3. bootstrap confidence intervals
4. appendix on the jackknife and percentile-interval justification

## Two-step bootstrap principle

The chapter states the bootstrap idea in two steps.

### Step 1

Estimate the variance of the statistic under the unknown distribution by replacing `F` with `hat F_n`:

`V_F(T_n)` becomes `V_hat F_n(T_n)`.

### Step 2

Approximate `V_hat F_n(T_n)` by simulation.

This is the real conceptual point. The bootstrap does not conjure uncertainty from nowhere. It replaces the unknown world by the empirical world, then simulates within that empirical world.

## Section 8.1: simulation

If `Y_1, ..., Y_B` are iid from a distribution `G`, then by LLN,

`B^{-1} sum_j h(Y_j) -> E_G h(Y)`

for suitable `h`.

The bootstrap leans on this trivial but powerful fact:

- if you can simulate from the right law, then sample averages over many simulations approximate features of that law

In particular, sample variance of simulated draws approximates variance under the simulation law.

This means the bootstrap has two layers of approximation:

1. `hat F_n` must be a good stand-in for `F`
2. Monte Carlo with finite `B` must approximate the target quantity under `hat F_n`

The second error can often be made small by taking `B` large. The first error is the deeper statistical one.

## Bootstrap world versus real world

The chapter's diagram is the key conceptual map:

Real world:

- `F -> X_1, ..., X_n -> T_n`

Bootstrap world:

- `hat F_n -> X_1^*, ..., X_n^* -> T_n^*`

This is the right way to think about the bootstrap. One is not resampling because it is fashionable. One is replacing the true sampling experiment by an empirical surrogate experiment.

## Why sampling from `hat F_n` means resampling with replacement

The empirical cdf puts mass `1/n` on each observed data point. Therefore, drawing one observation from `hat F_n` means:

- pick one of the observed `X_i` uniformly at random

Drawing `n` iid bootstrap observations from `hat F_n` is exactly:

- sampling `n` observations with replacement from the data

This equivalence is the operational content of the bootstrap.

## Bootstrap variance estimation

The algorithm is:

1. draw a bootstrap sample `X_1^*, ..., X_n^*`
2. compute `T_n^*`
3. repeat `B` times
4. use empirical variance of `T_n^*` values as the variance estimate

The chapter defines

`v_boot = B^{-1} sum_b (T_{n,b}^* - B^{-1} sum_r T_{n,r}^*)^2`.

### What is being estimated

`v_boot` is estimating the variance of the statistic under the bootstrap law, which is itself intended to approximate the variance under the true law.

So there are two approximations:

`V_F(T_n) approx V_hat F_n(T_n) approx v_boot`.

The chapter explicitly points this out. It is one of the most important cautionary lines in the chapter.

## Example: bootstrap for the median

The median is a perfect example because:

- it is a nonlinear statistic
- direct analytic standard-error derivation is awkward
- bootstrap implementation is simple

This illustrates why the bootstrap became so influential. It is most attractive when the estimator is easy to recompute but hard to analyze algebraically.

## Confidence intervals

The chapter presents three methods.

### Method 1: Normal interval

`hat theta_n +- z_{alpha/2} hat se_boot`.

This is the simplest method, but it assumes the statistic is close to Normal after centering and scaling. If the sampling law is skewed or strongly asymmetric, the interval can be poor.

### Method 2: pivotal interval

Define the pivot

`R_n = hat theta_n - theta`.

If one knew the cdf `H` of `R_n`, one could invert its quantiles to get an exact interval. Since `H` is unknown, bootstrap replicates of the pivot are used instead.

The bootstrap pivotal interval becomes

`(2 hat theta_n - hat theta^*_{1 - alpha/2}, 2 hat theta_n - hat theta^*_{alpha/2})`.

### Why pivotal logic is attractive

The pivot centers the problem around the estimation error itself, not the raw parameter scale. If the distribution of the pivot is more stable than the raw statistic, the interval can behave better.

### Method 3: percentile interval

Take the bootstrap quantiles directly:

`(hat theta^*_{alpha/2}, hat theta^*_{1 - alpha/2})`.

This is operationally simple and often used in practice, but it requires care.

## Theorem 8.3

Under weak conditions on `T(F)`, the chapter states that the pivotal bootstrap interval has asymptotically correct coverage:

`P_F(T(F) in C_n) -> 1 - alpha`.

The theorem matters because it upgrades the bootstrap from heuristic to asymptotic procedure.

## Appendix justification for the percentile interval

The appendix argues as follows.

Suppose there exists a monotone transformation `U = m(T)` such that

`U ~ N(phi, c^2)`.

Then quantiles on the transformed scale transport back through the monotone map. Since monotone transformations preserve quantile order, the percentile interval becomes justified on the original scale.

### What this means conceptually

The percentile interval is appealing when the estimator is approximately normal after some unknown monotone reparameterization. The appendix is not claiming percentile intervals are magically exact. It is giving one structural regime in which they make asymptotic sense.

## Jackknife appendix

The chapter also presents the jackknife:

- remove one observation at a time
- recompute the statistic
- use variation across leave-one-out replicates

The jackknife is computationally lighter and works well for some smooth statistics, but the chapter explicitly notes it is less general than the bootstrap and does not consistently estimate standard errors of sample quantiles.

This is an important contrast:

- bootstrap: more general, simulation-based
- jackknife: cheaper, more brittle, more tied to smoothness

## What the chapter is really teaching

The bootstrap is not "resample and hope." It is:

1. identify the statistic
2. recognize that its finite-sample law depends on unknown `F`
3. estimate `F` by `hat F_n`
4. simulate the statistic under that estimated world
5. use the simulated law for variance or interval construction

That is a serious inferential architecture.

## Monte Carlo error versus bootstrap error

The chapter implicitly separates two distinct issues:

### Monte Carlo error

- finite `B`
- disappears as the number of resamples grows

### Statistical bootstrap error

- `hat F_n` may be a poor surrogate for `F` for the statistic of interest
- does not disappear merely by increasing `B`

This distinction is essential. Many users mistakenly believe a very large `B` guarantees a good bootstrap. It only removes simulation noise, not statistical mismatch.

## Exercises that carry the chapter

The exercises are more revealing than the friendly examples:

- compare interval coverage methods by simulation
- examine quantile-based functionals
- count distinct bootstrap samples combinatorially
- compute conditional mean and variance of the bootstrap mean
- study a case where the bootstrap fails badly for the sample maximum under `Uniform(0, theta)`

That last exercise is especially important. It teaches that the bootstrap is not universally valid, especially for boundary or nonsmooth problems.

## Failure modes

- forgetting that the bootstrap targets the sampling distribution of the estimator, not the parameter directly
- assuming the Normal interval is fine whenever a bootstrap standard error is available
- using percentile intervals without checking skewness or parameterization sensitivity
- increasing `B` and thinking that alone fixes a bad bootstrap problem
- ignoring nonsmooth or boundary estimators
- applying iid bootstrap logic to dependent time series without modification

## Quant research relevance

The bootstrap is highly relevant to quant work because many quantities of interest are nonlinear and analytically awkward:

- Sharpe-like functionals
- rank statistics
- skewness and tail summaries
- quantiles and drawdowns
- performance gaps between strategies
- nested statistics built from fitted models

But the chapter also gives the correct warning for finance:

- raw iid bootstrap is not automatically appropriate for serially dependent returns

So this chapter is a conceptual foundation, not a universal off-the-shelf solution for time series.

## Promoted durable notes

- [[Bootstrap]]

## Next promotion targets

- a durable note on dependent-data bootstrap methods
- a durable note on Normal, pivotal, and percentile bootstrap intervals
- a durable note on bootstrap failure modes
- a durable note comparing bootstrap and jackknife

## Related notes

- [[All of Statistics]]
- [[Bootstrap]]
- [[All of Statistics - Ch 07 Estimating the cdf and Statistical Functionals]]
- [[Monte Carlo Methods]]
- [[Stats Map]]

## Sources

- [[All of Statistics]]
- [[raw/math_statistics/2004 - wasserman - all of statistics.pdf]]
