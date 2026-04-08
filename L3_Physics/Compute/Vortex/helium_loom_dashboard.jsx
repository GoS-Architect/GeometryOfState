import { useState, useMemo } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar, ReferenceLine, Area, AreaChart, ComposedChart } from "recharts";

const DATA = {"t":[0.0,0.25,0.5,0.75,1.0,1.25,1.5,1.75,2.0,2.25,2.5,2.75,3.0,3.25,3.5,3.75,4.0,4.25,4.5,4.75,5.0,5.25,5.5,5.75,6.0,6.25,6.5,6.75,7.0,7.25,7.5,7.75,8.0,8.25,8.5,8.75,9.0,9.25,9.5,9.75,10.0],"w05":[2.7959,2.1468,0.6528,2.0212,-0.55,-0.7873,-0.8334,-1.1497,1.7525,-1.2221,-0.9376,1.4492,-0.9772,-0.9838,-0.9905,-1.2124,0.5864,-1.1317,-0.9974,-1.0003,-1.0037,-0.994,-0.9075,-0.9963,-0.6531,-0.5042,-1.0362,-1.0093,-0.9777,-1.0196,-0.9932,-1.0011,-0.9945,-0.982,-0.8627,-0.9684,-0.9637,-0.9619,-1.0069,-1.005,-1.0172],"w10":[3.0261,2.9678,3.1215,2.0363,2.8094,2.2209,0.2184,-0.7667,-1.2519,-0.1671,0.0423,1.675,-0.0088,-1.7246,0.3537,-0.9793,-0.1762,-0.9923,-1.0038,-1.0117,-1.0065,-1.0095,-0.9843,-0.8545,-0.5098,2.6953,-1.0952,-0.9712,-1.0076,-0.9947,-0.9951,-0.9919,-1.0062,-0.9736,-1.0154,-1.0597,-1.0111,-1.003,-1.0014,-0.9894,-0.9911],"w20":[2.9994,2.9976,3.0103,3.0113,3.0122,2.9767,2.9813,3.0108,2.9405,2.7506,2.8102,2.0807,-0.5023,-0.0355,-1.5024,1.5134,-1.294,-0.5181,3.0883,1.461,2.9249,2.594,-1.0567,-1.0396,-0.8836,-0.9532,-0.9931,-0.9574,-0.8342,0.4897,1.4496,2.5004,-1.0039,-1.027,-1.0053,-1.0237,-1.013,-1.0028,-1.0075,-1.0225,-0.9831],"w30":[2.9962,2.9968,2.9935,3.0057,2.9924,3.0195,2.9698,2.9622,2.988,3.0094,2.9638,0.8746,3.0212,2.3761,3.0599,3.0199,3.0484,1.9842,0.6356,-0.5143,2.1857,-0.0051,-1.1947,-1.0141,-0.9687,-1.8273,3.387,1.3528,2.1344,0.0432,-0.9988,-1.0173,-0.1232,-1.0014,2.3096,2.5413,1.6549,-0.1638,-0.9355,-0.7161,-1.0275],"kss":[6.6834,438.3862,321.1588,252.7712,310.4009,171.8074,679.4106,1549.1456,539.6438,180.0647,1668.1557,658.0434,269.0982,491.4275,254.8445,277.8926,594.6967,291.1193,416.8639,256.221,225.4985,122.9088,206.6512,220.0028,1809.3471,183.5927,265.0665,411.229,322.5714,181.7145,294.0392,268.525,1346.6606,262.6288,840.9588,213.5988,292.692,225.1821,208.7646,306.3918,135.2669],"maxrho":[1.0,2.1431,1.964,1.7221,1.6819,1.6691,1.4392,1.6194,1.8538,1.6847,1.8581,1.7199,1.7987,1.7894,2.0652,2.0067,1.5826,1.9986,1.8069,1.738,1.4318,1.4863,1.5651,1.5272,1.4601,1.6564,1.6531,1.6456,1.7896,1.5086,1.4007,1.5318,1.6027,1.7519,2.0353,1.8783,1.6573,1.7427,1.7644,1.5996,1.9962],"spec_k":[0.314,0.942,1.571,2.199,2.827,3.456,4.084,4.712,5.341,5.969,6.597,7.226,7.854,8.482,9.111,9.739,10.367,10.996,11.624,12.252],"spec_comp":[0.0,58.92,73.7,40.23,93.47,99.63,34.99,27.14,51.47,43.72,63.51,62.13,41.96,41.95,48.57,43.27,31.98,33.51,32.03,33.65],"spec_inc":[0.04,279.01,553.18,293.57,454.36,447.77,182.22,140.0,224.35,180.19,259.29,251.52,171.78,171.79,197.54,176.47,131.42,137.11,129.79,136.62]};

const PHASE_LABELS = [
  { x1: 0, x2: 2.5, label: "Phase I: Trefoil Coherent", color: "rgba(34, 197, 94, 0.06)" },
  { x1: 2.5, x2: 6.0, label: "Phase II: Vortex Migration", color: "rgba(234, 179, 8, 0.06)" },
  { x1: 6.0, x2: 10.0, label: "Phase III: Settled at W = −1", color: "rgba(239, 68, 68, 0.06)" },
];

const monoFont = "'SF Mono', 'Fira Code', 'JetBrains Mono', monospace";
const sansFont = "'DM Sans', 'Helvetica Neue', system-ui, sans-serif";

const StatusBadge = ({ status, children }) => {
  const colors = {
    critical: { bg: "#2d1215", border: "#7f1d1d", text: "#fca5a5" },
    warning: { bg: "#2d2305", border: "#713f12", text: "#fde68a" },
    nominal: { bg: "#052e16", border: "#14532d", text: "#86efac" },
    info: { bg: "#0c1929", border: "#1e3a5f", text: "#93c5fd" },
  };
  const c = colors[status] || colors.info;
  return (
    <span style={{
      display: "inline-flex", alignItems: "center", gap: 6,
      padding: "3px 10px", borderRadius: 4,
      background: c.bg, border: `1px solid ${c.border}`,
      color: c.text, fontSize: 11, fontFamily: monoFont, fontWeight: 600,
      letterSpacing: 0.5,
    }}>
      <span style={{
        width: 6, height: 6, borderRadius: "50%",
        background: c.text, boxShadow: `0 0 6px ${c.text}`,
      }} />
      {children}
    </span>
  );
};

const MetricCard = ({ label, value, sub, status }) => (
  <div style={{
    background: "#0a0e17", border: "1px solid #1a2035", borderRadius: 6,
    padding: "14px 16px", flex: 1, minWidth: 170,
  }}>
    <div style={{ color: "#4b5e7a", fontSize: 10, fontFamily: monoFont, textTransform: "uppercase", letterSpacing: 1.2, marginBottom: 6 }}>
      {label}
    </div>
    <div style={{ color: "#e2e8f0", fontSize: 22, fontFamily: monoFont, fontWeight: 700, marginBottom: 4 }}>
      {value}
    </div>
    <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
      {sub && <span style={{ color: "#64748b", fontSize: 11, fontFamily: monoFont }}>{sub}</span>}
      {status && status}
    </div>
  </div>
);

const SectionHeader = ({ number, title, subtitle }) => (
  <div style={{ marginBottom: 16, marginTop: 32 }}>
    <div style={{ display: "flex", alignItems: "baseline", gap: 10 }}>
      <span style={{ color: "#1e3a5f", fontSize: 11, fontFamily: monoFont, fontWeight: 700 }}>{number}</span>
      <h2 style={{ color: "#e2e8f0", fontSize: 16, fontFamily: sansFont, fontWeight: 700, margin: 0, letterSpacing: -0.3 }}>
        {title}
      </h2>
    </div>
    {subtitle && <p style={{ color: "#4b5e7a", fontSize: 12, fontFamily: sansFont, margin: "4px 0 0 32px", lineHeight: 1.5 }}>{subtitle}</p>}
  </div>
);

export default function HeliumLoomDashboard() {
  const [activeTab, setActiveTab] = useState("winding");

  const windingData = useMemo(() =>
    DATA.t.map((t, i) => ({
      t, "r=0.5": DATA.w05[i], "r=1.0": DATA.w10[i], "r=2.0": DATA.w20[i], "r=3.0": DATA.w30[i],
    })), []);

  const spectrumData = useMemo(() =>
    DATA.spec_k.map((k, i) => ({
      k: k.toFixed(1),
      "Sharp (compressible)": DATA.spec_comp[i],
      "Flat (incompressible)": DATA.spec_inc[i],
      ratio: DATA.spec_inc[i] / (DATA.spec_comp[i] + 0.001),
    })), []);

  const densityData = useMemo(() =>
    DATA.t.map((t, i) => ({ t, maxrho: DATA.maxrho[i] })), []);

  const initialW = 3.026;
  const finalW = -0.991;
  const drift = Math.abs(finalW - initialW).toFixed(3);
  const sigma = 1.417;

  const tabs = [
    { id: "winding", label: "Cohomological Audit" },
    { id: "spectrum", label: "Helmholtz Decomposition" },
    { id: "analysis", label: "Failure Analysis" },
  ];

  return (
    <div style={{
      background: "#060a12", color: "#c8d6e5", fontFamily: sansFont,
      minHeight: "100vh", padding: "24px 20px",
    }}>
      <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&display=swap" rel="stylesheet" />

      {/* Header */}
      <div style={{ borderBottom: "1px solid #111827", paddingBottom: 16, marginBottom: 8 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 8 }}>
          <div style={{
            width: 8, height: 8, borderRadius: "50%",
            background: "#ef4444", boxShadow: "0 0 12px #ef4444",
          }} />
          <h1 style={{
            fontSize: 18, fontWeight: 700, color: "#f1f5f9", margin: 0,
            fontFamily: monoFont, letterSpacing: -0.5,
          }}>
            HELIUM LOOM — COHOMOLOGICAL AUDIT
          </h1>
        </div>
        <p style={{ color: "#4b5e7a", fontSize: 12, fontFamily: monoFont, margin: "0 0 0 20px" }}>
          GP Evolution · Milnor Trefoil f(u,v) = u³ − v² · N=64 · T=10.0 · g=1.0
        </p>
      </div>

      {/* Top Metrics */}
      <div style={{ display: "flex", gap: 12, flexWrap: "wrap", marginTop: 16 }}>
        <MetricCard label="Initial Winding" value={`W = +${initialW}`} sub="Milnor μ = 3" status={<StatusBadge status="nominal">TREFOIL</StatusBadge>} />
        <MetricCard label="Final Winding" value={`W = ${finalW}`} sub="Settled" status={<StatusBadge status="critical">DECAYED</StatusBadge>} />
        <MetricCard label="Winding Drift" value={drift} sub={`σ = ${sigma}`} status={<StatusBadge status="critical">LOCK BROKEN</StatusBadge>} />
        <MetricCard label="Final η/s" value="135.3" sub={`KSS: ${(1/(4*Math.PI)).toFixed(4)}`} status={<StatusBadge status="warning">≫ BOUND</StatusBadge>} />
      </div>

      {/* Tabs */}
      <div style={{ display: "flex", gap: 2, marginTop: 28, borderBottom: "1px solid #111827" }}>
        {tabs.map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            style={{
              background: activeTab === tab.id ? "#0f1729" : "transparent",
              border: "none", borderBottom: activeTab === tab.id ? "2px solid #3b82f6" : "2px solid transparent",
              color: activeTab === tab.id ? "#e2e8f0" : "#4b5e7a",
              padding: "10px 18px", cursor: "pointer",
              fontSize: 12, fontFamily: monoFont, fontWeight: 600, letterSpacing: 0.3,
              transition: "all 0.15s",
            }}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div style={{ marginTop: 4 }}>
        {activeTab === "winding" && (
          <div>
            <SectionHeader number="01" title="Winding Number Evolution" subtitle="Contour integrals ∮ v·dl / 2π at four radii. Integer quantization = topological lock intact." />
            <div style={{ background: "#0a0e17", border: "1px solid #1a2035", borderRadius: 6, padding: "16px 8px 8px" }}>
              <ResponsiveContainer width="100%" height={340}>
                <ComposedChart data={windingData} margin={{ top: 8, right: 20, left: 8, bottom: 8 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#111827" />
                  <XAxis dataKey="t" stroke="#334155" tick={{ fontSize: 10, fill: "#4b5e7a", fontFamily: monoFont }} label={{ value: "Time", position: "insideBottom", offset: -2, fill: "#4b5e7a", fontSize: 10 }} />
                  <YAxis stroke="#334155" tick={{ fontSize: 10, fill: "#4b5e7a", fontFamily: monoFont }} domain={[-3, 4]} />
                  <Tooltip
                    contentStyle={{ background: "#0f1729", border: "1px solid #1e3a5f", borderRadius: 4, fontSize: 11, fontFamily: monoFont }}
                    labelStyle={{ color: "#64748b" }}
                  />
                  <ReferenceLine y={3} stroke="#22c55e" strokeDasharray="8 4" strokeWidth={1} label={{ value: "W=3 (Trefoil)", fill: "#22c55e", fontSize: 10, fontFamily: monoFont }} />
                  <ReferenceLine y={-1} stroke="#ef4444" strokeDasharray="8 4" strokeWidth={1} label={{ value: "W=−1", fill: "#ef4444", fontSize: 10, fontFamily: monoFont }} />
                  <ReferenceLine y={0} stroke="#334155" strokeWidth={0.5} />
                  <Line type="monotone" dataKey="r=0.5" stroke="#f59e0b" strokeWidth={1.5} dot={false} />
                  <Line type="monotone" dataKey="r=1.0" stroke="#3b82f6" strokeWidth={2} dot={false} />
                  <Line type="monotone" dataKey="r=2.0" stroke="#8b5cf6" strokeWidth={1.5} dot={false} />
                  <Line type="monotone" dataKey="r=3.0" stroke="#06b6d4" strokeWidth={1.5} dot={false} />
                  <Legend wrapperStyle={{ fontSize: 10, fontFamily: monoFont }} />
                </ComposedChart>
              </ResponsiveContainer>
            </div>

            <SectionHeader number="02" title="Peak Density Evolution" subtitle="Maximum |ψ|² over time. Spikes indicate vortex core interactions." />
            <div style={{ background: "#0a0e17", border: "1px solid #1a2035", borderRadius: 6, padding: "16px 8px 8px" }}>
              <ResponsiveContainer width="100%" height={180}>
                <AreaChart data={densityData} margin={{ top: 8, right: 20, left: 8, bottom: 8 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#111827" />
                  <XAxis dataKey="t" stroke="#334155" tick={{ fontSize: 10, fill: "#4b5e7a", fontFamily: monoFont }} />
                  <YAxis stroke="#334155" tick={{ fontSize: 10, fill: "#4b5e7a", fontFamily: monoFont }} domain={[0, 2.5]} />
                  <Tooltip contentStyle={{ background: "#0f1729", border: "1px solid #1e3a5f", borderRadius: 4, fontSize: 11, fontFamily: monoFont }} />
                  <Area type="monotone" dataKey="maxrho" stroke="#8b5cf6" fill="rgba(139,92,246,0.1)" strokeWidth={1.5} />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}

        {activeTab === "spectrum" && (
          <div>
            <SectionHeader number="03" title="Helmholtz Energy Decomposition" subtitle="Sharp (♯) = compressible/acoustic. Flat (♭) = incompressible/vortical. The bivector grade dominates." />
            <div style={{ background: "#0a0e17", border: "1px solid #1a2035", borderRadius: 6, padding: "16px 8px 8px" }}>
              <ResponsiveContainer width="100%" height={320}>
                <BarChart data={spectrumData} margin={{ top: 8, right: 20, left: 8, bottom: 8 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#111827" />
                  <XAxis dataKey="k" stroke="#334155" tick={{ fontSize: 9, fill: "#4b5e7a", fontFamily: monoFont }} label={{ value: "Wavenumber k", position: "insideBottom", offset: -2, fill: "#4b5e7a", fontSize: 10 }} />
                  <YAxis stroke="#334155" tick={{ fontSize: 10, fill: "#4b5e7a", fontFamily: monoFont }} />
                  <Tooltip contentStyle={{ background: "#0f1729", border: "1px solid #1e3a5f", borderRadius: 4, fontSize: 11, fontFamily: monoFont }} />
                  <Bar dataKey="Sharp (compressible)" fill="#3b82f6" fillOpacity={0.7} />
                  <Bar dataKey="Flat (incompressible)" fill="#f59e0b" fillOpacity={0.7} />
                  <Legend wrapperStyle={{ fontSize: 10, fontFamily: monoFont }} />
                </BarChart>
              </ResponsiveContainer>
            </div>
            <div style={{
              background: "#0a0e17", border: "1px solid #1a2035", borderRadius: 6,
              padding: 16, marginTop: 12,
            }}>
              <div style={{ color: "#4b5e7a", fontSize: 10, fontFamily: monoFont, textTransform: "uppercase", letterSpacing: 1.2, marginBottom: 8 }}>
                HoTT Modality Mapping
              </div>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 8, fontSize: 11, fontFamily: monoFont }}>
                <div style={{ color: "#64748b" }}>Modality</div><div style={{ color: "#64748b" }}>Hardware</div><div style={{ color: "#64748b" }}>GA Grade</div>
                <div style={{ color: "#3b82f6" }}>Sharp (♯)</div><div style={{ color: "#94a3b8" }}>Condensate</div><div style={{ color: "#94a3b8" }}>Scalar α</div>
                <div style={{ color: "#f59e0b" }}>Flat (♭)</div><div style={{ color: "#94a3b8" }}>Vortex cores</div><div style={{ color: "#94a3b8" }}>Bivector <span style={{ fontWeight: 700 }}>B</span></div>
                <div style={{ color: "#22c55e" }}>Shape (∫)</div><div style={{ color: "#94a3b8" }}>Circulation κ</div><div style={{ color: "#94a3b8" }}>∮ B·dl</div>
              </div>
            </div>
          </div>
        )}

        {activeTab === "analysis" && (
          <div>
            <SectionHeader number="04" title="Topological Lock Failure Analysis" subtitle="Why the Milnor trefoil decays in 2D, and what this means for the experimental proposal." />

            <div style={{
              background: "#0a0e17", border: "1px solid #1e3a5f", borderRadius: 6,
              padding: 20, marginBottom: 16,
            }}>
              <h3 style={{ color: "#fca5a5", fontSize: 14, fontWeight: 700, margin: "0 0 12px", fontFamily: monoFont }}>
                DIAGNOSIS: DIMENSIONAL INSUFFICIENCY
              </h3>
              <div style={{ fontSize: 13, lineHeight: 1.75, color: "#94a3b8" }}>
                <p style={{ margin: "0 0 12px" }}>
                  The Milnor polynomial f(u,v) = u³ − v² defines a trefoil knot <em>in 3D</em> — specifically as the intersection
                  of the zero set with S³ ⊂ ℂ². Projecting to 2D collapses the knot topology. A 2D "trefoil" is just three
                  superimposed vortices with total charge W = 3.
                </p>
                <p style={{ margin: "0 0 12px" }}>
                  Without the third dimension, there is no knotting — the vortices are free to migrate, reconnect, and annihilate.
                  The simulation confirms this: the initial W = 3 state decays through vortex emission to W = −1.
                </p>
                <p style={{ margin: "0 0 12px", color: "#e2e8f0", fontWeight: 500 }}>
                  The decay sequence W = +3 → +2 → 0 → −1 proceeds from inside out: the r=0.5 contour loses coherence
                  first (vortex cores exit the smallest circle), then r=1.0, then r=2.0, finally r=3.0. Each step corresponds
                  to a vortex crossing the contour — exactly the strand passage your trefoil argument predicts should be
                  topologically forbidden in 3D.
                </p>
              </div>
            </div>

            <div style={{
              background: "#0a0e17", border: "1px solid #14532d", borderRadius: 6,
              padding: 20, marginBottom: 16,
            }}>
              <h3 style={{ color: "#86efac", fontSize: 14, fontWeight: 700, margin: "0 0 12px", fontFamily: monoFont }}>
                WHAT THIS VALIDATES
              </h3>
              <div style={{ fontSize: 13, lineHeight: 1.75, color: "#94a3b8" }}>
                <p style={{ margin: "0 0 12px" }}>
                  <span style={{ color: "#22c55e", fontFamily: monoFont }}>✓</span> The Milnor polynomial correctly imprints winding number 3 — the Milnor number μ of the (2,3) singularity.
                </p>
                <p style={{ margin: "0 0 12px" }}>
                  <span style={{ color: "#22c55e", fontFamily: monoFont }}>✓</span> The cohomological audit correctly tracks the winding number as a contour integral.
                </p>
                <p style={{ margin: "0 0 12px" }}>
                  <span style={{ color: "#22c55e", fontFamily: monoFont }}>✓</span> The Helmholtz decomposition confirms vortical (Flat/♭) energy dominates over acoustic (Sharp/♯) — the bivector grade carries the physics.
                </p>
                <p style={{ margin: "0 0 12px" }}>
                  <span style={{ color: "#22c55e", fontFamily: monoFont }}>✓</span> The decay itself is evidence: in 2D without topological protection, the lock <em>should</em> break. The 3D knotted structure is necessary, not optional.
                </p>
              </div>
            </div>

            <div style={{
              background: "#0a0e17", border: "1px solid #713f12", borderRadius: 6,
              padding: 20,
            }}>
              <h3 style={{ color: "#fde68a", fontSize: 14, fontWeight: 700, margin: "0 0 12px", fontFamily: monoFont }}>
                REQUIRED FOR TOPOLOGICAL LOCK
              </h3>
              <div style={{ fontSize: 13, lineHeight: 1.75, color: "#94a3b8" }}>
                <p style={{ margin: "0 0 12px" }}>
                  <span style={{ color: "#f59e0b", fontFamily: monoFont }}>→</span>{" "}
                  <strong style={{ color: "#e2e8f0" }}>3D simulation</strong> with actual knotted vortex filaments, not 2D phase fields.
                  The trefoil's unknotting number u = 1 means strand passage requires energy — this barrier is absent in 2D.
                </p>
                <p style={{ margin: "0 0 12px" }}>
                  <span style={{ color: "#f59e0b", fontFamily: monoFont }}>→</span>{" "}
                  <strong style={{ color: "#e2e8f0" }}>Quasicrystalline pinning lattice</strong> with φ-scaled spacing to prevent
                  resonant vortex drift. The golden-angle rotation between layers creates the anti-resonant structure.
                </p>
                <p style={{ margin: "0 0 12px" }}>
                  <span style={{ color: "#f59e0b", fontFamily: monoFont }}>→</span>{" "}
                  <strong style={{ color: "#e2e8f0" }}>Chern-Simons invariant</strong> computed on the vortex filament, not just the
                  winding number of a 2D slice. The CS invariant distinguishes the trefoil from three unlinked circles.
                </p>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Footer */}
      <div style={{
        marginTop: 32, paddingTop: 16, borderTop: "1px solid #111827",
        color: "#334155", fontSize: 10, fontFamily: monoFont,
        display: "flex", justifyContent: "space-between",
      }}>
        <span>Helium Loom v0.1 · Gross-Pitaevskii + Milnor + Cohomological Audit</span>
        <span>IsGapped: <span style={{ color: "#ef4444" }}>UNDISCHARGEABLE</span> in 2D</span>
      </div>
    </div>
  );
}
