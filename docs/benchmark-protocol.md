# Seed Benchmark Protocol

## Purpose

This protocol defines the minimum evidence for a seed multimodal thermal-fluid
benchmark. It is not a claim that the initial data release is representative of
all fluids, surfaces, geometries, facilities, or operating regimes.

## Initial tasks

1. Optical segmentation/tracking with mask and event-quality metrics.
2. Heat-flux or wall-state regression with MAE, RMSE, calibration, and
   condition-stratified error.
3. Explicitly defined regime or event classification with confusion matrix,
   precision/recall, class support, and timing error where applicable.

## Split rule

Random frame-level splits are prohibited for headline claims. Splits must hold
out an independent unit appropriate to the task, such as experiment run,
surface, geometry, fluid, pressure, facility, or heat-load trajectory. Each
release stores immutable split identifiers.

## Required reporting

Report the source manifest version, data version/checksum, preprocessing,
baseline comparison, split definition, metric uncertainty, failure cases, and
known applicability limits. A model must provide an out-of-distribution or
abstention behavior before it is described as suitable for unseen conditions.
