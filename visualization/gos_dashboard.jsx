import { useState } from "react";

const layers = [
  {
    id: "L5", name: "Verification", question: "How do we know it's real?",
    color: "#7C3AED", colorLight: "#EDE9FE", files: [],
    docs: [
      { name: "MZM Certification Architecture", status: "needs update", desc: "Three-gate protocol: gap certification, strain invariance, NV-transport consistency. Strain as Cl(2,0) rotor transformation." },
      { name: "Thermodynamic Bootstrap", status: "needs update", desc: "5kW fridge vs 22MW supercomputer. TAS dialectic. Red/blue team. Structural XAI. DO-254 aerospace precedent." },
      { name: "Majorana Research Brief", status: "current", desc: "Station Q history, Majorana 1, 2018 retraction, 2025 Nature caveats, TGP false-positive challenge, DARPA US2QC." }
    ],
    concepts: [
      { term: "TAS Dialectic", def: "Thesis (simulation) \u2192 Antithesis (type checker rejects) \u2192 Synthesis (hidden assumption surfaced). v1\u2192v2\u2192v3 IS a TAS loop. Stage 1 FAIL is the latest antithesis." },
      { term: "Three-Gate Protocol", def: "Gate 1: gap certification (IsGappedAt). Gate 2: strain invariance (ZBCP pinned within \u0394_topo/10). Gate 3: NV-transport consistency (T\u2081 minimum = gap closing). All must pass." },
      { term: "Majorana vs Andreev Crisis", def: "ABS, YSR, quasi-MZMs mimic real MZMs. 2018 Nature retraction proved standard evidence insufficient. Three independent gates needed. No single measurement suffices." },
      { term: "Topological Gap Protocol", def: "Microsoft's TGP challenged by Legg (Basel, 2025) for false positives. Not in the Nature paper. Your certification architecture addresses gaps in their framework." },
      { term: "Structural XAI", def: "AI outputs verified by type checker at generation, not explained post-hoc. Lean kernel doesn't care who wrote the proof. Type-checks = explanation. Error = precise localization of failure." },
      { term: "DO-254 Precedent", def: "Aerospace flight-critical verification. SEU bit-flips = quasiparticle poisoning. Hardware-in-the-loop finds <4% of deep bugs. Formal verification required for the rest." }
    ],
    theorems: 0, sorry: 0
  },
  {
    id: "L4", name: "Device", question: "What do we build?",
    color: "#2563EB", colorLight: "#DBEAFE", files: [],
    docs: [
      { name: "FWS Engineering Spec", status: "needs update", desc: "Si-28 / C-12 diamond / Penrose graphene / Nb / He-3/4. Five layers, each addressing one physical requirement. Needs PGTC, BdG bridge, ratchet chirality." },
      { name: "FWS Simulation Roadmap", status: "needs update", desc: "7 stages, gated. Stage 0 (1D) PASS. Stage 1 (2D) FAIL\u2014wrong lattice. Stages 3\u20137 require HPC. Needs diagnosis update." }
    ],
    concepts: [
      { term: "Fractonic Weyl Semimetal", def: "Target phase: fractons + Weyl chirality. Ground state = analog Kodama wavefunction. SPECULATIVE\u2014depends on Stage 6 fracton diagnostics." },
      { term: "Material Stack", def: "L1: Si-28 (\u226599.995%, spin silence). L2: C-12 diamond (phonon decoupling). L3: Penrose graphene (curvature). L4: Nb (proximity SC). L5: He-3/He-4 (tuning)." },
      { term: "Stage 1 FAIL", def: "Penrose vertex lattice: t_max/t_min=6.85\u00D7, \u03B4t=59%. Physical graphene+SW: \u00B15-8%. Past Aubry-Andr\u00E9 threshold. Wrong lattice, not wrong physics." },
      { term: "Proximity Effect", def: "Nb contacts induce pairing \u0394 in graphene. Stage 5 tests if gap survives at 5/7 defect sites. If \u0394 suppressed where MZMs should live = fatal mismatch." }
    ],
    theorems: 0, sorry: 0
  },
  {
    id: "L3", name: "Physics", question: "What does the math predict?",
    color: "#059669", colorLight: "#D1FAE5",
    files: [
      { name: "ratchet_full.py", type: "python", status: "PASS", desc: "1D: w=1, 2 MZMs at |E|\u224810\u207B\u00B9\u2074, 99.7% edge, \u03BC\u2208[0,1.95t\u2080], \u03BA ratio 0.86, 5\u00D7 safety margin." },
      { name: "penrose_bdg_2d.py", type: "python", status: "FAIL", desc: "2D Stage 1: 476 vertices, 0 zero modes, Bott\u22480. \u03B4t/t\u2080=59.3%. Wrong lattice." },
      { name: "penrose_phonon_2d.py", type: "python", status: "PARTIAL", desc: "2D Stage 2: \u03BA=0.92. Min \u03BE/L=0.042, 2 localized modes, spectral gaps visible." },
      { name: "run_all.py", type: "python", status: "ok", desc: "Runner for stages 1+2." }
    ],
    docs: [
      { name: "Quasiperiodic Ratchet Thesis", status: "needs v4", desc: "Needs: ascending ladder, PGTC, 1D DEMONSTRATED, Stage 1 antithesis, TAS framing." },
      { name: "Topological Invariants as Dependent Types", status: "mostly stable", desc: "IsGapped \u2192 \u2124. Phase transition as type error. Three-layer architecture." }
    ],
    concepts: [
      { term: "BdG Hamiltonian", def: "2N\u00D72N matrix in Nambu space. Normal hopping + superconducting pairing. Built-in particle-hole symmetry \u2192 AZ classes supporting topology." },
      { term: "Winding Number w=1", def: "W=(1/2\u03C0)\u222Ed\u03B8. Integer from closed curve. w=1 = one unpaired Majorana per boundary. DERIVED from Cl(2,0) rotor phase." },
      { term: "PGTC", def: "Phonon Glass Topological Crystal. Same modulation: electrons 9.7% (extended, carry topology) + phonons 19.3% (scattered, glass-like \u03BA). Self-protecting." },
      { term: "Harrison Scaling", def: "t(x)=t\u2080(d\u2080/d(x))\u00B2. Springs: k\u221Dd\u207B\u2074. This asymmetry IS the PGTC mechanism." },
      { term: "Kitaev Chain", def: "H=-\u03BCc\u2020c - t(c\u2020c+h.c.) + \u0394(cc+h.c.). Topological when |\u03BC|<2t. Simplest MZM host." },
      { term: "Aubry-Andr\u00E9", def: "t_i=t\u2080(1+\u03B4t cos(2\u03C0i/\u03C6\u00B2)). Localization at \u03B4t=1. Physical=9.7%, safe. 2D Penrose=59.3%, past threshold." },
      { term: "Phonon Glass Mechanism", def: "Quasicrystals: low \u03BA despite sharp diffraction. Not disorder\u2014excess of structure. \u03C6 has slowest converging continued fraction." }
    ],
    theorems: 0, sorry: 0
  },
  {
    id: "L2", name: "Classification", question: "Which topological phase?",
    color: "#D97706", colorLight: "#FEF3C7",
    files: [
      { name: "AlgebraicLadder.lean", type: "lean", status: "0 sorry", desc: "13 thm. Ascending ladder, AZ tenfold (all 10 classes), Bott periodicity, domain walls, conditional MZM theorem." },
      { name: "KitaevChain.lean", type: "lean", status: "0 sorry", desc: "35 thm. Phase boundary (7), bulk-boundary (23), universal \u2200N\u22652 (5)." },
      { name: "EdgeModes.lean", type: "lean", status: "0 sorry", desc: "33 thm. Inductive BBC, migration, scan to N=50. Fixed: Float.min, list_any_append, leftEdge proof." },
      { name: "Bridge.lean", type: "lean", status: "0 sorry", desc: "9 thm, 21 axioms. Pipeline, conservation laws (winding, knot, helicity)." },
      { name: "FWS.lean", type: "lean", status: "0 sorry", desc: "22 thm. Curvature algebra, AZ class D, SW defects, PGTC, Chern-Simons, Kodama." }
    ],
    docs: [],
    concepts: [
      { term: "Altland-Zirnbauer", def: "10 symmetry classes. T (time-reversal), C (particle-hole), S (chiral). Period 2 (complex) + period 8 (real) = Bott periodicity = Clifford periodicity." },
      { term: "Class D", def: "Kitaev chain. C\u00B2=+1, no T, no S. d=1: \u2124/2 (fermion parity). d=2: \u2124 (Chern). The winding number mod 2 determines MZM." },
      { term: "Ascending Ladder", def: "\u211D\u2192\u2102: ordering\u2192rotation. \u2102\u2192\u210D: commutativity\u2192spin. \u210D\u2192\uD835\uDD46: associativity\u2192gauge. Every loss is a birth. MZM = witness of emergence." },
      { term: "Bulk-Boundary Correspondence", def: "Winding number (bulk) = edge modes (boundary). This IS the index theorem. Proved \u2200N\u22652 by structural induction." },
      { term: "Index Theorem", def: "Atiyah-Singer: analytical index = topological index. left_edge_always_free IS an instance. Gapped = Fredholm = index defined. Gap closes = not Fredholm = type error." },
      { term: "Domain Wall", def: "Boundary between phases with different invariants. MZM lives here. wallIsTopological in AlgebraicLadder.lean." },
      { term: "Conditional MZM", def: "if_conjecture_then_MZM: IF 5/7 maps to AI\u2192D, THEN wall is topological. Proved by decide. Antecedent needs Hamiltonian computation." },
      { term: "Fermion Parity", def: "w mod 2. Even=paired (trivial). Odd=unpaired MZM (topological). The \u2124/2 clock." }
    ],
    theorems: 112, sorry: 0
  },
  {
    id: "L1", name: "Algebra", question: "What are the structures?",
    color: "#DC2626", colorLight: "#FEE2E2",
    files: [
      { name: "Clifford.lean", type: "lean", status: "0 sorry", desc: "12 thm. Cl(2,0), Cl(3,0), gap condition, edge modes (3-site), MHD, protection hierarchy." },
      { name: "CayleyDickson.lean", type: "lean", status: "0 sorry", desc: "3 thm. Octonion non-associativity. Top of the algebraic ladder." },
      { name: "Winding.lean", type: "lean", status: "ok", desc: "Definitions only. Cl(1,0), Cl(2,0), rotors, winding number computation." },
      { name: "CLHoTT.lean", type: "lean", status: "6 sorry", desc: "7 thm. Dagger category. FROZEN\u2014Float ring lemmas. Fix: \u2124/\u211A or Agda." }
    ],
    docs: [],
    concepts: [
      { term: "Cl(2,0)", def: "4D: {1,e\u2081,e\u2082,e\u2081\u2082}. Three rules: signature, anticommutativity, associativity. e\u2081\u2082\u00B2=-1 DERIVED. Imaginary unit from geometry." },
      { term: "Cl(3,0)", def: "8D. Even subalgebra \u2245 quaternions. 64-term product. 3D rotors by sandwich product." },
      { term: "IsGappedAt", def: "Proof obligation: bivector magnitude \u2260 0. Without proof, safeBivectorInv uncallable. Phase transition = absent proof term." },
      { term: "Rotor", def: "R=cos(\u03B8/2)+sin(\u03B8/2)\u00B7e\u2081\u2082. Factor of \u00BD IS the spinor double cover. 360\u00B0=sign flip, 720\u00B0=identity." },
      { term: "Clifford-Majorana Isomorphism", def: "\u03B3\u1D62\u03B3\u2C7C=-\u03B3\u2C7C\u03B3\u1D62, \u03B3\u1D62\u00B2=1. These ARE Cl(n,0) relations. Not analogy\u2014isomorphism." },
      { term: "Dagger Category", def: "Category with involution \u2020. rev on rotors. This IS CQM (Abramsky-Coecke). Quantum processes = morphisms in dagger compact categories." },
      { term: "Berry Phase", def: "Geometric phase from adiabatic evolution. Berry curvature = effective B-field in k-space. Integral = Chern number. Winding number is the 1D instance." }
    ],
    theorems: 22, sorry: 6
  },
  {
    id: "L0", name: "Foundations", question: "What can we prove?",
    color: "#6B7280", colorLight: "#F3F4F6",
    files: [
      { name: "Agda/README.md", type: "agda", status: "planned", desc: "Three imports: Foundations.Everything, HITs.S1, Homotopy.Loopspace. Targets: \u03C0\u2081(S\u00B9)\u2245\u2124, winding number, Univalence." }
    ],
    docs: [],
    concepts: [
      { term: "Lean 4", def: "v4.12.0. Zero Mathlib. Kernel checks everything. Handles algebraic/decidable: rfl, native_decide, decide, omega." },
      { term: "Cubical Agda", def: "HoTT-native. Univalence built-in. Paths proof-relevant. Three imports give you everything TopologicalBridge axiomatizes." },
      { term: "Dependent Types", def: "(hGap : IsGapped H) \u2192 \u2124. Can only compute integer if you PROVE gap open. Compile-time guarantee, not runtime check." },
      { term: "Higher Inductive Types", def: "S\u00B9 = base + loop. In Lean: axiom. In Agda: definition with computational content. Can pattern match on loop." },
      { term: "Univalence", def: "(A \u2243 B) \u2243 (A \u2261 B). Equivalent types identical. Promotes succ:\u2124\u2243\u2124 to path. Essential for \u03C0\u2081(S\u00B9)\u2245\u2124." },
      { term: "Universal Cover", def: "cover:S\u00B9\u2192Type, cover(base)=\u2124, transport along loop = successor. HOW \u03C0\u2081(S\u00B9)\u2245\u2124 is proved." },
      { term: "Two-Prover Strategy", def: "Lean: algebra. Agda: homotopy. Bridge: both express IsGapped H \u2192 \u2124." }
    ],
    theorems: 0, sorry: 0
  }
];

const crossCutting = [
  { term: "Singularity = Type Error", def: "THE CORE CLAIM. IsGappedAt fails \u2192 safeBivectorInv uncallable \u2192 winding number untypeable. Proved L1, classified L2, computed L3, applied L4, certified L5. Each layer adds content.", layer: "core" },
  { term: "Category Theory", def: "You're already doing it. ProtectionLevel = discrete category. bottSucc = endofunctor. classifyDim1 = functor. rev = dagger = CQM. The vocabulary names what you built.", layer: "meta" },
  { term: "Index Theorem", def: "Atiyah-Singer: zero modes = winding number. left_edge_always_free IS an instance. gapless_blocks_inversion = non-Fredholm has no index. In three lines.", layer: "meta" },
  { term: "Sheaf Theory", def: "Local invariants on parameter patches gluing consistently. Relevant for 2D (different patches, different phases, MZMs at boundaries). Don't need the formalism yet.", layer: "future" },
  { term: "Ascending Interpretation", def: "Same formal structure, different reading. ascend is primary; descent derived. Standard: property lost. Ascending: constraint traded for capability. MZM = witness of emergence, not breakdown.", layer: "core" },
  { term: "TAS Across Versions", def: "v1: construction + gap. v2: gap = type error. v3: gap filled (1D). Stage 1: antithesis (wrong lattice). Next: synthesis (corrected lattice). Each version more honest.", layer: "meta" },
];

const problems = [
  { p: 1, name: "Corrected 2D lattice", desc: "Graphene grid + Penrose-seeded SW defects (\u03B4t\u224810%). Re-run Stage 1. The most important next computation." },
  { p: 2, name: "AZ classification", desc: "Formally show 5/7 \u2192 AI\u2192D. Conditional theorem proved; antecedent needs this." },
  { p: 3, name: "Cubical Agda", desc: "\u03C0\u2081(S\u00B9)\u2245\u2124 proved. Winding with content. TopologicalBridge axioms \u2192 theorems." },
  { p: 4, name: "Float sorry", desc: "CLHoTT to \u2124/\u211A (ring tactic) or Agda. 6 sorry, one root cause." },
  { p: 5, name: "Document updates", desc: "Thesis v4, White Paper v3, spec, roadmap, certification, bootstrap." },
  { p: 6, name: "2D phonon glass", desc: "Dynamical matrix on corrected lattice. Target \u03BA<0.5. Currently 0.92." },
];

const sc = { "PASS":"#059669","FAIL":"#DC2626","PARTIAL":"#D97706","0 sorry":"#059669","6 sorry":"#D97706","ok":"#6B7280","planned":"#6B7280","needs update":"#D97706","needs v4":"#DC2626","mostly stable":"#059669","current":"#059669" };
const Badge = ({s}) => <span className="inline-block px-2 py-0.5 rounded-full text-xs font-semibold text-white" style={{backgroundColor:sc[s]||"#6B7280"}}>{s}</span>;

export default function App() {
  const [sel, setSel] = useState(null);
  const [exp, setExp] = useState(new Set());
  const [view, setView] = useState("architecture");
  const [search, setSearch] = useState("");
  const tog = k => setExp(p => { const n = new Set(p); n.has(k)?n.delete(k):n.add(k); return n; });
  const all = [...layers.flatMap(l => l.concepts.map(c => ({...c, lid: l.id, lc: l.color}))), ...crossCutting.map(c => ({...c, lid: c.layer==="core"?"CORE":c.layer==="future"?"NEXT":"META", lc: c.layer==="core"?"#DC2626":c.layer==="future"?"#6B7280":"#1E293B"}))];
  const filt = search ? all.filter(c => c.term.toLowerCase().includes(search.toLowerCase())||c.def.toLowerCase().includes(search.toLowerCase())) : all;
  const act = layers.find(l => l.id === sel);

  return (
    <div className="min-h-screen" style={{backgroundColor:"#0F172A",color:"#E2E8F0"}}>
      <div className="border-b" style={{borderColor:"#1E293B"}}>
        <div className="max-w-6xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between flex-wrap gap-2">
            <div>
              <h1 className="text-2xl font-bold" style={{color:"#F8FAFC"}}>Geometry of State</h1>
              <p className="text-sm mt-1" style={{color:"#94A3B8"}}>Systems Architecture \u00B7 147 theorems \u00B7 7 sorry \u00B7 L0\u2013L5 \u00B7 8 documents</p>
            </div>
            <div className="flex gap-1">
              {["architecture","glossary","problems"].map(v => (
                <button key={v} onClick={()=>setView(v)} className="px-3 py-1.5 rounded text-sm font-medium" style={{backgroundColor:view===v?"#334155":"transparent",color:view===v?"#F8FAFC":"#94A3B8"}}>
                  {v==="architecture"?"Architecture":v==="glossary"?"Glossary":"Problems"}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
      <div className="max-w-6xl mx-auto px-4 py-6">
        {view==="architecture"&&(
          <div className="flex gap-6 flex-col lg:flex-row">
            <div className="lg:w-80 flex-shrink-0 space-y-2">
              {layers.map(l=>(
                <button key={l.id} onClick={()=>setSel(sel===l.id?null:l.id)} className="w-full text-left rounded-lg p-3 transition-all" style={{backgroundColor:sel===l.id?l.colorLight:"#1E293B",borderLeft:`4px solid ${l.color}`}}>
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold" style={{color:sel===l.id?l.color:"#94A3B8"}}>{l.id}</span>
                    <div className="flex gap-2">{l.theorems>0&&<span className="text-xs" style={{color:"#64748B"}}>{l.theorems} thm</span>}{l.sorry>0&&<span className="text-xs" style={{color:"#D97706"}}>{l.sorry} sorry</span>}</div>
                  </div>
                  <div className="font-semibold text-sm" style={{color:sel===l.id?"#1F2937":"#E2E8F0"}}>{l.name}</div>
                  <div className="text-xs mt-0.5" style={{color:sel===l.id?"#6B7280":"#64748B"}}>{l.question}</div>
                </button>
              ))}
              <div className="mt-2 text-center text-xs" style={{color:"#64748B"}}>\u2191 each layer imports from below \u2191</div>
              <div className="mt-2 rounded-lg p-3" style={{backgroundColor:"#1E293B",border:"1px solid #334155"}}>
                <div className="text-xs font-bold mb-1" style={{color:"#F59E0B"}}>CORE CLAIM</div>
                <div className="text-sm" style={{color:"#E2E8F0"}}>Singularities are type errors.</div>
                <div className="mt-2 text-xs" style={{color:"#64748B"}}>Proved L1 \u00B7 Classified L2 \u00B7 Computed L3 \u00B7 Applied L4 \u00B7 Certified L5</div>
              </div>
              <div className="rounded-lg p-3" style={{backgroundColor:"#1E293B",border:"1px solid #334155"}}>
                <div className="text-xs font-bold mb-1" style={{color:"#059669"}}>ASCENDING LADDER</div>
                <div className="text-xs space-y-1" style={{color:"#94A3B8"}}>
                  <div>\u211D\u2192\u2102: ordering \u2192 <span style={{color:"#E2E8F0"}}>rotation</span></div>
                  <div>\u2102\u2192\u210D: commutativity \u2192 <span style={{color:"#E2E8F0"}}>spin</span></div>
                  <div>\u210D\u2192\uD835\uDD46: associativity \u2192 <span style={{color:"#E2E8F0"}}>gauge</span></div>
                </div>
                <div className="mt-2 text-xs" style={{color:"#64748B"}}>Every loss is a birth.</div>
              </div>
            </div>
            <div className="flex-1 min-w-0">
              {!act?(
                <div className="rounded-lg p-6" style={{backgroundColor:"#1E293B"}}>
                  <h2 className="text-lg font-bold mb-4" style={{color:"#F8FAFC"}}>Select a layer to explore</h2>
                  <div className="grid grid-cols-2 gap-3 text-sm">
                    {[["134","Active theorems","#059669"],["7","Sorry (Float)","#D97706"],["9","Lean files","#2563EB"],["8","Documents","#7C3AED"],["4","Python scripts","#059669"],["6","Open problems","#DC2626"]].map(([v,l,c])=>(
                      <div key={l} className="rounded p-3" style={{backgroundColor:"#0F172A"}}><div className="font-bold" style={{color:c}}>{v}</div><div style={{color:"#94A3B8"}}>{l}</div></div>
                    ))}
                  </div>
                </div>
              ):(
                <div className="space-y-4">
                  <div className="rounded-lg p-4" style={{backgroundColor:"#1E293B"}}>
                    <div className="flex items-center gap-3">
                      <div className="w-12 h-12 rounded-lg flex items-center justify-center font-bold text-white text-lg" style={{backgroundColor:act.color}}>{act.id}</div>
                      <div><h2 className="text-lg font-bold" style={{color:"#F8FAFC"}}>{act.name}</h2><p className="text-sm" style={{color:"#94A3B8"}}>{act.question}</p></div>
                    </div>
                  </div>
                  {act.files.length>0&&<div><h3 className="text-sm font-bold mb-2 px-1" style={{color:"#94A3B8"}}>FILES</h3><div className="space-y-2">{act.files.map((f,i)=>(
                    <div key={i} className="rounded-lg p-3" style={{backgroundColor:"#1E293B"}}><div className="flex items-center justify-between mb-1"><span className="font-mono text-sm" style={{color:"#E2E8F0"}}>{f.name}</span><Badge s={f.status}/></div><p className="text-xs" style={{color:"#94A3B8"}}>{f.desc}</p></div>
                  ))}</div></div>}
                  {act.docs.length>0&&<div><h3 className="text-sm font-bold mb-2 px-1" style={{color:"#94A3B8"}}>DOCUMENTS</h3><div className="space-y-2">{act.docs.map((d,i)=>(
                    <div key={i} className="rounded-lg p-3" style={{backgroundColor:"#1E293B"}}><div className="flex items-center justify-between mb-1"><span className="text-sm font-semibold" style={{color:"#E2E8F0"}}>{d.name}</span><Badge s={d.status}/></div><p className="text-xs" style={{color:"#94A3B8"}}>{d.desc}</p></div>
                  ))}</div></div>}
                  {act.concepts.length>0&&<div><h3 className="text-sm font-bold mb-2 px-1" style={{color:"#94A3B8"}}>CONCEPTS</h3><div className="space-y-2">{act.concepts.map((c,i)=>{const k=`${act.id}-${i}`;return(
                    <div key={k} className="rounded-lg p-3 cursor-pointer" style={{backgroundColor:"#1E293B"}} onClick={()=>tog(k)}><div className="flex items-center justify-between"><span className="text-sm font-semibold" style={{color:"#E2E8F0"}}>{c.term}</span><span style={{color:"#64748B"}}>{exp.has(k)?"\u25BC":"\u25B6"}</span></div>{exp.has(k)&&<p className="mt-2 text-sm leading-relaxed" style={{color:"#94A3B8"}}>{c.def}</p>}</div>
                  );})}</div></div>}
                </div>
              )}
            </div>
          </div>
        )}
        {view==="glossary"&&(
          <div>
            <input type="text" placeholder="Search concepts..." value={search} onChange={e=>setSearch(e.target.value)} className="w-full rounded-lg px-4 py-2 text-sm outline-none mb-4" style={{backgroundColor:"#1E293B",color:"#E2E8F0",border:"1px solid #334155"}}/>
            <div className="space-y-2">{filt.map((c,i)=>{const k=`g-${i}`;return(
              <div key={k} className="rounded-lg p-3 cursor-pointer" style={{backgroundColor:"#1E293B"}} onClick={()=>tog(k)}>
                <div className="flex items-center justify-between"><div className="flex items-center gap-2"><span className="text-xs font-bold px-1.5 py-0.5 rounded" style={{backgroundColor:c.lc+"22",color:c.lc}}>{c.lid}</span><span className="text-sm font-semibold" style={{color:"#E2E8F0"}}>{c.term}</span></div><span style={{color:"#64748B"}}>{exp.has(k)?"\u25BC":"\u25B6"}</span></div>
                {exp.has(k)&&<p className="mt-2 text-sm leading-relaxed" style={{color:"#94A3B8"}}>{c.def}</p>}
              </div>
            );})}</div>
          </div>
        )}
        {view==="problems"&&(
          <div className="space-y-3">
            <h2 className="text-lg font-bold mb-2" style={{color:"#F8FAFC"}}>Open Problems</h2>
            {problems.map(pr=>(
              <div key={pr.p} className="rounded-lg p-4" style={{backgroundColor:"#1E293B"}}>
                <div className="flex items-center gap-3 mb-2">
                  <div className="w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm" style={{backgroundColor:pr.p<=2?"#DC2626":pr.p<=4?"#D97706":"#6B7280",color:"white"}}>{pr.p}</div>
                  <span className="font-semibold" style={{color:"#F8FAFC"}}>{pr.name}</span>
                </div>
                <p className="text-sm ml-11" style={{color:"#94A3B8"}}>{pr.desc}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
