---
title: Bayesian Filtering and Smoothing - Ch 01 What Are Bayesian Filtering and Smoothing
type: source
status: chapter_ingested
updated: 2026-04-21
tags:
  - source
  - bayesian
  - filtering
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: chapter_scan
extraction_basis: contents_plus_preface_and_chapter_intro
technical_depth: light
ingest_stage: scan
chapter_or_section: Ch 01 What Are Bayesian Filtering and Smoothing
parent_source: "[[Bayesian Filtering and Smoothing]]"
sources:
  - "[[Bayesian Filtering and Smoothing]]"
  - "[[raw/math_statistics/Simo Särkkä and Lennart Svensson, Bayesian Filtering and Smoothing.pdf]]"
---
# Bayesian Filtering and Smoothing - Ch 01 What Are Bayesian Filtering and Smoothing

## Ingest Scope and Depth

- Ingest stage: `scan`
- Pass 1: full chapter scan completed.
- Pass 2: no theorem-level deepening applied. This chapter is a framing and orientation chapter rather than a technical bottleneck.

## Role of the chapter

This chapter names the whole problem class. It explains what filtering, smoothing, and parameter estimation are trying to recover and why they arise in navigation, tracking, signal processing, and other latent-state settings.

## Section map

- applications of Bayesian filtering and smoothing
- origins of Bayesian filtering and smoothing
- optimal filtering and smoothing as Bayesian inference
- algorithms for Bayesian filtering and smoothing
- parameter estimation

## Main contributions from the scan pass

- The chapter frames filtering as posterior inference using data only up to time `k`, while smoothing conditions on the full data history.
- It makes the architectural point early: exact linear-Gaussian methods, Gaussian approximations, and particle methods are all solving the same Bayesian estimation problem under different computational compromises.
- It previews parameter estimation as part of the same system rather than a separate modeling phase.

## Why it remains scan-level

The chapter is valuable as orientation, but its main job is to supply vocabulary and method families that later chapters derive more precisely.

## Quant relevance

This chapter matters because many quant objects are latent and sequential:

- fair value
- signal strength
- hidden volatility components
- regime state
- execution-state variables

## Promotion candidates

- none yet; later chapters carry the durable technical content

## Related notes

- [[Bayesian Filtering and Smoothing]]
- [[State Space Models]]
- [[Kalman Filtering]]
- [[Particle Filtering]]

## Sources

- [[Bayesian Filtering and Smoothing]]
- [[raw/math_statistics/Simo Särkkä and Lennart Svensson, Bayesian Filtering and Smoothing.pdf]]
