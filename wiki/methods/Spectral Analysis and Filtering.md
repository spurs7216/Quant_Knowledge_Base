---
title: Spectral Analysis and Filtering
type: method
status: seed
updated: 2026-04-21
tags:
  - method
  - time-series
  - spectral
  - filtering
domain: statistics
sources:
  - "[[Time Series Analysis and Its Applications]]"
  - "[[Time Series Analysis and Its Applications - Ch 04 Spectral Analysis and Filtering]]"
---
# Spectral Analysis and Filtering

## Summary

Spectral analysis rewrites time-series dependence in terms of frequency content rather than only lag structure. Filtering then becomes the problem of amplifying, attenuating, or extracting selected frequency components.

This is useful whenever the main structure is cyclical, seasonal, noisy, or horizon-specific.

## Core logic

- autocovariance and spectral density are Fourier partners
- the DFT and periodogram reveal how variance is distributed across frequencies
- raw periodograms are unstable, so smoothing or parametric structure is needed for inference
- cross-spectra and coherence describe frequency-specific dependence between series
- linear filters operate through transfer functions that reshape frequency content

## Workflow

1. Confirm the series is stationary enough for a spectral interpretation.
2. Identify whether the problem is univariate, cross-series, or signal-extraction oriented.
3. Compute the DFT and periodogram or use a parametric spectral model when that is more stable.
4. Smooth or regularize the spectral estimate rather than trusting the raw periodogram.
5. If two series are involved, inspect cross-spectrum and coherence rather than relying only on raw cross-correlation.
6. Design or interpret filters in terms of the frequencies they pass, attenuate, or delay.
7. Translate the spectral result back into the decision problem: seasonality, business cycle, market microstructure noise, or horizon-specific predictability.

## Assumptions

- weak stationarity over the analyzed window
- enough sample length to resolve the frequencies of interest
- a defensible smoothing or parametric choice for stable estimation

## Failure modes

- interpreting raw periodogram spikes as stable facts without smoothing
- using spectral tools on heavily nonstationary or regime-breaking data without adjustment
- discussing "cycles" without checking whether frequency resolution is adequate
- applying filters without asking what information or delay they impose

## Quant relevance

This note matters for:

- seasonality and calendar-cycle detection
- macro and business-cycle components
- de-noising high-frequency or microstructure-heavy series
- lead-lag analysis by horizon
- extracting latent signal from noisy observed series

## Related notes

- [[Transfer Function Models]]
- [[Time-Series Forecasting]]
- [[State Space Models]]
- [[Signal Processing Map]]
- [[Time Series Analysis and Its Applications]]

## Sources

- [[Time Series Analysis and Its Applications]]
- [[Time Series Analysis and Its Applications - Ch 04 Spectral Analysis and Filtering]]
