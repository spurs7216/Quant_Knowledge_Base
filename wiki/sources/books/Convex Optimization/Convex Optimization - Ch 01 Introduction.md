---
title: Convex Optimization - Ch 01 Introduction
type: source
status: chapter_ingested
updated: 2026-04-21
tags:
  - source
  - optimization
  - convex-optimization
  - chapter-digest
source_type: book
source_class: chapter_digest
read_scope: chapter_scan
extraction_basis: chapter_opening_pages_plus_section_map_and_preface_alignment
technical_depth: moderate
ingest_stage: scan
chapter_or_section: Ch 01 Introduction
parent_source: "[[Convex Optimization]]"
sources:
  - "[[Convex Optimization]]"
  - "[[raw/math_statistics/Boyd and Vandenberghe, Convex Optimization.pdf]]"
---
# Convex Optimization - Ch 01 Introduction

## Ingest Scope and Depth

- Ingest stage: `scan`
- Pass 1: chapter scan completed from the chapter text and section map.
- Pass 2: this chapter was not selected for theorem-level deepening.

## Role of the chapter

This chapter is a framing chapter. It does not yet carry the full mathematical load, but it fixes the book's operating viewpoint:

- optimization is a modeling language, not only a solver call
- least squares and linear programming are the first practical examples
- convex optimization is the tractable core that generalizes both
- algorithm choice only matters after the problem class is understood

## Section map

- mathematical optimization
- least squares and linear programming
- convex optimization
- nonlinear optimization
- outline
- notation

## What the chapter is really doing

### 1. It draws the boundary between generic optimization and convex optimization

The chapter introduces optimization broadly, then narrows attention to the subclass where global structure can be certified. That distinction is the whole point of the book.

### 2. It uses least squares and linear programming as the first intuition pumps

These examples are not decorative. They show that convex optimization already contains many economically and statistically relevant problems before any advanced theory appears.

### 3. It treats formulation as part of the method

The chapter makes clear that recognition and reformulation are part of optimization skill. That is important for the vault because many quant tasks are better understood as reformulation problems than as raw prediction problems.

## Worth attending later

- the difference between generic nonlinear optimization and the convex subclass
- the role of least squares and linear programming as canonical examples
- the claim that modeling discipline precedes algorithm choice

## Quant relevance

For quant work this chapter mainly sets the standard that an optimization result is only as good as the stated objective, constraints, and problem class.

## Promotion candidates

- [[Convex Optimization Methods]]

## Related notes

- [[Convex Optimization]]
- [[Convex Optimization Methods]]
- [[Portfolio Construction]]

## Sources

- [[Convex Optimization]]
- [[raw/math_statistics/Boyd and Vandenberghe, Convex Optimization.pdf]]
