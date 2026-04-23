---
title: Convex Optimization - Ch 08 Geometric Problems
type: source
status: chapter_ingested
updated: 2026-04-21
tags:
  - source
  - optimization
  - convex-optimization
  - chapter-digest
  - geometry
source_type: book
source_class: chapter_digest
read_scope: selected_chapter
extraction_basis: chapter_text_plus_section_map_plus_selected_projection_and_ellipsoid_sections
technical_depth: mixed
ingest_stage: selective_deepen
chapter_or_section: Ch 08 Geometric Problems
parent_source: "[[Convex Optimization]]"
sources:
  - "[[Convex Optimization]]"
  - "[[raw/math_statistics/Boyd and Vandenberghe, Convex Optimization.pdf]]"
---
# Convex Optimization - Ch 08 Geometric Problems

## Ingest Scope and Depth

- Ingest stage: `selective_deepen`
- Pass 1: full chapter scan completed.
- Pass 2: local deepening completed around projection, distance-between-sets formulations, extremal-volume ellipsoids, and classification-style formulations.

## Why this chapter still matters

This chapter is less central than duality or solver design, but it is valuable because it shows how many apparently geometric tasks are really convex programs in disguise.

## Core objects

- projection onto a convex set
- distance between convex sets
- separating hyperplane
- Euclidean angle and norm geometry
- minimum-volume or maximum-volume ellipsoid
- classification and placement formulations

## Structural map

- projection on a convex set
- distance between sets
- Euclidean distance and angle problems
- extremal volume ellipsoids
- centering and placement
- classification and floor planning

## What the chapter is really doing

### 1. It turns geometric questions into optimization templates

Projection, distance, and separation are not only geometry exercises. They are generic modeling patterns that appear in statistics, control, and portfolio feasibility analysis.

### 2. Ellipsoid problems are early semidefinite intuition

The extremal-ellipsoid sections are one of the book's quiet bridges toward semidefinite modeling and matrix inequalities.

### 3. Classification can be phrased geometrically before it is phrased probabilistically

The classification examples matter because they show another way convexity enters learning problems: through margins, distances, and feasible separating structures.

## Worth promoting later

- extremal ellipsoids and semidefinite geometry
- convex classification geometry
- projection and distance problems as reusable templates

## Quant relevance

This chapter mainly matters as a modeling library:

- nearest feasible portfolio repair as projection
- uncertainty-set geometry through ellipsoids
- distance and separation formulations in risk and classification tasks

## Promotion candidates

- cone programs, generalized inequalities, and semidefinite optimization

## Related notes

- [[Convex Optimization]]
- [[Convex Optimization - Ch 04 Convex Optimization Problems]]
- [[Support Vector Machines]]
- [[Principal Component Analysis]]

## Sources

- [[Convex Optimization]]
- [[raw/math_statistics/Boyd and Vandenberghe, Convex Optimization.pdf]]
