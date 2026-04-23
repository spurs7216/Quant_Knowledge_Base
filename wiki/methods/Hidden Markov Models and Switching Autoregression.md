---
title: Hidden Markov Models and Switching Autoregression
type: method
status: seed
updated: 2026-04-22
tags:
  - method
  - time-series
  - hidden-markov
  - regime-switching
domain: statistics
sources:
  - "[[Time Series Analysis and Its Applications]]"
  - "[[Time Series Analysis and Its Applications - Ch 06 State Space Models]]"
  - "[[Bayesian Filtering and Smoothing]]"
  - "[[Bayesian Filtering and Smoothing - Ch 05 Modeling with State Space Models]]"
  - "[[Bayesian Filtering and Smoothing - Ch 06 Bayesian Filtering Equations and Exact Solutions]]"
  - "[[Bayesian Filtering and Smoothing - Ch 12 Bayesian Smoothing Equations and Exact Solutions]]"
---
# Hidden Markov Models and Switching Autoregression

## Summary

Hidden Markov and switching autoregression models assume the observed process is driven by a latent discrete regime that evolves as a Markov chain. They are exact discrete-state Bayesian state-space models, not just heuristic regime labels.

## Core equations

With latent regime $S_k \in \{1,\dots,m\}$ and transition matrix
$$\Pi_{ij} = \Prob(S_k=j \given S_{k-1}=i),$$
the forward filtering recursion is
$$\alpha_k(j) \propto p(y_k \given S_k=j)\sum_i \Pi_{ij}\,\alpha_{k-1}(i), \qquad \alpha_k(j)=\Prob(S_k=j \given y_{1:k}).$$

Backward smoothing uses
$$\beta_k(i)=\sum_j \Pi_{ij}\,p(y_{k+1}\given S_{k+1}=j)\,\beta_{k+1}(j),$$
with
$$\Prob(S_k=i \given y_{1:T}) \propto \alpha_k(i)\beta_k(i).$$

Viterbi path inference uses
$$V_k(j)=p(y_k \given S_k=j)\max_i \Pi_{ij}V_{k-1}(i).$$

## Core logic

### 1. Discrete-state filtering is just Bayesian filtering with sums instead of integrals

The same recursive Bayesian logic used for continuous states survives exactly in the discrete setting.

### 2. Regime persistence can explain dependence that a single linear model cannot

Switching models let persistence come from both within-regime dynamics and regime occupancy.

### 3. Smoothing and Viterbi solve different posterior questions

Smoothed probabilities answer "which regimes are plausible?" Viterbi answers "what is the most likely full path?" Those are not the same object.

### 4. Switching autoregression is the time-series specialization

The emission law can itself be autoregressive and regime-dependent, which is why HMM logic is useful for regime-switching macro or volatility systems.

## When this method is the right tool

- the latent state is naturally discrete
- regime persistence is more plausible than smooth continuous latent movement
- filtered and smoothed regime probabilities are interpretable

## Failure modes

- inventing regimes that only absorb outliers or structural breaks
- overinterpreting hard state labels when posterior regime probabilities are diffuse
- using too many regimes relative to the sample
- confusing smoothed probabilities with the Viterbi path

## Quant relevance

This method matters for:

- regime-switching macro or volatility models
- hidden event-state systems
- separating calm/stress or expansion/contraction dynamics

## Related notes

- [[State Space Models]]
- [[General Gaussian Filtering and Smoothing]]
- [[Kalman Filtering]]
- [[Time-Series Forecasting]]
- [[Bayesian Filtering and Smoothing]]

## Sources

- [[Time Series Analysis and Its Applications]]
- [[Time Series Analysis and Its Applications - Ch 06 State Space Models]]
- [[Bayesian Filtering and Smoothing]]
- [[Bayesian Filtering and Smoothing - Ch 05 Modeling with State Space Models]]
- [[Bayesian Filtering and Smoothing - Ch 06 Bayesian Filtering Equations and Exact Solutions]]
- [[Bayesian Filtering and Smoothing - Ch 12 Bayesian Smoothing Equations and Exact Solutions]]
