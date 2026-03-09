# The Geometry of State 
**A Digital Triplet Framework for Verifiable Topological Quantum Materials**

## Overview
This repository provides a comprehensive, formally verified architecture for topological quantum computation and magnetohydrodynamics (MHD). By bridging **Lean 4** dependent type theory with **JAX-accelerated** physical simulations, this framework resolves the epistemological ambiguity of the Majorana verification crisis. 

The core operational thesis: **In a properly formalized system, a physical phase transition (singularity) manifests as a logical Type Error.** ## Repository Architecture

This project is structured as a **Digital Triplet** (Physical ↔ Digital ↔ Logical), ensuring that autonomous controllers cannot force quantum or plasma hardware into topologically unstable states.

### 📁 01_Logical_Layer_Lean4
The formal verification stack and deductive certification layer. 
* `KitaevChain.lean`: Demonstrates that the topological winding number function becomes uncallable (a type error) when the energy gap closes.
* `TopologicalLock3D.lean`: Proves that 3D knotted vortex filaments are protected by exact topological invariants below a specific reconnection energy.
* `MHDTopology.lean`: Scales the superfluid lock to fusion plasmas, formally defining the "Stellarator Theorem" for magnetic confinement.

### 📁 02_Physical_Layer_Simulations
The empirical physics engines that discharge the Lean 4 proof obligations.
* `gp3d_solver.py`: A GPU-ready 3D Gross-Pitaevskii solver with imaginary-time relaxation.
* `gp3d_readwrite.py`: Implements a 4-phase protocol testing controlled topological state mutation (X-point splicing).
* `stellarator_taylor_relaxation.py`: Demonstrates selective dissipation where energy decays faster than helicity, allowing convergence to the Beltrami state.

### 📁 03_Foundational_Pillars_(Archive)
The theoretical bedrock and foundational axioms of the framework.
* Includes the complete Cohesive Linear Homotopy Type Theory (CL-HoTT) logical kernel.
* Contains the foundational proofs mapping geometric bivectors to physical symmetries (e.g., the Nestar Gearbox, the Ni62 Anchor, and the Triad Handshake protocol).

## Note to Reviewers & Recruiters
To see the direct bridge between formal logic and quantum physics, begin with `01_Logical_Layer_Lean4/KitaevChain.lean`. 

## License
MIT License
