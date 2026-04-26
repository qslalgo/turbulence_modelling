## Overview

This repository contains turbulence modelling exercises performed using ANSYS Fluent.
The focus is on evaluating the performance of different RANS turbulence models across benchmark flow configurations.

## Objectives
Understand behaviour of common turbulence models
Compare accuracy vs computational cost
Validate simulations against reference/analytical data

## Models Used
k–ε (standard / realizable), k–ω SST

## Cases Studied (examples)
Channel flow, flow over a flat plate, backward-facing step, pipe flow, duct flow

## Methodology
Geometry and mesh generation in ANSYS
Boundary condition specification (Re, inlet profiles, etc.)
Solver setup (steady-state RANS)
Post-processing of:
velocity profiles
pressure drop
wall shear stress

## Key Outcomes
Observed sensitivity of results to turbulence model choice
SST model showed improved near-wall prediction (if true)
Differences in recirculation length / velocity profiles across models
