---
title: Ridge Regression for Manifold-valued Time-Series with Application to Meteorological Forecast
id: 2411.18339
author: Nava-Yazdani, Esfandiar
publish_date: 2024-11-27
url: https://arxiv.org/abs/2411.18339v2
summary: Intrinsic extension of ridge regression (Tikhonov regularization) to Riemannian manifolds using Riemannian least-squares, empirical covariance, and Mahalanobis distance; trajectories are modelled as best-fitting intrinsic Bézier curves via the de Casteljau algorithm; applied to hurricane track and wind speed forecasting.
---

# Ridge Regression for Manifold-valued Time-Series with Application to Meteorological Forecast

**arXiv:** 2411.18339 | 2024 (v2: July 2025) | math.DG / cs.LG

## Summary

Extends ridge regression from Euclidean space to arbitrary Riemannian manifolds. Trajectories are represented as best-fitting intrinsic Bézier (polynomial) curves via the de Casteljau algorithm. The ridge penalty is formulated using Riemannian covariance and Mahalanobis distance, giving a geometrically intrinsic regularizer. Explicit gradient formulas enable efficient numerical optimization. Demonstrated on hurricane track and wind speed forecasting using real-world data.

## Key Contributions

- Geometry-aware, intrinsic ridge regression that operates directly on Riemannian manifolds (no embedding required).
- Trajectory representation via best-fitting intrinsic Bézier curves (least-squares fit of manifold-valued polynomials via de Casteljau).
- Riemannian covariance and Mahalanobis distance extended to manifold setting as the regularization prior.
- Coefficient of determination R² defined intrinsically using Fréchet mean as baseline.
- Explicit gradient formulas for the objective function, enabling efficient optimization.
- Applied to hurricane track (sphere-valued) and wind speed time-series forecasting.

## Relevance to This Project

LLM hidden states for clinical concepts live in high-dimensional spaces that may have non-Euclidean geometry — particularly if the representations form curved manifolds shaped by SNOMED hierarchy. This paper provides the formal machinery for regression and prediction directly on such manifolds without flattening to Euclidean space, which would distort distances. The Bézier curve trajectory model is a natural candidate for representing disease progression paths through concept space. The Mahalanobis-distance regularizer is especially relevant: it encodes a learned prior over the manifold geometry, analogous to using ontological distance as a prior over concept representation space.
