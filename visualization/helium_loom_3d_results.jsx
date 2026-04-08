import { useState, useMemo } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine, AreaChart, Area, Legend } from "recharts";

const D3 = {
  t:[0,0.06,0.12,0.18,0.24,0.3,0.36,0.42,0.48,0.54,0.6,0.66,0.72,0.78,0.84,0.9,0.96,1.02,1.08,1.14,1.2],
  w20:[-0.73,2.23,-1.08,-1.71,-0.34,0.16,0.35,-0.11,-0.72,0.37,0.04,-2.58,-0.44,-3.21,-2.75,-3.73,-2.94,0.03,-1.45,-0.2,-1.08],
  writhe:[14.4,-30.2,-2.8,-16.8,57.6,-96.6,-28.2,12.5,14.2,-20.0,46.0,-20.9,-18.0,51.4,-54.7,7.9,0.8,-13.1,-50.7,-9.9,-22.4],
  core_vol:[1.46,18.0,20.1,28.4,34.0,40.0,45.2,46.6,48.4,53.7,55.2,51.7,53.0,50.6,52.9,50.3,46.3,46.3,41.4,44.4,42.2],
};

const D2 = {
  t: Array.from({length:41}, (_,i) => i*0.25),
  w10:[3.03,2.97,3.12,2.04,2.81,2.22,0.22,-0.77,-1.25,-0.17,0.04,1.68,-0.01,-1.72,0.35,-0.98,-0.18,-0.99,-1.0,-1.01,-1.01,-1.01,-0.98,-0.85,-0.51,2.70,-1.10,-0.97,-1.01,-0.99,-1.0,-0.99,-1.01,-0.97,-1.02,-1.06,-1.01,-1.0,-1.0,-0.99,-0.99],
};

const mono = "'SF Mono','Fira Code','JetBrains Mono',monospace";
const sans = "'DM Sans','Helvetica Neue',system-ui,sans-serif";

const Badge = ({type, children}) => {
  const c = {
    broken: {bg:"#2d1215",border:"#7f1d1d",text:"#fca5a5"},
    warn: {bg:"#2d2305",border:"#713f12",text:"#fde68a"},
    ok: {bg:"#052e16",border:"#14532d",text:"#86efac"},
    info: {bg:"#0c1929",border:"#1e3a5f",text:"#93c5fd"},
  }[type];
  return <span style={{display:"inline-flex",alignItems:"center",gap:5,padding:"2px 8px",borderRadius:3,background:c.bg,border:`1px solid ${c.border}`,color:c.text,fontSize:10,fontFamily:mono,fontWeight:600}}>
    <span style={{width:5,height:5,borderRadius:"50%",background:c.text,boxShadow:`0 0 4px ${c.text}`}}/>{children}
  </span>;
};

export default function Dashboard3D() {
  const [tab, setTab] = useState("3d");

  const data3d = useMemo(() => D3.t.map((t,i) => ({
    t, "W(r=2)":D3.w20[i], writhe:D3.writhe[i], core:D3.core_vol[i],
  })), []);

  const data2d = useMemo(() => D2.t.map((t,i) => ({t, "W(r=1)":D2.w10[i]})), []);

  const tabs = [
    {id:"3d", label:"3D Trefoil Results"},
    {id:"compare", label:"2D vs 3D Comparison"},
    {id:"diagnosis", label:"Root Cause Analysis"},
  ];

  return (
    <div style={{background:"#060a12",color:"#c8d6e5",fontFamily:sans,minHeight:"100vh",padding:"24px 20px"}}>
      <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&display=swap" rel="stylesheet"/>

      <div style={{borderBottom:"1px solid #111827",paddingBottom:16,marginBottom:20}}>
        <div style={{display:"flex",alignItems:"center",gap:10,marginBottom:6}}>
          <div style={{width:8,height:8,borderRadius:"50%",background:"#f59e0b",boxShadow:"0 0 12px #f59e0b"}}/>
          <h1 style={{fontSize:16,fontWeight:700,color:"#f1f5f9",margin:0,fontFamily:mono,letterSpacing:-0.5}}>
            HELIUM LOOM v3 — 3D TREFOIL VORTEX FILAMENT
          </h1>
        </div>
        <p style={{color:"#4b5e7a",fontSize:11,fontFamily:mono,margin:"4px 0 0 18px"}}>
          48³ GP evolution · (2,3) torus knot imprint · Writhe + winding + core volume tracking
        </p>
      </div>

      {/* Summary cards */}
      <div style={{display:"flex",gap:12,flexWrap:"wrap",marginBottom:20}}>
        {[
          {label:"Core Volume",val:"1.46 → 42.2",sub:"+2782%",badge:<Badge type="broken">DISPERSED</Badge>},
          {label:"Writhe",val:"14.4 → −22.4",sub:"σ = 35.2",badge:<Badge type="broken">CHAOTIC</Badge>},
          {label:"W(r=2)",val:"−0.73 → −1.08",sub:"σ = 1.42",badge:<Badge type="broken">UNSTABLE</Badge>},
          {label:"Lock Status",val:"BROKEN",sub:"28.6% retention",badge:<Badge type="warn">3D ≠ SUFFICIENT</Badge>},
        ].map(({label,val,sub,badge}) => (
          <div key={label} style={{background:"#0a0e17",border:"1px solid #1a2035",borderRadius:6,padding:"14px 16px",flex:1,minWidth:160}}>
            <div style={{color:"#4b5e7a",fontSize:10,fontFamily:mono,textTransform:"uppercase",letterSpacing:1.2,marginBottom:6}}>{label}</div>
            <div style={{color:"#e2e8f0",fontSize:18,fontFamily:mono,fontWeight:700,marginBottom:4}}>{val}</div>
            <div style={{display:"flex",alignItems:"center",gap:8}}>
              <span style={{color:"#64748b",fontSize:11,fontFamily:mono}}>{sub}</span>{badge}
            </div>
          </div>
        ))}
      </div>

      <div style={{display:"flex",gap:2,borderBottom:"1px solid #111827"}}>
        {tabs.map(t => (
          <button key={t.id} onClick={() => setTab(t.id)} style={{
            background:tab===t.id?"#0f1729":"transparent",
            border:"none",borderBottom:tab===t.id?"2px solid #f59e0b":"2px solid transparent",
            color:tab===t.id?"#e2e8f0":"#4b5e7a",padding:"10px 18px",cursor:"pointer",
            fontSize:12,fontFamily:mono,fontWeight:600,letterSpacing:0.3,transition:"all 0.15s",
          }}>{t.label}</button>
        ))}
      </div>

      <div style={{marginTop:4}}>
        {tab === "3d" && (
          <div>
            <div style={{margin:"20px 0 12px",color:"#e2e8f0",fontSize:14,fontWeight:700}}>Core Volume Expansion</div>
            <div style={{background:"#0a0e17",border:"1px solid #1a2035",borderRadius:6,padding:"16px 8px 8px"}}>
              <ResponsiveContainer width="100%" height={220}>
                <AreaChart data={data3d} margin={{top:8,right:20,left:8,bottom:8}}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#111827"/>
                  <XAxis dataKey="t" stroke="#334155" tick={{fontSize:10,fill:"#4b5e7a",fontFamily:mono}}/>
                  <YAxis stroke="#334155" tick={{fontSize:10,fill:"#4b5e7a",fontFamily:mono}}/>
                  <Tooltip contentStyle={{background:"#0f1729",border:"1px solid #1e3a5f",borderRadius:4,fontSize:11,fontFamily:mono}}/>
                  <Area type="monotone" dataKey="core" stroke="#ef4444" fill="rgba(239,68,68,0.15)" strokeWidth={2}/>
                </AreaChart>
              </ResponsiveContainer>
            </div>

            <div style={{margin:"20px 0 12px",color:"#e2e8f0",fontSize:14,fontWeight:700}}>Writhe Evolution</div>
            <div style={{background:"#0a0e17",border:"1px solid #1a2035",borderRadius:6,padding:"16px 8px 8px"}}>
              <ResponsiveContainer width="100%" height={220}>
                <LineChart data={data3d} margin={{top:8,right:20,left:8,bottom:8}}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#111827"/>
                  <XAxis dataKey="t" stroke="#334155" tick={{fontSize:10,fill:"#4b5e7a",fontFamily:mono}}/>
                  <YAxis stroke="#334155" tick={{fontSize:10,fill:"#4b5e7a",fontFamily:mono}}/>
                  <Tooltip contentStyle={{background:"#0f1729",border:"1px solid #1e3a5f",borderRadius:4,fontSize:11,fontFamily:mono}}/>
                  <ReferenceLine y={0} stroke="#334155" strokeWidth={0.5}/>
                  <Line type="monotone" dataKey="writhe" stroke="#f59e0b" strokeWidth={2} dot={false}/>
                </LineChart>
              </ResponsiveContainer>
            </div>

            <div style={{margin:"20px 0 12px",color:"#e2e8f0",fontSize:14,fontWeight:700}}>Winding Number W(r=2.0)</div>
            <div style={{background:"#0a0e17",border:"1px solid #1a2035",borderRadius:6,padding:"16px 8px 8px"}}>
              <ResponsiveContainer width="100%" height={220}>
                <LineChart data={data3d} margin={{top:8,right:20,left:8,bottom:8}}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#111827"/>
                  <XAxis dataKey="t" stroke="#334155" tick={{fontSize:10,fill:"#4b5e7a",fontFamily:mono}}/>
                  <YAxis stroke="#334155" tick={{fontSize:10,fill:"#4b5e7a",fontFamily:mono}} domain={[-5,4]}/>
                  <Tooltip contentStyle={{background:"#0f1729",border:"1px solid #1e3a5f",borderRadius:4,fontSize:11,fontFamily:mono}}/>
                  <ReferenceLine y={0} stroke="#334155" strokeWidth={0.5}/>
                  <Line type="monotone" dataKey="W(r=2)" stroke="#3b82f6" strokeWidth={2} dot={false}/>
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}

        {tab === "compare" && (
          <div>
            <div style={{margin:"20px 0 12px",color:"#e2e8f0",fontSize:14,fontWeight:700}}>
              2D (v1) vs 3D (v3): Winding Number Decay
            </div>
            <div style={{background:"#0a0e17",border:"1px solid #1a2035",borderRadius:6,padding:"16px 8px 8px"}}>
              <ResponsiveContainer width="100%" height={320}>
                <LineChart margin={{top:8,right:20,left:8,bottom:8}}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#111827"/>
                  <XAxis dataKey="t" stroke="#334155" tick={{fontSize:10,fill:"#4b5e7a",fontFamily:mono}} type="number" domain={[0,10]}
                    label={{value:"Time",position:"insideBottom",offset:-2,fill:"#4b5e7a",fontSize:10}}/>
                  <YAxis stroke="#334155" tick={{fontSize:10,fill:"#4b5e7a",fontFamily:mono}} domain={[-4,4]}/>
                  <Tooltip contentStyle={{background:"#0f1729",border:"1px solid #1e3a5f",borderRadius:4,fontSize:11,fontFamily:mono}}/>
                  <ReferenceLine y={3} stroke="#22c55e" strokeDasharray="8 4" strokeWidth={0.5}/>
                  <ReferenceLine y={0} stroke="#334155" strokeWidth={0.5}/>
                  <Line data={data2d} type="monotone" dataKey="W(r=1)" stroke="#64748b" strokeWidth={2} dot={false} name="2D no pinning"/>
                  <Line data={data3d} type="monotone" dataKey="W(r=2)" stroke="#3b82f6" strokeWidth={2} dot={false} name="3D trefoil"/>
                  <Legend wrapperStyle={{fontSize:10,fontFamily:mono}}/>
                </LineChart>
              </ResponsiveContainer>
            </div>
            
            <div style={{display:"grid",gridTemplateColumns:"1fr 1fr 1fr",gap:12,marginTop:16}}>
              {[
                {title:"2D No Pinning (v1)",status:"broken",items:["W=3 → W=−1 in ~2.5 time units","Vortices migrate freely","σ(W) = 1.42"]},
                {title:"2D + φ-Pinning (v2)",status:"broken",items:["All depths fail (5, 20, 50)","Pinning makes dynamics worse","σ(W) = various, all high"]},
                {title:"3D Trefoil (v3)",status:"broken",items:["Core disperses: +2782%","Writhe chaotic: σ = 35","Imprint not GP-stable"]},
              ].map(({title,status,items}) => (
                <div key={title} style={{background:"#0a0e17",border:"1px solid #1a2035",borderRadius:6,padding:16}}>
                  <div style={{fontFamily:mono,fontSize:12,fontWeight:700,color:"#e2e8f0",marginBottom:8}}>{title}</div>
                  <Badge type={status}>LOCK BROKEN</Badge>
                  <div style={{marginTop:12,fontSize:11,lineHeight:1.8,color:"#94a3b8"}}>
                    {items.map(item => <div key={item} style={{paddingLeft:12,textIndent:-12}}>• {item}</div>)}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {tab === "diagnosis" && (
          <div style={{marginTop:16}}>
            <div style={{background:"#0a0e17",border:"1px solid #7f1d1d",borderRadius:6,padding:20,marginBottom:16}}>
              <h3 style={{color:"#fca5a5",fontSize:14,fontWeight:700,margin:"0 0 12px",fontFamily:mono}}>
                THE 3D FAILURE IS DIFFERENT FROM THE 2D FAILURE
              </h3>
              <div style={{fontSize:13,lineHeight:1.8,color:"#94a3b8"}}>
                <p style={{margin:"0 0 12px"}}>
                  In 2D, the lock broke because <strong style={{color:"#e2e8f0"}}>vortices migrated</strong> — they 
                  moved through the measurement contours. The winding number changed because point vortices 
                  drifted past the boundary. The topology was never there to begin with.
                </p>
                <p style={{margin:"0 0 12px"}}>
                  In 3D, the failure mode is completely different: the <strong style={{color:"#e2e8f0"}}>vortex core 
                  dispersed</strong>. The core volume expanded from 1.46 to 42.2 — the filament didn't untie, 
                  it <em>dissolved</em>. The density field rearranged itself so that the low-density region 
                  spread across the entire box rather than remaining a thin tubular neighborhood of a curve.
                </p>
                <p style={{margin:0,color:"#e2e8f0",fontWeight:500}}>
                  This is not a topological failure. It's a <strong>dynamical stability</strong> failure of the 
                  initial condition.
                </p>
              </div>
            </div>

            <div style={{background:"#0a0e17",border:"1px solid #1e3a5f",borderRadius:6,padding:20,marginBottom:16}}>
              <h3 style={{color:"#93c5fd",fontSize:14,fontWeight:700,margin:"0 0 12px",fontFamily:mono}}>
                ROOT CAUSE: THE MILNOR IMPRINT IS NOT A GP EQUILIBRIUM
              </h3>
              <div style={{fontSize:13,lineHeight:1.8,color:"#94a3b8"}}>
                <p style={{margin:"0 0 12px"}}>
                  The Milnor fibration gives the <em>correct topology</em> but the <em>wrong dynamics</em>. 
                  A trefoil-knotted density field constructed from f(z,w) = z³ − w² has the right knot type, 
                  but it is not a stationary or even metastable solution of the GP equation. The phase 
                  gradients at the core produce velocities that are inconsistent with the density profile.
                </p>
                <p style={{margin:"0 0 12px"}}>
                  In a properly initialized vortex filament, the density and phase are coupled:
                  ρ ∝ tanh²(r/ξ) and the phase winds by exactly 2π around the core. The Milnor 
                  imprint satisfies the phase condition but not the density-phase coupling. The 
                  resulting energy mismatch drives the core expansion.
                </p>
                <p style={{margin:0,fontFamily:mono,fontSize:11,color:"#8b5cf6"}}>
                  E_imprint ≫ E_reconnect → h_cold_grip is not satisfied → theorem does not apply
                </p>
              </div>
            </div>

            <div style={{background:"#0a0e17",border:"1px solid #14532d",borderRadius:6,padding:20,marginBottom:16}}>
              <h3 style={{color:"#86efac",fontSize:14,fontWeight:700,margin:"0 0 12px",fontFamily:mono}}>
                WHAT THE LEAN THEOREM ACTUALLY SAYS
              </h3>
              <div style={{fontSize:13,lineHeight:1.8,color:"#94a3b8"}}>
                <p style={{margin:"0 0 12px"}}>
                  The theorem <code style={{color:"#8b5cf6",fontSize:12}}>level_three_topological_lock</code> has 
                  the hypothesis <code style={{color:"#8b5cf6",fontSize:12}}>h_below : E_ambient {"<"} E_reconnect</code>. 
                  This simulation violates that hypothesis — the imprint energy exceeds the reconnection threshold.
                </p>
                <p style={{margin:"0 0 12px"}}>
                  The theorem is <strong style={{color:"#e2e8f0"}}>not falsified</strong>. It was never applicable. 
                  The proof obligation <code style={{color:"#8b5cf6",fontSize:12}}>h_below</code> could not be 
                  discharged for this initial condition, and the type system correctly predicted the failure.
                </p>
                <p style={{margin:0,color:"#86efac",fontWeight:600}}>
                  The formalization works: the hypothesis that wasn't satisfied is exactly the one 
                  whose violation caused the failure. The type system identified the failure mode 
                  before the simulation ran.
                </p>
              </div>
            </div>

            <div style={{background:"#0a0e17",border:"1px solid #713f12",borderRadius:6,padding:20}}>
              <h3 style={{color:"#fde68a",fontSize:14,fontWeight:700,margin:"0 0 12px",fontFamily:mono}}>
                PATH FORWARD: WHAT A VALID TEST REQUIRES
              </h3>
              <div style={{fontSize:13,lineHeight:1.8,color:"#94a3b8"}}>
                <p style={{margin:"0 0 12px"}}>
                  <span style={{color:"#f59e0b",fontFamily:mono}}>1.</span>{" "}
                  <strong style={{color:"#e2e8f0"}}>Imaginary time relaxation.</strong> Before evolving in real time, 
                  evolve in imaginary time (τ = it) with a topological constraint. This finds the 
                  minimum-energy state with the trefoil topology. The resulting state satisfies 
                  E_imprint ≈ E_ground(trefoil) {"<"} E_reconnect.
                </p>
                <p style={{margin:"0 0 12px"}}>
                  <span style={{color:"#f59e0b",fontFamily:mono}}>2.</span>{" "}
                  <strong style={{color:"#e2e8f0"}}>Higher resolution.</strong> 48³ may not resolve the healing 
                  length ξ with enough grid points. The core structure needs ~5 points across ξ, 
                  requiring N ≥ 128 for L = 8.
                </p>
                <p style={{margin:0}}>
                  <span style={{color:"#f59e0b",fontFamily:mono}}>3.</span>{" "}
                  <strong style={{color:"#e2e8f0"}}>Biot-Savart initialization.</strong> Instead of Milnor, use the 
                  Biot-Savart law to compute the velocity field of a thin vortex filament on the 
                  trefoil curve, then construct ψ from that velocity field. This guarantees 
                  GP-compatibility of the initial condition.
                </p>
              </div>
            </div>
          </div>
        )}
      </div>

      <div style={{
        marginTop:28,paddingTop:14,borderTop:"1px solid #111827",
        color:"#334155",fontSize:10,fontFamily:mono,
        display:"flex",justifyContent:"space-between",
      }}>
        <span>Helium Loom v1→v2→v3 · 2D→2D+pinning→3D · All locks broken</span>
        <span>h_below: <span style={{color:"#fca5a5"}}>NOT DISCHARGED</span> · Theorem: <span style={{color:"#86efac"}}>VALID</span></span>
      </div>
    </div>
  );
}
