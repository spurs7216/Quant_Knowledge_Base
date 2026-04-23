---
title: Probability Theory The Logic of Science
type: source
status: overview_source
updated: 2026-04-22
tags:
  - source
  - book
  - probability
  - bayesian
  - statistics
source_type: book
source_class: overview_source
read_scope: full_source
source_author:
  - Edwin T. Jaynes
source_year: 1996
source_order: 11
domain: statistics
extraction_basis: fragmentary_1996_pdf_full_chapter_scan_plus_selected_theorem_pages_via_pymupdf
technical_depth: deep
parent_source: null
sources:
  - "[[raw/math_statistics/Probability Theory The Logic of Science.pdf]]"
---
# Probability Theory The Logic of Science

## Citation / metadata

- Author: Edwin T. Jaynes
- Source form in `raw/`: fragmentary PDF edition dated March 1996
- Canonical later publication: posthumous 2003 book edition
- Source type: textbook / monograph
- Read scope: `full_source`
- Shelf role: Bayesian probability side-branch after the core statistics, time-series, filtering, and optimization spine
- Raw source: [[raw/math_statistics/Probability Theory The Logic of Science.pdf]]

## Why this book matters

This is the vault's main Bayesian probability manifesto. Its durable value is not only Bayes' theorem. Jaynes reframes probability as extended logic, builds inference rules from consistency, and then pushes that foundation into maximum entropy, decision theory, regression, model comparison, and criticisms of orthodox statistics.

For quant work, the strongest reusable material is:

- probability as a logic of incomplete information
- prior construction by maximum entropy
- explicit posterior-to-decision logic
- Bayesian model comparison and Occam-factor reasoning

## Reading logic from the source

This ingest treats the raw PDF honestly as a fragmentary edition rather than pretending it is the complete later book.

The workflow was:

1. scan every chapter that actually appears in this PDF
2. deepen the load-bearing chapters to theorem-level detail, especially the rule derivations, maximum entropy, decision theory, model comparison, and matrix MaxEnt material
3. promote the strongest reusable Bayesian probability material into durable concept and method notes

## Stage map

- `deep`: [[Probability Theory The Logic of Science - Ch 01 Plausible Reasoning]]
- `deep`: [[Probability Theory The Logic of Science - Ch 02 The Quantitative Rules]]
- `selective_deepen`: [[Probability Theory The Logic of Science - Ch 03 Elementary Sampling Theory]]
- `selective_deepen`: [[Probability Theory The Logic of Science - Ch 04 Elementary Hypothesis Testing]]
- `selective_deepen`: [[Probability Theory The Logic of Science - Ch 05 Queer Uses for Probability Theory]]
- `deep`: [[Probability Theory The Logic of Science - Ch 06 Elementary Parameter Estimation]]
- `deep`: [[Probability Theory The Logic of Science - Ch 07 The Central Gaussian, or Normal, Distribution]]
- `deep`: [[Probability Theory The Logic of Science - Ch 08 Sufficiency, Ancillarity, and All That]]
- `selective_deepen`: [[Probability Theory The Logic of Science - Ch 09 Repetitive Experiments - Probability and Frequency]]
- `selective_deepen`: [[Probability Theory The Logic of Science - Ch 10 Physics of Random Experiments]]
- `deep`: [[Probability Theory The Logic of Science - Ch 11 Discrete Prior Probabilities - The Entropy Principle]]
- `deep`: [[Probability Theory The Logic of Science - Ch 13 Decision Theory - Historical Background]]
- `selective_deepen`: [[Probability Theory The Logic of Science - Ch 14 Simple Applications of Decision Theory]]
- `selective_deepen`: [[Probability Theory The Logic of Science - Ch 15 Paradoxes of Probability Theory]]
- `scan`: [[Probability Theory The Logic of Science - Ch 16 Orthodox Statistics - Historical Background]]
- `selective_deepen`: [[Probability Theory The Logic of Science - Ch 17 Principles and Pathology of Orthodox Statistics]]
- `deep`: [[Probability Theory The Logic of Science - Ch 18 The Ap Distribution and Rule of Succession]]
- `deep`: [[Probability Theory The Logic of Science - Ch 19 Physical Measurements]]
- `selective_deepen`: [[Probability Theory The Logic of Science - Ch 20 Trend and Seasonality in Time Series]]
- `deep`: [[Probability Theory The Logic of Science - Ch 21 Regression and Linear Models]]
- `deep`: [[Probability Theory The Logic of Science - Ch 24 Model Comparison]]
- `selective_deepen`: [[Probability Theory The Logic of Science - Ch 27 Introduction to Communication Theory]]
- `deep`: [[Probability Theory The Logic of Science - Ch 30 Maximum Entropy - Matrix Formulation]]

## Chapter shelf

- [[Probability Theory The Logic of Science - Ch 01 Plausible Reasoning]]
- [[Probability Theory The Logic of Science - Ch 02 The Quantitative Rules]]
- [[Probability Theory The Logic of Science - Ch 03 Elementary Sampling Theory]]
- [[Probability Theory The Logic of Science - Ch 04 Elementary Hypothesis Testing]]
- [[Probability Theory The Logic of Science - Ch 05 Queer Uses for Probability Theory]]
- [[Probability Theory The Logic of Science - Ch 06 Elementary Parameter Estimation]]
- [[Probability Theory The Logic of Science - Ch 07 The Central Gaussian, or Normal, Distribution]]
- [[Probability Theory The Logic of Science - Ch 08 Sufficiency, Ancillarity, and All That]]
- [[Probability Theory The Logic of Science - Ch 09 Repetitive Experiments - Probability and Frequency]]
- [[Probability Theory The Logic of Science - Ch 10 Physics of Random Experiments]]
- [[Probability Theory The Logic of Science - Ch 11 Discrete Prior Probabilities - The Entropy Principle]]
- [[Probability Theory The Logic of Science - Ch 13 Decision Theory - Historical Background]]
- [[Probability Theory The Logic of Science - Ch 14 Simple Applications of Decision Theory]]
- [[Probability Theory The Logic of Science - Ch 15 Paradoxes of Probability Theory]]
- [[Probability Theory The Logic of Science - Ch 16 Orthodox Statistics - Historical Background]]
- [[Probability Theory The Logic of Science - Ch 17 Principles and Pathology of Orthodox Statistics]]
- [[Probability Theory The Logic of Science - Ch 18 The Ap Distribution and Rule of Succession]]
- [[Probability Theory The Logic of Science - Ch 19 Physical Measurements]]
- [[Probability Theory The Logic of Science - Ch 20 Trend and Seasonality in Time Series]]
- [[Probability Theory The Logic of Science - Ch 21 Regression and Linear Models]]
- [[Probability Theory The Logic of Science - Ch 24 Model Comparison]]
- [[Probability Theory The Logic of Science - Ch 27 Introduction to Communication Theory]]
- [[Probability Theory The Logic of Science - Ch 30 Maximum Entropy - Matrix Formulation]]

## Core objects and modeling vocabulary

- plausibility represented numerically
- product rule
  $$\Prob(AB \mid C)=\Prob(A \mid BC)\Prob(B \mid C)$$
- sum rule
  $$\Prob(A \mid B)+\Prob(\neg A \mid B)=1$$
- Bayes' theorem
  $$\Prob(H \mid D,I)=\frac{\Prob(H \mid I)\Prob(D \mid H,I)}{\Prob(D \mid I)}$$
- entropy of a discrete distribution
  $$H(p)=-\sum_i p_i \log p_i$$
- posterior expected loss
  $$\bar L(a)=\int L(\theta,a)\,p(\theta \mid D,I)\,\diff \theta$$
- model evidence
  $$p(D \mid M,I)=\int p(\theta \mid M,I)\,p(D \mid \theta,M,I)\,\diff \theta$$
- matrix MaxEnt form
  $$\rho = \frac{1}{Z(\lambda)}\exp\paren{-\sum_k \lambda_k A_k}$$

## Main themes

- Probability is a logic of incomplete information, not merely a frequency calculus.
- Prior design is part of inference. Maximum entropy is Jaynes' main answer when only partial expectation information is known.
- Bayesian updating, decision-making, and model comparison should be one coherent pipeline rather than separate doctrines.
- Much of the book is also a critique of orthodox statistics, especially where frequentist procedures lose information or hide priors.

## Promoted durable notes

- [[Probability as Extended Logic]]
- [[Maximum Entropy Principle]]
- [[Bayesian Model Comparison and Occam Factors]]
- [[Statistical Decision Theory]]

## Next promotion targets

- a durable note on rule of succession and predictive updating
- a durable note on sufficiency, ancillarity, and the likelihood principle
- a durable note on Gaussian asymptotics and posterior concentration

## Caveats

- This raw PDF is a fragmentary edition. Numbered chapters `12`, `22`, `23`, `25`, `26`, `28`, and `29` are not present in the source file and therefore are not faked in the shelf.
- The available text for Chapter `30` is itself partial in this fragmentary PDF. The chapter note records only the matrix-MaxEnt material that is actually present before the source drops into the references.
- The book mixes foundational mathematics, philosophical argument, historical critique, and advanced applications. Not every chapter deserves the same durable promotion weight.
- Some OCR in the raw PDF is noisy; the notes below normalize notation into stable MathJax.

## Related notes

- [[All of Statistics]]
- [[Applied Probability]]
- [[Bayesian Filtering and Smoothing]]
- [[Statistical Decision Theory]]
- [[Maximum Likelihood Estimation]]
- [[Bayesian Reasoning and Machine Learning]]

## Sources

- [[raw/math_statistics/Probability Theory The Logic of Science.pdf]]
