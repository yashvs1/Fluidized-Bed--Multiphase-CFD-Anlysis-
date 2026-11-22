# Multiphase Euler–Euler Modeling of Fluidized-Bed Flotation: Effect of KTGF and Drag Closure Models

**Conference paper accepted at FMFP 2025**  
B.Tech Major Technical Project — IIT Mandi

## Overview
This computational fluid dynamics (CFD) study investigates the hydrodynamics of a scaled, realistic fluidized-bed flotation (FBF) cell using the Euler–Euler model in OpenFOAM’s `twoPhaseEulerFoam` solver. The simulations replicate a geometry for which companion experiments were previously conducted by collaborators at the University of Queensland (JKMRC).

Eleven model combinations, varying Kinetic Theory of Granular Flow (KTGF) and drag closures, were evaluated in full 3-D. The work focuses on predicting bed expansion and solids distribution, which are important for optimizing coarse particle recovery in mineral processing.

## Objectives
- Develop a 3D Eulerian–Eulerian multiphase CFD model of a lab-scale fluidized-bed flotation cell
- Perform grid independence study
- Evaluate the effect of different KTGF and drag closure model combinations
- Validate bed height predictions against experimental measurements
- Analyse axial and radial solids volume fraction profiles

## Methodology
- **Solver**: OpenFOAM `twoPhaseEulerFoam`
- **Modelling approach**: Euler–Euler (two-fluid model)
- **Phases**: Water and solid particles treated as interpenetrating continua
- **Mesh generation**: blockMesh and snappyHexMesh
- **Grid independence**: Study performed across meshes ranging from 20,000 to 3.3 million cells; convergence established at approximately 650k cells
- **Closures tested**: Multiple combinations of KTGF viscosity models and drag models (including Syamlal–O’Brien and Gidaspow)

### Governing Equations
Continuity and momentum equations were solved for both phases. Solid-phase stresses were modelled using the Kinetic Theory of Granular Flow (KTGF), and interphase momentum transfer was prescribed through various drag correlations.

## Key Results
- Grid-independent solution achieved with bed height predictions in the range of 0.29–0.31 m
- Syamlal–O’Brien drag model in conjunction with the Gidaspow viscosity model produced the closest agreement with experimental bed height (**error of approximately 6%**)
- Axial and radial solids volume fraction profiles were analysed to understand flow patterns and model sensitivity

## Tools Used
- OpenFOAM (`twoPhaseEulerFoam`)
- ParaView
- Python (post-processing of VTK results)

## Repository Structure
