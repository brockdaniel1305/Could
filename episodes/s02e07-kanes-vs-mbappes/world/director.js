// S2E07 "Could 11 Kanes beat 11 Mbappés?" - the 2026 Ballon d'Or debate (Kane won by 28 points) settled on the pitch.
// Thread: Kane lifts the Ballon d'Or, Mbappé jumps for it and is 28 points short; Mbappé sprints through all eleven Kanes (0-1);
// all eleven Kanes drop deep, Kane plays a long ball to himself (1-1); minute 90 penalty - Kane puts the golden ball on the spot,
// short 2022 flashback (ball into the stands, POP!), the Mbappés can't look, freeze as the ball flies -> comments decide.
// Mbappés attack -x (Kane goal at x = -52.5), Kanes attack +x (Mbappé goal at x = 52.5).
// Gags: trophy out of reach, turnstile Kanes, linesman too late, all eleven in midfield, pass to himself, Mbappés don't defend,
// golden ball on the penalty spot, popcorn flashback, Mbappés can't look.
import { path, sstep, clamp, lerp } from "./engine.js";

export default function plot(T) {
  const c = (k) => { if (!(k in T.cue)) throw new Error("cue " + k); return T.cue[k]; };
  const s = (k) => T.start[k];
  const END = T.duration, CUT = 1.3, LOOPJ = c("s8.loop") - 0.5;

  const RUN0 = c("s4.run") + 0.1, RUN1 = c("s4.nil") - 0.75, G1 = c("s4.nil") - 0.1;           // Mbappé sprints through everyone, 0-1
  const LB = c("s6.long") + 0.1, LAND = c("s6.self") - 0.1, G2 = c("s6.eq") - 0.1;            // long ball to himself, 1-1
  const PEN = c("s7.pen"), FB = c("s7.last"), FBE = FB + 2.75;                                  // penalty, 2022 flashback
  const KICK = c("s8.but") + 1.35;                                                               // the kick that freezes in the air
  const SPOT = [41.5, 0, 0];

  const W = {}, names = [];
  for (let i = 0; i < 11; i++) names.push("K" + i, "M" + i);
  names.push("REF", "LIN");
  names.forEach((n) => (W[n] = []));
  const at = (n, t, x, z, e) => W[n].push([t, x, z, e]);
  const idx = (n) => (n === "REF" || n === "LIN" ? -1 : +n.slice(1));
  const jumpAll = (t, f) => names.forEach((n) => { const p = f(n, idx(n), n[0] === "K"); if (p) at(n, t, p[0], p[1], "j"); });
  const LZ = (i) => -9 + i * 1.8;

  // hook: Mbappé M10 sprints at the camera with the ball, Kane K9 in the foreground
  const HOOKPOS = (n, i, kk) => (n === "M10" ? [-6.4, 0.2] : n === "K9" ? [-3.6, -1.1] : n === "REF" ? [-14, 10] : n === "LIN" ? [-10, -34.2] :
    kk ? [-16 - i * 1.4, (i % 2 ? 1 : -1) * (5 + i)] : [-22 - i * 1.3, (i % 2 ? -1 : 1) * (4 + i)]);
  names.forEach((n) => { const [x, z] = HOOKPOS(n, idx(n), n[0] === "K"); at(n, 0, x, z); });
  at("M10", CUT, -2.6, 0.25, "l");
  jumpAll(CUT + 0.01, (n, i, kk) => (n === "REF" ? [0, -9.5] : n === "LIN" ? [0, -34.2] : [kk ? -1.6 : 1.6, LZ(i)]));
  // s2: the Ballon d'Or - Kane lifts it, Mbappé jumps for it; both teams in rows behind them
  jumpAll(s("s2") - 0.05, (n, i, kk) => (n === "K9" ? [-0.75, 0] : n === "M10" ? [0.95, 0.15] : n === "REF" ? [6, -8] : n === "LIN" ? [0, -34.2] :
    kk ? [-1.8 - (i % 5) * 1.35, -3.2 - (i > 5 ? 1.7 : 0) - (i % 2) * 0.3] : [1.9 + (i % 5) * 1.35, -3.2 - (i > 5 ? 1.7 : 0) - (i % 2) * 0.3]));
  // s3: kick-off formation
  const KO = (n, i, kk) => (n === "M10" ? [0.6, 0] : n === "K9" ? [-1.4, 1.8] : n === "K0" ? [-51.6, 0] : n === "M0" ? [51.6, 0] : n === "REF" ? [-4, 9] :
    n === "LIN" ? [0, -34.2] : kk ? [-5 - (i % 4) * 3.2, ((i % 3) - 1) * 6 + (i % 2) * 1.5] : [6 + (i % 4) * 3.2, ((i % 3) - 1) * 6 - (i % 2) * 1.5]);
  jumpAll(s("s3") - 0.3, KO);
  // s4: Mbappé sprints through all eleven Kanes, lined up across his path; the linesman is too late
  const LANE = [-4, -8, -12, -16, -20, -24, -28, -32, -36, -41];
  const LANEK = ["K1", "K2", "K3", "K4", "K5", "K6", "K7", "K8", "K9", "K10"];
  jumpAll(s("s4") - 0.3, (n, i, kk) => (n === "M10" ? [0.6, 0] : n === "K0" ? [-51.6, 0] : n === "M0" ? [51.6, 0] : n === "REF" ? [-10, 10] :
    n === "LIN" ? [-38.5, -34.2] : kk ? [LANE[LANEK.indexOf(n)], (i % 2 ? 1 : -1) * 0.8] : [6 + i * 1.6, (i % 2 ? 1 : -1) * (5 + i)]));
  at("M10", RUN0, 0.6, 0); at("M10", RUN1, -46.4, 0.2, "i"); at("M10", G1 + 0.9, -49, 2.6, "o");
  const PASSAT = (x) => RUN0 + ((0.6 - x) / 47) * (RUN1 - RUN0);
  // s5: face to face on halfway
  jumpAll(s("s5") - 0.3, (n, i, kk) => (n === "K9" ? [-0.7, 0] : n === "M10" ? [0.7, 0] : n === "REF" ? [0, -3] : n === "LIN" ? [0, -34.2] :
    kk ? [-6 - i, (i % 2 ? 1 : -1) * (5 + i)] : [6 + i, (i % 2 ? 1 : -1) * (5 + i)]));
  // s6: all eleven Kanes drop deep into one cluster; the Mbappés wait on halfway; long ball - and Kane runs onto it himself
  const CL = (i) => [-2.6 + Math.cos(i * 2.1) * (1 + (i % 3) * 0.9), Math.sin(i * 2.1) * (1 + (i % 3) * 0.9)];
  jumpAll(s("s6") - 0.3, (n, i, kk) => (n === "K9" ? [-1.9, 0.3] : n === "K0" ? [-6.5, -2.2] : n === "M0" ? [51.6, 0] : n === "REF" ? [-8, 9] :
    n === "LIN" ? [10, -34.2] : kk ? CL(i) : [4.2 + (i % 3) * 1.6, -7 + i * 1.4]));
  at("K9", LB + 0.05, -1.9, 0.3); at("K9", LB + 0.4, 4.5, 0.6, "i"); at("K9", LB + 0.45, 33.0, 2.5, "j"); at("K9", LAND, 35.9, 2.0, "o");
  at("K9", G2 - 0.35, 37.2, 1.4); at("K9", G2 + 0.9, 41, 4.2, "o");
  // s7: penalty - Kane, the referee and the golden ball; Mbappés in two groups beside the box
  const PENPOS = (n, i, kk) => (n === "K9" ? [40.2, 0.6] : n === "M0" ? [52.1, 0] : n === "K0" ? [-51.6, 0] : n === "REF" ? [44.6, 3.6] :
    n === "LIN" ? [40, -34.2] : kk ? [33 - (i % 4) * 1.5, (i % 2 ? 1 : -1) * (16 + (i % 3) * 1.5)] :
    [37 + (i % 5) * 1.1, (i % 2 ? -1 : 1) * (10.2 + (i % 3) * 0.9)]);
  jumpAll(s("s7") - 0.3, PENPOS);
  at("REF", PEN + 0.1, 44.6, 3.6); at("REF", PEN + 0.75, 42.3, 0.9, "s"); at("REF", PEN + 1.25, 42.3, 0.9); at("REF", PEN + 2.1, 42.6, 3.2, "s");
  at("K9", FB + 0.15, 40.2, 0.6); at("K9", FB + 0.55, 41.1, 0.15, "i"); at("K9", FBE - 0.05, 41.4, 0.1);   // 2022: the run-up
  at("K9", FBE, 40.2, 0.6, "j");
  // s8: the run-up, the kick ... freeze
  at("K9", KICK - 0.45, 40.2, 0.6); at("K9", KICK, 41.1, 0.15, "i");
  // loop
  names.forEach((n) => { const [x, z] = HOOKPOS(n, idx(n), n[0] === "K"); at(n, LOOPJ, x - (n === "M10" ? 3.8 * (END - LOOPJ) / CUT : 0), z, "j"); at(n, END, x, z, "l"); });
  for (const n of names) W[n].sort((p, q) => p[0] - q[0]);

  const A = {};
  for (const n of names) {
    const kk = n[0] === "K", i = idx(n), ev = [];
    if (n === "M10") {
      ev.push(["charge", 0, CUT]);
      for (let k = 0; k < 6; k++) ev.push(["jump", c("s2.won") + 0.3 + k * 0.62, 0.38]);                     // jumping for the trophy
      ev.push(["armsUp", c("s2.won") + 0.25, s("s3") - c("s2.won") - 0.4], ["charge", RUN0, RUN1 - RUN0], ["armsUp", G1 + 0.15, 1.4]);
    }
    if (n === "K9") ev.push(["armsUp", c("s2.won"), s("s3") - c("s2.won") - 0.4], ["charge", LB + 0.7, LAND - LB - 0.7], ["armsUp", G2 + 0.15, 1.4]);
    if (LANEK.includes(n)) ev.push(["spin", PASSAT(LANE[LANEK.indexOf(n)]) - 0.05, 0.7]);
    if (n === "K0") ev.push(["dive", G1 - 0.25, 1, -1], ["up", G1 + 1.2]);
    if (n === "M0") ev.push(["dive", G2 - 0.2, 1, 1], ["up", G2 + 1.2], ["dive", KICK + 0.1, 1, -1]);
    if (n === "M7") ev.push(["yawn", c("s6.deep") + 0.6, 1.8]);
    if (n === "M5") ev.push(["cross", c("s6.deep") + 0.4, 2.2]);
    if (!kk && i >= 1 && i !== 10) ev.push(["armsUp", c("s8.but") - 0.1, END - c("s8.but")]);                // hands on heads: can't look
    if (n === "LIN") ev.push(["armR", PASSAT(-37) + 0.35, 1.4]);
    if (n === "REF") ev.push(["armR", PEN - 0.1, 0.8]);
    A[n] = { path: W[n], ev, h: kk ? 1.88 : 1.78, unit: 360, stride: kk ? 2.0 : 2.2 };
  }

  // ---------------- ball ----------------
  const ball = [
    { t0: 0, k: "at", who: "M10", dx: 0.55, dz: 0.1 },
    { t0: CUT + 0.01, k: "rest", p: [0, 0, 0.6] },
    { t0: s("s2") - 0.05, k: "rest", p: [0, -50, 0] },
    { t0: s("s3") - 0.3, k: "rest", p: [0.05, 0, 0] },
    { t0: c("s3.ko"), k: "at", who: "M10", dx: -0.55, dz: 0.1 },
    { t0: RUN1, t1: G1, k: "fly", a: [-47, 0, 0.2], b: [-52.8, 0.9, 1.8], h: 0.3 },
    { t0: G1, k: "rest", p: [-53.2, 0.1, 1.8] },
    { t0: s("s5") - 0.3, k: "rest", p: [0, 0, 0.3] },
    { t0: s("s6") - 0.3, k: "at", who: "K9", dx: 0.55, dz: 0.1 },
    { t0: LB, t1: LAND, k: "fly", a: [-1.3, 0, 0.4], b: [36.4, 0, 2.0], h: 17, ease: "s" },
    { t0: LAND, k: "at", who: "K9", dx: 0.55, dz: 0.05 },
    { t0: G2 - 0.35, t1: G2, k: "fly", a: [37.8, 0, 1.4], b: [52.8, 1.0, -2.0], h: 0.4 },
    { t0: G2, k: "rest", p: [53.2, 0.1, -2.0] },
    { t0: s("s7") - 0.3, k: "rest", p: [0, -50, 0] },
    { t0: PEN + 1.05, k: "rest", p: SPOT },
    { t0: FB + 0.55, t1: FB + 2.0, k: "fly", a: SPOT, b: [64, 15, -3.5], h: 2 },
    { t0: FB + 2.0, k: "rest", p: [0, -50, 0] },
    { t0: FBE, k: "rest", p: SPOT },
    { t0: KICK, t1: KICK + 0.3, k: "fly", a: SPOT, b: [46.2, 1.15, -0.9], h: 0.15 },
    { t0: KICK + 0.3, k: "rest", p: [46.2, 1.15, -0.9] },                                                // freeze
    { t0: LOOPJ, k: "at", who: "M10", dx: 0.55, dz: 0.1 },
  ];

  // ---------------- the golden ball (prop) ----------------
  const PS = {}; const pos = (n, t) => { const p = (PS[n] = PS[n] || path(A[n].path))(t); return [p.x, p.z]; };
  const props = {
    bdor: { h: 0.7, unit: 165, only: [0, END], at: (t) => {
      if (t < s("s2") - 0.05 || t >= LOOPJ) return [-14, 0, -2.6];
      if (t < c("s2.won")) return [0.1, 0, 0.8];
      if (t < s("s3") - 0.3) { const k = pos("K9", t), f = sstep(c("s2.won"), c("s2.won") + 0.35, t); return [lerp(0.1, k[0] + 0.05, f), lerp(0, 2.05, f), lerp(0.8, k[1] + 0.05, f)]; }
      if (t < PEN - 0.4) return [0, -60, 0];
      if (t < PEN + 1.25) return SPOT;
      if (t < PEN + 2.1) { const r = pos("REF", t); return [r[0] + 0.35, 1.0, r[1] + 0.1]; }
      return [41.7, 0, 2.2];
    } },
  };

  // ---------------- camera ----------------
  const sh = [], add = (o) => sh.push(o);
  const HOOKCAM = { k: "path", P: [[1.4, 0.85, 0.5], [1.4, 0.85, 0.5]], T: [[-5, 1.4, 0], [-5, 1.4, 0]], fov: [46, 46], roll: 5, blur: 2.2 };
  add({ t0: 0, ...HOOKCAM });
  add({ t0: CUT, k: "path", P: [[0, 1.2, 12], [0, 1.25, 11]], T: [[0, 1.7, 0], [0, 1.7, 0]], fov: [50, 46], blur: 1.4 });
  add({ t0: s("s2") + 0.05, whip: true, k: "path", P: [[0.1, 1.65, 7.8], [0.1, 1.65, 6.9]], T: [[0.1, 1.8, 0], [0.1, 1.85, 0]], fov: [44, 40], blur: 2.2 });
  add({ t0: s("s3") + 0.05, blend: 0.5, whip: true, k: "path", P: [[4.6, 1.9, 1.4], [4.0, 1.9, 1.1]], T: [[-6, 1.0, -0.6], [-6, 1.0, -0.6]], fov: [50, 48], blur: 1.4 });
  add({ t0: RUN0 - 0.05, blend: 0.3, k: "follow", who: "M10", off: [[0.6, 1.4, 6.0], [0.5, 1.4, 5.6]], look: [-0.4, 1.2, 0], fov: [50, 50], blur: 1.8 });
  add({ t0: PASSAT(-37) - 0.25, whip: true, k: "path", P: [[-36.6, 1.55, -36.8], [-36.9, 1.55, -36.8]], T: [[-40.5, 1.35, -30.2], [-40.7, 1.35, -30]], fov: [48, 46], blur: 1.4 });
  add({ t0: RUN1 - 0.05, blend: 0.25, k: "path", P: [[-46.5, 1.6, -8.5], [-47.5, 1.8, -8]], T: [[-53, 1.3, 1.5], [-52.5, 1.3, 1.5]], fov: [48, 44], blur: 1.4 });
  add({ t0: s("s5") + 0.05, blend: 0.4, whip: true, k: "path", P: [[0, 1.55, 4.2], [0, 1.6, 3.4]], T: [[0, 1.65, 0], [0, 1.7, 0]], fov: [48, 42], blur: 2.4 });
  add({ t0: c("s6.deep") - 0.1, blend: 0.45, whip: true, k: "path", P: [[-6.5, 7.5, 9.5], [-6, 7, 9]], T: [[-1.2, 0, -0.6], [-1, 0, -0.6]], fov: [54, 52], blur: 0.6 });
  add({ t0: c("s6.deep") + 0.75, blend: 0.35, whip: true, k: "path", P: [[3.4, 1.5, 6.4], [3.6, 1.5, 5.6]], T: [[3.6, 1.3, -1], [3.6, 1.3, -1]], fov: [48, 44], blur: 2.0 });
  add({ t0: LB - 0.35, blend: 0.3, whip: true, k: "path", P: [[-5.6, 1.4, 2.6], [-5.8, 1.5, 2.8]], T: [[2, 1.6, 0], [3, 2.2, 0]], fov: [50, 52], blur: 1.8 });
  add({ t0: LB + 0.5, whip: true, k: "path", P: [[30.8, 1.5, 7.4], [31.4, 1.5, 7.0]], T: [[34.5, 1.3, 1.8], [36.6, 1.3, 1.4]], fov: [48, 46], blur: 1.8 });
  add({ t0: G2 - 0.2, blend: 0.2, k: "path", P: [[46.5, 1.6, 8.5], [47.5, 1.8, 8]], T: [[53, 1.1, -1.5], [52.5, 1.3, -1.5]], fov: [48, 44], blur: 1.4 });
  add({ t0: c("s7.min") - 0.1, blend: 0.4, whip: true, k: "path", P: [[37.6, 1.65, 2.5], [38.2, 1.65, 2.1]], T: [[41, 1.6, 0], [41, 1.6, 0]], fov: [44, 38], blur: 2.4 });
  add({ t0: PEN - 0.05, blend: 0.3, k: "path", P: [[37.2, 1.1, 4.3], [37.4, 1.1, 4.1]], T: [[41.6, 0.9, 0.6], [41.7, 0.9, 0.6]], fov: [48, 46], blur: 1.8 });
  add({ t0: FB - 0.05, whip: true, k: "path", P: [[35.6, 1.6, 2.3], [36.2, 2.6, 2.6]], T: [[50, 2.0, 0], [57, 8.5, -1.5]], fov: [50, 54], blur: 1.0 });
  add({ t0: FBE, whip: true, k: "path", P: [[37.6, 1.5, 9.0], [37.8, 1.5, 8.4]], T: [[41.0, 1.0, 1.3], [41.0, 1.0, 1.3]], fov: [42, 38], blur: 2.0 });
  add({ t0: c("s8.but") - 0.05, blend: 0.3, whip: true, k: "path", P: [[40.6, 1.55, -4.6], [40.4, 1.55, -5.2]], T: [[39, 1.4, -11], [39, 1.4, -11]], fov: [48, 44], blur: 2.0 });
  add({ t0: KICK - 0.55, whip: true, k: "path", P: [[35.8, 1.5, 2.5], [36.2, 1.5, 2.3]], T: [[47, 1.2, -0.4], [47, 1.25, -0.4]], fov: [46, 44], blur: 1.6 });
  add({ t0: c("s8.loop") - 0.3, blend: 0.3, whip: true, ...HOOKCAM });
  sh.forEach((x, i) => { x.t1 = x.t1 ?? (sh[i + 1] ? sh[i + 1].t0 : END); });
  sh[sh.length - 1].t1 = END;

  // ---------------- overlays ----------------
  const chip = (id, t0, t1, kk, v, x, y, cls = "", from = "right") => ({ id, t0, t1, from, cls: "chip " + cls, style: `left:${x}px;top:${y}px`,
    html: `<div class="ck">${kk}</div><div class="cv">${v}</div>` });
  const slam = (id, t0, t1, html, top, size = 128) => ({ id, t0, t1, slam: true, cls: "slam", style: `top:${top}px;font-size:${size}px`, html });
  const lower = (id, t0, who, min) => chip(id, t0, t0 + 1.4, "GOAL · " + min, who, 60, 560, "dark", "left");
  const overlays = [
    slam("sl-a", -1, s("s2") - 0.05, "11 KANES<br><b>vs.</b> 11 MBAPPÉS", 340, 100),
    { id: "votes", t0: c("s2.bd"), t1: s("s3") - 0.05, cls: "votes", style: "top:250px",
      html: `<div class="hd">BALLON D'OR 2026 · VOTES</div>
        <div class="row"><span class="nm">KANE</span><div class="bar" id="vbk" style="width:0px;background:#f4f4f2"></div><span class="pt" id="vpk">0</span></div>
        <div class="row"><span class="nm">MBAPPÉ</span><div class="bar" id="vbm" style="width:0px;background:#4f7bff"></div><span class="pt" id="vpm">0</span></div>` },
    chip("c-fast", RUN0 + 0.2, PASSAT(-37) - 0.3, "TOP SPEED", "≈ 36 km/h", 120, 400, "red"),
    lower("g1", G1 + 0.3, "Mbappé (sprint)", "9'"),
    lower("g2", G2 + 0.3, "Kane (assist: Kane)", "27'"),
    { id: "flash", t0: FB - 0.05, t1: FBE, cls: "flash", html: "" },
    { id: "flashlbl", t0: FB, t1: FBE, cls: "flashlbl", html: "2022" },
    slam("pop", FB + 1.95, FBE, "POP! 🍿", 560, 150),
    chip("c-who", c("s8.who"), LOOPJ, "COMMENT", "Who will win?", 120, 460, "red"),
    { id: "hud", t0: c("s3.ko") - 0.1, t1: LOOPJ, cls: "hud", style: "opacity:0",
      html: `<span class="t">KAN</span><span class="sc"><b id="hs">0</b>–<b id="as">0</b></span><span class="t">MBA</span><span class="mn" id="mn">1'</span>` },
    slam("sl-end", END - 0.3, END + 1, "11 KANES<br><b>vs.</b> 11 MBAPPÉS", 340, 100),
  ];
  const bubbles = [
    { who: "M10", t0: c("s2.sec"), t1: s("s3") - 0.1, text: "28?!", cls: "dark" },
    { who: "LIN", t0: PASSAT(-37) + 0.5, t1: RUN1 - 0.1, text: "?!", cls: "" },
    { who: "REF", t0: c("s5.follow") + 0.05, t1: c("s5.q") - 0.05, text: "♥ LIKE + FOLLOW +", cls: "red follow" },
    { who: "K9", t0: c("s5.q"), t1: s("s6") - 0.1, text: "KANE?", cls: "" },
    { who: "M10", t0: c("s5.q") + 0.3, t1: s("s6") - 0.1, text: "MBAPPÉ?", cls: "dark" },
    { who: "K4", t0: c("s6.deep") + 0.15, t1: c("s6.deep") + 0.8, text: "WHO'S UP FRONT?", cls: "" },
    { who: "M7", t0: c("s6.deep") + 0.85, t1: LB - 0.4, text: "NOT MY JOB", cls: "dark" },
    { who: "K9", t0: LAND - 0.05, t1: G2 + 0.1, text: "THANKS, ME", cls: "" },
    { who: "REF", t0: PEN + 0.45, t1: PEN + 1.9, text: "WRONG BALL!", cls: "red" },
    { who: "M7", t0: c("s8.but") + 0.1, t1: KICK - 0.6, text: "CAN'T LOOK!", cls: "dark small" },
    { who: "M1", t0: c("s8.but") + 0.35, t1: KICK - 0.6, text: "NOPE", cls: "small" },
  ];
  const bursts = [{ who: "M10", t: RUN0 + 0.05, text: "ZOOM!" }, { who: "K9", t: LB, text: "BOOM!" }];
  const minute = (t) => t >= c("s7.min") ? "90'" : t >= s("s6") ? "27'" : t >= s("s4") ? "9'" : "1'";
  const sepia = (t) => t >= FB - 0.05 && t < FBE;

  return {
    actors: A, ball, shots: sh, overlays, bubbles, bursts, props,
    grade: "contrast(1.14) saturate(1.2) brightness(0.95)",
    nets: { left: [G1], right: [G2] }, shake: [G1, G2],
    crowd: (t) => [G1, G2].some((g) => t > g && t < g + 2.6) ? 0.5 : t > RUN0 && t < G1 ? 0.3 : 0.1,
    flashes: (t) => ([G1, G2].some((g) => t > g && t < g + 2) ? 0.3 : 0.05),
    speedlines: (t) => Math.max(0.55 * (1 - sstep(CUT - 0.1, CUT + 0.1, t)), 0.55 * sstep(END - 0.35, END - 0.2, t),
      0.45 * sstep(RUN0, RUN0 + 0.2, t) * (1 - sstep(RUN1, RUN1 + 0.3, t)), 0.35 * sstep(LB + 0.6, LB + 0.8, t) * (1 - sstep(LAND, LAND + 0.2, t))),
    custom: (t, { el }) => {
      const kv = sstep(c("s2.won") - 0.2, c("s2.won") + 0.6, t), mv = sstep(c("s2.pts") - 0.2, c("s2.pts") + 0.6, t);
      const strain = t > c("s2.sec") ? 1 + Math.abs(Math.sin(t * 9)) * 0.012 : 1;                        // Mbappé's bar straining upwards
      el("vbk").style.width = (520 * kv).toFixed(0) + "px"; el("vpk").textContent = String(Math.round(1055 * kv));
      el("vbm").style.width = (520 * (1027 / 1055) * mv * strain).toFixed(0) + "px"; el("vpm").textContent = String(Math.round(1027 * mv));
      el("hs").textContent = String(t >= G2 ? 1 : 0);
      el("as").textContent = String(t >= G1 ? 1 : 0);
      el("mn").textContent = sepia(t) ? "2022" : minute(t);
      let pop = 0; for (const g of [G1, G2]) if (t >= g && t < g + 0.3) pop = Math.sin(((t - g) / 0.3) * Math.PI);
      el("hud").style.transform = `scale(${1 + pop * 0.15})`;
    },
  };
}
