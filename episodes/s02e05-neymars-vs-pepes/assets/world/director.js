// S2E05 "Could 11 Neymars beat 11 Pepes?" - joga bonito vs pure violence, night stadium, broadcast style.
// Thread: Pepe tackles, Neymar rolls, Pepe gets sent off; then Neymar shows the joga bonito (rainbow flick, elastico, nutmeg, 1-0),
// Pepe heads in a corner (1-1), more reds, last-minute penalty frozen on the run-up -> comments.
// Neymars attack +x (Pepe goal at x = 52.5), Pepes attack -x.
import { path, sstep, clamp, lerp } from "./engine.js";

export default function plot(T) {
  const c = (k) => { if (!(k in T.cue)) throw new Error("cue " + k); return T.cue[k]; };
  const s = (k) => T.start[k];
  const END = T.duration, CUT = 1.3, LOOPJ = c("s8.loop") - 0.5;

  const TK = c("s3.tackle") + 0.35, ROLL0 = TK + 0.1, ROLL1 = c("s3.red") - 0.1, RED1 = c("s3.red");
  const RB = c("s4.rb"), EL = c("s4.el"), NUT = c("s4.nut"), SHOT = c("s4.goal") - 0.45, G1 = c("s4.goal") - 0.05;
  const CK = c("s6.head") - 0.55, HEAD = c("s6.head") + 0.05, G2 = c("s6.eq") - 0.1;
  const RR = [c("s7.r1"), c("s7.r2"), c("s7.r3")];
  const STUT = c("s8.stut"), FREEZE = c("s8.who") + 0.2;

  const W = {}, names = [];
  for (let i = 0; i < 11; i++) names.push("N" + i, "P" + i);
  names.push("REF");
  names.forEach((n) => (W[n] = []));
  const at = (n, t, x, z, e) => W[n].push([t, x, z, e]);
  const jumpAll = (t, f) => names.forEach((n) => { const p = f(n, n === "REF" ? -1 : +n.slice(1), n[0] === "N"); if (p) at(n, t, p[0], p[1], "j"); });
  const LZ = (i) => -9 + i * 1.8;
  // hook: Pepe P4 slides at the camera, Neymar N9 hops over him
  const HOOKPOS = (n, i, nn) => (n === "P4" ? [-6, 0] : n === "N9" ? [-1.5, 0] : n === "REF" ? [-10, 12] : nn ? [-16 - i * 1.4, (i % 2 ? 1 : -1) * (4 + i)] : [14 + i * 1.5, (i % 2 ? -1 : 1) * (4 + i)]);
  names.forEach((n) => { const [x, z] = HOOKPOS(n, n === "REF" ? -1 : +n.slice(1), n[0] === "N"); at(n, 0, x, z); });
  at("P4", CUT, -1.2, 0.2, "o"); at("N9", CUT, -3.2, 0, "l");
  // line-ups on halfway
  jumpAll(CUT + 0.01, (n, i, nn) => (n === "REF" ? [0, -9.5] : [nn ? -1.6 : 1.6, LZ(i)]));
  // s3 kick-off: P2 slides into N9, N9 rolls seven times, referee runs in with the red card
  jumpAll(c("s3.ko") - 0.3, (n, i, nn) => (n === "N9" ? [-2, 0] : n === "P2" ? [4.5, 1.5] : n === "REF" ? [-4, 6] : n === "N0" ? [-51.6, 0] : n === "P0" ? [51.6, 0] :
    nn ? [-14 + (i % 4) * 2.5, (i % 2 ? 1 : -1) * (5 + i)] : [9 + (i % 4) * 2.5, (i % 2 ? -1 : 1) * (5 + i)]));
  at("N9", TK - 0.5, -2, 0); at("N9", TK, 1.2, 0.2, "i"); at("N9", ROLL1, 6.5, 1.2, "o");
  at("P2", TK - 0.4, 4.5, 1.5); at("P2", TK, 1.6, 0.3, "o");
  at("REF", TK + 0.3, -4, 6); at("REF", RED1 - 0.2, 3.5, 3.0, "s");
  at("P2", RED1 + 0.4, 1.6, 0.3); at("P2", c("s3.ten") + 0.9, 1.0, 9, "l");
  // s4 joga bonito: three Pepes on Neymar's line, then the shot
  const TX = [24, 31, 38], TRICK = { P5: 0, P6: 1, P7: 2 };
  jumpAll(c("s4.then") - 0.3, (n, i, nn) => (n === "N9" ? [16, 0] : n in TRICK ? [TX[TRICK[n]], 0.1] : n === "P0" ? [51.6, 0] : n === "N0" ? [-51.6, 0] :
    n === "REF" ? [28, 9] : n === "P2" ? [0, 60] : nn ? [6 + i * 1.2, (i % 2 ? 1 : -1) * (9 + i)] : [30 + i, (i % 2 ? -1 : 1) * (11 + i)]));
  at("N9", RB - 0.6, 20.5, 0, "i");
  at("N9", RB + 0.7, 26.5, 0.4, "l");                 // rainbow flick over P5
  at("N9", EL - 0.2, 29.6, 0.1, "l"); at("N9", EL + 0.4, 32.5, -0.5, "l");   // elastico past P6
  at("N9", NUT - 0.15, 36.6, 0.1, "l"); at("N9", NUT + 0.5, 40.2, 0.6, "l"); // nutmeg P7
  at("N9", SHOT, 44.5, 0.3, "l"); at("N9", G1 + 0.6, 46.2, 0.4, "o");
  at("P6", EL - 0.05, TX[1], 0.1); at("P6", EL + 0.3, TX[1] - 0.2, 1.4, "o");          // P6 bites on the elastico
  // s6 corner: Pepes in Neymar's box, P5 heads it in
  const BOX = [[-49.5, -4], [-49, 0.5], [-49.4, 4.4], [-46.6, -2.6], [-46, 0], [-46.4, 3], [-43.6, -4], [-43.4, 1.2], [-44, 4.6]];
  jumpAll(c("s6.ans") - 0.3, (n, i, nn) => {
    if (n === "N0") return [-51.6, 0]; if (n === "P0") return [30, 0]; if (n === "P10") return [-52, 33.4]; if (n === "REF") return [-36, 10]; if (n === "P2") return [0, 60];
    const b = BOX[(i - 1) % 9]; return nn ? [b[0] + 0.9, b[1] + 0.7] : b; });
  // s7 reds: three tackles in midfield, three sent off (P6, P7, P8)
  const RX = [-6, 2, 10];
  jumpAll(c("s7.half") - 0.3, (n, i, nn) => (n === "REF" ? [-8, 6] : n === "P2" ? [0, 60] : n === "N0" ? [-51.6, 0] : n === "P0" ? [51.6, 0] :
    n === "N9" ? [-10, 0] : n === "P6" ? [RX[0] + 3, 1.6] : n === "P7" ? [RX[1] + 3, -1.6] : n === "P8" ? [RX[2] + 3, 1.6] :
    nn ? [-20 + i * 2, (i % 2 ? 1 : -1) * (8 + i)] : [16 + i, (i % 2 ? -1 : 1) * (9 + i)]));
  at("N9", RR[0] - 0.6, RX[0] - 1, 0, "i"); at("N9", RR[2] + 0.4, RX[2] + 2, 0, "l");
  ["P6", "P7", "P8"].forEach((n, k) => { at(n, RR[k] - 0.45, RX[k] + 3, (k % 2 ? -1 : 1) * 1.6); at(n, RR[k] - 0.1, RX[k] + 0.6, 0.2, "o");
    at(n, RR[k] + 0.5, RX[k] + 0.6, 0.2); at(n, s("s8") - 0.3, RX[k] + 2, 12, "l"); });
  at("REF", RR[0] - 0.3, -8, 6); at("REF", RR[2] + 0.3, RX[2], 4, "s");
  // s8 penalty: Pepe P1 in goal, Neymar at the spot with the stutter run-up, frozen on "Who wins?"
  jumpAll(c("s8.last") - 0.3, (n, i, nn) => (n === "P1" ? [52, 0] : n === "N9" ? [37.6, 1.2] : n === "P0" ? [56, 14] : n === "REF" ? [38, -6] :
    ["P2", "P6", "P7", "P8"].includes(n) ? [0, 60] : nn ? [30 + (i % 5) * 1.1, -7 - (i > 5 ? 1.4 : 0)] : [30 + (i % 5) * 1.1, 7 + (i > 5 ? 1.4 : 0)]));
  at("N9", STUT, 37.6, 1.2); at("N9", STUT + 0.35, 38.6, 0.8, "s"); at("N9", STUT + 0.9, 38.7, 0.8); at("N9", STUT + 1.15, 39.5, 0.5, "s");
  at("N9", STUT + 1.8, 39.6, 0.45); at("N9", FREEZE, 40.6, 0.2, "i");
  // loop back into the hook
  names.forEach((n) => { const [x, z] = HOOKPOS(n, n === "REF" ? -1 : +n.slice(1), n[0] === "N"); at(n, LOOPJ, x - (n === "P4" ? 4.8 : n === "N9" ? -1.7 : 0) * (END - LOOPJ) / CUT, z, "j"); at(n, END, x, z, "l"); });

  const A = {};
  for (const n of names) {
    const nn = n[0] === "N", i = n === "REF" ? -1 : +n.slice(1), ev = [];
    if (n === "P4") ev.push(["fall", 0.05, 0.3, 1], ["up", CUT], ["fall", LOOPJ + 0.05, 0.3, 1]);
    if (n === "N9") ev.push(["jump", 0.25, 0.9], ["fall", ROLL0, 0.3, 1], ["spin", ROLL0 + 0.05, ROLL1 - ROLL0], ["up", ROLL1],
      ["jump", RB - 0.1, 0.4], ["armsUp", G1 + 0.1, 1.4], ["fall", RR[0], 0.3, -1], ["up", RR[0] + 0.25], ["fall", RR[1], 0.3, 1], ["up", RR[1] + 0.25],
      ["fall", RR[2], 0.3, -1], ["up", RR[2] + 0.35], ["jump", LOOPJ + 0.25, 0.9]);
    if (n === "P2") ev.push(["fall", TK - 0.15, 0.3, -1], ["up", TK + 0.4]);
    if (n in TRICK) ev.push(["spin", [RB + 0.2, EL + 0.25, NUT + 0.1][TRICK[n]], 0.7], ["dizzy", [RB + 0.3, EL + 0.4, NUT + 0.2][TRICK[n]], 1.6]);
    if (n === "P6") ev.push(["fall", EL + 0.35, 0.3, 1], ["up", EL + 1.4]);
    if (["P6", "P7", "P8"].includes(n)) { const k = ["P6", "P7", "P8"].indexOf(n); ev.push(["fall", RR[k] - 0.2, 0.3, k % 2 ? 1 : -1], ["up", RR[k] + 0.3]); }
    if (n === "P5") ev.push(["jump", HEAD - 0.25, 0.5], ["armsUp", G2 + 0.1, 1.6]);
    if (n === "P1") ev.push(["armsUp", c("s8.pg"), FREEZE - c("s8.pg")]);
    if (n === "N0") ev.push(["dive", HEAD + 0.05, 1, 1], ["up", G2 + 1.2]);
    if (n === "P0") ev.push(["dive", SHOT + 0.2, 1, -1], ["up", G1 + 1.3]);
    if (n === "REF") ev.push(["armR", RED1 - 0.05, 1.2], ...RR.map((t) => ["armR", t - 0.05, 0.45]));
    const offAt = n === "P2" ? c("s3.ten") + 0.9 : ["P6", "P7", "P8"].includes(n) ? s("s8") - 0.3 : null;
    if (offAt) ev.push(["hide", offAt, LOOPJ - offAt]);
    A[n] = { path: W[n], ev, h: nn ? 1.75 : n === "REF" ? 1.8 : 1.88, unit: 360, stride: nn ? 1.9 : 2.2 };
  }

  // ---------------- ball ----------------
  const NP = (t) => { const p = path(W.N9)(t); return [p.x, 0, p.z]; };
  const ball = [
    { t0: 0, k: "at", who: "N9", dx: 0.5, dz: 0.1 },
    { t0: 0.2, t1: 0.9, k: "fly", a: [-1.0, 0, 0.1], b: [-2.6, 0, 0.1], h: 1.2 },
    { t0: 0.9, k: "at", who: "N9", dx: -0.5, dz: 0.1 },
    { t0: CUT + 0.01, k: "rest", p: [0, 0, 0] },
    { t0: c("s3.ko") - 0.3, k: "at", who: "N9", dx: 0.5, dz: 0.1 },
    { t0: TK, t1: TK + 0.6, k: "fly", a: [1.7, 0, 0.3], b: [5, 0, -1.5], h: 0.2 },
    { t0: TK + 0.6, k: "rest", p: [5, 0, -1.5] },
    { t0: c("s4.then") - 0.3, k: "at", who: "N9", dx: 0.55, dz: 0.1 },
    { t0: RB - 0.1, t1: RB + 0.75, k: "fly", a: NP(RB - 0.1).map((v, j) => v + [0.3, 0, 0][j]), b: [27.1, 0, 0.4], h: 3.2 },     // over P5's head
    { t0: RB + 0.75, k: "at", who: "N9", dx: 0.55, dz: 0.1 },
    { t0: EL - 0.2, t1: EL + 0.05, k: "fly", a: [30.1, 0, 0.1], b: [30.4, 0, 0.75], h: 0.05 },                                     // elastico: out...
    { t0: EL + 0.05, t1: EL + 0.4, k: "fly", a: [30.4, 0, 0.75], b: [33, 0, -0.5], h: 0.05 },                                     // ...and back in
    { t0: EL + 0.4, k: "at", who: "N9", dx: 0.55, dz: 0.05 },
    { t0: NUT - 0.15, t1: NUT + 0.5, k: "fly", a: [37.1, 0, 0.1], b: [40.8, 0, 0.6], h: 0.02 },                                    // through P7's legs
    { t0: NUT + 0.5, k: "at", who: "N9", dx: 0.55, dz: 0.05 },
    { t0: SHOT, t1: G1, k: "fly", a: [45, 0, 0.35], b: [52.8, 1.9, -2.6], h: 1.2, curve: -1.4 },
    { t0: G1, k: "rest", p: [53.2, 0.1, -2.6] },
    { t0: c("s6.ans") - 0.3, k: "rest", p: [-51.7, 0, 33.2] },
    { t0: CK, t1: HEAD, k: "fly", a: [-51.7, 0, 33.2], b: [-46, 2.7, 0], h: 7 },
    { t0: HEAD, t1: G2, k: "fly", a: [-46, 2.7, 0], b: [-53.1, 1.2, 1.4], h: 0.2 },
    { t0: G2, k: "rest", p: [-53.3, 0.1, 1.4] },
    { t0: c("s7.half") - 0.3, k: "at", who: "N9", dx: 0.55, dz: 0.1 },
    { t0: c("s8.last") - 0.3, k: "rest", p: [41.5, 0, 0] },
    { t0: LOOPJ, k: "at", who: "N9", dx: 0.5, dz: 0.1 },
  ];

  // ---------------- camera ----------------
  const sh = [], add = (o) => sh.push(o);
  const HOOKCAM = { k: "path", P: [[1.6, 0.8, 0.6], [1.6, 0.8, 0.6]], T: [[-5, 1.3, 0], [-5, 1.3, 0]], fov: [46, 46], roll: 5, blur: 2.2 };
  add({ t0: 0, ...HOOKCAM });
  add({ t0: CUT, k: "path", P: [[0, 1.2, 12], [0, 1.25, 11]], T: [[0, 1.7, 0], [0, 1.7, 0]], fov: [50, 46], blur: 1.4 });
  add({ t0: c("s2.tn") + 0.1, blend: 0.5, k: "path", P: [[-4.6, 1.35, 8.5], [-4.6, 1.35, -7.5]], T: [[-1.6, 1.25, 8.5], [-1.6, 1.25, -7.5]], fov: [48, 48], blur: 2.0 });
  add({ t0: c("s2.floor") - 0.1, blend: 0.4, k: "path", P: [[-3.2, 1.3, 1.2], [-3.0, 1.3, 1.0]], T: [[-1.6, 1.5, 0.6], [-1.6, 1.55, 0.6]], fov: [40, 34], blur: 2.4 });
  add({ t0: c("s2.tp") + 0.05, blend: 0.4, whip: true, k: "path", P: [[4.8, 1.25, -8.5], [4.8, 1.25, 7.5]], T: [[1.6, 1.9, -8.5], [1.6, 1.9, 7.5]], fov: [48, 48], roll: [-3, -3], blur: 2.0 });
  add({ t0: c("s3.ko") - 0.1, blend: 0.5, whip: true, k: "path", P: [[-1, 4.5, 9], [0, 3.2, 7.5]], T: [[1.5, 0.6, 0], [2, 0.7, 0]], fov: [52, 50], blur: 0.8 });
  add({ t0: TK - 0.15, blend: 0.3, k: "follow", who: "N9", off: [[0.5, 2.4, 7.5], [0.5, 2.3, 7.0]], look: [0.3, 0.5, 0], fov: [54, 54], blur: 1.6 });
  add({ t0: RED1 - 0.1, blend: 0.25, k: "path", P: [[8.2, 1.5, 7.6], [7.8, 1.5, 7.2]], T: [[2.8, 1.4, 1.6], [2.8, 1.45, 1.6]], fov: [50, 46], roll: [3, 4], blur: 1.6 });
  add({ t0: c("s4.then") - 0.1, blend: 0.45, whip: true, k: "path", P: [[20.2, 1.45, 1.4], [19.8, 1.5, 1.3]], T: [[16.6, 1.55, 0], [17.2, 1.6, 0]], fov: [46, 40], blur: 2.4 });
  add({ t0: RB - 0.6, blend: 0.3, k: "follow", who: "N9", off: [0.2, 1.6, 6.2], look: [1.2, 1.3, -1], fov: [54, 54], blur: 2.0 });
  add({ t0: SHOT + 0.05, blend: 0.3, k: "path", P: [[46.5, 1.6, 8.5], [47.5, 1.8, 8]], T: [[53, 1.1, -1.5], [52.5, 1.3, -1.5]], fov: [48, 44], blur: 1.4 });
  add({ t0: s("s5") + 0.05, blend: 0.4, k: "path", P: [[49.2, 1.5, 1.6], [48.8, 1.5, 1.4]], T: [[46.2, 1.6, 0.4], [46.2, 1.65, 0.4]], fov: [44, 38], blur: 2.4 });
  add({ t0: c("s6.ans") - 0.1, blend: 0.45, whip: true, k: "path", P: [[-44.5, 0.55, 5.5], [-44.3, 0.6, 5.0]], T: [[-48.5, 2.6, -1], [-48.5, 2.6, -1]], fov: [56, 52], roll: [4, 6], blur: 1.6 });
  add({ t0: HEAD - 0.2, blend: 0.25, k: "path", P: [[-40.5, 3.2, 7.5], [-41.5, 3.0, 7.0]], T: [[-49, 1.6, 0.5], [-50, 1.5, 1.0]], fov: [50, 46], blur: 1.0 });
  add({ t0: c("s7.half") - 0.1, blend: 0.45, whip: true, k: "path", P: [[-12, 2.4, 6], [-10, 2.2, 5.5]], T: [[-4, 1.2, 0], [-2, 1.2, 0]], fov: [52, 50], blur: 1.4 });
  add({ t0: RR[0] - 0.5, blend: 0.3, k: "follow", who: "N9", off: [[0, 1.8, 6.5], [0, 1.8, 6.5]], look: [1.5, 1.0, -0.6], fov: [56, 56], blur: 1.8 });
  add({ t0: c("s8.last") - 0.1, blend: 0.45, whip: true, k: "path", P: [[34.6, 1.5, 0.3], [35.0, 1.5, 0.3]], T: [[52.5, 1.4, 0.7], [52.5, 1.4, 0.7]], fov: [50, 46], blur: 1.6 });
  add({ t0: c("s8.pg") - 0.1, blend: 0.3, k: "path", P: [[48.2, 1.7, 0.4], [48.6, 1.75, 0.35]], T: [[52, 1.9, 0], [52, 1.95, 0]], fov: [42, 36], blur: 2.6 });
  add({ t0: c("s8.who") - 0.3, blend: 0.3, k: "path", P: [[35.4, 1.6, -2.0], [35.8, 1.6, -1.9]], T: [[52.5, 1.3, 1.4], [52.5, 1.3, 1.4]], fov: [50, 46], roll: [0, 3], blur: 1.4 });
  add({ t0: c("s8.loop") - 0.3, blend: 0.3, whip: true, ...HOOKCAM });
  sh.forEach((x, i) => { x.t1 = x.t1 ?? (sh[i + 1] ? sh[i + 1].t0 : END); });
  sh[sh.length - 1].t1 = END;

  // ---------------- overlays ----------------
  const chip = (id, t0, t1, k, v, x, y, cls = "", from = "right") => ({ id, t0, t1, from, cls: "chip " + cls, style: `left:${x}px;top:${y}px`,
    html: `<div class="ck">${k}</div><div class="cv">${v}</div>` });
  const slam = (id, t0, t1, html, top, size = 128) => ({ id, t0, t1, slam: true, cls: "slam", style: `top:${top}px;font-size:${size}px`, html });
  const lower = (id, t0, who, min) => chip(id, t0, t0 + 1.4, "GOAL · " + min, who, 60, 560, "dark", "left");
  const ROLLS = (t) => Math.max(1, Math.min(7, Math.ceil(7 * clamp((t - ROLL0) / (ROLL1 - ROLL0), 0, 1))));
  const PEPES = (t) => 11 - (t >= c("s3.ten") - 0.1 ? 1 : 0) - RR.filter((r) => t >= r + 0.05).length;
  const overlays = [
    slam("sl-a", -1, s("s2") - 0.05, "11 NEYMARS<br><b>vs.</b> 11 PEPES", 340, 112),
    chip("c-jb", c("s2.jb"), c("s2.floor") - 0.05, "TEAM NEYMAR", "The last true joga bonito", 40, 400, "gold"),
    chip("c-floor", c("s2.floor"), c("s2.tp") - 0.05, "WORLD CUP 2018", "≈ 14 min on the floor", 80, 400, "dark"),
    chip("c-ban", c("s2.ban"), s("s3") - 0.05, "TEAM PEPE · 2009", "10-match ban", 120, 400, "red"),
    { id: "c-rolls", t0: ROLL0, t1: RED1, from: "right", cls: "chip gold", style: "left:120px;top:400px", html: '<div class="ck">ROLLS</div><div class="cv" id="rolln">1</div>' },
    { id: "c-pepes", t0: RED1 + 0.3, t1: s("s4") - 0.05, from: "right", cls: "chip red", style: "left:120px;top:400px", html: '<div class="ck">PEPES ON THE PITCH</div><div class="cv" id="pepen">11</div>' },
    lower("g1", G1 + 0.3, "Neymar (joga bonito)", "34'"),
    lower("g2", G2 + 0.3, "Pepe (header)", "44'"),
    { id: "c-pepes2", t0: RR[0], t1: s("s8") - 0.05, from: "right", cls: "chip red", style: "left:120px;top:400px", html: '<div class="ck">PEPES ON THE PITCH</div><div class="cv" id="pepen2">10</div>' },
    chip("c-who", c("s8.who"), LOOPJ, "COMMENT", "Who wins?", 120, 400, "red"),
    { id: "hud", t0: c("s3.ko") - 0.1, t1: LOOPJ, cls: "hud", style: "opacity:0",
      html: `<span class="t">NEY</span><span class="sc"><b id="hs">0</b>–<b id="as">0</b></span><span class="t">PEP</span><span class="mn" id="mn">1'</span>` },
    slam("sl-end", END - 0.3, END + 1, "11 NEYMARS<br><b>vs.</b> 11 PEPES", 340, 112),
  ];
  const bubbles = [
    { who: "REF", t0: RED1, t1: RED1 + 1.1, text: ".", cls: "redcard" },
    ...RR.map((t) => ({ who: "REF", t0: t, t1: t + 0.42, text: ".", cls: "redcard" })),
    { who: "P2", t0: RED1 + 0.15, t1: c("s3.ten") + 0.6, text: "ME?!", cls: "" },
    { who: "N9", t0: c("s5.follow") + 0.1, t1: s("s6") - 0.1, text: "FOLLOW +", cls: "red follow" },
    { who: "N9", t0: STUT + 0.3, t1: FREEZE, text: "...", cls: "" },
  ];
  const bursts = [{ who: "N9", t: TK, text: "OUCH?" }, { who: "P5", t: RB + 0.3, text: "RAINBOW!" }, { who: "P6", t: EL + 0.1, text: "ELASTICO!" },
    { who: "P7", t: NUT + 0.1, text: "NUTMEG!" }, ...RR.map((t) => ({ who: "N9", t: t - 0.1, text: "BAM!" }))];
  const minute = (t) => t >= c("s8.last") ? "90+3'" : t >= s("s7") ? `${Math.round(lerp(52, 78, clamp((t - s("s7")) / 4, 0, 1)))}'` : t >= s("s6") ? "44'" : t >= s("s4") ? "34'" : "1'";

  return {
    actors: A, ball, shots: sh, overlays, bubbles, bursts,
    grade: "contrast(1.14) saturate(1.2) brightness(0.95)",
    nets: { right: [G1], left: [G2] }, shake: [G1, G2, ...RR],
    crowd: (t) => [G1, G2].some((g) => t > g && t < g + 2.6) ? 0.5 : t < s("s3") ? 0.2 : 0.1,
    flashes: (t) => (t > G1 && t < G1 + 2 ? 0.3 : 0.05),
    speedlines: (t) => Math.max(0.55 * (1 - sstep(CUT - 0.1, CUT + 0.1, t)), 0.55 * sstep(END - 0.35, END - 0.2, t),
      0.35 * sstep(RB - 0.4, RB, t) * (1 - sstep(SHOT, SHOT + 0.3, t))),
    custom: (t, { el }) => {
      el("rolln").textContent = String(ROLLS(t));
      el("pepen").textContent = String(PEPES(t)); el("pepen2").textContent = String(PEPES(t));
      el("hs").textContent = String(t >= G1 ? 1 : 0); el("as").textContent = String(t >= G2 ? 1 : 0);
      el("mn").textContent = minute(t);
      let pop = 0; for (const g of [G1, G2]) if (t >= g && t < g + 0.3) pop = Math.sin(((t - g) / 0.3) * Math.PI);
      el("hud").style.transform = `scale(${1 + pop * 0.15})`;
    },
  };
}
