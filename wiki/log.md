---
title: Wiki Log
type: log
status: active
updated: 2026-04-23
tags:
  - log
  - wiki
---
# Wiki Log

## 2026-04-23 | source reingest | kalman filter tutorial

- Reingested [[Kalman Filter Tutorial]] as a bounded article-source rather than leaving it as a thin tutorial stub.
- Used staged PDF evidence directly: full PyMuPDF text extraction for the 8-page source, then rendered-page verification on the state-space, gain, recursive algorithm, chi-square, and information-form pages where notation mattered.
- Marked `Kalman filter.pdf` as `DONE` in `raw/math_statistics/README.md`, which closes the current ordered math/statistics shelf with no remaining `NEXT` item.

## 2026-04-23 | promotion | kalman filtering bridge refresh

- Rewrote [[Kalman Filtering]] out of seed mode so the durable method note now carries the core recursion in MathJax, the innovation-covariance logic, the recursive-least-squares interpretation, and the information-form update.
- Kept the promotion deliberately narrow: the strongest reusable content from this short tutorial belonged in the existing Kalman method note rather than in a new one-off note.

## 2026-04-23 | govern | index and log role split

- Tightened the control-note doctrine after reviewing the LLM knowledge-base sources again: `wiki/index.md` is now treated as a curated human gateway, not the primary machine retrieval surface once the vault is large.
- Clarified in `agent/operations.md`, `wiki/README.md`, and `wiki/index.md` that broad discovery should move to exact search, Obsidian, or QMD rather than bloating the index further.
- Kept `wiki/log.md` as the chronological audit trail instead of letting it drift into a second content index.

## 2026-04-22 | govern | llm knowledge-base lifecycle and supersession rules

- Reviewed the `raw/LLM Knowledge Bases/` shelf again after adding the v2 guide and compared it against the current vault doctrine instead of copying it wholesale.
- Updated `agent/operations.md`, `agent/notes.md`, `README.md`, and `projects/README.md` to formalize memory tiers, trigger-style maintenance rules, explicit supersession or verification metadata, and sensitive-data redaction rules.
- Rejected two v2 suggestions as direct vault law: numeric fact-confidence scoring and forgetting inside `wiki/`, because they would add false precision and weaken inspectable durable memory in this research vault.

## 2026-04-22 | source ingest | llm wiki v2 guide

- Added [[LLM Wiki v2 Guide]] from the new raw article and linked it into the design-source shelf.
- Rewrote [[LLM Knowledge Base Workflow]] so it now reflects the stronger system design: raw sources, episodic project memory, durable semantic or procedural wiki notes, evidence layers, explicit supersession, and trigger-based maintenance.
- Updated [[Wiki Index]] so the new guide appears in the source-article navigation layer.

## 2026-04-22 | source reingest | bayesian filtering and smoothing theorem-level rebuild

- Reingested [[Bayesian Filtering and Smoothing]] under the current theorem-first rule instead of keeping the earlier approximation-family summary pass.
- Used the staged PDF rule directly: TOC and theorem-list mapping first, full PyMuPDF chapter extraction for broad coverage, then selected rendered-page reads for enabling linearization, posterior linearization, particle methods, IERTSS, and parameter-learning equations where notation mattered.
- Reset the source overview to the stronger stage map: Chapters 4 to 16 now sit at `deep`, Chapter 3 remains `selective_deepen`, and only Chapters 1, 2, and 17 remain `scan`.

## 2026-04-22 | promotion | bayesian filtering durable layer rebuild

- Promoted [[Posterior Linearization in State Space Inference]] out of the reingested source shelf and refreshed [[State Space Discretization from Continuous-Time Models]], [[General Gaussian Filtering and Smoothing]], [[Particle Filtering]], [[Particle Smoothing]], and [[Parameter Estimation in State Space Models]] so they now carry real equations rather than thin prose summaries.
- Refreshed [[Hidden Markov Models and Switching Autoregression]] with the book's exact discrete-state filtering, smoothing, and Viterbi logic instead of leaving that Bayesian machinery trapped in Chapters 5, 6, and 12.
- Updated [[Wiki Index]] so the Bayesian shelf now advertises the stronger stage map and the new posterior-linearization durable note explicitly.

## 2026-04-22 | source reingest | modelling extremal events theorem-level rebuild

- Reingested [[Modelling Extremal Events for insurance and finance]] under the current theorem-first rule instead of keeping the earlier EVT-core-biased pass.
- Used the staged PDF rule directly: TOC and front-matter renders to remap the book, full text extraction for broad coverage, then selected theorem-page renders for the risk-theory, sum-limit, ruin, ARCH, large-deviation, and stable-process sections where notation mattered.
- Upgraded Chapters 1, 2, and 8 into deep notes and reset the overview stage map so the full 8-chapter shelf now sits at `deep` level, with the application-facing insurance and time-series extensions no longer treated as side material.

## 2026-04-22 | promotion | evt durable layer rebuild

- Promoted [[Point Process Methods for Extremes]], [[Ruin Asymptotics with Small and Large Claims]], and [[Stochastic Recurrence Equations and ARCH Tail Behavior]] out of the reingested source shelf.
- Refreshed [[Regular Variation and Heavy-Tailed Distributions]], [[Extremal Index and Clustering of Extremes]], and [[Heavy-Tailed Time Series Analysis]] so the durable EVT branch now carries subexponentiality, cluster-size interpretations, and multiplicative tail-generation logic rather than stopping at a thin maxima-only layer.
- Updated [[Wiki Index]] so the EVT source shelf and the durable method layer now show the stronger stage map and the newly promoted notes explicitly.

## 2026-04-22 | source ingest | arbitrage theory in continuous time

- Reingested [[Arbitrage Theory in Continuous Time]] from the old shallow stub into a full-source overview note with a complete 38-chapter shelf under `wiki/sources/books/Arbitrage Theory in Continuous Time/`.
- Used the token-aware PDF rule directly: UTF-8 text extraction for broad coverage, rendered TOC pages to map the book, and rendered only selected theorem or derivation pages for the martingale, numeraire, rates, control, incomplete-market, and equilibrium chapters.
- Marked `Björk - Arbitrage theory in continuous time (2020).pdf` as `DONE` in `raw/math_statistics/README.md` and advanced the next active shelf target to `Kalman filter.pdf`.

## 2026-04-22 | promotion | continuous-time finance and equilibrium durable batch

- Promoted [[Stochastic Discount Factors]], [[Market Completeness and Incomplete Markets]], [[Heath-Jarrow-Morton Drift Condition]], [[LIBOR Market Models]], [[Stochastic Optimal Control and Hamilton-Jacobi-Bellman Equation]], [[Martingale Methods for Portfolio Optimization]], [[Esscher Transform and Minimal Martingale Measure]], [[Utility Indifference Pricing]], [[Good Deal Bounds]], and [[Dynamic Equilibrium Asset Pricing]] out of the new Bjork source shelf.
- Refreshed [[Risk-Neutral Pricing and Fundamental Theorems of Asset Pricing]], [[Change of Numeraire and Forward Measures]], [[Term-Structure Models]], and [[American Options and Optimal Stopping]] so the earlier Shreve branch and the new Bjork branch now point at the same durable finance layer.
- Updated [[Wiki Index]], [[Math Map]], and [[Finance Map]] so the continuous-time finance branch is now connected to incomplete markets, control, fixed income, and equilibrium notes rather than stopping at vanilla derivative pricing.

## 2026-04-22 | govern | token-aware pdf ingest and cache hygiene

- Updated `agent/operations.md` so PDF-heavy ingest now uses an explicit staged rule: broad text extraction first, targeted rendered-page reading second, and theorem-page escalation only when notation or layout is ambiguous.
- Added a page-selection policy for rendered PDF reads: start with TOC and structure pages, then render only load-bearing theorem, derivation, figure, table, or extraction-failure pages plus any needed continuation pages.
- Added a cache-hygiene rule that treats `.codex/memories` as scratch space rather than a shadow archive, keeping only the minimal short-horizon render set after ingest verification.

## 2026-04-22 | source ingest | stochastic calculus for finance ii

- Reingested [[Stochastic Calculus for Finance II]] from the old shallow stub into a full-source overview note with an 11-note shelf under `wiki/sources/books/Stochastic Calculus for Finance II/`.
- Used a staged map based on the raw source and rendered theorem pages: `deep` for Chapters 2, 3, 4, 5, 6, 8, 9, 10, and 11; `selective_deepen` for Chapters 1 and 7.
- Marked `Steven E. Shreve-Stochastic Calculus for Finance II_20150303200346.pdf` as `DONE` in `raw/math_statistics/README.md` and advanced the next active shelf target to `Björk - Arbitrage theory in continuous time (2020).pdf`.

## 2026-04-22 | promotion | continuous-time finance durable batch

- Promoted [[Brownian Motion and Quadratic Variation]], [[Ito Calculus and Stochastic Differential Equations]], [[Risk-Neutral Pricing and Fundamental Theorems of Asset Pricing]], [[American Options and Optimal Stopping]], [[Change of Numeraire and Forward Measures]], [[Term-Structure Models]], and [[Jump Processes and Compensators]] out of the new Shreve source shelf.
- Refreshed [[Stochastic Calculus]] so the umbrella method note now exposes the Brownian, Ito, pricing, rates, and jump branches explicitly instead of staying a thin prose stub.
- Updated [[Wiki Index]], [[Math Map]], and [[Finance Map]] so the continuous-time finance branch is reachable from both the mathematical and financial navigation layers.

## 2026-04-22 | source ingest | modelling extremal events for insurance and finance

- Ingested [[Modelling Extremal Events for insurance and finance]] into a full-source overview note with an 8-note shelf under `wiki/sources/books/Modelling Extremal Events for insurance and finance/`.
- Used a staged map based on the raw source: `deep` for Chapters 3, 4, 5, 6, and 7; `selective_deepen` for Chapters 1 and 8; `scan` for Chapter 2.
- Marked `Modelling Extremal Events for insurance and finance.pdf` as `DONE` in `raw/math_statistics/README.md` and advanced the next active shelf target to `Steven E. Shreve-Stochastic Calculus for Finance II_20150303200346.pdf`.

## 2026-04-22 | promotion | extreme value theory durable batch

- Promoted [[Regular Variation and Heavy-Tailed Distributions]], [[Extreme Value Theory for Maxima and Threshold Exceedances]], [[Tail Index Estimation]], [[Extremal Index and Clustering of Extremes]], and [[Heavy-Tailed Time Series Analysis]] out of the new extremes source shelf.
- Updated [[Wiki Index]] so the new EVT branch is visible from both the source layer and the durable concept or method layer.
- Kept point-process methods for extremes, heavy-tailed ruin asymptotics, and stochastic-recurrence tails as explicit next-promotion targets rather than pretending the first batch exhausted the book.

## 2026-04-22 | source ingest | probability theory the logic of science

- Ingested [[Probability Theory The Logic of Science]] into a full-source overview note with a 23-note shelf under `wiki/sources/books/Probability Theory The Logic of Science/`, matching the fragmentary raw PDF honestly instead of inventing missing chapters.
- Used a staged map based on the raw source: `deep` for Chapters 1, 2, 6, 7, 8, 11, 13, 18, 19, 21, 24, and 30; `selective_deepen` for Chapters 3, 4, 5, 9, 10, 14, 15, 17, 20, and 27; `scan` for Chapter 16.
- Marked `Probability Theory The Logic of Science.pdf` as `DONE` in `raw/math_statistics/README.md` and advanced the next active shelf target to `Modelling Extremal Events for insurance and finance.pdf`.

## 2026-04-22 | promotion | jaynes bayesian probability durable batch

- Promoted [[Probability as Extended Logic]], [[Maximum Entropy Principle]], and [[Bayesian Model Comparison and Occam Factors]] out of the Jaynes source shelf.
- Refreshed [[Statistical Decision Theory]] so the durable concept note now carries the posterior-expected-loss rule and the Jaynes distinction between inference and decision.
- Updated [[Wiki Index]] so the new Bayesian probability branch is reachable from the durable concept and method layer.

## 2026-04-22 | source reingest | convex optimization mathjax rebuild

- Reingested the deep convex-optimization shelf again after the MathJax and math-parsing upgrade, this time rebuilding the notes around explicit equations, theorem statements, and derivation skeletons rather than code-style pseudo-math.
- Rewrote the parent note [[Convex Optimization]] plus the deep chapters on convex sets, convex functions, convex problem form, duality, approximation and fitting, statistical estimation, unconstrained minimization, and interior-point methods using real MathJax notation.
- Refreshed [[Convex Duality and KKT Conditions]], [[Regularization and Robust Approximation]], [[Interior-Point Methods]], [[Gradient Descent and Preconditioning]], and [[Convex Optimization Methods]] so the promoted method layer now matches the new source-writing standard.

## 2026-04-21 | tooling | mathjax preamble and math parsing stack

- Added the shared vault `preamble.sty` for Extended MathJax so recurring math, probability, linear-algebra, and optimization notation can be written consistently across notes.
- Installed `latex2sympy2_extended`, `pylatexenc`, and `pix2tex`, giving the local workflow a LaTeX parser, normalization layer, and formula-OCR path in addition to the existing PDF tooling.
- Updated `agent/operations.md`, `agent/notes.md`, `README.md`, and `wiki/README.md` so future math-heavy ingest work writes real MathJax equations, uses the shared preamble, and symbolically checks critical formulas when extraction is uncertain.

## 2026-04-21 | source deepen | convex optimization theorem rewrite

- Rewrote the selected `deep` chapters of [[Convex Optimization]] so the source shelf now carries theorem statements, equations, proof or derivation skeletons, and misuse points instead of only structured summaries.
- The strongest upgrade was in Chapters 2, 3, 5, 6, 7, 9, and 11: separation geometry, first-order and second-order convexity conditions, duality and KKT, Tikhonov regularization, experiment-design scalarizations, gradient/Newton convergence, and central-path / primal-dual residual equations are now explicit in the notes.
- Refreshed [[Convex Duality and KKT Conditions]], [[Regularization and Robust Approximation]], and [[Interior-Point Methods]] so the promoted method layer also carries the core equations from the book rather than only high-level prose.

## 2026-04-21 | promotion | convex optimization durable batch

- Promoted [[Convex Duality and KKT Conditions]], [[Regularization and Robust Approximation]], and [[Interior-Point Methods]] out of the new convex-optimization source shelf.
- Refreshed [[Convex Optimization Methods]] and [[Gradient Descent and Preconditioning]] so the durable optimization layer now carries stronger convex modeling, duality, conditioning, and solver-routing support.
- Updated [[Wiki Index]] and `raw/math_statistics/README.md` so the shelf controller now points forward to [[Probability Theory The Logic of Science]] as the next active book.

## 2026-04-21 | source ingest | convex optimization

- Reingested [[Convex Optimization]] from the old shallow stub into a full-source overview note with an 11-chapter shelf under `wiki/sources/books/Convex Optimization/`.
- Used a staged map based on the raw source: `deep` for Chapters 2, 3, 4, 5, 6, 7, 9, 11; `selective_deepen` for Chapters 8, 10; `scan` for Chapter 1.
- Marked `Boyd and Vandenberghe, Convex Optimization.pdf` as `DONE` in `raw/math_statistics/README.md` and advanced the next active shelf target to `Probability Theory The Logic of Science.pdf`.

## 2026-04-21 | promotion | bayesian filtering durable batch

- Promoted [[State Space Discretization from Continuous-Time Models]], [[General Gaussian Filtering and Smoothing]], [[Particle Smoothing]], and [[Parameter Estimation in State Space Models]] out of the new Bayesian filtering source shelf.
- Refreshed [[Particle Filtering]] so the durable note now carries the stronger importance-sampling, auxiliary, and Rao-Blackwellized framing from the new monograph.
- Updated [[Wiki Index]] and `raw/math_statistics/README.md` so the method spine and shelf controller now point forward to [[Convex Optimization]] as the next active source.

## 2026-04-21 | source ingest | bayesian filtering and smoothing

- Reingested [[Bayesian Filtering and Smoothing]] from the old shallow stub into a full-source overview note with a 17-chapter shelf under `wiki/sources/books/Bayesian Filtering and Smoothing/`.
- Used a staged map based on the raw source: `deep` for Chapters 4, 6, 8, 12, 14, 16; `selective_deepen` for Chapters 5, 7, 9, 10, 11, 13, 15; `scan` for Chapters 1, 2, 3, 17.
- Updated `raw/math_statistics/README.md` so `Simo Särkkä and Lennart Svensson, Bayesian Filtering and Smoothing.pdf` is now `DONE` and the next main-spine book advances to `Boyd and Vandenberghe, Convex Optimization.pdf`.

## 2026-04-21 | promotion | state space methods durable batch

- Promoted [[Diffuse Initialization in State Space Models]], [[Simulation Smoothing]], [[Particle Filtering]], and [[Dynamic Factor Models]] out of the new state-space source shelf.
- Refreshed [[State Space Models]] and [[Kalman Filtering]] so the durable method layer now carries the stronger initialization, simulation, and nonlinear-extension support from the Durbin-Koopman monograph.
- Updated [[Wiki Index]] and `raw/math_statistics/README.md` so the shelf state and method spine now point forward to [[Bayesian Filtering and Smoothing]] as the next active source.

## 2026-04-21 | source ingest | time series analysis by state space methods

- Ingested [[Time Series Analysis by State Space Methods]] into a full-source overview note with a 14-chapter shelf under `wiki/sources/books/Time Series Analysis by State Space Methods/`.
- Used a staged map based on the raw source: `deep` for Chapters 2, 3, 4, 5, 7; `selective_deepen` for Chapters 6, 9, 10, 11, 12, 13; `scan` for Chapters 1, 8, 14.
- Marked `Time Series Analysis by State Space Methods (2012).pdf` as `DONE` in `raw/math_statistics/README.md` and advanced the main-spine shelf target to `Simo Särkkä and Lennart Svensson, Bayesian Filtering and Smoothing.pdf`.

## 2026-04-21 | promotion | shumway time series durable batch

- Promoted [[Stationarity and Unit-Root Diagnostics]], [[Spectral Analysis and Filtering]], [[Long Memory and Fractional Differencing]], [[Transfer Function Models]], and [[Hidden Markov Models and Switching Autoregression]] out of the new Shumway source shelf.
- Updated [[Wiki Index]] and [[Time-Series Forecasting]] so the new time-series layer is reachable from the durable method spine rather than remaining trapped under the source note.

## 2026-04-21 | source ingest | time series analysis and its applications

- Reingested [[Time Series Analysis and Its Applications]] from the old shallow stub into a full-source overview note with a 7-chapter shelf under `wiki/sources/books/Time Series Analysis and Its Applications/`.
- Used a staged map based on the raw source: `deep` for Chapters 1, 3, 4, 6 and `selective_deepen` for Chapters 2, 5, 7.
- Updated `raw/math_statistics/README.md` so the Shumway and Stoffer book is now `DONE` and the next main-spine book advances to `Time Series Analysis by State Space Methods (2012).pdf`.

## 2026-04-21 | schema | lowest-cost tool routing rule

- Added a cheap-first control-tool rule to `agent/operations.md` so the system now separates evidence-layer choice from tool choice.
- Defined an explicit ladder: direct reads or exact search first, then Obsidian for note-local context, then QMD for broad discovery, and only then `raw/` or PDF tooling for source-level verification.
- Updated `README.md`, `agent/obsidian.md`, `wiki/README.md`, and `[[LLM Knowledge Base Workflow]]` so future vault work escalates tool cost deliberately instead of defaulting to semantic search or raw-source reads.

## 2026-04-21 | schema | qmd query routing rule

- Added a flexible QMD routing rule to `agent/operations.md` instead of a hard "always use QMD" law.
- Defined QMD as the preferred broad-discovery layer for cross-source and fuzzy retrieval, while keeping Obsidian and direct note reads as the preferred path for note-local inspection and editing.
- Updated `agent/obsidian.md` and `wiki/README.md` so future query work treats QMD as a discovery aid rather than as a replacement for exact note reads or provenance checks.

## 2026-04-20 | source ingest | mathematical methods

- Reclassified `raw/math_statistics/Mathematical Methods.pdf` as a book-level connector source on the shelf rather than a bridge reference.
- Reingested [[Mathematical Methods]] from the old shallow stub into a full-source overview note with a 4-chapter shelf under `wiki/sources/books/Mathematical Methods/`.
- Used a staged map based on the raw source: `scan` for Chapter 1, `deep` for Chapters 2 and 3, and `selective_deepen` for Chapter 4.
- Promoted [[Graph Laplacians and Spectral Graph Methods]], [[Support Vector Machines]], and [[Principal Component Analysis]] out of the source shelf, and updated [[Wiki Index]] plus `raw/math_statistics/README.md` so the new shelf state is visible.

## 2026-04-20 | schema | math statistics shelf widened to all sources

- Rewrote `raw/math_statistics/README.md` into one ordered 14-source shelf instead of splitting main books from short bridge resources.
- Added explicit source-class labeling so books, bridge tutorials, and compact references now live in the same shelf controller without pretending to be the same kind of source.
- Updated `agent/operations.md` and `raw/README.md` so shelf README notes must order all source-like items in a folder and treat `NEXT` as the next active ingest target rather than only the next unfinished book.

## 2026-04-20 | shelf order | math statistics queue refreshed

- Reordered `raw/math_statistics/README.md` after the shelf gained `Probability Theory The Logic of Science` and `Modelling Extremal Events for insurance and finance`.
- Kept `[[Applied Probability]]` as the correct fourth main book, treated Jaynes as a later Bayesian side-branch, and placed the extremes text later as a specialization rather than an immediate prerequisite.
- Advanced the shelf target to `[[Time Series Analysis and Its Applications]]` after completing the fourth-book ingest.

## 2026-04-20 | source ingest | applied probability

- Reingested `[[Applied Probability]]` under the current 3-step rule instead of leaving the old shallow overview stub in place.
- Rebuilt the parent note as a full-source shelf controller and added the full 15-chapter shelf under `wiki/sources/books/Applied Probability/`.
- Used a staged map based on the raw source: `deep` for Chapters 6, 7, 8, 10, 11; `selective_deepen` for Chapters 2, 3, 9, 12, 13, 14; `scan` for Chapters 1, 4, 5, 15.

## 2026-04-20 | promotion | applied probability durable batch

- Promoted `[[Poisson Processes]]`, `[[Continuous-Time Markov Chains]]`, `[[Martingales]]`, and `[[Diffusion Processes]]` out of the source shelf.
- Refreshed `[[Markov Chains]]` so the durable note now reflects the stronger reversible-chain, coupling, and hitting-time support from `[[Applied Probability]]`.
- Updated `wiki/index.md`, `raw/math_statistics/README.md`, and `[[Stochastic Calculus]]` so the new process layer is visible outside the source shelf.

## 2026-04-18 | init | wiki scaffolding

- Added `glossary.md`, the original research-map note now evolved into `maps/reading_map.md`, and `inbox.md` as the baseline navigation notes.
- Created lightweight note templates under `wiki/_templates/`.
- Added empty topical folders for future source, method, factor, model, strategy, market, risk, and system notes.
- Added `AGENTS.md` at the vault root so Codex reads `agent.md` as the primary schema.

## 2026-04-18 | ingest | llm knowledge base sources

- Added source notes for the Karpathy thread, the `llm-wiki` gist, the Atlan enterprise guide, and the Obsidian spaced-repetition plugin documentation.
- Added [[LLM Knowledge Base Workflow]] as the first system-level synthesis note for how this vault should operate.

## 2026-04-18 | ingest | econometrics and derivatives sources

- Added source notes for Hull, Hansen, Brooks, and Wooldridge.
- Added [[Panel Data]] as the first reusable econometrics method note.
- Added [[Derivatives Markets]] as the first reusable market note tied to the options and Treasury datasets.

## 2026-04-18 | ingest | dataset expansion

- Added dataset notes for `ownership_13F`, `option_volumne`, `Treasurey_Daily_Time_Series`, and `Treasurey_Term_structure`.
- Recorded important mirror caveats, including sample-versus-full coverage mismatches and legacy path spellings that should be preserved.

## 2026-04-18 | schema | deep ingest rule

- Updated `agent.md` and `AGENTS.md` to require chapter-by-chapter ingest for chaptered raw resources and section-by-section ingest for long markdown resources.
- Updated the source-note template so future source notes preserve ingest depth explicitly.

## 2026-04-18 | ingest | chapter-by-chapter source re-ingest

- Reworked the LLM knowledge-base sources into section-by-section notes instead of top-level stubs.
- Reworked the Hull, Hansen, Brooks, and Wooldridge notes into chapter-by-chapter source digests.
- Updated [[LLM Knowledge Base Workflow]] so the ingest-depth rule is part of the vault's operating doctrine.
- Expanded [[Panel Data]] and [[Derivatives Markets]] so the deeper source pass also changed the reusable concept layer.

## 2026-04-18 | init | vault contract rewritten

- Rewrote the vault documentation around the new Obsidian structure: `raw/`, `catalog/`, `wiki/`, `projects/`, and `artifacts/`.
- Reframed `agent.md` as a vault-maintenance schema instead of a generic repo note.
- Aligned the README files with the active Obsidian plugin stack and Karpathy-style workflow.

## 2026-04-18 | seed | first wiki spine

- Created the first dataset notes for `daily_stock`, `CCM`, `comp_na_daily_all_annual`, `option_forward_price`, and `risk_free_rate`.
- Created the first identifier notes for `permno`, `gvkey`, `secid`, `ticker`, and `cusip`.
- Added `index.md` and this `log.md` so the vault now has both a content map and a chronological maintenance record.

## 2026-04-18 | note | current emphasis

- The current wiki seed focuses on the core join spine between market data, fundamentals, options, and excess-return construction.
- The next high-value expansion should document additional datasets and then connect them to active project notes in `projects/`.

## 2026-04-18 | ingest | machine learning and quantitative finance source shelf

- Added deep source notes for the core `raw/machine_learning/` books, including ISL, Bishop, Murphy, Bayesian reasoning, financial signal processing, Lopez de Prado, and reinforcement learning.
- Added deep source notes for the core `raw/quantitative_finance/` books, including HFT, algorithmic trading, portfolio optimization, risk management, quantitative trading, computational finance, Monte Carlo, and alpha research.
- Ingested `Causality and Factor Investing A Primer` section by section to anchor causal caution in the factor-research layer.

## 2026-04-18 | crystallize | cross-source quant synthesis

- Added [[Probabilistic Machine Learning]], [[Reinforcement Learning]], [[Financial Machine Learning Workflow]], and [[Monte Carlo Methods]].
- Added [[Portfolio Construction]], [[High-Frequency Trading]], [[Alpha Research]], and [[Backtest Overfitting]].
- Updated `index.md`, the reading-map layer, and `inbox.md` so the vault map reflects the new source shelf and synthesis layer.

## 2026-04-18 | restructure | wiki taxonomy tightened

- Added `maps/` and split the vault map into a top-level reading map plus domain maps.
- Reorganized `sources/` into `books/`, `papers/`, and `articles/` so provenance is easier to read.
- Collapsed the old `models/`, `markets/`, `risks/`, and `systems/` folders into a broader `concepts/` layer.
- Kept `glossary.md`, `inbox.md`, and `_templates/` at the root because they are maintenance surfaces rather than topic buckets.

## 2026-04-18 | audit | raw shelf coverage expanded

- Audited the full `raw/` tree against the current wiki source layer instead of relying on memory or the earlier backlog.
- Added the missing `raw/math_statistics/` source notes, including [[All of Statistics]], [[Applied Probability]], [[Arbitrage Theory in Continuous Time]], [[Convex Optimization]], [[Time Series Analysis and Its Applications]], [[Bayesian Filtering and Smoothing]], [[Stochastic Calculus for Finance II]], and [[Kalman Filter Tutorial]].
- Added the remaining ML, finance, and interview notes, including [[Ensemble Methods in Data Mining]], [[GraphSAGE with Deep Reinforcement Learning for Financial Portfolio Optimization]], [[Financial Risk Manager Handbook]], [[Heard on the Street]], [[A Practical Guide to Quantitative Finance Interviews]], and [[Quant Job Interview Questions and Answers]].
- Folded the Chinese editions of Aldridge, Chan, and Tulchinsky into their existing English source notes as alternate editions, and added [[Quantitative Strategies for Achieving Alpha]] for the distinct Chinese-only alpha book.
- Logged the image capture `[[Target from Quant Firm]]` so the source inventory is complete even though manual visual review is still pending.

## 2026-04-18 | crystallize | methods from the new source shelf

- Added [[Kalman Filtering]] as the first durable state-estimation method note built from the Kalman tutorial, Bayesian filtering, time-series, and signal-processing sources.
- Added [[Time-Series Forecasting]] to turn the new time-series shelf into a reusable forecasting workflow note instead of leaving it source-bound.
- Added [[Stochastic Calculus]] as the continuous-time bridge between probability, pricing, hedging, and dynamic portfolio problems.
- Added [[Convex Optimization Methods]] to connect the new optimization shelf with portfolio construction and regularized estimation.
- Updated the index and map layer so the new methods are visible as top-level entry points rather than only as source byproducts.

## 2026-04-18 | tooling | obsidian mcp verified

- Verified that the Obsidian tool layer can list the vault and read wiki notes directly.
- Verified that wiki maintenance can be written through the Obsidian layer by appending this log entry.
- Updated `agent.md` so future vault work prefers Obsidian operations for note-local tasks while keeping `apply_patch` for large or diff-sensitive refactors.

## 2026-04-18 | ingest | obsidian cli operating note

- Ingested `raw/Obsidian/Obsidian_README.md` into [[Obsidian CLI README]].
- Updated [[LLM Knowledge Base Workflow]] so links, Bases, and tags are treated as the most important Obsidian operating surfaces for this vault.
- Tightened `agent.md` so future vault maintenance prefers Obsidian-native operations for note-local work and treats Bases as an operational dashboard layer rather than a second source of truth.

## 2026-04-18 | tooling | obsidian cli partial verification

- Confirmed that `Obsidian.com` exists at the standard Windows install path, so the CLI binary is installed.
- Confirmed that the bare `obsidian` command is not on `PATH` in this shell.
- Confirmed that invoking `Obsidian.com` directly reaches the CLI, but IPC still reports that it cannot find Obsidian from this session, so the shell-side CLI is not fully usable yet even though the Obsidian MCP layer works.

## 2026-04-19 | tooling | obsidian cli fixed for desktop ipc

- Identified the real failure mode: sandboxed shell commands run under a different Windows identity than the interactive Obsidian desktop session, so the shell could see the CLI binary but could not attach to the named pipe.
- Confirmed that `obsidian` works when executed unsandboxed against the running desktop app.
- Updated `agent.md`, `README.md`, and `wiki/README.md` so future sessions treat Obsidian MCP as the default sandbox-safe path and use unsandboxed shell CLI commands only for app-native operations.

## 2026-04-19 | maps | knowledge base canvas added

- Added `wiki/maps/knowledge_base.canvas` as the first spatial overview of the vault.
- Structured the canvas around the five working layers: governance, inputs, compiled wiki, active research, and evidence outputs.
- Anchored the canvas to real vault files instead of free-floating text so it remains a navigation surface rather than a second knowledge store.

## 2026-04-19 | source rewrite | all of statistics

- Rewrote [[All of Statistics]] from a shallow chapter list into an honest overview-source note with bibliographic framing, recurring notation, major themes, and chapter-by-chapter technical digests.
- Marked the note's ingest basis explicitly as `sampled_sections` and `overview_source` so it no longer overclaims depth.
- Preserved the next correct step: split mathematically important chapters into dedicated chapter digests if this source becomes a central teaching spine for the vault.

## 2026-04-19 | chapter digests | all of statistics foundations

- Added chapter-digest notes for [[All of Statistics - Ch 01 Probability]] through [[All of Statistics - Ch 08 The Bootstrap]].
- Reframed [[All of Statistics]] as a partial chapter-ingested overview note with explicit links to the new digests.
- Raised the ingest standard from whole-book prose summary to chapter-level notes with objects, results, assumptions, diagnostics, failure modes, and quant relevance.

## 2026-04-19 | structure | deep book ingest layout

- Moved the current [[All of Statistics]] chapter digests into `wiki/sources/books/All of Statistics/` while keeping [[All of Statistics]] at the root of the book shelf as the stable overview note.
- Updated the vault schema so deeply ingested books use a parent-note plus child-folder pattern instead of crowding `wiki/sources/books/` with dozens of chapter files.
- Updated the index and wiki folder documentation so future source ingest follows the same storage rule for large technical books.
- Tightened the ingest rule so foundational math and statistics chapter digests are written as theorem-oriented notes, not generic chapter summaries.

## 2026-04-19 | schema | explicit knowledge inclusion rule

- Updated `agent.md` so note inclusion is no longer tied to what the current model already knows.
- Added a model-memory policy: latent recall can help reasoning, but durable answers and durable notes must be grounded in explicit vault knowledge.
- Added an inclusion test for `wiki/` notes based on research leverage, assumptions, theorem conditions, reuse, and failure prevention rather than novelty to the model.

## 2026-04-19 | source rewrite | all of statistics ch 01 probability

- Rewrote [[All of Statistics - Ch 01 Probability]] as a theorem-oriented source note rather than a structured summary.
- Anchored the note in the chapter's actual definitions, lemmas, theorem statements, proof skeletons, appendix caveat on sigma-fields, and high-value exercises.
- Raised `technical_depth` to `deep` because the note now extracts the mathematical structure the rest of the book depends on.

## 2026-04-19 | source rewrite | all of statistics ch 02 random variables

- Rewrote [[All of Statistics - Ch 02 Random Variables]] as a theorem-oriented note centered on induced laws, cdf characterization, pmf versus pdf distinctions, marginals, conditionals, independence, multivariate normal structure, and change-of-variables logic.
- Anchored the note in the chapter's actual definitions and theorems rather than a high-level chapter summary.
- Raised `technical_depth` to `deep` because the note now captures the mathematical machinery that later statistics and quant modeling rely on.

## 2026-04-19 | source completion | all of statistics full chapter ingest

- Completed theorem-oriented or method-oriented chapter notes for all 24 chapters of [[All of Statistics]].
- Rewrote Chapters 3 to 8 to the deeper standard used for Chapters 1 and 2, and added new source notes for Chapters 9 to 24.
- Updated [[All of Statistics]] from a partial source overview to a full chapter-ingested map of the book shelf.

## 2026-04-19 | schema | two-pass long-source ingest rule

- Updated `agent.md` so books, long papers, long reports, and long markdown sources are ingested in two passes: a full scan pass first, then selective deepening.
- Added the rule that not every chapter must be deepened equally; load-bearing chapters get deep notes, while other chapters may remain scan notes.
- Added the exception that a mostly routine chapter can still receive one deep subsection when it contains a critical theorem, derivation, caveat, or modeling idea.
- Updated `wiki/_templates/source_note.md` and `wiki/README.md` so the new scan-versus-deepen workflow is part of the working vault contract.

## 2026-04-19 | source reingest | all of statistics staged by chapter depth

- Reingested the full [[All of Statistics]] chapter shelf under the new two-pass rule rather than treating every chapter note as equally deep.
- Added `ingest_stage` and explicit scope/depth blocks to all 24 chapter notes.
- Marked Chapters 1 to 3 as `deep`, assigned scan-only status to the more structural overview chapters, and marked the load-bearing applied chapters as `selective_deepen`.
- Updated the parent source note so the book overview now records the scan-versus-deepen stage map honestly.

## 2026-04-19 | source deepen | all of statistics ch 04 ch 05 ch 07 ch 08

- Rewrote [[All of Statistics - Ch 04 Inequalities]] at full theorem-oriented depth, including the mgf proof idea for Hoeffding and the structural role of Jensen and Cauchy-Schwarz.
- Rewrote [[All of Statistics - Ch 05 Convergence of Random Variables]] at full asymptotic depth, including convergence modes, implication logic, WLLN, CLT, Berry-Esseen, and scalar/vector delta methods.
- Rewrote [[All of Statistics - Ch 07 Estimating the cdf and Statistical Functionals]] at full depth around the empirical cdf, Glivenko-Cantelli, DKW, and the plug-in principle.
- Rewrote [[All of Statistics - Ch 08 The Bootstrap]] at full depth around second-order plug-in logic, interval construction, percentile justification, and jackknife contrasts.
- Updated the parent source note and root index so Chapters 4, 5, 7, and 8 are now recorded as `deep` rather than `selective_deepen`.

## 2026-04-19 | source deepen | all of statistics ch 09 to ch 12

- Rewrote [[All of Statistics - Ch 09 Parametric Inference]] at full depth around method of moments, likelihood, KL-based consistency, Fisher information, mle asymptotics, efficiency, and the parametric bootstrap.
- Rewrote [[All of Statistics - Ch 10 Hypothesis Testing and p-values]] at full depth around power and size, Wald testing, p-value calibration, permutation tests, likelihood-ratio tests, multiple testing, and goodness-of-fit.
- Rewrote [[All of Statistics - Ch 11 Bayesian Inference]] at full depth around posterior construction, conjugate shrinkage, posterior simulation, large-sample Bayesian behavior, prior problems, and Bayesian failure cases.
- Rewrote [[All of Statistics - Ch 12 Statistical Decision Theory]] at full depth around loss, risk, Bayes rules, minimax rules, admissibility, and Stein's paradox.
- Updated the parent source note and root index so Chapters 9 to 12 are now recorded as `deep` rather than `selective_deepen`.

## 2026-04-19 | source deepen | all of statistics ch 16 and ch 17, rescan ch 13 to ch 15

- Rewrote [[All of Statistics - Ch 16 Causal Inference]] at full depth around potential outcomes, consistency, randomized identification, causal response functions, adjustment under no unmeasured confounding, and Simpson's paradox.
- Rewrote [[All of Statistics - Ch 17 Directed Graphs and Conditional Independence]] at full depth around conditional independence algebra, DAG factorization, local Markov structure, d-separation, collider logic, Markov equivalence, and the distinction between observation and intervention.
- Rescanned [[All of Statistics - Ch 13 Linear and Logistic Regression]], [[All of Statistics - Ch 14 Multivariate Models]], and [[All of Statistics - Ch 15 Inference About Independence]] and left them at `scan`, but flagged the load-bearing theorems and subparts that justify later deepening.
- Updated [[All of Statistics]] and [[Wiki Index]] so the staged chapter map now records Chapters 16 and 17 as `deep`.

## 2026-04-19 | source deepen | all of statistics ch 20 and ch 21, rescan ch 18 and ch 19

- Rewrote [[All of Statistics - Ch 20 Nonparametric Curve Estimation]] at full depth around the MISE decomposition, histogram and kernel risk expansions, cross-validation, Stone's theorem, kernel regression, and the curse of dimensionality.
- Rewrote [[All of Statistics - Ch 21 Smoothing Using Orthogonal Functions]] at full depth around orthonormal basis expansions, coefficient-risk decompositions, orthogonal-series density and regression estimation, and Haar-wavelet thresholding.
- Rescanned [[All of Statistics - Ch 18 Undirected Graphs]] and [[All of Statistics - Ch 19 Log-Linear Models]] and kept them at `scan`, but marked the pairwise/global Markov equivalence, clique factorization, conditional-independence restrictions in log-linear form, and deviance fitting as the load-bearing subparts.
- Updated [[All of Statistics]] and [[Wiki Index]] so the staged chapter map now records Chapters 20 and 21 as `deep`.

## 2026-04-19 | source deepen | all of statistics ch 22 to ch 24

- Rewrote [[All of Statistics - Ch 22 Classification]] at full depth around the Bayes classifier, Gaussian discriminant rules, logistic versus LDA, naive Bayes, tree impurity, cross-validation, VC bounds, support vectors, and kernelization.
- Rewrote [[All of Statistics - Ch 23 Probability Redux Stochastic Processes]] at full depth around Chapman-Kolmogorov, communicating classes, recurrence and decomposition, ergodic convergence, detailed balance, Markov-chain inference, and Poisson-process waiting-time structure.
- Rewrote [[All of Statistics - Ch 24 Simulation Methods]] at full depth around Monte Carlo integration, importance sampling, Metropolis-Hastings, detailed balance, tuning and mixing, Gibbs sampling, and Metropolis-within-Gibbs.
- Updated [[All of Statistics]] and [[Wiki Index]] so the book shelf no longer has any `selective_deepen` chapters; only `deep` and `scan` remain.

## 2026-04-19 | schema | three-step long-source ingest rule

- Updated `agent.md` so long-source ingest is now explicitly a three-step workflow: scan, selective deepen, then promote.
- Added the rule that non-selected chapters must still be rescanned for any local theorem, caveat, or concept that deserves partial deepening.
- Updated `wiki/README.md` and the source-note template so the promotion step is part of the written vault contract rather than only an implied habit.

## 2026-04-19 | promotion | all of statistics first durable batch

- Promoted [[Convergence and Limit Theory]], [[Bootstrap]], [[Maximum Likelihood Estimation]], [[Statistical Decision Theory]], [[Bayes Classifier]], [[Markov Chains]], and [[Markov Chain Monte Carlo]] out of the source shelf.
- Updated [[All of Statistics]] so promoted notes and next promotion targets are separated explicitly.
- Updated [[Wiki Index]] so the new durable notes are visible at the concept and method layer.

## 2026-04-19 | source ingest | linear algebra for ds ml sp

- Added [[Linear Algebra for Data Science, Machine Learning, and Signal Processing]] as the new source overview for the next `raw/math_statistics/` shelf book.
- Added full chapter scan notes for Chapters 1 to 12 under `wiki/sources/books/Linear Algebra for Data Science, Machine Learning, and Signal Processing/`.
- Selected Chapters 3, 5, 7, and 9 for deep treatment, and marked Chapters 4, 6, 8, and 12 as selective-deepen chapters with explicit follow-up targets.

## 2026-04-19 | promotion | linear algebra first durable batch

- Promoted [[Singular Value Decomposition]], [[Least Squares and Pseudoinverse]], [[Low-Rank Approximation]], and [[Gradient Descent and Preconditioning]] out of the source shelf.
- Updated the new source overview and deep chapter notes so the promoted notes are linked back into the book shelf.
- Updated [[Wiki Index]] so the new linear-algebra durable notes are visible at the concept and method layer.

## 2026-04-20 | schema | agent file split

- Split the old monolithic `agent.md` into a compact top-level schema plus detailed subfiles under `agent/`.
- Kept the theorem-level deepen requirement explicit in the new ingest documentation rather than leaving it implicit in the split.
- Updated the root `AGENTS.md` shim so future sessions know to read `agent.md` first and then the relevant `agent/` subfiles.

## 2026-04-20 | schema | operations file rename

- Renamed `agent/ingest.md` to `agent/operations.md` because the detailed workflow file covers query, lint, crystallize, and governance in addition to ingest.
- Updated `agent.md` so the top-level read order now points to `agent/operations.md`.

## 2026-04-20 | source reingest | linear algebra for ds ml sp

- Reingested [[Linear Algebra for Data Science, Machine Learning, and Signal Processing]] from scratch under the current 3-step rule after replacing the stale shelf state.
- Rebuilt the overview note and recreated all 12 chapter notes under `wiki/sources/books/Linear Algebra for Data Science, Machine Learning, and Signal Processing/`.
- Used a fresh stage map based on the raw source: `deep` for Chapters 3, 5, 7, 9; `selective_deepen` for Chapters 4, 6, 8, 10, 12; `scan` for Chapters 1, 2, 11.
- The deep chapters now center on theorem-level or derivation-level structure rather than summary-level prose.

## 2026-04-20 | promotion | linear algebra durable batch refreshed

- Rewrote [[Singular Value Decomposition]], [[Least Squares and Pseudoinverse]], [[Low-Rank Approximation]], and [[Gradient Descent and Preconditioning]] so they now reflect the fresh linear-algebra ingest rather than the stale shelf.
- Updated [[Wiki Index]] so the new shelf state is visible from the main vault map.

## 2026-04-20 | schema | merge agent and AGENTS

- Merged the old `agent.md` schema into `AGENTS.md` so the vault now has one authoritative agent file instead of two overlapping top-level schema files.
- Updated README, wiki navigation, detailed agent subfiles, concept notes, and the knowledge-base canvas to point to `AGENTS.md`.
- Removed `agent.md` to avoid split authority and future drift.

## 2026-04-20 | source ingest | applied time series analysis and forecasting with python

- Added [[Applied Time Series Analysis and Forecasting with Python]] as the third fully ingested `raw/math_statistics/` book under the current 3-step rule.
- Created the full 10-chapter shelf under `wiki/sources/books/Applied Time Series Analysis and Forecasting with Python/`.
- Used a staged map based on the raw source: `deep` for Chapters 3, 4, 6, 7, 9; `selective_deepen` for Chapters 5 and 8; `scan` for Chapters 1, 2, 10.
- The deep chapters now center on stationary-model structure, ARIMA workflow, financial volatility, multivariate systems, and nonstationarity/cointegration rather than chapter-summary prose.

## 2026-04-20 | promotion | applied time series durable batch

- Promoted [[ARIMA and Box-Jenkins Modeling]], [[GARCH Models]], [[Vector Autoregression and Impulse Response Analysis]], [[State Space Models]], and [[Cointegration and Error Correction Models]] out of the new time-series source shelf.
- Refreshed [[Time-Series Forecasting]] so it now organizes the classical time-series layer by failure mode and links the new durable notes together.
- Updated [[Wiki Index]] and `raw/math_statistics/README.md` so the shelf status now records the time-series book as `DONE` and advances [[Applied Probability]] to `NEXT`.

## 2026-04-20 | schema | full-source overview note standard

- Standardized `overview_source` notes with `read_scope: full_source` to one fixed top-level section order: Citation / metadata, Why this book matters, Reading logic from the source, Stage map, Chapter shelf, Core objects and modeling vocabulary, Main themes, Promoted durable notes, Next promotion targets, Caveats, Related notes, Sources.
- Rewrote [[All of Statistics]] and tightened [[Linear Algebra for Data Science, Machine Learning, and Signal Processing]] so the three fully ingested math/statistics book overviews now share the same shelf-level structure.
- Updated `agent/operations.md`, `agent/notes.md`, `wiki/README.md`, and `wiki/_templates/source_note.md` so future long-source ingests follow the same rule by default.
