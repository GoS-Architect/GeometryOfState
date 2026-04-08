import { useState } from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, LineChart, Line, CartesianGrid, ReferenceLine, Area, AreaChart, ComposedChart, ScatterChart, Scatter, Cell } from "recharts";

const DATA = {
  control: { option:"Control", label:"No Ni-62", gap:0.0200, nzm:8, edge:0.2088, defect:0.0, bulk:0.7912, status:"TRIVIAL", az:"BDI", stack:"Si-28 / C-12 graphene / Nb", energies:[0.020,-0.020,-0.020,0.020,0.045,-0.045,-0.045,0.045,0.084,-0.084], diagnosis:"No T-breaking. Class BDI, trivial phase. Need h > 0.583, have h = 0." },
  a: { option:"A", label:"Uniform Exchange", gap:0.0192, nzm:6, edge:0.2058, defect:0.0, bulk:0.7942, status:"FAIL", az:"D", stack:"Si-28 / C-12 graphene / Ni-62 (2nm) / Nb", energies:[0.019,-0.019,0.028,-0.028,-0.038,0.038,0.051,-0.051,-0.089,0.089], diagnosis:"Continuous Ni film suppresses \u0394_eff to 10%. Exchange wins, pairing loses. Gap too small for certification.", delta_eff:0.03 },
  b: { option:"B", label:"Ni-62 Substrate", gap:0.0055, nzm:22, edge:0.1856, defect:0.0, bulk:0.8144, status:"FAIL", az:"\u2014", stack:"Si-28 / Ni-62(111) / C-12 graphene / Nb", energies:[-0.006,0.006,-0.017,0.017,-0.018,0.018,0.020,-0.020,-0.026,0.026], diagnosis:"Ni\u2013C hybridization shifts \u03bc by ~2 eV. Dirac cone destroyed. Threshold h > 2.52, have 0.6. Structural failure." },
  c: { option:"C", label:"Patterned at Defects", gap:0.0149, nzm:8, edge:0.2093, defect:0.104, bulk:0.6867, status:"PARTIAL", az:"D (local)", stack:"Si-28 / C-12 graphene + Ni-62 @ 5/7 / Nb", energies:[-0.015,0.015,0.026,-0.026,-0.038,0.038,-0.048,0.048,0.083,-0.083], diagnosis:"Right physics, wrong size. 11-site defect region too narrow \u2014 MZMs hybridize. Width sweep shows PASS at \u226551 sites.", defect_width:11 },
  d: { option:"D", label:"Triplet Generator", gap:0.0092, nzm:4, edge:0.2062, defect:0.0, bulk:0.7938, status:"FAIL", az:"DIII", stack:"Si-28 / C-12 graphene / Nb / Ni-62 (cap)", energies:[-0.009,0.009,-0.009,0.009,-0.058,0.058,0.058,-0.058,-0.076,0.076], diagnosis:"No exchange at graphene level. Triplet alone can\u2019t drive transition without T-breaking. Architecturally indirect." },
  e: { option:"E", label:"Hybrid (C + Triplet)", gap:0.0143, nzm:8, edge:0.2093, defect:0.1038, bulk:0.6868, status:"PARTIAL", az:"D (local)", stack:"Si-28 / C-12 graphene + Ni-62 @ 5/7 / Nb", energies:[-0.014,0.014,0.026,-0.026,0.038,-0.038,0.048,-0.048,0.082,-0.082], diagnosis:"Same as C. Triplet at boundaries adds complexity without qualitative change at this defect width." },
};

const SWEEP_WIDTH = [
  {w:5,gap:0.0229,dw:0.049,topo:false},{w:7,gap:0.0126,dw:0.064,topo:false},{w:9,gap:0.0167,dw:0.088,topo:false},
  {w:11,gap:0.0149,dw:0.104,topo:false},{w:13,gap:0.0126,dw:0.130,topo:false},{w:15,gap:0.0200,dw:0.137,topo:false},
  {w:17,gap:0.0120,dw:0.160,topo:false},{w:19,gap:0.0188,dw:0.183,topo:false},{w:21,gap:0.0166,dw:0.205,topo:false},
  {w:23,gap:0.0161,dw:0.225,topo:false},{w:25,gap:0.0203,dw:0.242,topo:false},{w:27,gap:0.0149,dw:0.267,topo:false},
  {w:29,gap:0.0185,dw:0.273,topo:false},{w:31,gap:0.0168,dw:0.297,topo:false},{w:33,gap:0.0138,dw:0.314,topo:false},
  {w:35,gap:0.0216,dw:0.345,topo:false},{w:37,gap:0.0175,dw:0.357,topo:false},{w:39,gap:0.0210,dw:0.381,topo:false},
  {w:41,gap:0.0201,dw:0.394,topo:false},{w:43,gap:0.0161,dw:0.412,topo:false},{w:45,gap:0.0235,dw:0.431,topo:false},
  {w:47,gap:0.0132,dw:0.459,topo:false},{w:49,gap:0.0184,dw:0.479,topo:false},{w:51,gap:0.0198,dw:0.504,topo:true},
  {w:53,gap:0.0184,dw:0.519,topo:true},{w:55,gap:0.0246,dw:0.534,topo:true},{w:57,gap:0.0171,dw:0.549,topo:true},
  {w:59,gap:0.0211,dw:0.572,topo:true},
];

const SWEEP_HEX = [
  {h:0.0,gap:0.0253,dw:0.101},{h:0.1,gap:0.0250,dw:0.101},{h:0.2,gap:0.0243,dw:0.101},
  {h:0.3,gap:0.0230,dw:0.102},{h:0.4,gap:0.0209,dw:0.103},{h:0.5,gap:0.0181,dw:0.103},
  {h:0.6,gap:0.0149,dw:0.104},{h:0.7,gap:0.0116,dw:0.110},{h:0.8,gap:0.0086,dw:0.115},
  {h:0.9,gap:0.0067,dw:0.127},{h:1.0,gap:0.0070,dw:0.141},{h:1.1,gap:0.0085,dw:0.134},
  {h:1.2,gap:0.0082,dw:0.110},{h:1.3,gap:0.0081,dw:0.110},{h:1.4,gap:0.0106,dw:0.237},
  {h:1.5,gap:0.0116,dw:0.143},
];

const PARAMS = { N:100, t:"1.0", mu:"0.5", Delta:"0.3", alpha:"0.5", h_ex:"0.6", threshold:"0.583" };

const STATUS_COLORS = { PASS:"#22c55e", PARTIAL:"#f59e0b", FAIL:"#ef4444", TRIVIAL:"#6b7280" };
const STATUS_BG = { PASS:"rgba(34,197,94,0.08)", PARTIAL:"rgba(245,158,11,0.08)", FAIL:"rgba(239,68,68,0.08)", TRIVIAL:"rgba(107,114,128,0.08)" };

const CustomTooltip = ({active, payload, label}) => {
  if (!active || !payload?.length) return null;
  return (
    <div style={{background:"#1a1a2e", border:"1px solid #333", borderRadius:4, padding:"8px 12px", fontSize:11, fontFamily:"'JetBrains Mono', monospace"}}>
      <div style={{color:"#8892b0", marginBottom:4}}>{label}</div>
      {payload.map((p,i) => (
        <div key={i} style={{color:p.color||"#ccd6f6"}}>{p.name}: {typeof p.value === 'number' ? p.value.toFixed(4) : p.value}</div>
      ))}
    </div>
  );
};

function StatusBadge({status}) {
  return (
    <span style={{
      display:"inline-block", padding:"2px 10px", borderRadius:3, fontSize:11, fontWeight:700,
      letterSpacing:1, fontFamily:"'JetBrains Mono', monospace",
      color: STATUS_COLORS[status] || "#fff",
      background: STATUS_BG[status] || "rgba(255,255,255,0.05)",
      border: `1px solid ${STATUS_COLORS[status] || "#444"}`,
    }}>{status}</span>
  );
}

function SpectrumChart({energies, color, label}) {
  const data = energies.map((e,i) => ({idx:i, E:e}));
  return (
    <ResponsiveContainer width="100%" height={130}>
      <BarChart data={data} layout="vertical" margin={{left:0,right:10,top:4,bottom:4}}>
        <XAxis type="number" domain={[-0.1,0.1]} tick={{fontSize:9, fill:"#4a5568"}} tickCount={5} />
        <YAxis type="category" dataKey="idx" hide />
        <ReferenceLine x={0} stroke="#333" strokeWidth={1} />
        <Bar dataKey="E" fill={color} opacity={0.8} barSize={8} radius={[2,2,2,2]} />
      </BarChart>
    </ResponsiveContainer>
  );
}

function OptionCard({data, selected, onClick}) {
  const isSelected = selected === data.option;
  return (
    <div onClick={onClick} style={{
      background: isSelected ? "rgba(100,120,180,0.12)" : "rgba(255,255,255,0.02)",
      border: `1px solid ${isSelected ? "#5b6abf" : "#222"}`,
      borderLeft: `3px solid ${STATUS_COLORS[data.status]}`,
      borderRadius: 6, padding: "12px 14px", cursor: "pointer",
      transition: "all 0.2s ease",
    }}>
      <div style={{display:"flex", justifyContent:"space-between", alignItems:"center", marginBottom:6}}>
        <span style={{fontSize:13, fontWeight:600, color:"#ccd6f6", fontFamily:"'JetBrains Mono', monospace"}}>{data.option}</span>
        <StatusBadge status={data.status} />
      </div>
      <div style={{fontSize:11, color:"#8892b0", marginBottom:8}}>{data.label}</div>
      <div style={{display:"grid", gridTemplateColumns:"1fr 1fr 1fr", gap:4, fontSize:10, color:"#4a5568"}}>
        <div><span style={{color:"#8892b0"}}>Gap</span><br/><span style={{color:"#ccd6f6", fontFamily:"'JetBrains Mono', monospace"}}>{data.gap.toFixed(4)}</span></div>
        <div><span style={{color:"#8892b0"}}>ZM</span><br/><span style={{color:"#ccd6f6", fontFamily:"'JetBrains Mono', monospace"}}>{data.nzm}</span></div>
        <div><span style={{color:"#8892b0"}}>AZ</span><br/><span style={{color:"#ccd6f6", fontFamily:"'JetBrains Mono', monospace"}}>{data.az}</span></div>
      </div>
    </div>
  );
}

export default function Ni62Dashboard() {
  const [selected, setSelected] = useState("C");
  const [tab, setTab] = useState("overview");
  const opts = Object.values(DATA);
  const sel = Object.values(DATA).find(d => d.option === selected) || DATA.c;

  const comparisonData = opts.map(d => ({
    name: d.option, gap: d.gap, defect: d.defect, edge: d.edge,
    fill: STATUS_COLORS[d.status],
  }));

  const localizationData = opts.map(d => ({
    name: d.option, Edge: +(d.edge*100).toFixed(1), Defect: +(d.defect*100).toFixed(1), Bulk: +(d.bulk*100).toFixed(1),
  }));

  return (
    <div style={{
      minHeight:"100vh", background:"#0a0a1a", color:"#ccd6f6",
      fontFamily:"'Crimson Pro', Georgia, serif", padding:0, margin:0,
    }}>
      <link href="https://fonts.googleapis.com/css2?family=Crimson+Pro:wght@400;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet"/>

      {/* Header */}
      <div style={{
        borderBottom:"1px solid #1a1a2e", padding:"20px 24px",
        background:"linear-gradient(180deg, rgba(20,20,40,1) 0%, rgba(10,10,26,1) 100%)",
      }}>
        <div style={{display:"flex", justifyContent:"space-between", alignItems:"flex-start", flexWrap:"wrap", gap:12}}>
          <div>
            <div style={{fontSize:10, letterSpacing:3, color:"#5b6abf", fontFamily:"'JetBrains Mono', monospace", marginBottom:4}}>GEOMETRY OF STATE \u00b7 L3 PHYSICS</div>
            <h1 style={{fontSize:22, fontWeight:700, margin:0, letterSpacing:-0.5}}>
              Ni-62 FWS Stack Simulations
            </h1>
            <div style={{fontSize:12, color:"#4a5568", marginTop:4, fontFamily:"'JetBrains Mono', monospace"}}>
              Spinful BdG \u00b7 Rashba nanowire \u00b7 5 options + control \u00b7 TAS methodology
            </div>
          </div>
          <div style={{
            background:"rgba(255,255,255,0.03)", border:"1px solid #1a1a2e", borderRadius:6, padding:"8px 14px",
            fontSize:10, fontFamily:"'JetBrains Mono', monospace", color:"#4a5568", lineHeight:1.7,
          }}>
            <div>N={PARAMS.N} &nbsp; t={PARAMS.t} &nbsp; \u03bc={PARAMS.mu} &nbsp; \u0394={PARAMS.Delta}</div>
            <div>\u03b1_R={PARAMS.alpha} &nbsp; h_ex={PARAMS.h_ex} &nbsp; h_c={PARAMS.threshold}</div>
          </div>
        </div>
      </div>

      {/* Tab nav */}
      <div style={{display:"flex", gap:0, borderBottom:"1px solid #1a1a2e", background:"rgba(15,15,30,0.5)"}}>
        {[["overview","Overview"],["detail","Detail View"],["sweeps","Parameter Sweeps"],["tas","TAS Analysis"]].map(([id,lbl]) => (
          <button key={id} onClick={() => setTab(id)} style={{
            background:"none", border:"none", borderBottom: tab===id ? "2px solid #5b6abf" : "2px solid transparent",
            color: tab===id ? "#ccd6f6" : "#4a5568", padding:"10px 20px", cursor:"pointer",
            fontSize:12, fontFamily:"'JetBrains Mono', monospace", fontWeight: tab===id ? 600 : 400,
            transition:"all 0.15s ease",
          }}>{lbl}</button>
        ))}
      </div>

      <div style={{padding:"16px 24px", maxWidth:1200, margin:"0 auto"}}>

        {/* ─── OVERVIEW TAB ─── */}
        {tab === "overview" && (
          <div>
            {/* Option cards grid */}
            <div style={{display:"grid", gridTemplateColumns:"repeat(auto-fill, minmax(200px, 1fr))", gap:10, marginBottom:20}}>
              {opts.map(d => (
                <OptionCard key={d.option} data={d} selected={selected} onClick={() => setSelected(d.option)} />
              ))}
            </div>

            {/* Comparison charts */}
            <div style={{display:"grid", gridTemplateColumns:"1fr 1fr", gap:16, marginBottom:20}}>
              <div style={{background:"rgba(255,255,255,0.02)", border:"1px solid #1a1a2e", borderRadius:6, padding:16}}>
                <div style={{fontSize:11, color:"#5b6abf", fontFamily:"'JetBrains Mono', monospace", marginBottom:10}}>TOPOLOGICAL GAP COMPARISON</div>
                <ResponsiveContainer width="100%" height={180}>
                  <BarChart data={comparisonData} margin={{left:0,right:0,top:4,bottom:4}}>
                    <XAxis dataKey="name" tick={{fontSize:10, fill:"#8892b0"}} />
                    <YAxis tick={{fontSize:9, fill:"#4a5568"}} tickCount={5} />
                    <Tooltip content={<CustomTooltip/>} />
                    <Bar dataKey="gap" radius={[3,3,0,0]} barSize={28}>
                      {comparisonData.map((d,i) => <Cell key={i} fill={d.fill} opacity={0.8} />)}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>

              <div style={{background:"rgba(255,255,255,0.02)", border:"1px solid #1a1a2e", borderRadius:6, padding:16}}>
                <div style={{fontSize:11, color:"#5b6abf", fontFamily:"'JetBrains Mono', monospace", marginBottom:10}}>ZERO-MODE LOCALIZATION (%)</div>
                <ResponsiveContainer width="100%" height={180}>
                  <BarChart data={localizationData} margin={{left:0,right:0,top:4,bottom:4}}>
                    <XAxis dataKey="name" tick={{fontSize:10, fill:"#8892b0"}} />
                    <YAxis tick={{fontSize:9, fill:"#4a5568"}} />
                    <Tooltip content={<CustomTooltip/>} />
                    <Bar dataKey="Edge" stackId="a" fill="#3b82f6" opacity={0.7} />
                    <Bar dataKey="Defect" stackId="a" fill="#f59e0b" opacity={0.8} />
                    <Bar dataKey="Bulk" stackId="a" fill="#1e293b" opacity={0.5} radius={[3,3,0,0]} />
                  </BarChart>
                </ResponsiveContainer>
                <div style={{display:"flex", gap:16, justifyContent:"center", marginTop:6, fontSize:10, fontFamily:"'JetBrains Mono', monospace"}}>
                  <span><span style={{display:"inline-block",width:8,height:8,background:"#3b82f6",borderRadius:2,marginRight:4}}/>Edge</span>
                  <span><span style={{display:"inline-block",width:8,height:8,background:"#f59e0b",borderRadius:2,marginRight:4}}/>Defect</span>
                  <span><span style={{display:"inline-block",width:8,height:8,background:"#1e293b",borderRadius:2,marginRight:4}}/>Bulk</span>
                </div>
              </div>
            </div>

            {/* Key finding */}
            <div style={{
              background:"rgba(91,106,191,0.06)", border:"1px solid rgba(91,106,191,0.2)", borderRadius:6,
              padding:"14px 18px", fontSize:13,
            }}>
              <div style={{fontSize:10, color:"#5b6abf", fontFamily:"'JetBrains Mono', monospace", marginBottom:6}}>KEY FINDING</div>
              Options C and E show the right physics (local exchange at defects, preserved bulk Dirac cone) but the 11-site
              defect region is too narrow for decoupled MZMs. The defect width sweep identifies <span style={{color:"#22c55e", fontFamily:"'JetBrains Mono', monospace", fontWeight:700}}>\u226551 sites</span> as
              the minimum for topological certification. This constrains the Penrose tiling geometry for the corrected 2D lattice.
            </div>
          </div>
        )}

        {/* ─── DETAIL TAB ─── */}
        {tab === "detail" && (
          <div>
            <div style={{display:"grid", gridTemplateColumns:"200px 1fr", gap:16}}>
              <div style={{display:"flex", flexDirection:"column", gap:8}}>
                {opts.map(d => (
                  <OptionCard key={d.option} data={d} selected={selected} onClick={() => setSelected(d.option)} />
                ))}
              </div>
              <div style={{background:"rgba(255,255,255,0.02)", border:"1px solid #1a1a2e", borderRadius:6, padding:20}}>
                <div style={{display:"flex", justifyContent:"space-between", alignItems:"center", marginBottom:16}}>
                  <div>
                    <h2 style={{fontSize:18, margin:0, fontWeight:600}}>{sel.label}</h2>
                    <div style={{fontSize:11, color:"#4a5568", marginTop:2, fontFamily:"'JetBrains Mono', monospace"}}>{sel.stack}</div>
                  </div>
                  <StatusBadge status={sel.status} />
                </div>

                <div style={{display:"grid", gridTemplateColumns:"1fr 1fr", gap:16, marginBottom:16}}>
                  <div>
                    <div style={{fontSize:10, color:"#5b6abf", fontFamily:"'JetBrains Mono', monospace", marginBottom:8}}>LOW-ENERGY BdG SPECTRUM</div>
                    <SpectrumChart energies={sel.energies} color={STATUS_COLORS[sel.status]} label={sel.option} />
                  </div>
                  <div>
                    <div style={{fontSize:10, color:"#5b6abf", fontFamily:"'JetBrains Mono', monospace", marginBottom:8}}>METRICS</div>
                    <div style={{display:"grid", gridTemplateColumns:"1fr 1fr", gap:8, fontSize:12, fontFamily:"'JetBrains Mono', monospace"}}>
                      {[
                        ["Gap", sel.gap.toFixed(4)],
                        ["Zero modes", sel.nzm],
                        ["AZ class", sel.az],
                        ["Edge wt", (sel.edge*100).toFixed(1)+"%"],
                        ["Defect wt", (sel.defect*100).toFixed(1)+"%"],
                        ["Bulk wt", (sel.bulk*100).toFixed(1)+"%"],
                      ].map(([k,v]) => (
                        <div key={k} style={{background:"rgba(0,0,0,0.2)", borderRadius:4, padding:"6px 10px"}}>
                          <div style={{fontSize:9, color:"#4a5568"}}>{k}</div>
                          <div style={{color:"#ccd6f6", fontWeight:500}}>{v}</div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>

                <div style={{
                  background:"rgba(0,0,0,0.2)", borderRadius:4, padding:"12px 16px",
                  fontSize:12, lineHeight:1.6, color:"#8892b0",
                  borderLeft:`3px solid ${STATUS_COLORS[sel.status]}`,
                }}>
                  <div style={{fontSize:10, color:"#5b6abf", fontFamily:"'JetBrains Mono', monospace", marginBottom:6}}>DIAGNOSIS</div>
                  {sel.diagnosis}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ─── SWEEPS TAB ─── */}
        {tab === "sweeps" && (
          <div style={{display:"grid", gap:20}}>
            <div style={{background:"rgba(255,255,255,0.02)", border:"1px solid #1a1a2e", borderRadius:6, padding:20}}>
              <div style={{fontSize:11, color:"#5b6abf", fontFamily:"'JetBrains Mono', monospace", marginBottom:4}}>OPTION C \u2014 DEFECT WIDTH SWEEP</div>
              <div style={{fontSize:12, color:"#4a5568", marginBottom:12}}>Scanning defect region width from 5 to 59 sites. Green region = topological (defect weight &gt; 50%).</div>
              <ResponsiveContainer width="100%" height={260}>
                <ComposedChart data={SWEEP_WIDTH} margin={{left:10,right:10,top:10,bottom:10}}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1a1a2e" />
                  <XAxis dataKey="w" tick={{fontSize:10, fill:"#8892b0"}} label={{value:"Defect width (sites)", position:"insideBottom", offset:-4, fontSize:10, fill:"#4a5568"}} />
                  <YAxis yAxisId="left" tick={{fontSize:9, fill:"#4a5568"}} label={{value:"Gap", angle:-90, position:"insideLeft", fontSize:10, fill:"#4a5568"}} />
                  <YAxis yAxisId="right" orientation="right" tick={{fontSize:9, fill:"#4a5568"}} label={{value:"Defect weight", angle:90, position:"insideRight", fontSize:10, fill:"#4a5568"}} />
                  <Tooltip content={<CustomTooltip/>} />
                  <ReferenceLine yAxisId="right" y={0.5} stroke="#22c55e" strokeDasharray="6 3" label={{value:"Topo threshold", position:"top", fontSize:9, fill:"#22c55e"}} />
                  <ReferenceLine x={51} stroke="#22c55e" strokeDasharray="4 2" strokeWidth={2} label={{value:"w=51", position:"top", fontSize:10, fill:"#22c55e"}} />
                  <Line yAxisId="left" type="monotone" dataKey="gap" stroke="#f59e0b" strokeWidth={2} dot={{r:3, fill:"#f59e0b"}} name="Gap" />
                  <Line yAxisId="right" type="monotone" dataKey="dw" stroke="#3b82f6" strokeWidth={2} dot={false} name="Defect wt" />
                  {SWEEP_WIDTH.map((d,i) => d.topo ? (
                    <ReferenceLine key={i} x={d.w} stroke="rgba(34,197,94,0.15)" strokeWidth={14} yAxisId="left" />
                  ) : null)}
                </ComposedChart>
              </ResponsiveContainer>
            </div>

            <div style={{background:"rgba(255,255,255,0.02)", border:"1px solid #1a1a2e", borderRadius:6, padding:20}}>
              <div style={{fontSize:11, color:"#5b6abf", fontFamily:"'JetBrains Mono', monospace", marginBottom:4}}>OPTION C \u2014 EXCHANGE STRENGTH SWEEP</div>
              <div style={{fontSize:12, color:"#4a5568", marginBottom:12}}>h_ex from 0 to 1.5 at fixed defect width = 11 sites. Gap closes near threshold then reopens.</div>
              <ResponsiveContainer width="100%" height={260}>
                <ComposedChart data={SWEEP_HEX} margin={{left:10,right:10,top:10,bottom:10}}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1a1a2e" />
                  <XAxis dataKey="h" tick={{fontSize:10, fill:"#8892b0"}} label={{value:"Exchange field h_ex", position:"insideBottom", offset:-4, fontSize:10, fill:"#4a5568"}} />
                  <YAxis yAxisId="left" tick={{fontSize:9, fill:"#4a5568"}} />
                  <YAxis yAxisId="right" orientation="right" tick={{fontSize:9, fill:"#4a5568"}} />
                  <Tooltip content={<CustomTooltip/>} />
                  <ReferenceLine x={0.583} stroke="#ef4444" strokeDasharray="6 3" label={{value:"h_c=0.583", position:"top", fontSize:9, fill:"#ef4444"}} />
                  <Line yAxisId="left" type="monotone" dataKey="gap" stroke="#f59e0b" strokeWidth={2} dot={{r:3, fill:"#f59e0b"}} name="Gap" />
                  <Line yAxisId="right" type="monotone" dataKey="dw" stroke="#3b82f6" strokeWidth={2} dot={false} name="Defect wt" />
                </ComposedChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}

        {/* ─── TAS TAB ─── */}
        {tab === "tas" && (
          <div style={{display:"grid", gap:16}}>
            {[
              {phase:"THESIS", color:"#3b82f6", text:"Ni-62 at 5/7 defect sites provides local time-reversal symmetry breaking via exchange proximity (J ~ 6 meV). Combined with Nb superconducting proximity and intrinsic + enhanced SOC, this drives the local Altland-Zirnbauer class from BDI \u2192 D at defect boundaries. MZMs appear at the domain walls between trivial bulk and topological defect regions. The isotopic purity of Ni-62 (I = 0, highest nuclear binding energy per nucleon) extends the Si-28 / C-12 nuclear-silence strategy."},
              {phase:"ANTITHESIS", color:"#ef4444", text:"At the simulated defect width of 11 sites, the two domain-wall MZMs are too close and hybridize, splitting away from zero energy. The defect localization is only 10.4% \u2014 insufficient for certification. The width sweep reveals the minimum topological defect width is 51 sites. The exchange sweep shows no topological phase at any h_ex for 11-site width, confirming this is a geometric constraint, not a parameter tuning problem. Options A (pair-breaking), B (Dirac cone destruction), and D (no local T-breaking) fail for structural reasons."},
              {phase:"SYNTHESIS", color:"#22c55e", text:"The corrected 2D lattice (graphene + Penrose-seeded Stone-Wales defects at \u03b4t ~ 10%) must produce defect clusters with spatial extent \u226551 sites across for Option C/E to work. This is a concrete constraint on the Penrose tiling geometry feeding back into the Stage 1 re-run. The Ni-62 nano-island size and defect region geometry become co-design parameters: the tiling must be tuned so that topological domains are wide enough for MZM decoupling while remaining quasiperiodic."},
            ].map(({phase, color, text}) => (
              <div key={phase} style={{
                background:"rgba(255,255,255,0.02)", border:"1px solid #1a1a2e",
                borderLeft:`4px solid ${color}`, borderRadius:6, padding:"16px 20px",
              }}>
                <div style={{fontSize:11, color, fontFamily:"'JetBrains Mono', monospace", fontWeight:700, marginBottom:8, letterSpacing:2}}>{phase}</div>
                <div style={{fontSize:13, lineHeight:1.7, color:"#8892b0"}}>{text}</div>
              </div>
            ))}

            <div style={{
              background:"rgba(91,106,191,0.06)", border:"1px solid rgba(91,106,191,0.2)", borderRadius:6,
              padding:"14px 18px",
            }}>
              <div style={{fontSize:10, color:"#5b6abf", fontFamily:"'JetBrains Mono', monospace", marginBottom:6}}>OPEN PROBLEMS</div>
              <div style={{fontSize:12, lineHeight:1.8, color:"#8892b0"}}>
                <div><span style={{color:"#f59e0b", fontFamily:"'JetBrains Mono', monospace"}}>1.</span> Corrected 2D lattice with Penrose-seeded SW defects producing \u226551-site topological domains</div>
                <div><span style={{color:"#f59e0b", fontFamily:"'JetBrains Mono', monospace"}}>2.</span> AZ classification: formally show 5/7 + Ni-62 boundary maps to BDI \u2192 D class transition (L2)</div>
                <div><span style={{color:"#f59e0b", fontFamily:"'JetBrains Mono', monospace"}}>3.</span> Ni-62 nano-island fabrication: defect-site selective nucleation feasibility study</div>
                <div><span style={{color:"#f59e0b", fontFamily:"'JetBrains Mono', monospace"}}>4.</span> Singlet-to-triplet conversion at island boundaries: quantify conversion efficiency</div>
                <div><span style={{color:"#f59e0b", fontFamily:"'JetBrains Mono', monospace"}}>5.</span> 2D BdG with site-dependent exchange: extend from 1D chain to 2D Penrose lattice</div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Footer */}
      <div style={{
        borderTop:"1px solid #1a1a2e", padding:"12px 24px", marginTop:24,
        display:"flex", justifyContent:"space-between", fontSize:10, color:"#333",
        fontFamily:"'JetBrains Mono', monospace",
      }}>
        <span>GoS-Architect \u00b7 Geometry of State \u00b7 March 2026</span>
        <span>Model: Spinful BdG, Rashba nanowire, site-dependent h_ex + SOC</span>
      </div>
    </div>
  );
}
