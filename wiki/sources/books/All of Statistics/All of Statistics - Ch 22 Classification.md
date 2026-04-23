---
title: All of Statistics - Ch 22 Classification
type: source
status: chapter_ingested
updated: 2026-04-19
tags:
  - source
  - statistics
  - classification
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: full_source
extraction_basis: full_text
technical_depth: deep
ingest_stage: deep
chapter_or_section: Ch 22 Classification
parent_source: "[[All of Statistics]]"
sources:
  - "[[All of Statistics]]"
  - "[[raw/math_statistics/2004 - wasserman - all of statistics.pdf]]"
---
# All of Statistics - Ch 22 Classification

## Ingest Scope and Depth

- Ingest stage: `deep`
- Pass 1: full chapter scan completed against the raw source.
- Pass 2: deep rewrite completed on Bayes-optimal classification, model-based rules, empirical-risk control, VC theory, and support-vector geometry.

## Deepening Targets

- Promote the Bayes-classifier, generalization, and support-vector machinery into durable learning notes once the vault starts using classification as a real research tool rather than as background method knowledge.

## Deepened Subparts

- The Bayes classifier, Gaussian discriminant rules, logistic-versus-LDA comparison, naive Bayes, tree construction, cross-validation, VC generalization bounds, support vectors, and kernelization were rewritten at full note depth.

## Role of the chapter

This chapter is where the book makes the transition from estimating population objects to choosing actions that minimize classification error. The key change is that the target is now a decision rule `h(x)`, not a parameter or a curve.

It covers:

- Bayes-optimal classification
- Gaussian and linear classifiers
- logistic regression and LDA
- naive Bayes
- trees
- SVMs
- error-rate assessment
- VC-style uniform convergence
- kernelization

This is one of the clearest places where the book explicitly merges statistics and machine learning.

## Core mathematical objects

- classifier `h(x)`
- true error rate
- Bayes classifier
- class-conditional densities
- LDA and logistic-regression rules
- empirical error rate
- cross-validation
- VC dimension
- margin
- support vectors
- kernel function

## Bayes classification rule

### Definitions 22.3 and 22.4, Theorems 22.5 and 22.6

The chapter starts from the true error rate

`L(h) = P(h(X) != Y)`

and the training error

`\hat L_n(h) = (1 / n) sum_i I(h(X_i) != Y_i)`.

For binary classification, the regression function is

`r(x) = P(Y = 1 | X = x)`.

The Bayes rule is

`h*(x) = 1` if `r(x) > 1/2`, otherwise `0`.

Equivalently,

`h*(x) = argmax_k P(Y = k | X = x) = argmax_k pi_k f_k(x)`

in the multiclass case.

Theorem 22.5 is the chapter's first load-bearing result: the Bayes classifier minimizes the true error rate over all measurable classifiers.

This is the benchmark against which all practical classifiers are judged.

The important lesson is that classification is a decision problem under a loss function, not a vague pattern-recognition exercise.

It also clarifies the three main roads to a classifier:

1. empirical risk minimization over a class `H`
2. estimate the regression function and threshold it
3. estimate class-conditional densities and priors, then plug into Bayes' rule

## Model-based classifiers

### Theorems 22.7, 22.9, 22.10

If `X | Y = k` is Gaussian, then the Bayes rule has discriminant score

`delta_k(x) = -(1/2) log |Sigma_k| - (1/2)(x - mu_k)^T Sigma_k^{-1} (x - mu_k) + log pi_k`.

This is quadratic discriminant analysis when the covariance matrices differ.

If all classes share a common covariance matrix, the quadratic terms cancel and the discriminant becomes linear:

`delta_k(x) = x^T Sigma^{-1} mu_k - (1/2) mu_k^T Sigma^{-1} mu_k + log pi_k`.

This is linear discriminant analysis.

This is useful because it ties classification back to density modeling and likelihood ideas already developed earlier.

The Fisher linear discriminant interpretation is also important. Instead of starting from a full generative model, it projects the data to maximize between-class separation relative to within-class spread via the Rayleigh quotient. That makes the geometric meaning of LDA explicit.

## Logistic regression, naive Bayes, trees, SVMs

The chapter does something important pedagogically: it places several seemingly different classifiers in one framework.

They differ in:

- probabilistic assumptions
- geometric decision boundaries
- complexity and flexibility

but they are all judged by predictive error under the same statistical logic.

The logistic-regression section matters because it shows that logistic regression and LDA can induce the same linear decision boundary while using different estimation strategies:

- LDA models the joint law `f(x, y) = f(x | y) f(y)`
- logistic regression models only `f(y | x)` and leaves `f(x)` unspecified

That is a clean example of generative versus conditional modeling.

The naive Bayes section is load-bearing in high dimensions. It replaces the impossible task of high-dimensional density estimation with a product approximation across coordinates. The independence assumption is usually wrong, but the classifier can still work well if the ranking induced by `pi_k f_k(x)` is approximately preserved.

The tree section matters because it turns classification into recursive partitioning and impurity minimization. The Gini index

`gamma_s = 1 - sum_j \hat p_s(j)^2`

is the splitting criterion. The note that unrestricted tree growth overfits is not incidental; it is the reason model selection must be tied to estimated out-of-sample error.

For support vector machines, the important geometric idea is the margin. Among separating hyperplanes, choose the one that maximizes distance to the closest points. Theorem 22.28 turns this into a constrained optimization problem, and Theorem 22.29 shows that the solution depends only on a subset of observations, the support vectors.

That sparsity and the margin viewpoint are the chapter's main SVM ideas, not the quadratic-programming details themselves.

Kernelization is the final bridge to richer nonlinear decision boundaries. A linear classifier in feature space becomes nonlinear in the original covariates, while computation is preserved if the algorithm depends only on inner products that can be replaced by a kernel `K(x, x')`.

## Assessing error rates

The chapter stresses that empirical error rates are optimistic when measured on training data, and cross-validation is introduced as a way to estimate predictive error more honestly.

This is one of the most practically important parts of the chapter.

The tree and logistic examples are doing real conceptual work here: increasing model complexity can drive training error down steadily while cross-validated error eventually turns back up. This is the classification version of the bias-variance tradeoff from Chapter 20.

## Uniform convergence and VC theory

### Theorems 22.16 to 22.20

The final section introduces the generalization-theory view:

- when does empirical performance approximate true performance uniformly over a class of classifiers?

The VC dimension enters as a complexity measure controlling generalization capacity.

This is a major bridge from classical statistics into statistical learning theory.

Theorem 22.16 gives finite-class uniform convergence:

`P(max_{h in H} | \hat L_n(h) - L(h) | > eps) <= 2 m e^{-2 n eps^2}`

for finite `H` with `m` classifiers.

Theorem 22.17 then converts that into a confidence interval for the true error of the empirically selected classifier.

Theorems 22.18 and 22.19 replace the finite cardinality `m` with the shatter coefficient `s(H, n)`, and Definition 22.20 introduces VC dimension as the complexity quantity that controls how fast `s(H, n)` grows.

Theorem 22.21 is the real payoff: finite VC dimension implies polynomial rather than exponential growth of the shatter coefficient.

That is why VC dimension matters. It turns a potentially useless uniform bound into something that can actually shrink with `n`.

## What the chapter is really teaching

Classification is a risk-minimization problem with:

- a target loss
- a model or hypothesis class
- a tradeoff between fit and complexity
- and a need for out-of-sample error assessment

That is the unifying logic across all the algorithms in the chapter.

The chapter is also teaching a useful hierarchy:

- Bayes rule = unattainable oracle benchmark
- parametric / semiparametric approximations = practical structured rules
- cross-validation and uniform bounds = guardrails against self-deception
- margin and kernel methods = geometry for richer boundaries without abandoning tractable optimization

## Failure modes the chapter is trying to prevent

- judging classifiers only by training accuracy
- forgetting the Bayes classifier is a theoretical benchmark, not a directly implementable rule without the true law
- confusing posterior classification with regression output without checking loss
- ignoring hypothesis-class complexity when interpreting empirical fit
- forgetting that generative and conditional approaches can induce similar boundaries but behave differently under misspecification
- treating kernelization as magic rather than as a choice of feature geometry

## Quant research relevance

This chapter is relevant to quant work when the target is categorical:

- event prediction
- regime classification
- default or distress labeling
- signal sign prediction
- execution-state or market-state labeling

The most important warning is that noisy labels and weak class imbalance can make apparent predictive success unstable. The chapter's generalization logic is therefore highly relevant.

For real trading research, the most reusable parts are:

- Bayes risk as the conceptual benchmark
- LDA / logistic / naive Bayes as structured low-data classifiers
- cross-validation as the minimum acceptable evaluation discipline
- SVM margins and kernelization as controlled ways to enrich the hypothesis class

## Promoted durable notes

- [[Bayes Classifier]]

## Next promotion targets

- a durable note on LDA versus logistic regression
- a durable note on cross-validated classification error
- a durable note on VC dimension and generalization
- a durable note on support vector machines and kernelization

## Related notes

- [[All of Statistics]]
- [[Bayes Classifier]]
- [[All of Statistics - Ch 13 Linear and Logistic Regression]]
- [[Reinforcement Learning]]
- [[ML Map]]

## Sources

- [[All of Statistics]]
- [[raw/math_statistics/2004 - wasserman - all of statistics.pdf]]
