---
title: Murphy Probabilistic Machine Learning
type: source
status: chapter_ingested
updated: 2026-04-18
tags:
  - source
  - machine-learning
  - probabilistic-modeling
  - advanced
sources:
  - "[[raw/machine_learning/Probabilistic Machine Learning.pdf]]"
---
# Murphy Probabilistic Machine Learning

## Summary

This advanced Murphy volume expands probabilistic machine learning into graphical models, inference algorithms, filtering and smoothing, Monte Carlo methods, deep generative models, state-space models, reinforcement learning, and causality. The extracted contents show a deliberately unified map from inference machinery to modern representation and decision-making methods.

## Chapter-by-Chapter Ingest

- `Chapter 1. Introduction`: frames the advanced volume as an extension from foundations to modern probabilistic methods.
- `Chapter 2. Probability`: refreshes the probability core for later advanced inference.
- `Chapter 3. Statistics`: develops estimation, uncertainty, and statistical decision tools.
- `Chapter 4. Graphical Models`: formalizes conditional-independence structure as a modeling language.
- `Chapter 5. Information Theory`: links compression, uncertainty, and learning objectives.
- `Chapter 6. Optimization`: treats optimization as the computational backbone of learning and inference.
- `Chapter 7. Inference Algorithms: an Overview`: situates exact and approximate inference in one framework.
- `Chapter 8. Gaussian Filtering and Smoothing`: develops Kalman-style sequential inference for latent linear systems.
- `Chapter 9. Message Passing Algorithms`: makes belief propagation and related methods operational.
- `Chapter 10. Variational Inference`: introduces deterministic approximate posterior inference.
- `Chapter 11. Monte Carlo Methods`: covers generic stochastic-integration tools.
- `Chapter 12. Markov Chain Monte Carlo`: develops posterior sampling for harder models.
- `Chapter 13. Sequential Monte Carlo`: handles online inference in dynamic latent systems.
- `Chapter 14. Predictive Models: an Overview`: frames prediction as a broad model family rather than a single method.
- `Chapter 15. Generalized Linear Models`: extends probabilistic regression and classification.
- `Chapter 16. Deep Neural Networks`: treats deep function classes inside the larger statistical toolkit.
- `Chapter 17. Bayesian Neural Networks`: combines flexible representations with posterior uncertainty.
- `Chapter 18. Gaussian Processes`: develops nonparametric Bayesian prediction.
- `Chapter 19. Beyond the iid Assumption`: handles dependence, hierarchy, and structure beyond independent samples.
- `Chapter 20. Generative Models: an Overview`: organizes modern generative modeling objectives.
- `Chapter 21. Variational Autoencoders`: studies latent-variable deep generative models.
- `Chapter 22. Autoregressive Models`: develops factorized likelihood modeling.
- `Chapter 23. Normalizing Flows`: treats invertible transformations as density models.
- `Chapter 24. Energy-Based Models`: studies unnormalized density and score-style learning.
- `Chapter 25. Diffusion Models`: introduces iterative denoising-based generation.
- `Chapter 26. Generative Adversarial Networks`: handles adversarial generation and distribution matching.
- `Chapter 27. Discovery Methods: an Overview`: organizes methods aimed at uncovering latent or structural regularities.
- `Chapter 28. Latent Factor Models`: develops factor structure and hidden dimensions.
- `Chapter 29. State-Space Models`: extends sequential latent modeling in full generality.
- `Chapter 30. Graph Learning`: studies graph structure as a target of inference.
- `Chapter 31. Nonparametric Bayesian Models`: develops model classes with flexible complexity.
- `Chapter 32. Representation Learning`: emphasizes learned latent structure over manual features.
- `Chapter 33. Interpretability`: treats explanation and interpretability as modeling concerns.
- `Chapter 34. Decision Making Under Uncertainty`: connects probabilistic prediction to action selection.
- `Chapter 35. Reinforcement Learning`: places RL inside the probabilistic decision framework.
- `Chapter 36. Causality`: closes by linking prediction, intervention, and structural reasoning.

## Key Claims

- Advanced ML can still be organized coherently around probability, inference, and decision making.
- Sequential filtering, state-space modeling, generative modeling, RL, and causality are not separate islands.
- Model uncertainty and latent structure remain central even in modern deep-learning regimes.

## Methods and Data

- graphical models and message passing
- variational, Monte Carlo, MCMC, and sequential Monte Carlo inference
- Kalman filtering and state-space models
- deep generative models and representation learning
- Bayesian neural networks and Gaussian processes
- reinforcement learning and causality

## Why It Matters Here

This is one of the most important long-run sources in the vault because it connects several quant-relevant fronts at once: filtering, latent factors, non-iid data, representation learning, decision making, and causal reasoning.

## Reflection

The quant value of this book is its unification. It makes it easier to treat hidden-state models, Monte Carlo methods, deep models, and causal ideas as pieces of one larger research system rather than as separate specializations.

## Caveats

- It is extremely broad and not intended as a finance-specific implementation guide.
- Depth is sometimes schematic because the scope is so large.

## Related Notes

- [[Probabilistic Machine Learning]]
- [[Reinforcement Learning]]
- [[Monte Carlo Methods]]
- [[Alpha Research]]

## Sources

- [[raw/machine_learning/Probabilistic Machine Learning.pdf]]
