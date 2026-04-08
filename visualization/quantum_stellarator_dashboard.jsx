import { useState, useEffect, useCallback, useRef } from "react";

const TIERS = {
  proved: { label: "Proved", color: "#4CAF50", bg: "#1b2e1b", border: "#2d5a2d" },
  demonstrated: { label: "Demonstrated", color: "#42A5F5", bg: "#1a2533", border: "#2a4a6b" },
  motivated: { label: "Motivated", color: "#FFCA28", bg: "#2e2a1a", border: "#6b5a2a" },
  conjectured: { label: "Conjectured", color: "#FFA726", bg: "#2e251a", border: "#6b4a2a" },
  speculative: { label: "Speculative", color: "#EF5350", bg: "#2e1a1a", border: "#6b2a2a" },
};

const LAYERS = [
  { id: "L0-1", name: "Superconducting substrate", layers: "0–1", system: "Nb + Penrose graphene", domain: "Algebraic geometry", tier: "motivated", continent: "asia", anchor: "Cl(2,0) / Cl(3,0)", details: "Niobium superconductor (Tc ≈ 9.3K) patterned with Penrose quasicrystal graphene. The aperiodic tiling creates the scaling asymmetry exploited by PGTC. Mathematical domain: Clifford algebras verified in GoS.", trl: 3 },
  { id: "L2-3", name: "Phonon glass + NV centers", layers: "2–3", system: "NV centers + carbon + phonon glass", domain: "Materials physics", tier: "demonstrated", continent: "africa", anchor: "Harrison/Keating asymmetry", details: "PGTC core layer. 70% phonon suppression via d⁻² vs d⁻⁴ scaling asymmetry. NV centers for quantum sensing. 12 localized phonon modes, spectral gap ratio 58.8×.", trl: 4 },
  { id: "L4-5", name: "Superfluid medium", layers: "4–5", system: "He-3/He-4 + Ni-62 trefoil", domain: "SVT + ER=EPR", tier: "conjectured", continent: "europe", anchor: "Superfluid vacuum / analog gravity", details: "Most speculative physics. He-3 as topological superfluid (class DIII). Trefoil-wound Ni-62 wire for confinement. SVT and ER=EPR connections theoretical. No downstream claims depend on this layer.", trl: 2 },
  { id: "L6-7", name: "Control layer", layers: "6–7", system: "Bismuth + OAM lasers", domain: "ZX calculus control", tier: "motivated", continent: "northamerica", anchor: "OAM encoding", details: "Bi topological semimetal with strong spin-orbit coupling. OAM lasers provide high-dimensional Hilbert space (ℓ = 0, ±1, ±2...). ZX calculus for quantum circuit compilation.", trl: 3 },
  { id: "ST", name: "Stellarator integration", layers: "Topos", system: "Quantum stellarator", domain: "Trefoil knot topology", tier: "conjectured", continent: "oceania", anchor: "All layers compose", details: "Separate topos where all layers compose. Trefoil knot geometry — simplest nontrivial knot. The integration test for the entire architecture. Mathematical structure is Motivated; physical device is Conjectured.", trl: 1 },
];

const AXIOMS = [
  { id: 1, name: "Conservation", short: "Truth is reallocated, not destroyed", full: "Retraction preserves information. A reclassification from tier n to tier m produces the original claim, the reclassification record, the evidence, and the updated dependency graph. All four are conserved.", icon: "⟲" },
  { id: 2, name: "Symmetry", short: "Promotion and demotion are identical", full: "Promotion and demotion on the epistemic lattice are formally identical operations. Both trigger Rung Rule propagation. Neither carries moral valence. A node reporting a capability downgrade performs the same function as one reporting a breakthrough.", icon: "⇅" },
  { id: 3, name: "Fault as type error", short: "Failures are well-typed, not moral", full: "When a dependency fails, the protocol asks which type constraint was violated and what reallocation restores type safety. The compiler does not blame the programmer. It points to the line where the types don't match.", icon: "⊥" },
  { id: 4, name: "Load-bearing failure", short: "Nontrivial cohomology requires obstructions", full: "A system requires nontrivial cohomology to be topologically protected. Obstructions are the network's immune system. A collaboration that has never failed has never been tested. A system with no obstructions has trivial cohomology, no topological protection, and no robustness.", icon: "△" },
  { id: 5, name: "Gauge autonomy", short: "Constrain overlaps, not patches", full: "Each node operates with full internal freedom. The protocol constrains only the transition functions — the interfaces between nodes. Governance is a connection on overlaps, not a mandate on patches.", icon: "◇" },
  { id: 6, name: "Cryptographic blame-freedom", short: "Attribution is gauge-dependent", full: "Failure reports contain the obstruction class (type, severity, routing specification) and no attribution. The encryption makes the failure channel trustworthy. A node that can report failure without consequence will report failure early. The encryption is load-bearing infrastructure.", icon: "◈" },
  { id: 7, name: "Cognitive liberty DMZ", short: "Undefined, not prohibited", full: "The governance type system has no constructors for cognitive coercion, weaponized application, or surveillance targeting. These operations are not prohibited — they are undefined. The sheaf has empty stalks in the DMZ. There is nothing to violate.", icon: "◻" },
];

const CONTINENTS = [
  { id: "antarctica", name: "Antarctica", role: "Governance substrate", layer: "Layer 0", color: "#B0BEC5", resources: ["Antarctic Treaty precedent", "Extreme cryo environments", "Environmental stewardship"], seasonal: true },
  { id: "africa", name: "Africa", role: "Diamond & He supply", layer: "Layers 0–1", color: "#FFA726", resources: ["Natural diamond (SA, Botswana)", "¹²C isotopic carbon", "He-4 (Tanzania Rukwa)", "SKA Observatory"] },
  { id: "asia", name: "Asia", role: "Nanofabrication", layer: "Layers 0–1", color: "#EF5350", resources: ["EBL lithography (TSMC, Samsung)", "CVD graphene", "Twisted bilayer graphene", "Penrose patterning (target)"] },
  { id: "southamerica", name: "South America", role: "Nb supply + Constitution", layer: "Layers 0–1", color: "#66BB6A", resources: ["Niobium — CBMM (~80% global)", "Neuro rights framework (Chile)", "Constitutional XAI precedent"] },
  { id: "europe", name: "Europe", role: "Superfluids + Stellarator", layer: "Layers 4–5", color: "#42A5F5", resources: ["W7-X stellarator (Greifswald)", "mK cryogenics (Lancaster, Aalto)", "He-3 superfluid physics", "CERN governance model"] },
  { id: "northamerica", name: "North America", role: "Verification + Isotopes", layer: "Layers 6–7", color: "#AB47BC", resources: ["ORNL isotope enrichment", "DOE He-3 custody", "GoS framework (Lean 4)", "CUDA-Q / Station Q"] },
  { id: "oceania", name: "Oceania", role: "Integration topos", layer: "Stellarator", color: "#26C6DA", resources: ["UNSW quantum computing", "Broad measurement capability", "Pacific network position", "Integration & validation"] },
];

const PGTC = [
  { quantity: "Phonon suppression", value: "κ_QP/κ_ordered = 0.30", meaning: "70% reduction in thermal conductivity", tier: "demonstrated" },
  { quantity: "Localized modes", value: "12 modes", meaning: "Quasiperiodic disorder creates localization", tier: "demonstrated" },
  { quantity: "Spectral gap ratio", value: "58.8×", meaning: "Topological protection margin", tier: "demonstrated" },
  { quantity: "Winding number", value: "w = −1", meaning: "Nontrivial topological invariant", tier: "proved" },
  { quantity: "MZM edge localization", value: "99.7%", meaning: "Majorana zero modes at boundaries", tier: "proved" },
  { quantity: "Class transition", value: "BDI → D", meaning: "Exchange field breaks time-reversal", tier: "demonstrated" },
];

const ISOTOPES = [
  { symbol: "⁹³Nb", name: "Niobium", layer: "0", source: "CBMM (Brazil)", custody: "Purchase", recovery: "Melt/recast", risk: "Medium — CBMM dominance", tier: "proved" },
  { symbol: "¹²C", name: "Carbon-12", layer: "2–3", source: "Cambridge Isotope", custody: "Purchase", recovery: "Mechanical separation", risk: "Low", tier: "demonstrated" },
  { symbol: "⁶²Ni", name: "Nickel-62", layer: "4–5", source: "ORNL", custody: "DOE custodial loan", recovery: "Wire extraction", risk: "High — enrichment capacity", tier: "conjectured" },
  { symbol: "⁴He", name: "Helium-4", layer: "4–5", source: "Commercial (crisis)", custody: "Purchase + recycling", recovery: "Closed-loop", risk: "Critical — Hormuz closure", tier: "speculative" },
  { symbol: "³He", name: "Helium-3", layer: "4–5", source: "DOE", custody: "Custodial loan", recovery: "Sealed recovery", risk: "High — strategic material", tier: "conjectured" },
  { symbol: "²⁰⁹Bi", name: "Bismuth", layer: "6–7", source: "Commercial", custody: "Purchase", recovery: "Standard", risk: "Low", tier: "proved" },
];

const TABS = [
  { id: "layers", label: "Layer stack" },
  { id: "axioms", label: "Seven axioms" },
  { id: "network", label: "Seven continents" },
  { id: "pgtc", label: "PGTC results" },
  { id: "logistics", label: "Logistics" },
  { id: "notes", label: "Notes" },
];

function TierBadge({ tier, small }) {
  const t = TIERS[tier];
  if (!t) return null;
  return (
    <span style={{ display:"inline-block", padding: small ? "1px 6px" : "2px 10px", borderRadius: 4, fontSize: small ? 10 : 11, fontWeight: 600, letterSpacing: 0.5, color: t.color, background: t.bg, border: `1px solid ${t.border}`, textTransform: "uppercase", whiteSpace: "nowrap" }}>
      {t.label}
    </span>
  );
}

function TRLBar({ value }) {
  return (
    <div style={{ display:"flex", alignItems:"center", gap: 6 }}>
      <div style={{ flex:1, height: 4, background:"#1a1a2e", borderRadius: 2, overflow:"hidden" }}>
        <div style={{ width:`${(value/9)*100}%`, height:"100%", background: value >= 7 ? "#4CAF50" : value >= 4 ? "#FFCA28" : "#EF5350", borderRadius: 2, transition:"width 0.4s" }} />
      </div>
      <span style={{ fontSize: 11, color:"#8a8a9a", fontFamily:"'JetBrains Mono', monospace", minWidth: 32 }}>TRL {value}</span>
    </div>
  );
}

function LayersView() {
  const [selected, setSelected] = useState(null);
  return (
    <div>
      <p style={{ color:"#8a8a9a", fontSize: 13, marginBottom: 20, lineHeight: 1.6 }}>
        Eight physical layers (0–7) plus integration topos. Each layer occupies a distinct mathematical domain. Click to expand.
      </p>
      <div style={{ display:"flex", flexDirection:"column", gap: 2 }}>
        {LAYERS.map((l, i) => {
          const t = TIERS[l.tier];
          const open = selected === i;
          return (
            <div key={l.id} onClick={() => setSelected(open ? null : i)} style={{ background: open ? t.bg : "#0d0d14", border: `1px solid ${open ? t.border : "#1a1a2e"}`, borderRadius: 6, padding: "14px 18px", cursor:"pointer", transition:"all 0.2s" }}>
              <div style={{ display:"flex", justifyContent:"space-between", alignItems:"center", gap: 12 }}>
                <div style={{ display:"flex", alignItems:"center", gap: 12, flex:1, minWidth:0 }}>
                  <span style={{ fontFamily:"'JetBrains Mono', monospace", fontSize: 12, color: t.color, fontWeight: 700, minWidth: 48 }}>{l.layers}</span>
                  <span style={{ fontWeight: 500, color:"#e0e0e8", fontSize: 14 }}>{l.name}</span>
                </div>
                <TierBadge tier={l.tier} small />
              </div>
              {open && (
                <div style={{ marginTop: 14, paddingTop: 14, borderTop:`1px solid ${t.border}` }}>
                  <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:"8px 24px", marginBottom: 12 }}>
                    <div><span style={{ fontSize:11, color:"#6a6a7a", textTransform:"uppercase", letterSpacing:0.5 }}>System</span><div style={{ fontSize:13, color:"#c0c0cc", marginTop:2 }}>{l.system}</div></div>
                    <div><span style={{ fontSize:11, color:"#6a6a7a", textTransform:"uppercase", letterSpacing:0.5 }}>Domain</span><div style={{ fontSize:13, color:"#c0c0cc", marginTop:2 }}>{l.domain}</div></div>
                    <div><span style={{ fontSize:11, color:"#6a6a7a", textTransform:"uppercase", letterSpacing:0.5 }}>Anchor</span><div style={{ fontSize:13, color:"#c0c0cc", marginTop:2 }}>{l.anchor}</div></div>
                    <div><span style={{ fontSize:11, color:"#6a6a7a", textTransform:"uppercase", letterSpacing:0.5 }}>Primary node</span><div style={{ fontSize:13, color:"#c0c0cc", marginTop:2 }}>{CONTINENTS.find(c=>c.id===l.continent)?.name}</div></div>
                  </div>
                  <TRLBar value={l.trl} />
                  <p style={{ fontSize: 13, color:"#9a9aaa", lineHeight: 1.65, marginTop: 12 }}>{l.details}</p>
                </div>
              )}
            </div>
          );
        })}
      </div>
      <div style={{ marginTop: 20, padding: "12px 16px", background:"#0d0d14", borderRadius: 6, border:"1px solid #1a1a2e" }}>
        <div style={{ fontSize: 11, color:"#6a6a7a", textTransform:"uppercase", letterSpacing: 0.5, marginBottom: 8 }}>Epistemic tier legend</div>
        <div style={{ display:"flex", flexWrap:"wrap", gap: 8 }}>
          {Object.entries(TIERS).map(([k,v]) => <TierBadge key={k} tier={k} />)}
        </div>
      </div>
    </div>
  );
}

function AxiomsView() {
  const [expanded, setExpanded] = useState(null);
  return (
    <div>
      <p style={{ color:"#8a8a9a", fontSize: 13, marginBottom: 20, lineHeight: 1.6 }}>
        Seven constitutional axioms. Formally verifiable constraints on the governance type system. Not policy — mathematics.
      </p>
      <div style={{ display:"flex", flexDirection:"column", gap: 3 }}>
        {AXIOMS.map((a) => {
          const open = expanded === a.id;
          const isDMZ = a.id === 7;
          return (
            <div key={a.id} onClick={() => setExpanded(open ? null : a.id)} style={{ background: isDMZ && open ? "#1a1525" : open ? "#12121e" : "#0d0d14", border: `1px solid ${isDMZ && open ? "#4a2a6b" : open ? "#2a2a3e" : "#1a1a2e"}`, borderRadius: 6, padding: "14px 18px", cursor:"pointer", transition:"all 0.2s" }}>
              <div style={{ display:"flex", alignItems:"center", gap: 14 }}>
                <span style={{ fontFamily:"'JetBrains Mono', monospace", fontSize: 18, color: isDMZ ? "#AB47BC" : "#42A5F5", width: 28, textAlign:"center" }}>{a.icon}</span>
                <div style={{ flex:1 }}>
                  <div style={{ display:"flex", alignItems:"center", gap: 8 }}>
                    <span style={{ fontFamily:"'JetBrains Mono', monospace", fontSize: 11, color:"#6a6a7a" }}>§{a.id}</span>
                    <span style={{ fontWeight: 600, color:"#e0e0e8", fontSize: 14 }}>{a.name}</span>
                  </div>
                  <div style={{ fontSize: 12, color:"#8a8a9a", marginTop: 3, fontStyle:"italic" }}>{a.short}</div>
                </div>
              </div>
              {open && (
                <div style={{ marginTop: 14, paddingTop: 14, borderTop:"1px solid #1a1a2e" }}>
                  <p style={{ fontSize: 13, color:"#b0b0be", lineHeight: 1.7, margin: 0 }}>{a.full}</p>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}

function NetworkView() {
  const [selected, setSelected] = useState(null);
  return (
    <div>
      <p style={{ color:"#8a8a9a", fontSize: 13, marginBottom: 20, lineHeight: 1.6 }}>
        Seven continents. Fully connected dependency graph. No node is self-sufficient. The physics creates the politics.
      </p>
      <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap: 3 }}>
        {CONTINENTS.map((c) => {
          const open = selected === c.id;
          return (
            <div key={c.id} onClick={() => setSelected(open ? null : c.id)} style={{ background: open ? "#12121e" : "#0d0d14", border: `1px solid ${open ? c.color+"44" : "#1a1a2e"}`, borderRadius: 6, padding: "12px 14px", cursor:"pointer", transition:"all 0.2s", gridColumn: c.id === "antarctica" ? "1 / -1" : undefined }}>
              <div style={{ display:"flex", alignItems:"center", gap: 10 }}>
                <div style={{ width: 8, height: 8, borderRadius:"50%", background: c.color, flexShrink:0, opacity: c.seasonal ? undefined : 1, animation: c.seasonal ? "pulse 3s ease-in-out infinite" : undefined }} />
                <div style={{ flex:1, minWidth:0 }}>
                  <div style={{ fontWeight: 600, color:"#e0e0e8", fontSize: 13 }}>{c.name}</div>
                  <div style={{ fontSize: 11, color:"#6a6a7a" }}>{c.role}</div>
                </div>
                <span style={{ fontSize: 10, color:"#5a5a6a", fontFamily:"'JetBrains Mono', monospace" }}>{c.layer}</span>
              </div>
              {open && (
                <div style={{ marginTop: 10, paddingTop: 10, borderTop:`1px solid ${c.color}22` }}>
                  {c.resources.map((r,i) => (
                    <div key={i} style={{ fontSize: 12, color:"#9a9aaa", padding:"3px 0", display:"flex", alignItems:"baseline", gap: 8 }}>
                      <span style={{ color: c.color, fontSize: 8 }}>●</span>{r}
                    </div>
                  ))}
                  {c.seasonal && <div style={{ fontSize: 11, color:"#8a6a9a", marginTop: 8, fontStyle:"italic" }}>Seasonal topology: accessible ~Oct–Feb. Protocol treats closure as node failure — obstruction routes to other nodes.</div>}
                </div>
              )}
            </div>
          );
        })}
      </div>
      <div style={{ marginTop: 16, padding: "14px 16px", background:"#0d0d14", borderRadius: 6, border:"1px solid #1a1a2e" }}>
        <div style={{ fontSize: 11, color:"#6a6a7a", textTransform:"uppercase", letterSpacing: 0.5, marginBottom: 10 }}>Critical dependencies (non-exhaustive)</div>
        {[
          ["South America → All", "Niobium substrate"],
          ["Africa → Asia, Europe", "¹²C diamond substrates"],
          ["N. America → Europe", "He-3 custodial loan"],
          ["Asia → Europe, Oceania", "Patterned graphene"],
          ["All → Oceania", "Components for integration"],
          ["N. America → All", "GoS formal verification"],
        ].map(([flow, dep], i) => (
          <div key={i} style={{ display:"flex", alignItems:"center", gap: 12, padding:"4px 0", fontSize: 12 }}>
            <span style={{ color:"#42A5F5", fontFamily:"'JetBrains Mono', monospace", minWidth: 180, fontSize: 11 }}>{flow}</span>
            <span style={{ color:"#8a8a9a" }}>{dep}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

function PGTCView() {
  return (
    <div>
      <p style={{ color:"#8a8a9a", fontSize: 13, marginBottom: 6, lineHeight: 1.6 }}>
        Proof of Geometric Topological Chirality — core experimental contribution. Harrison/Keating scaling asymmetry: electron hopping scales as d⁻², phonon spring constants as d⁻⁴.
      </p>
      <p style={{ color:"#6a6a7a", fontSize: 12, marginBottom: 20, fontStyle:"italic" }}>
        Mechanism: In quasiperiodic lattices, the d⁻⁴ variation disrupts phonons far more than the d⁻² variation disrupts electrons → phonon glass, electron crystal.
      </p>
      <div style={{ display:"flex", flexDirection:"column", gap: 2 }}>
        {PGTC.map((r, i) => {
          const t = TIERS[r.tier];
          return (
            <div key={i} style={{ display:"grid", gridTemplateColumns:"140px 140px 1fr auto", alignItems:"center", gap: 16, padding:"12px 16px", background:"#0d0d14", borderRadius: 4, borderLeft:`3px solid ${t.color}` }}>
              <span style={{ fontSize: 13, color:"#c0c0cc", fontWeight: 500 }}>{r.quantity}</span>
              <span style={{ fontSize: 14, color: t.color, fontFamily:"'JetBrains Mono', monospace", fontWeight: 700 }}>{r.value}</span>
              <span style={{ fontSize: 12, color:"#8a8a9a" }}>{r.meaning}</span>
              <TierBadge tier={r.tier} small />
            </div>
          );
        })}
      </div>
      <div style={{ marginTop: 24, padding:"16px 18px", background:"#1a2533", border:"1px solid #2a4a6b", borderRadius: 6 }}>
        <div style={{ fontSize: 12, fontWeight: 600, color:"#42A5F5", marginBottom: 8, textTransform:"uppercase", letterSpacing: 0.5 }}>Critical path</div>
        <div style={{ display:"flex", alignItems:"center", gap: 8, flexWrap:"wrap" }}>
          {["Penrose mask design", "→", "Graphene patterning", "→", "Phonon measurement", "→", "GO / NO-GO"].map((s,i) => 
            s === "→" ? <span key={i} style={{ color:"#3a3a4a" }}>→</span> :
            s === "GO / NO-GO" ? <span key={i} style={{ padding:"4px 12px", borderRadius:4, background:"#2e1a1a", border:"1px solid #6b2a2a", color:"#EF5350", fontSize:12, fontWeight:700, fontFamily:"'JetBrains Mono', monospace" }}>{s}</span> :
            <span key={i} style={{ padding:"4px 10px", borderRadius:4, background:"#12121e", border:"1px solid #2a2a3e", color:"#b0b0be", fontSize:12 }}>{s}</span>
          )}
        </div>
        <p style={{ fontSize: 12, color:"#7a9abc", marginTop: 10, lineHeight: 1.5 }}>
          If κ_QP/κ_ordered falls within 0.15–0.60, proceed. If phonon suppression is not observed, revise the model before further investment.
        </p>
      </div>
      <div style={{ marginTop: 16, padding:"16px 18px", background:"#0d0d14", border:"1px solid #1a1a2e", borderRadius: 6 }}>
        <div style={{ fontSize: 12, fontWeight: 600, color:"#c0c0cc", marginBottom: 8, textTransform:"uppercase", letterSpacing: 0.5 }}>GoS verification status</div>
        <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap: 12 }}>
          <div><span style={{ fontSize: 28, fontWeight: 700, color:"#4CAF50", fontFamily:"'JetBrains Mono', monospace" }}>144</span><div style={{ fontSize: 11, color:"#6a6a7a" }}>Zero-dependency theorems</div></div>
          <div><span style={{ fontSize: 28, fontWeight: 700, color:"#4CAF50", fontFamily:"'JetBrains Mono', monospace" }}>0</span><div style={{ fontSize: 11, color:"#6a6a7a" }}>sorry in L2 classification</div></div>
          <div><span style={{ fontSize: 28, fontWeight: 700, color:"#FFCA28", fontFamily:"'JetBrains Mono', monospace" }}>6</span><div style={{ fontSize: 11, color:"#6a6a7a" }}>sorry in CLHoTT.lean (Float ring laws)</div></div>
          <div><span style={{ fontSize: 28, fontWeight: 700, color:"#42A5F5", fontFamily:"'JetBrains Mono', monospace" }}>10</span><div style={{ fontSize: 11, color:"#6a6a7a" }}>AZ symmetry classes verified</div></div>
        </div>
      </div>
    </div>
  );
}

function LogisticsView() {
  const [view, setView] = useState("isotopes");
  return (
    <div>
      <div style={{ display:"flex", gap: 2, marginBottom: 16 }}>
        {[["isotopes","Isotope custody"],["cleanroom","Cleanroom segregation"],["thermal","Thermal staging"],["risks","Supply risks"]].map(([id,label]) => (
          <button key={id} onClick={() => setView(id)} style={{ padding:"6px 14px", borderRadius: 4, border:"1px solid", borderColor: view===id ? "#42A5F5" : "#1a1a2e", background: view===id ? "#1a2533" : "transparent", color: view===id ? "#42A5F5" : "#6a6a7a", fontSize: 12, cursor:"pointer", fontFamily:"inherit", fontWeight: view===id ? 600 : 400 }}>{label}</button>
        ))}
      </div>
      {view === "isotopes" && (
        <div>
          <p style={{ color:"#8a8a9a", fontSize: 12, marginBottom: 14, fontStyle:"italic" }}>Custody, not ownership. All enriched isotopes held under protocols modeled on DOE He-3 custodial loan system.</p>
          <div style={{ display:"flex", flexDirection:"column", gap: 2 }}>
            {ISOTOPES.map((iso, i) => {
              const t = TIERS[iso.tier];
              return (
                <div key={i} style={{ padding:"10px 14px", background:"#0d0d14", borderRadius: 4, borderLeft:`3px solid ${t.color}` }}>
                  <div style={{ display:"flex", alignItems:"center", gap: 12, marginBottom: 6 }}>
                    <span style={{ fontFamily:"'JetBrains Mono', monospace", fontWeight: 700, fontSize: 15, color: t.color, minWidth: 40 }}>{iso.symbol}</span>
                    <span style={{ fontSize: 13, color:"#c0c0cc", fontWeight: 500 }}>{iso.name}</span>
                    <span style={{ fontSize: 11, color:"#5a5a6a", marginLeft:"auto" }}>Layer {iso.layer}</span>
                  </div>
                  <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr 1fr", gap: 4, fontSize: 11 }}>
                    <div><span style={{ color:"#5a5a6a" }}>Source: </span><span style={{ color:"#8a8a9a" }}>{iso.source}</span></div>
                    <div><span style={{ color:"#5a5a6a" }}>Custody: </span><span style={{ color:"#8a8a9a" }}>{iso.custody}</span></div>
                    <div><span style={{ color:"#5a5a6a" }}>Risk: </span><span style={{ color: iso.risk.startsWith("Critical") ? "#EF5350" : iso.risk.startsWith("High") ? "#FFA726" : "#8a8a9a" }}>{iso.risk}</span></div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
      {view === "cleanroom" && (
        <div>
          <div style={{ padding:"14px 16px", background:"#2e1a1a", border:"1px solid #6b2a2a", borderRadius: 6, marginBottom: 16 }}>
            <div style={{ fontSize: 12, fontWeight: 700, color:"#EF5350", marginBottom: 6 }}>HARD CONSTRAINT</div>
            <p style={{ fontSize: 13, color:"#d0a0a0", lineHeight: 1.6, margin: 0 }}>Nickel is non-CMOS-compatible. Mobile Ni ions cause device failure at contamination levels above 10¹⁰ atoms/cm². The flow from CMOS-clean to metals is one-directional and irreversible.</p>
          </div>
          <div style={{ display:"flex", flexDirection:"column", gap: 3 }}>
            {[
              { stage: 1, name: "CMOS-clean", where: "Asia", desc: "Graphene CVD, Penrose EBL, transfer to Nb", class: "CMOS-clean", color:"#4CAF50" },
              { stage: 2, name: "Diamond integration", where: "Africa/Asia", desc: "NV-center nanodiamond deposition", class: "CMOS-compatible", color:"#4CAF50" },
              { stage: 3, name: "Metals fabrication", where: "N. America", desc: "Ni-62 trefoil wire winding", class: "Metals-only", color:"#EF5350" },
              { stage: 4, name: "Superfluid cell", where: "Europe", desc: "He-3/He-4 cell fabrication", class: "Independent", color:"#42A5F5" },
              { stage: 5, name: "Control layer", where: "N. America", desc: "Bi thin film, OAM optical assembly", class: "Parallel", color:"#42A5F5" },
              { stage: 6, name: "Integration", where: "Oceania", desc: "All components assembled", class: "Non-cleanroom", color:"#FFCA28" },
            ].map((s) => (
              <div key={s.stage} style={{ display:"flex", alignItems:"center", gap: 14, padding:"10px 14px", background:"#0d0d14", borderRadius: 4, borderLeft:`3px solid ${s.color}` }}>
                <span style={{ fontFamily:"'JetBrains Mono', monospace", fontSize: 18, fontWeight: 700, color: s.color, width: 28, textAlign:"center" }}>{s.stage}</span>
                <div style={{ flex:1 }}>
                  <div style={{ display:"flex", alignItems:"center", gap: 8 }}>
                    <span style={{ fontSize: 13, fontWeight: 600, color:"#c0c0cc" }}>{s.name}</span>
                    <span style={{ fontSize: 10, color:"#5a5a6a", fontFamily:"'JetBrains Mono', monospace" }}>{s.class}</span>
                  </div>
                  <div style={{ fontSize: 12, color:"#7a7a8a" }}>{s.where} — {s.desc}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
      {view === "thermal" && (
        <div>
          <p style={{ color:"#8a8a9a", fontSize: 12, marginBottom: 14 }}>Six orders of magnitude in temperature. Concentric thermal shields. Trefoil geometry requires custom cryostat (TRL 1–2).</p>
          <div style={{ display:"flex", flexDirection:"column", gap: 2 }}>
            {[
              { stage: "Room temp", temp: "~300 K", layers: "OAM optics", tech: "Ambient", color:"#EF5350" },
              { stage: "LN₂ shield", temp: "77 K", layers: "Radiation shielding", tech: "Liquid nitrogen", color:"#FFA726" },
              { stage: "LHe shield", temp: "4.2 K", layers: "Bi, Nb substrate", tech: "Liquid He-4 bath", color:"#FFCA28" },
              { stage: "He-4 pot", temp: "1.5 K", layers: "He-4 superfluid", tech: "Pumped He-4", color:"#66BB6A" },
              { stage: "Still", temp: "~0.7 K", layers: "Thermal anchor", tech: "Dilution refrigerator", color:"#42A5F5" },
              { stage: "Mixing chamber", temp: "5–10 mK", layers: "He-3, Ni-62 wire", tech: "Dilution refrigerator", color:"#AB47BC" },
            ].map((s, i) => (
              <div key={i} style={{ display:"grid", gridTemplateColumns:"120px 80px 1fr 1fr", alignItems:"center", gap: 12, padding:"10px 14px", background:"#0d0d14", borderRadius: 4, borderLeft:`3px solid ${s.color}` }}>
                <span style={{ fontSize: 13, color:"#c0c0cc", fontWeight: 500 }}>{s.stage}</span>
                <span style={{ fontSize: 13, color: s.color, fontFamily:"'JetBrains Mono', monospace", fontWeight: 700 }}>{s.temp}</span>
                <span style={{ fontSize: 12, color:"#8a8a9a" }}>{s.layers}</span>
                <span style={{ fontSize: 11, color:"#6a6a7a" }}>{s.tech}</span>
              </div>
            ))}
          </div>
        </div>
      )}
      {view === "risks" && (
        <div>
          <p style={{ color:"#8a8a9a", fontSize: 12, marginBottom: 14 }}>Geopolitical supply chain risk assessment. March 2026: Strait of Hormuz closure has removed ~30% of global He-4.</p>
          {[
            { material: "He-4", chokepoint: "Strait of Hormuz / Qatar", severity: "Critical", mitigation: "Diversify to US/Tanzania/Australia; closed-loop recovery", tier: "speculative" },
            { material: "He-3", chokepoint: "DOE tritium program", severity: "High", mitigation: "European reactor production (ILL Grenoble)", tier: "conjectured" },
            { material: "Nb", chokepoint: "CBMM market dominance", severity: "Medium", mitigation: "Strategic stockpile; Australian sources", tier: "conjectured" },
            { material: "Ni-62", chokepoint: "ORNL enrichment capacity", severity: "Medium", mitigation: "Russian alternatives (sanctions risk)", tier: "conjectured" },
          ].map((r, i) => {
            const t = TIERS[r.tier];
            return (
              <div key={i} style={{ padding:"12px 14px", background:"#0d0d14", borderRadius: 4, borderLeft:`3px solid ${t.color}`, marginBottom: 3 }}>
                <div style={{ display:"flex", alignItems:"center", gap: 12, marginBottom: 4 }}>
                  <span style={{ fontWeight: 700, color:"#c0c0cc", fontSize: 14 }}>{r.material}</span>
                  <span style={{ fontSize: 11, padding:"1px 8px", borderRadius: 3, background: r.severity==="Critical" ? "#2e1a1a" : r.severity==="High" ? "#2e251a" : "#1a1a2e", color: r.severity==="Critical" ? "#EF5350" : r.severity==="High" ? "#FFA726" : "#8a8a9a", border:`1px solid ${r.severity==="Critical" ? "#6b2a2a" : r.severity==="High" ? "#6b4a2a" : "#2a2a3e"}` }}>{r.severity}</span>
                </div>
                <div style={{ fontSize: 12, color:"#7a7a8a" }}>{r.chokepoint}</div>
                <div style={{ fontSize: 12, color:"#6a9a7a", marginTop: 4 }}>Mitigation: {r.mitigation}</div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

function NotesView() {
  const [notes, setNotes] = useState([]);
  const [loaded, setLoaded] = useState(false);
  const [draft, setDraft] = useState("");
  const [draftTier, setDraftTier] = useState("motivated");
  const [draftTag, setDraftTag] = useState("general");
  const [filter, setFilter] = useState("all");
  const textareaRef = useRef(null);

  useEffect(() => {
    (async () => {
      try {
        const result = await window.storage.get("qs-notes");
        if (result && result.value) setNotes(JSON.parse(result.value));
      } catch (e) { /* no notes yet */ }
      setLoaded(true);
    })();
  }, []);

  const saveNotes = useCallback(async (newNotes) => {
    setNotes(newNotes);
    try { await window.storage.set("qs-notes", JSON.stringify(newNotes)); } catch(e) { console.error(e); }
  }, []);

  const addNote = useCallback(() => {
    if (!draft.trim()) return;
    const note = { id: Date.now(), text: draft.trim(), tier: draftTier, tag: draftTag, ts: new Date().toISOString() };
    saveNotes([note, ...notes]);
    setDraft("");
  }, [draft, draftTier, draftTag, notes, saveNotes]);

  const deleteNote = useCallback((id) => {
    saveNotes(notes.filter(n => n.id !== id));
  }, [notes, saveNotes]);

  const tags = ["general", "physics", "governance", "logistics", "verification", "outreach"];
  const filtered = filter === "all" ? notes : notes.filter(n => n.tag === filter || n.tier === filter);

  if (!loaded) return <div style={{ color:"#6a6a7a", padding: 20 }}>Loading notes...</div>;

  return (
    <div>
      <div style={{ marginBottom: 16, padding:"16px", background:"#0d0d14", borderRadius: 6, border:"1px solid #1a1a2e" }}>
        <textarea ref={textareaRef} value={draft} onChange={e => setDraft(e.target.value)} onKeyDown={e => { if (e.key === "Enter" && e.metaKey) addNote(); }} placeholder="Add a note... (⌘+Enter to save)" style={{ width:"100%", minHeight: 72, padding: 12, background:"#08080e", border:"1px solid #1a1a2e", borderRadius: 4, color:"#c0c0cc", fontSize: 13, fontFamily:"inherit", lineHeight: 1.6, resize:"vertical", outline:"none", boxSizing:"border-box" }} />
        <div style={{ display:"flex", alignItems:"center", gap: 8, marginTop: 8, flexWrap:"wrap" }}>
          <span style={{ fontSize: 11, color:"#5a5a6a" }}>Tier:</span>
          {Object.entries(TIERS).map(([k,v]) => (
            <button key={k} onClick={() => setDraftTier(k)} style={{ padding:"2px 8px", borderRadius: 3, border:`1px solid ${draftTier===k ? v.color : "#1a1a2e"}`, background: draftTier===k ? v.bg : "transparent", color: draftTier===k ? v.color : "#5a5a6a", fontSize: 10, cursor:"pointer", fontFamily:"inherit", textTransform:"uppercase" }}>{v.label}</button>
          ))}
          <span style={{ fontSize: 11, color:"#5a5a6a", marginLeft: 8 }}>Tag:</span>
          <select value={draftTag} onChange={e => setDraftTag(e.target.value)} style={{ padding:"3px 8px", background:"#08080e", border:"1px solid #1a1a2e", borderRadius: 3, color:"#8a8a9a", fontSize: 11, fontFamily:"inherit" }}>
            {tags.map(t => <option key={t} value={t}>{t}</option>)}
          </select>
          <button onClick={addNote} disabled={!draft.trim()} style={{ marginLeft:"auto", padding:"5px 16px", background: draft.trim() ? "#1a2533" : "#0d0d14", border:"1px solid", borderColor: draft.trim() ? "#42A5F5" : "#1a1a2e", borderRadius: 4, color: draft.trim() ? "#42A5F5" : "#3a3a4a", fontSize: 12, cursor: draft.trim() ? "pointer" : "default", fontFamily:"inherit", fontWeight: 600 }}>Save</button>
        </div>
      </div>
      <div style={{ display:"flex", gap: 4, marginBottom: 12, flexWrap:"wrap" }}>
        <button onClick={() => setFilter("all")} style={{ padding:"3px 10px", borderRadius: 3, border:`1px solid ${filter==="all" ? "#42A5F5" : "#1a1a2e"}`, background: filter==="all" ? "#1a2533" : "transparent", color: filter==="all" ? "#42A5F5" : "#5a5a6a", fontSize: 11, cursor:"pointer", fontFamily:"inherit" }}>All ({notes.length})</button>
        {tags.map(t => {
          const c = notes.filter(n => n.tag === t).length;
          return c > 0 ? <button key={t} onClick={() => setFilter(t)} style={{ padding:"3px 10px", borderRadius: 3, border:`1px solid ${filter===t ? "#42A5F5" : "#1a1a2e"}`, background: filter===t ? "#1a2533" : "transparent", color: filter===t ? "#42A5F5" : "#5a5a6a", fontSize: 11, cursor:"pointer", fontFamily:"inherit" }}>{t} ({c})</button> : null;
        })}
      </div>
      {filtered.length === 0 ? (
        <div style={{ padding: 40, textAlign:"center", color:"#3a3a4a", fontSize: 13 }}>
          {notes.length === 0 ? "No notes yet. Start documenting your understanding." : "No notes match this filter."}
        </div>
      ) : (
        <div style={{ display:"flex", flexDirection:"column", gap: 2 }}>
          {filtered.map(n => {
            const t = TIERS[n.tier];
            return (
              <div key={n.id} style={{ padding:"10px 14px", background:"#0d0d14", borderRadius: 4, borderLeft:`3px solid ${t.color}` }}>
                <div style={{ display:"flex", alignItems:"center", gap: 8, marginBottom: 6 }}>
                  <TierBadge tier={n.tier} small />
                  <span style={{ fontSize: 10, padding:"1px 6px", borderRadius: 2, background:"#12121e", color:"#6a6a7a", border:"1px solid #1a1a2e" }}>{n.tag}</span>
                  <span style={{ fontSize: 10, color:"#3a3a4a", marginLeft:"auto", fontFamily:"'JetBrains Mono', monospace" }}>{new Date(n.ts).toLocaleDateString()}</span>
                  <button onClick={(e) => { e.stopPropagation(); deleteNote(n.id); }} style={{ background:"none", border:"none", color:"#3a3a4a", cursor:"pointer", fontSize: 14, padding:"0 4px", fontFamily:"inherit" }} title="Delete">×</button>
                </div>
                <p style={{ fontSize: 13, color:"#b0b0be", lineHeight: 1.6, margin: 0, whiteSpace:"pre-wrap" }}>{n.text}</p>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

const VIEWS = { layers: LayersView, axioms: AxiomsView, network: NetworkView, pgtc: PGTCView, logistics: LogisticsView, notes: NotesView };

export default function Dashboard() {
  const [tab, setTab] = useState("layers");
  const View = VIEWS[tab];
  return (
    <div style={{ fontFamily:"'Söhne', -apple-system, sans-serif", color:"#c0c0cc", minHeight:"100vh", padding: 0 }}>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&display=swap');
        @keyframes pulse { 0%,100% { opacity:1 } 50% { opacity:0.3 } }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        ::-webkit-scrollbar { width: 4px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #2a2a3e; border-radius: 2px; }
        ::selection { background: #42A5F544; }
      `}</style>
      <div style={{ borderBottom:"1px solid #1a1a2e", padding:"16px 20px", display:"flex", alignItems:"center", gap: 14 }}>
        <div>
          <div style={{ fontSize: 15, fontWeight: 700, color:"#e0e0e8", letterSpacing: 0.3 }}>Quantum Stellarator</div>
          <div style={{ fontSize: 11, color:"#4a4a5a", marginTop: 1 }}>Interactive research dashboard</div>
        </div>
        <div style={{ marginLeft:"auto", display:"flex", alignItems:"center", gap: 6 }}>
          <div style={{ width: 6, height: 6, borderRadius:"50%", background:"#4CAF50" }} />
          <span style={{ fontSize: 10, color:"#4a4a5a", fontFamily:"'JetBrains Mono', monospace" }}>GoS v3 — 144 theorems</span>
        </div>
      </div>
      <div style={{ display:"flex", gap: 1, padding:"8px 20px", borderBottom:"1px solid #1a1a2e", overflowX:"auto" }}>
        {TABS.map(t => (
          <button key={t.id} onClick={() => setTab(t.id)} style={{ padding:"7px 14px", borderRadius: 4, border:"1px solid", borderColor: tab===t.id ? "#2a2a3e" : "transparent", background: tab===t.id ? "#12121e" : "transparent", color: tab===t.id ? "#e0e0e8" : "#5a5a6a", fontSize: 12, cursor:"pointer", fontFamily:"inherit", fontWeight: tab===t.id ? 600 : 400, whiteSpace:"nowrap", transition:"all 0.15s" }}>
            {t.label}
          </button>
        ))}
      </div>
      <div style={{ padding:"20px", maxWidth: 860 }}>
        <View />
      </div>
      <div style={{ padding:"16px 20px", borderTop:"1px solid #0a0a10", marginTop: 20 }}>
        <div style={{ fontSize: 10, color:"#2a2a3a", textAlign:"center", lineHeight: 1.6 }}>
          Quantum Stellarator Cooperation Protocol v0.1 — Draft March 2026 — The compiler is the credential
        </div>
      </div>
    </div>
  );
}
