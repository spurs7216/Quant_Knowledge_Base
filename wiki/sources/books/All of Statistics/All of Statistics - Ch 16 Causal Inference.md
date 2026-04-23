---
title: All of Statistics - Ch 16 Causal Inference
type: source
status: chapter_ingested
updated: 2026-04-19
tags:
  - source
  - statistics
  - causal-inference
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: full_source
extraction_basis: full_text
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 16 Causal Inference
parent_source: "[[All of Statistics]]"
sources:
  - "[[All of Statistics]]"
  - "[[raw/math_statistics/2004 - wasserman - all of statistics.pdf]]"
---
# All of Statistics - Ch 16 Causal Inference

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed against the raw source.
- Pass 2: deep rewrite completed on the chapter's identification logic, counterfactual algebra, and the conditioning traps that make causal claims fail.

## Deepening Targets

- Promote the counterfactual definitions and identification logic into durable causal-method notes once the vault starts storing trading questions that are genuinely intervention-based.

## Deepened Subparts

- The counterfactual model, randomized identification, nonbinary treatment response functions, observational adjustment, and Simpson's paradox were rewritten at full note depth.

## Role of the chapter

This chapter is one of the book's most important conceptual pivots because it forces a distinction between the law of the observed data and the law of outcomes under intervention. Up to this point, most of the book asks what can be learned about a distribution from data. Here the question changes:

- what outcome would have been observed under a different action?

That change requires new random objects.

The chapter distinguishes:

- association
- from causation

The chapter uses the counterfactual framework to make causal questions explicit and to show exactly which assumptions turn an unobservable causal estimand into an estimable statistical functional.

## Core mathematical objects

- potential outcomes
- consistency relation `Y = C_X`
- average treatment effect `theta = E(C_1) - E(C_0)`
- association `alpha = E(Y | X = 1) - E(Y | X = 0)`
- causal response function `theta(x) = E(C(x))`
- observational regression `r(x) = E(Y | X = x)`
- randomized assignment
- confounding
- observational versus experimental identification
- Simpson's paradox

## Counterfactual model

The chapter introduces two potential outcomes for each unit:

- `C_0`: the outcome that would be realized without treatment
- `C_1`: the outcome that would be realized with treatment

The observed outcome is

`Y = C_X`.

This is equation (16.1), the consistency relation. It is not yet an identifying assumption. It is a bookkeeping identity that says the observed outcome equals the relevant potential outcome under the treatment actually received.

The average causal effect is

`theta = E(C_1) - E(C_0)`,

while the observed association is

`alpha = E(Y | X = 1) - E(Y | X = 0)`.

The entire chapter is built around the gap between these two objects.

### Theorem 16.1: association is not causation

The chapter makes explicit that the observed regression or association function does not generally equal the causal effect.

Proof skeleton:

- `alpha` compares outcomes across the treated and untreated groups that actually appear in the data.
- `theta` compares the two potential outcomes across the same population of units.
- If treatment choice `X` is associated with latent type `(C_0, C_1)`, then the two comparisons do not use the same population weights.

The vitamin-C example in the chapter is not decoration. It shows the mechanism clearly: if healthier people are more likely to select treatment, treatment can look beneficial even when `C_1 = C_0` unit by unit.

This is the right starting point for all later causal work. Causal claims require more than predictive association.

### Theorem 16.3: random assignment identifies the average treatment effect

Random assignment identifies the average treatment effect because treatment is detached from potential outcomes.

The proof is short but structurally important:

`theta`
`= E(C_1) - E(C_0)`
`= E(C_1 | X = 1) - E(C_0 | X = 0)` because `X independent (C_0, C_1)`
`= E(Y | X = 1) - E(Y | X = 0)` because `Y = C_X`
`= alpha`.

Once randomization gives `X independent (C_0, C_1)`, the difference in observed means is no longer contaminated by treatment selection. This is the cleanest identification result in the chapter, and every observational substitute is trying to mimic this equality.

## Beyond binary treatments

For a general treatment level `x`, the chapter replaces the pair `(C_0, C_1)` with a counterfactual response function `C(x)`. The observed outcome remains

`Y = C(X)`,

and the causal target becomes

`theta(x) = E(C(x))`.

The observational regression is still

`r(x) = E(Y | X = x)`.

### Theorem 16.4: observational regression is not the causal response curve

When treatment is not binary, causal response functions and observational regression functions can still diverge unless assignment is effectively randomized or otherwise unconfounded.

The point is the same as in the binary case, but now phrased as functions:

- `theta(x)` asks what the average outcome would be if everyone were set to dose `x`
- `r(x)` asks for the average observed outcome among units that happened to choose or receive `x`

These differ whenever treatment intensity is related to latent type. Figure 16.2 in the chapter is load-bearing because it exhibits a case with no causal effect at all and yet a nonconstant observational regression curve.

The deeper lesson is that the object of interest is a causal response surface, not simply `E(Y | X = x)`.

## Observational studies and confounding

Observational studies fail because treatment selection is informative. The chapter encodes the condition needed to repair this:

`{C(x) : x in X} independent X | Z`.

This is the no-unmeasured-confounding or conditional ignorability condition. Within strata of `Z`, treatment behaves as if randomized.

### Theorem 16.6: identification by adjustment / standardization

Under appropriate unconfoundedness conditions, conditioning on covariates can recover causal effects.

The identification formula is

`theta(x) = integral E(Y | X = x, Z = z) dF_Z(z)`.

This equation is one of the chapter's most important pieces. It shows that causal adjustment is not the same as simply reading the regression surface at `X = x`.

What matters is the measure with respect to which the conditional mean is averaged:

- observational regression uses `dF_{Z|X}(z | x)`
- adjusted causal effect uses the marginal covariate distribution `dF_Z(z)`

So adjustment is a reweighting operation justified by the ignorability assumption.

Equation (16.8) in the linear case shows how this becomes regression adjustment in practice, but the chapter is careful: the condition is substantive, not automatic. Conditioning helps only if the chosen covariates are sufficient to block confounding.

## Simpson's paradox

The Simpson's paradox section is one of the most important practical warnings in the chapter because it shows that marginal and conditional associations can point in opposite directions without any contradiction.

It shows that:

- aggregated association can differ from within-group association
- conditioning can reverse conclusions
- naive interpretation of marginal relationships can be misleading

Wasserman's main point is that this is not a paradox in probability. It is a failure to specify the estimand. If treatment assignment is imbalanced across a confounder `Z`, then marginal comparisons can mix incomparable groups. Once the causal model is stated in terms of potential outcomes, the paradox becomes a conditioning problem rather than a mystery.

The practical lesson is severe: whenever a result reverses after conditioning, the first response should not be "which regression is right?" but "which estimand is being approximated under which assumptions?"

## What the chapter is really teaching

The chapter is teaching a four-step causal workflow:

1. define the intervention and the potential outcomes
2. define the estimand in terms of those potential outcomes
3. identify the estimand from observables under explicit assumptions
4. separate what is guaranteed by randomization from what is merely hoped for in observational data

This is the minimum level of causal hygiene required before any empirical researcher is allowed to use causal language.

## Failure modes the chapter is trying to prevent

- interpreting predictive models causally by default
- believing randomization and observational conditioning are the same thing
- ignoring confounding
- treating regression adjustment as if it mechanically creates identification
- reading Simpson's paradox as a paradox rather than a conditioning lesson
- trusting a single observational study without thinking about missing confounders or replication

## Quant research relevance

This chapter matters for quant research because many finance questions sound predictive on the surface but are causal once phrased operationally:

- does a factor proxy for a causal driver of returns or only comove with it?
- does a policy intervention change market behavior?
- does a portfolio rule itself alter execution quality or risk?
- does changing a signal threshold or execution schedule change realized outcomes, or is the observed association only selection?

If the question is causal, association alone is not enough. For real trading research, this matters whenever one moves from "what predicts returns?" to "what happens if we act differently?" The second question is the one that determines implementation.

## What should be promoted out of this source note

- a durable note on association versus causation
- a durable note on potential outcomes and identification
- a durable note on confounding
- a durable note on standardization / adjustment
- a durable note on Simpson's paradox

## Related notes

- [[All of Statistics]]
- [[All of Statistics - Ch 15 Inference About Independence]]
- [[All of Statistics - Ch 17 Directed Graphs and Conditional Independence]]
- [[Causality and Factor Investing A Primer]]
- [[Stats Map]]

## Sources

- [[All of Statistics]]
- [[raw/math_statistics/2004 - wasserman - all of statistics.pdf]]
