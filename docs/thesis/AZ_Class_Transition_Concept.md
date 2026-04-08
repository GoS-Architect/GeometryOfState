# Spatially Inhomogeneous AZ Classification at Stone-Wales Defect Boundaries:

## BDI→D Class Transition and Majorana Zero Mode Localization

*A Geometry of State Technical Concept Paper*

GoS-Architect | github.com/GoS-Architect

March 2026

---

**EPISTEMIC STATUS**

PROVED: AZ tenfold way (10 symmetry classes, invariants in d=1,2,3); BDI has ℤ in d=1, trivial in d=2; D has ℤ₂ in d=1, ℤ in d=2; Bott periodicity (period 2 complex, period 8 real); edge mode existence ∀N≥2 for BDI in d=1 (112 theorems, zero sorry)

DEMONSTRATED: BDI baseline trivial in d=2 (step1_clean_baseline.py); gap closure at h_ex ≈ 0.6 under exchange field (step3_spinful_bdg.py, step3b_finescan.py); 1D BDI chain: w = −1, 2 MZMs, 99.7% edge localization

CONJECTURED: Spatially inhomogeneous AZ classification — BDI in bulk graphene, D at Ni-62/Bi defect sites — produces domain-wall-localized MZMs at the class boundary. Kill condition: if the Bott index of the defect region is zero under physically realistic exchange and SOC parameters

SPECULATIVE: Experimental realization via patterned Ni-62 nano-islands at Stone-Wales defect sites with Bi adatom SOC injection

---

## 1. The Classification Problem in 2D

The Kitaev chain in d=1 belongs to symmetry class BDI (time-reversal T = +1, particle-hole C = +1, chiral S = 1). In d=1, BDI has topological invariant ℤ — the winding number — and supports boundary-localized Majorana zero modes when w ≠ 0. This is the basis of the GoS 1D results (ratchet_full.py, 35 Kitaev chain theorems).

In d=2, BDI has **trivial** topological invariant (0). No topological phase exists. This is not a limitation of the simulation — it is a theorem, proved in AlgebraicLadder.lean and confirmed computationally by step1_clean_baseline.py.

To achieve a nontrivial topological phase in 2D, the system must transition to a different AZ class. Breaking time-reversal symmetry (T: +1 → 0) while preserving particle-hole symmetry (C = +1) moves the system from BDI to class **D**. Class D in d=2 has topological invariant **ℤ** — the Bott index (or equivalently, the Chern number of the BdG Hamiltonian). This invariant is nonzero in the topological phase and supports chiral Majorana edge modes.

---

## 2. The Spatial Inhomogeneity Architecture

### 2.1 The Key Insight

The FWS device does not have a uniform AZ classification. Different spatial regions of the same graphene sheet belong to different symmetry classes:

| Region | T | C | S | AZ Class | Inv(d=2) |
|--------|---|---|---|----------|----------|
| Bulk graphene (far from defects) | +1 | +1 | 1 | BDI | 0 (trivial) |
| Defect site (5/7 + Ni-62 + Bi + Nb) | 0 | +1 | 0 | D | ℤ (Bott index) |
| Domain wall (defect perimeter) | Transition | — | — | BDI → D | MZM host |

At defect sites, three ingredients converge:
- **Ni-62 exchange** breaks T (BDI → D transition): J_ex ~ 6 meV
- **Bi adatom SOC** mixes spin channels: enhances graphene SOC from ~24 μeV to ~80 meV
- **Nb proximity** induces s-wave pairing (particle-hole symmetry): Δ_Nb ~ 1.5 meV

The MZMs localize at the **boundary between the trivial bulk (BDI, invariant 0) and the topological defect region (D, invariant ℤ)**.

### 2.2 Why This Is Not a Uniform Phase Diagram

Standard topological phase diagrams assume spatially uniform parameters. The PGTC device is fundamentally different: the topological phase is **local** to defect sites. This means:

- The winding number is not a global quantity — it must be computed for the defect region vs. the bulk separately
- The Bott index (which handles finite, disordered systems) replaces the Chern number (which requires translational invariance)
- The MZM lives at a spatial domain wall, not at a sample edge

This spatial inhomogeneity is a feature, not a complication. It is exactly the architecture described by the Topological Boundary Coherence Theorem: when a topological invariant changes across a spatial boundary, the coherence data at that boundary is a physically real, localized object.

---

## 3. The Three Ingredients

### 3.1 Ni-62 Exchange Field

Nickel-62 is selected for isotopic purity (I = 0, eliminating hyperfine decoherence) and nuclear stability (highest binding energy per nucleon of any nuclide, 8.7945 MeV).

**Option C/E architecture (recommended):** Patterned Ni-62 nano-islands deposited at Stone-Wales 5/7 defect sites only. This provides:

- Local time-reversal breaking at defects while preserving T in the bulk
- Magnetization inhomogeneity at island edges enabling singlet-to-triplet Cooper pair conversion
- Alignment with the Penrose-seeded defect architecture

**Critical constraint:** The Ni-62 island must not form a continuous film (kills superconducting proximity). The Ni(111)–graphene lattice mismatch is only 1.2%, enabling epitaxial growth at defect sites.

**Exchange coupling:** J_ex ~ 6 meV for Ni nanoparticles on graphene (measured). Substantially larger for epitaxial contact. The exchange field enters the BdG Hamiltonian as a site-dependent Zeeman term:

    h_ex(i) = 0          at bulk sites
    h_ex(i) = J_ex       at defect sites

### 3.2 Bismuth Spin-Orbit Coupling

Bi adatoms (Z = 83) deposited at ~6% coverage on graphene enhance the intrinsic SOC from ~24 μeV to ~80 meV (Weeks et al. 2011). This is a 3000× enhancement. The Rashba SOC from structural inversion asymmetry at the adatom sites entangles spin and momentum, enabling:

- Spin-momentum locking required for helical edge states
- Weyl splitting of the BdG bands
- Effective p-wave pairing character when combined with s-wave proximity

Like the exchange field, the SOC enhancement is **site-dependent**: strong at defect sites (Bi concentrated there), weak in the bulk.

### 3.3 Niobium Proximity

The Nb superconductor (T_c = 9.3 K, Δ_Nb ~ 1.5 meV) provides s-wave Cooper pair proximity to the graphene sheet. In the bulk (class BDI), this produces a trivial superconducting state. At defect sites (class D, with exchange + SOC), the proximity-induced pairing combines with the broken symmetries to produce a topological superconducting state.

The singlet-to-triplet conversion at Ni-62 island edges is critical: triplet pairs are immune to exchange pair-breaking and propagate as effective p-wave pairs — the pairing symmetry that directly supports MZMs.

---

## 4. Simulation Architecture

### 4.1 The BdG Hamiltonian

The Bogoliubov-de Gennes Hamiltonian for the spatially inhomogeneous system:

    H_BdG = H_0 + H_ex + H_SOC + H_Δ

where:
- H_0: tight-binding graphene Hamiltonian with SW-defect-modified hoppings
- H_ex: site-dependent exchange field (nonzero only at defect sites)
- H_SOC: site-dependent Rashba SOC (enhanced at defect sites)
- H_Δ: s-wave pairing from Nb proximity

### 4.2 Computational Pipeline

| Stage | Script | Input | Output | Gate Condition |
|-------|--------|-------|--------|----------------|
| 0 | graphene_sw_lattice.py | Lattice size N, defect count | Corrected honeycomb + SW defect coordinates | Coordination = 3 everywhere; δt/t₀ < 15% |
| 1 | step1_clean_baseline.py | Clean lattice, no exchange/SOC | BDI classification; Bott index | Bott = 0 (BDI trivial in d=2) |
| 2 | step3_spinful_bdg.py | Lattice + h_ex sweep | Gap closure scan; class D transition | Gap closes at finite h_ex |
| 3 | step3b_finescan.py | Lattice + (h_ex, SOC) sweep | Bott index phase diagram | Bott ≠ 0 in topological region |
| 4 | (planned) mzm_localization.py | Full H_BdG at optimal parameters | Eigenstate localization at defect boundaries | LDOS peak at 5/7 perimeter |

### 4.3 Minimum Lattice Size

The MZM localization length ξ must be smaller than the defect cluster width for the mode to be well-defined. The FWS spec requires defect clusters ≥ 51 lattice sites wide (from Ni-62 simulation constraints). For the current N=800 lattice with 30 defects, the defect clusters may be too small. Target: N ≥ 3200 for genuine localization tests.

---

## 5. Repository File Map

### 5.1 Existing Verified Files

| File | Theorems | Sorry | Relevant Content |
|------|----------|-------|-----------------|
| AlgebraicLadder.lean | 13 | 0 | AZ tenfold way; BDI trivial in d=2; D has ℤ in d=2; Bott periodicity |
| KitaevChain.lean | 35 | 0 | Kitaev chain in BDI class; winding number; gap condition |
| EdgeModes.lean | 33 | 0 | Edge mode existence ∀N≥2; boundary localization |
| BridgeTheorems.lean | 9 | 0 | Protection theorems across physical domains |
| FWSClassification.lean | 22 | 0 | Device-specific classification; symmetry class assignments |

### 5.2 Existing Computation Files

| File | Result | Status |
|------|--------|--------|
| step1_clean_baseline.py | BDI trivial in d=2 (Bott = 0) | PASS |
| step3_spinful_bdg.py | Gap closure at h_ex ≈ 0.6 | PASS |
| step3b_finescan.py | Bott index parameter scan | PASS |

### 5.3 Planned Files

| File | Target | Dependency |
|------|--------|------------|
| SpatialAZ.lean | Formalize spatially inhomogeneous AZ classification; domain structure with distinct classes in different regions | AlgebraicLadder.lean |
| DomainWallMZM.lean | Prove that class mismatch across spatial boundary implies boundary-localized zero mode (connects to TBC abstract theorem) | SpatialAZ.lean + EdgeModes.lean |
| mzm_localization.py | Full BdG diagonalization with site-dependent h_ex, SOC, Δ; compute LDOS at defect boundaries | graphene_sw_lattice.py + step3 results |

---

## 6. Epistemic Accounting

| Tag | Claim | Evidence |
|-----|-------|----------|
| PROVED | AZ classification: BDI trivial in d=2, D has ℤ; Bott periodicity; edge mode existence ∀N≥2 | 112 Lean 4 theorems, 0 sorry |
| DEMONSTRATED | BDI baseline trivial (Bott = 0); gap closure under exchange field at h_ex ≈ 0.6; 1D BDI chain w = −1 with 2 MZMs | Python simulations, reproducible |
| CONJECTURED | Spatial BDI/D domain structure with MZMs at domain walls; Bott index nonzero in defect region under realistic Ni-62 + Bi + Nb parameters | Kill condition: Bott = 0 at all scanned parameters → domain wall MZM claim fails |
| SPECULATIVE | Patterned Ni-62 nano-islands at SW sites; Bi adatom SOC injection; full FWS material stack fabrication | Individual techniques exist; combination undemonstrated |

---

## 7. Connection to Bivector Invariance Concept

The AZ class transition provides the **classification** of the topological phase. The bivector invariance criterion provides the **verification** of individual MZMs within that phase. The relationship:

1. AZ classification (this paper) tells you WHERE to look: at domain walls between BDI and D regions
2. Bivector invariance (companion paper) tells you HOW to verify: the mode's bivector representation must be invariant under Spin(2,0) rotations
3. Together they form a pipeline: classify → locate → verify

---

## 8. Next Steps

1. **mzm_localization.py:** Full BdG diagonalization on corrected lattice with site-dependent exchange and SOC. Compute LDOS. Verify MZM localization at defect boundaries.
2. **Larger lattice:** N=3200+ to test localization length ξ vs. cluster width.
3. **SpatialAZ.lean:** Formalize the spatial domain structure in Lean 4. Prove that class mismatch implies boundary mode.
4. **Parameter optimization:** Sweep (h_ex, λ_SOC, Δ) to identify optimal operating point for maximum topological gap at domain walls.
