---
title: Esscher Transform and Minimal Martingale Measure
type: method
status: seed
updated: 2026-04-22
tags:
  - method
  - quant-finance
  - incomplete-markets
  - measure-selection
domain: quant-finance
sources:
  - "[[Arbitrage Theory in Continuous Time]]"
  - "[[Arbitrage Theory in Continuous Time - Ch 30 The Esscher Transform and the Minimal Martingale Measure]]"
  - "[[Arbitrage Theory in Continuous Time - Ch 31 Minimizing f-Divergence]]"
---
# Esscher Transform and Minimal Martingale Measure

## Summary

These are two disciplined ways to choose a martingale measure in incomplete markets. The Esscher approach selects a measure by solving a transformed martingale equation, while the minimal martingale measure preserves nonpriced orthogonal risk as much as possible.

## Core equations

In Bjork's diffusion-factor setting, the Esscher solution is
$$
\psi_t^E=(\sigma_t\sigma_t^\ast)^{-1}(r_t-\mu_t),
$$
with Girsanov kernel
$$
\phi_t^E=\sigma_t^\ast(\sigma_t\sigma_t^\ast)^{-1}(r_t-\mu_t).
$$

The minimal reverse-entropy criterion coincides with the minimal martingale measure in the same chapter cluster.

## Main logic

- start from the family of admissible martingale measures
- impose a selection rule that is not given by no-arbitrage alone
- interpret the chosen measure economically and statistically

## Failure modes

- presenting one selected measure as universally correct in all incomplete models
- forgetting that different selection rules imply different prices

## Related notes

- [[Market Completeness and Incomplete Markets]]
- [[Utility Indifference Pricing]]
- [[Good Deal Bounds]]

## Sources

- [[Arbitrage Theory in Continuous Time]]
- [[Arbitrage Theory in Continuous Time - Ch 30 The Esscher Transform and the Minimal Martingale Measure]]
- [[Arbitrage Theory in Continuous Time - Ch 31 Minimizing f-Divergence]]

