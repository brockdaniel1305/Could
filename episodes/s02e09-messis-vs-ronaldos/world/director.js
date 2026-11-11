// S2E09 "Could 11 Messis beat 11 Ronaldos?" - the GOAT debate as a Clásico: prime Messi (Barça 2012) vs prime Ronaldo (Real 2014).
// Thread: Ronaldo's free-kick stance (legs wide). The Ronaldos take it mid-game - Messi nutmegs all eleven, the keeper too (1-0);
// Ronaldo's 2.5 m header (1-1), eleven Siuus at once shake the stadium, "calma"; minute 92 Messi wins it and all eleven show their
// shirts; last chance: Ronaldo free kick in the stance, freeze -> comments decide.
// Messis attack +x (Ronaldo goal at x = 52.5), Ronaldos attack -x (Messi goal at x = -52.5).
import { path, sstep, clamp, lerp } from "./engine.js";

export default function plot(T) {
  const c = (k) => { if (!(k in T.cue)) throw new Error("cue " + k); return T.cue[k]; };
  const s = (k) => T.start[k];
  const END = T.duration, CUT = 1.3, LOOPJ = c("s11.loop") - 0.5;

  const RUN0 = c("s5.mistake") + 0.25, RUN1 = c("s5.one") - 0.55, G1 = c("s5.one") - 0.1;     // eleven nutmegs, 1-0
  const H = c("s7.eq") - 0.75, G2 = c("s7.eq") - 0.1;                                           // the 2.5 m header, 1-1
  const SIUU = c("s8.same") + 0.15, LAND = SIUU + 0.62;                                         // eleven Siuus
  const SHOT3 = c("s10.messi") + 0.15, G3 = c("s10.win") - 0.1;                                 // minute 92, 2-1
  const FKK = c("s11.who") - 0.1;                                                                // the last free kick, freeze

  const W = {}, names = [];
  for (let i = 0; i < 11; i++) names.push("M" + i, "R" + i);
  names.push("REF");
  names.forEach((n) => (W[n] = []));
  const at = (n, t, x, z, e) => W[n].push([t, x, z, e]);
  const idx = (n) => (n === "REF" ? -1 : +n.slice(1));
  const jumpAll = (t, f) => names.forEach((n) => { const p = f(n, idx(n), n[0] === "M"); if (p) at(n, t, p[0], p[1], "j"); });
  const LZ = (i) => -9 + i * 1.8;
  const ROWS = (i, side) => [side * (1.9 + (i % 5) * 1.35), -3.2 - (i > 5 ? 1.7 : 0) - (i % 2) * 0.3];

  // hook: Ronaldo R7 in his free-kick stance, Messi M10 slips the ball through his legs
  const HOOKPOS = (n, i, mm) => (n === "R7" ? [-2.5, -0.25] : n === "M10" ? [-7.0, 0.35] : n === "REF" ? [-14, 10] :
    mm ? [-16 - i * 1.4, (i % 2 ? 1 : -1) * (5 + i)] : [-22 - i * 1.3, (i % 2 ? -1 : 1) * (4 + i)]);
  names.forEach((n) => { const [x, z] = HOOKPOS(n, idx(n), n[0] === "M"); at(n, 0, x, z); });
  at("M10", CUT, -3.4, 0.3, "l");
  jumpAll(CUT + 0.01, (n, i, mm) => (n === "REF" ? [0, -9.5] : [mm ? 1.6 : -1.6, LZ(i)]));
  // s2 / s3: the two line-ups, Messi and Ronaldo in front
  jumpAll(s("s2") - 0.05, (n, i, mm) => (n === "M10" ? [0.95, 0] : n === "R7" ? [-0.95, 0.05] : n === "REF" ? [0, -2.4] :
    mm ? ROWS(i === 10 ? 7 : i, 1) : ROWS(i === 7 ? 10 : i, -1)));
  // s4: kick-off - the Ronaldos line up in their stance, one behind the other, between Messi and their goal
  const LANE = [6, 9.5, 13, 16.5, 20, 23.5, 27, 30.5, 34, 37.5];
  const LANER = ["R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "R10"];
  jumpAll(s("s4") - 0.05, (n, i, mm) => (n === "M10" ? [1.2, 0] : n === "R0" ? [51.8, 0] : n === "M0" ? [-51.6, 0] : n === "REF" ? [-4, 8] :
    !mm ? [LANE[LANER.indexOf(n)], 0] : [-4 - (i % 4) * 3, ((i % 3) - 1) * 8]));
  at("M10", RUN0, 1.2, 0); at("M10", RUN1, 46.2, 0.15, "i"); at("M10", G1 + 0.9, 48.5, 3.2, "o");
  const PASSAT = (x) => RUN0 + ((x - 1.2) / 45) * (RUN1 - RUN0);
  // s6: face to face on halfway
  jumpAll(s("s6") - 0.3, (n, i, mm) => (n === "M10" ? [0.7, 0] : n === "R7" ? [-0.7, 0] : n === "REF" ? [0, -3] : mm ? [6 + i, (i % 2 ? 1 : -1) * (5 + i)] : [-6 - i, (i % 2 ? 1 : -1) * (5 + i)]));
  // s7: cross from the left wing, Ronaldo rises above the Messis
  jumpAll(s("s7") - 0.05, (n, i, mm) => (n === "R7" ? [-44.6, 0.4] : n === "R3" ? [-47.5, -24] : n === "M0" ? [-51.6, 0] : n === "M3" ? [-45.6, 1.4] :
    n === "M5" ? [-45.2, -0.9] : n === "M8" ? [-47.4, 1.2] : n === "REF" ? [-36, 10] : n === "R0" ? [51.6, 0] :
    mm ? [-42 + (i % 4) * 2.4, (i % 2 ? -1 : 1) * (4 + i * 0.8)] : [-38 + (i % 4) * 2.6, (i % 2 ? 1 : -1) * (6 + i * 0.7)]));
  at("R7", H - 0.6, -43.4, 0.5); at("R7", H, -45.8, 0.3, "i"); at("R7", G2 + 0.6, -45, 2.2, "o");
  // s8 / s9: all eleven Ronaldos in one diagonal row, a few Messis and the referee next to them
  const ROW = (k) => [-4.4 - 1.5 * k, 5.5 - 0.12 * k];
  const ORDER = ["R7", "R1", "R2", "R3", "R4", "R5", "R6", "R8", "R9", "R10", "R0"];
  jumpAll(s("s8") - 0.05, (n, i, mm) => (ORDER.includes(n) ? ROW(ORDER.indexOf(n)) : n === "REF" ? [-6.0, 3.0] : n === "M3" ? [-3.0, 8.0] :
    n === "M8" ? [-2.2, 6.6] : mm ? [8 + i, -6 - i] : [0, 0]));
  // s10: minute 92 - Messi from the edge of the box; then all Messis show their shirts
  jumpAll(s("s10") - 0.05, (n, i, mm) => (n === "M10" ? [35.6, 5.6] : n === "R0" ? [51.6, 0] : n === "M0" ? [-51.6, 0] : n === "REF" ? [30, -8] :
    mm ? [24 + (i % 4) * 3, ((i % 3) - 1) * 9] : [42 + (i % 3) * 2.2, ((i % 4) - 1.5) * 4.2]));
  at("M10", SHOT3 - 0.5, 35.6, 5.6); at("M10", SHOT3, 37.0, 4.6, "i");
  const SHIRTPOS = (i) => [38.6 + ((i - 1) % 5) * 1.25 - (i > 5 ? 0.6 : 0), 7.4 - (i > 5 ? 1.6 : 0)];
  jumpAll(c("s10.shirt") - 0.2, (n, i, mm) => (mm && i >= 1 && i <= 9 ? SHIRTPOS(i) : n === "M10" ? [41.2, 9.2] : null));
  // s11: last chance - Ronaldo's free kick, a wall of Messis
  const WALL = (k) => [-37.0 - k * 0.12, 3.2 - (k - 2) * 0.62];
  jumpAll(s("s11") - 0.3, (n, i, mm) => (n === "R7" ? [-27.6, 6.8] : n === "M0" ? [-51.8, 0] : n === "R0" ? [51.6, 0] : n === "REF" ? [-31, 11] :
    mm && i >= 1 && i <= 5 ? WALL(i - 1) : mm ? [-42 - (i % 3) * 2, -4 + (i % 4) * 3] : [-40 - (i % 4) * 2.2, -6 - (i % 3) * 3]));
  at("R7", FKK - 0.5, -27.6, 6.8); at("R7", FKK, -28.8, 6.1, "i");
  // loop
  names.forEach((n) => { const [x, z] = HOOKPOS(n, idx(n), n[0] === "M"); const dx = n === "M10" ? 3.6 : 0;
    at(n, LOOPJ, x - dx * (END - LOOPJ) / CUT, z, "j"); at(n, END, x, z, "l"); });
  for (const n of names) W[n].sort((p, q) => p[0] - q[0]);

  const A = {};
  for (const n of names) {
    const mm = n[0] === "M", i = idx(n), ev = [];
    if (n === "R7") ev.push(["stance", 0, CUT], ["arms", c("s3.pr") + 0.2, s("s4") - c("s3.pr") - 0.4, 95],
      ["leap", H - 0.5, 1.0, 1.35], ["armsUp", G2 + 0.1, 1.0], ["stance", c("s11.last"), FKK - 0.5 - c("s11.last")], ["stance", LOOPJ, END - LOOPJ + 0.1]);
    if (n === "M10") ev.push(["charge", 0, CUT], ["charge", RUN0, RUN1 - RUN0], ["armsUp", G1 + 0.1, 1.3], ["charge", SHOT3 - 0.5, 0.5]);
    if (!mm) ev.push(["stance", c("s4.stance") + 0.1 + (i % 4) * 0.08, (n === "R0" ? G1 + 0.4 : PASSAT(LANE[LANER.indexOf(n)] ?? 50) + 0.5) - c("s4.stance")]);
    if (LANER.includes(n)) ev.push(["spin", PASSAT(LANE[LANER.indexOf(n)]) + 0.1, 0.5]);
    if (n === "R0") ev.push(["dive", G1 + 0.15, 1, 1], ["up", G1 + 1.4]);
    if (!mm && n !== "R0" || n === "R0") ev.push(["spin", SIUU, 0.55], ["leap", SIUU, 0.62, 1.15], ["arms", LAND, 1.0, 50],
      ["arms", c("s9.calma") + 0.25, s("s10") - c("s9.calma") - 0.35, 40]);
    if (n === "M3" || n === "M5" || n === "M8") ev.push(["jump", H - 0.35, 0.45]);
    if (n === "M3" || n === "M8") ev.push(["leap", LAND, 0.4, 0.6]);
    if (n === "REF") ev.push(["fall", LAND + 0.05, 0, -1], ["up", s("s9") + 0.4]);
    if (n === "M0") ev.push(["dive", G2 - 0.15, 1, 1], ["up", G2 + 1.2], ["dive", FKK + 0.1, 1, -1], ["up", LOOPJ]);
    if (mm && i >= 1 && i <= 10) ev.push(["armsUp", c("s10.shirt") - 0.1, s("s11") - c("s10.shirt")]);
    if (mm && i >= 1 && i <= 5) ev.push(["jump", FKK - 0.05, 0.5]);
    A[n] = { path: W[n], ev, h: mm ? 1.7 : 1.87, unit: 360, stride: mm ? 1.8 : 2.1 };
  }

  // ---------------- ball ----------------
  const ball = [
    { t0: 0, k: "at", who: "M10", dx: 0.55, dz: 0.05 },
    { t0: CUT - 0.45, t1: CUT + 0.2, k: "fly", a: [-4.0, 0, 0.1], b: [0.5, 0, -0.35], h: 0.02 },               // through Ronaldo's legs
    { t0: CUT + 0.2, k: "rest", p: [0.5, 0, -0.35] },
    { t0: s("s2") - 0.05, k: "rest", p: [0, -50, 0] },
    { t0: s("s4") - 0.05, k: "at", who: "M10", dx: 0.55, dz: 0.05 },
    { t0: RUN1, t1: G1, k: "fly", a: [46.8, 0, 0.15], b: [52.8, 0.15, 0.0], h: 0.02 },                             // the keeper is nutmeg number eleven
    { t0: G1, k: "rest", p: [53.2, 0.1, 0] },
    { t0: s("s6") - 0.3, k: "rest", p: [0, 0, 0.3] },
    { t0: s("s7") - 0.05, k: "rest", p: [-47, 0, -23.6] },
    { t0: c("s7.head") - 0.1, t1: H, k: "fly", a: [-47, 0, -23.6], b: [-45.7, 3.15, 0.3], h: 6 },
    { t0: H, t1: G2, k: "fly", a: [-45.7, 3.15, 0.3], b: [-52.8, 1.7, 1.4], h: 0.2 },
    { t0: G2, k: "rest", p: [-53.2, 0.1, 1.4] },
    { t0: s("s8") - 0.05, k: "rest", p: [0, -50, 0] },
    { t0: s("s10") - 0.05, k: "at", who: "M10", dx: 0.55, dz: -0.05 },
    { t0: SHOT3, t1: G3, k: "fly", a: [37.5, 0, 4.5], b: [52.8, 0.7, -2.4], h: 0.4, curve: -0.6 },
    { t0: G3, k: "rest", p: [53.2, 0.1, -2.4] },
    { t0: s("s11") - 0.3, k: "rest", p: [-29.2, 0, 6.0] },
    { t0: FKK, t1: FKK + 0.32, k: "fly", a: [-29.2, 0, 6.0], b: [-38.0, 2.7, 2.6], h: 0.6, curve: -0.4 },
    { t0: FKK + 0.32, k: "rest", p: [-38.0, 2.7, 2.6] },                                                              // freeze
    { t0: LOOPJ, k: "at", who: "M10", dx: 0.55, dz: 0.05 },
  ];

  // ---------------- props: the shirts held up after the winner ----------------
  const PS = {}; const pos = (n, t) => { const p = (PS[n] = PS[n] || path(A[n].path))(t); return [p.x, p.z]; };
  const props = {};
  for (let k = 0; k < 11; k++) { const who = "M" + Math.min(k + 1, 10);
    props["shirt" + k] = { h: 0.62, unit: 115, only: k < 10 ? [c("s10.shirt") - 0.05, s("s11") - 0.05] : [0, 0],
      at: (t) => { const p = pos(who, t); return [p[0], 1.85, p[1] + 0.05]; } }; }

  // ---------------- camera ----------------
  const sh = [], add = (o) => sh.push(o);
  const HOOKCAM = { k: "path", P: [[1.4, 0.85, 0.5], [1.4, 0.85, 0.5]], T: [[-5, 1.2, 0], [-5, 1.2, 0]], fov: [46, 46], roll: 5, blur: 2.2 };
  add({ t0: 0, ...HOOKCAM });
  add({ t0: CUT, k: "path", P: [[0, 1.2, 12], [0, 1.25, 11]], T: [[0, 1.7, 0], [0, 1.7, 0]], fov: [50, 46], blur: 1.4 });
  add({ t0: s("s2") + 0.05, whip: true, k: "path", P: [[1.6, 1.6, 6.4], [1.4, 1.6, 5.8]], T: [[1.4, 1.75, 0], [1.3, 1.75, 0]], fov: [44, 42], blur: 2.2 });
  add({ t0: s("s3") + 0.05, whip: true, k: "path", P: [[-1.6, 1.7, 6.4], [-1.4, 1.7, 5.8]], T: [[-1.4, 1.85, 0], [-1.3, 1.85, 0]], fov: [44, 42], blur: 2.2 });
  add({ t0: s("s4") + 0.05, whip: true, k: "path", P: [[-2.6, 1.15, 1.6], [-2.0, 1.1, 1.3]], T: [[10, 0.95, -0.4], [10, 0.95, -0.4]], fov: [48, 44], blur: 1.6 });
  add({ t0: c("s4.legs") - 0.05, blend: 0.3, k: "path", P: [[3.4, 0.9, 3.6], [3.9, 0.9, 3.2]], T: [[6.4, 0.9, 0], [6.4, 0.9, 0]], fov: [50, 46], blur: 2.0 });
  add({ t0: RUN0 - 0.05, blend: 0.3, k: "follow", who: "M10", off: [[0.8, 1.3, 5.6], [0.6, 1.3, 5.2]], look: [0.2, 1.0, 0], fov: [52, 52], blur: 1.8 });
  add({ t0: RUN1 - 0.05, blend: 0.25, k: "path", P: [[45.6, 0.8, 5.4], [46.4, 0.8, 5.0]], T: [[52, 0.8, 0], [52, 0.8, 0]], fov: [50, 46], blur: 1.4 });
  add({ t0: s("s6") + 0.05, blend: 0.4, whip: true, k: "path", P: [[0, 1.55, 5.2], [0, 1.6, 4.4]], T: [[0, 1.65, 0], [0, 1.7, 0]], fov: [48, 42], blur: 2.4 });
  add({ t0: s("s7") + 0.05, whip: true, k: "path", P: [[-40.5, 0.7, 6.6], [-41, 0.7, 6.2]], T: [[-46, 1.6, -1], [-46, 2.4, 0]], fov: [52, 50], blur: 1.8 });
  add({ t0: H - 0.55, blend: 0.25, k: "path", P: [[-41.6, 0.6, 4.6], [-41.8, 0.7, 4.4]], T: [[-45.6, 3.0, 0.3], [-46, 2.6, 0.4]], fov: [50, 48], roll: [3, 5], blur: 1.6 });
  add({ t0: G2 - 0.1, blend: 0.2, k: "path", P: [[-46.5, 1.6, 8.5], [-47.5, 1.8, 8]], T: [[-53, 1.1, -1.5], [-52.5, 1.3, -1.5]], fov: [48, 44], blur: 1.4 });
  add({ t0: s("s8") + 0.05, whip: true, k: "path", P: [[1.6, 1.7, 10.6], [1.2, 1.65, 10.0]], T: [[-5.6, 1.6, 5.2], [-5.6, 1.6, 5.2]], fov: [48, 46], blur: 1.8 });
  add({ t0: s("s9") + 0.05, blend: 0.4, k: "path", P: [[0.6, 1.65, 9.6], [-0.2, 1.65, 8.8]], T: [[-5.2, 1.6, 5.4], [-5.4, 1.6, 5.4]], fov: [44, 40], roll: [-2, -3], blur: 2.0 });
  add({ t0: s("s10") + 0.05, whip: true, k: "follow", who: "M10", off: [[-4.0, 1.5, 4.6], [-4.4, 1.5, 4.2]], look: [3, 1.0, -2], fov: [50, 48], blur: 1.8 });
  add({ t0: SHOT3 + 0.05, blend: 0.25, k: "path", P: [[46.5, 1.6, -8.5], [47.5, 1.8, -8]], T: [[53, 1.1, -1.5], [52.5, 1.3, -1.5]], fov: [48, 44], blur: 1.4 });
  add({ t0: c("s10.shirt") - 0.15, whip: true, k: "path", P: [[40.6, 1.85, 16.2], [40.6, 1.85, 15.4]], T: [[40.6, 1.95, 7.4], [40.6, 1.95, 7.4]], fov: [46, 42], blur: 2.0 });
  add({ t0: s("s11") + 0.05, whip: true, k: "path", P: [[-23.4, 1.7, 9.2], [-23.9, 1.7, 8.9]], T: [[-38.6, 1.3, 3.5], [-38.6, 1.3, 3.5]], fov: [46, 42], blur: 2.0 });
  add({ t0: c("s11.loop") - 0.3, blend: 0.3, whip: true, ...HOOKCAM });
  sh.forEach((x, i) => { x.t1 = x.t1 ?? (sh[i + 1] ? sh[i + 1].t0 : END); });
  sh[sh.length - 1].t1 = END;

  // ---------------- overlays ----------------
  const chip = (id, t0, t1, kk, v, x, y, cls = "", from = "right") => ({ id, t0, t1, from, cls: "chip " + cls, style: `left:${x}px;top:${y}px`,
    html: `<div class="ck">${kk}</div><div class="cv">${v}</div>` });
  const slam = (id, t0, t1, html, top, size = 128) => ({ id, t0, t1, slam: true, cls: "slam", style: `top:${top}px;font-size:${size}px`, html });
  const lower = (id, t0, who, min, y = 560) => chip(id, t0, t0 + 1.3, "GOAL · " + min, who, 60, y, "dark", "left");
  const overlays = [
    slam("sl-a", -1, s("s2") - 0.05, "11 MESSIS<br><b>vs.</b> 11 RONALDOS", 340, 96),
    { id: "c-91", t0: c("s2.pm") + 0.3, t1: s("s3") - 0.05, from: "right", cls: "chip red", style: "left:100px;top:400px",
      html: '<div class="ck">PRIME MESSI · GOALS IN 2012</div><div class="cv" id="g91">0</div>' },
    chip("c-ucl", c("s3.pr") + 0.3, c("s3.ucl") - 0.05, "PRIME RONALDO", "2014", 120, 400, "dark"),
    chip("c-bdo", c("s3.ucl"), s("s4") - 0.05, "2014", "UCL + Ballon d'Or", 80, 400, "gold"),
    { id: "c-nut", t0: RUN0 + 0.1, t1: s("s6") - 0.05, from: "right", cls: "chip gold", style: "left:100px;top:400px",
      html: '<div class="ck">NUTMEGS</div><div class="cv" id="nutn">0</div>' },
    lower("g1", G1 + 0.3, "Messi (11 nutmegs)", "20'", 1180),
    chip("c-jump", H - 0.4, G2 + 0.2, "JUMP", "2.56 m", 120, 400, "red"),
    lower("g2", G2 + 0.3, "Ronaldo (header)", "55'"),
    slam("siuu", LAND - 0.05, s("s9") - 0.1, "SIUUU!", 520, 170),
    lower("g3", G3 + 0.3, "Messi", "90+2'"),
    chip("c-who", c("s11.who"), LOOPJ, "COMMENT", "Who will win?", 120, 460, "red"),
    { id: "hud", t0: c("s4.ko") - 0.1, t1: LOOPJ, cls: "hud", style: "opacity:0",
      html: `<span class="t">MES</span><span class="sc"><b id="hs">0</b>–<b id="as">0</b></span><span class="t">RON</span><span class="mn" id="mn">1'</span>` },
    slam("sl-end", END - 0.3, END + 1, "11 MESSIS<br><b>vs.</b> 11 RONALDOS", 340, 96),
  ];
  const bubbles = [
    { who: "R7", t0: c("s3.ucl") + 0.2, t1: s("s4") - 0.1, text: "💪", cls: "" },
    { who: "R7", t0: c("s4.legs") - 0.2, t1: RUN0 - 0.1, text: "BREATHE IN", cls: "dark small" },
    { who: "REF", t0: c("s6.follow") + 0.05, t1: c("s6.q") - 0.05, text: "♥ LIKE + FOLLOW +", cls: "red follow" },
    { who: "M10", t0: c("s6.q"), t1: s("s7") - 0.1, text: "MESSI?", cls: "red" },
    { who: "R7", t0: c("s6.q") + 0.3, t1: s("s7") - 0.1, text: "RONALDO?", cls: "" },
    { who: "R7", t0: c("s9.calma") + 0.3, t1: s("s10") - 0.1, text: "CALMA, CALMA", cls: "dark" },
    { who: "R7", t0: c("s11.fk") + 0.1, t1: FKK - 0.5, text: "BREATHE IN", cls: "dark small" },
  ];
  const bursts = [{ who: "R7", t: H, text: "BOOM!" }, { who: "R7", t: LAND, text: "SIUU!" }];
  const minute = (t) => t >= c("s10.min") ? "90+2'" : t >= s("s7") ? "55'" : t >= s("s5") ? "20'" : "1'";

  return {
    actors: A, ball, shots: sh, overlays, bubbles, bursts, props,
    grade: "contrast(1.14) saturate(1.2) brightness(0.95)",
    nets: { right: [G1, G3], left: [G2] }, shake: [G1, G2, LAND, G3],
    crowd: (t) => [G1, G2, LAND, G3].some((g) => t > g && t < g + 2.4) ? 0.5 : t > RUN0 && t < G1 ? 0.3 : 0.1,
    flashes: (t) => ([G1, LAND, G3].some((g) => t > g && t < g + 2) ? 0.3 : 0.05),
    speedlines: (t) => Math.max(0.55 * (1 - sstep(CUT - 0.1, CUT + 0.1, t)), 0.55 * sstep(END - 0.35, END - 0.2, t),
      0.4 * sstep(RUN0, RUN0 + 0.2, t) * (1 - sstep(RUN1, RUN1 + 0.3, t))),
    custom: (t, { el }) => {
      const g = Math.round(91 * sstep(c("s2.pm") + 0.4, c("s2.g91") + 0.6, t)), hot = g >= 91 ? Math.abs(Math.sin(t * 22)) : 0;
      el("g91").textContent = String(g); el("c-91").style.filter = `brightness(${(1 + hot * 0.35).toFixed(2)})`;            // the counter runs hot
      let nm = 0; LANE.forEach((x) => { if (t >= PASSAT(x) + 0.1) nm += 1; }); if (t >= RUN1 + 0.3) nm = 11;
      el("nutn").textContent = String(nm);
      el("hs").textContent = String(t >= G3 ? 2 : t >= G1 ? 1 : 0);
      el("as").textContent = String(t >= G2 ? 1 : 0);
      el("mn").textContent = minute(t);
      let pop = 0; for (const gg of [G1, G2, G3]) if (t >= gg && t < gg + 0.3) pop = Math.sin(((t - gg) / 0.3) * Math.PI);
      el("hud").style.transform = `scale(${1 + pop * 0.15})`;
    },
  };
}
