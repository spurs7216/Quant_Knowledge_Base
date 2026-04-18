---
title: Machine Learning for Asset Managers
type: source
status: chapter_ingested
updated: 2026-04-18
tags:
  - source
  - machine-learning
  - asset-management
  - quant-finance
sources:
  - "[[raw/machine_learning/Marcos López de Prado - Machine Learning for Asset Managers (2020).pdf]]"
---
# Machine Learning for Asset Managers

## Summary

This shorter Lopez de Prado volume translates financial ML into an asset-management workflow centered on denoising, detoning, distance metrics, clustering, labeling, feature importance, portfolio construction, and overfitting control. The extracted contents show a compact book about extracting usable portfolio structure from noisy cross-sections.

## Chapter-by-Chapter Ingest

- `Chapter 1. Introduction`: frames the role of ML in finance and pushes back against naive benchmark-style expectations.
- `Chapter 2. Denoising and Detoning`: studies covariance cleaning and the removal of common market components.
- `Chapter 3. Distance Metrics`: develops similarity measures for assets and features.
- `Chapter 4. Optimal Clustering`: groups assets or features into more stable structures.
- `Chapter 5. Financial Labels`: treats label construction as a financial-design problem, not a generic ML preprocessing step.
- `Chapter 6. Feature Importance Analysis`: evaluates what information actually matters in the fitted models.
- `Chapter 7. Portfolio Construction`: links cleaned structure and learned information to allocations.
- `Chapter 8. Testing Set Overfitting`: closes with the central warning that evaluation design determines whether the whole pipeline is trustworthy.

## Key Claims

- Covariance cleaning and structure extraction are central for asset management.
- Labels and feature importance must be designed around financial questions, not imported mechanically.
- Overfitting control is inseparable from portfolio construction.

## Methods and Data

- covariance denoising and detoning
- distance metrics and clustering
- financial labeling
- feature-importance analysis
- portfolio construction and overfitting diagnostics

## Why It Matters Here

This is a compact but high-value source for the portfolio-construction side of the vault. It is especially useful for connecting data cleaning, clustering, and labeling to actual allocations.

## Reflection

This book is narrower than `Advances in Financial Machine Learning`, but in a useful way. It keeps the focus on turning noisy financial structure into portfolios, which makes it highly relevant for a quant research knowledge base.

## Caveats

- It is short and therefore more like a focused workflow note than a complete textbook.
- The PDF metadata and encoding are noisy.

## Related Notes

- [[Portfolio Construction]]
- [[Financial Machine Learning Workflow]]
- [[Backtest Overfitting]]

## Sources

- [[raw/machine_learning/Marcos López de Prado - Machine Learning for Asset Managers (2020).pdf]]
