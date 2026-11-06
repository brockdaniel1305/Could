// S2E06 "Could 11 Bellinghams beat 11 Pedris?" - Real vs Barça, power vs possession, night stadium, broadcast style.
// Thread: the Pedris pass the Bellinghams dizzy and score with one pass through all eleven (0-1); Bellingham stops pressing and
// arrives late for a header (1-1); minute 92, "Bellingham time" (2-1, arms wide) ... VAR is checking -> comments decide.
// Pedris attack +x (Bellingham goal at x = 52.5), Bellinghams attack -x (Pedri goal at x = -52.5).
import { path, sstep, clamp, lerp } from "./engine.js";

export default function plot(T) {
  const c = (k) => { if (!(k in T.cue)) throw new Error("cue " + k); return T.cue[k]; };
  const s = (k) => T.start[k];
  const END = T.duration, CUT = 1.3, LOOPJ = c("s8.loop") - 0.5;

  const PASS0 = c("s4.one") + 0.25, PASS1 = c("s4.nil") - 0.5, G1 = c("s4.nil") - 0.1;          // one pass through all eleven, 0-1
  const CK = c("s6.head") - 0.55, HEAD = c("s6.head") + 0.05, G2 = c("s6.eq") - 0.1;           // late header, 1-1
  const SHOT = c("s7.win") - 0.55, G3 = c("s7.win") - 0.1;                                      // Bellingham time, 2-1
  const VAR = c("s8.var");

  const W = {}, names = [];
  for (let i = 0; i < 11; i++) names.push("B" + i, "P" + i);
  names.push("REF");
  names.forEach((n) => (W[n] = []));
  const at = (n, t, x, z, e) => W[n].push([t, x, z, e]);
  const jumpAll = (t, f) => names.forEach((n) => { const p = f(n, n === "REF" ? -1 : +n.slice(1), n[0] === "B"); if (p) at(n, t, p[0], p[1], "j"); });
  const LZ = (i) => -9 + i * 1.8;
  // hook: Bellingham B5 charges at the camera, Pedri P8 slips the ball past him without looking
  const HOOKPOS = (n, i, bb) => (n === "B5" ? [-7, 0.3] : n === "P8" ? [-1.4, -0.2] : n === "REF" ? [-12, 12] : bb ? [-18 - i * 1.4, (i % 2 ? 1 : -1) * (4 + i)] : [12 + i * 1.5, (i % 2 ? -1 : 1) * (4 + i)]);
  names.forEach((n) => { const [x, z] = HOOKPOS(n, n === "REF" ? -1 : +n.slice(1), n[0] === "B"); at(n, 0, x, z); });
  at("B5", CUT, -1.6, 0.4, "l"); at("P8", 0.5, -1.4, -0.2); at("P8", CUT, -1.2, -1.6, "s");
  jumpAll(CUT + 0.01, (n, i, bb) => (n === "REF" ? [0, -9.5] : [bb ? 1.6 : -1.6, LZ(i)]));
  // s3: rondo - four Pedris in a tight square, B5 chasing in the middle, the rest out of the way
  const RING = (k) => [Math.cos((k / 4) * 2 * Math.PI + 0.6) * 3.2, Math.sin((k / 4) * 2 * Math.PI + 0.6) * 3.2];
  const RONDO = { P8: 0, P6: 1, P10: 2, P4: 3 };
  jumpAll(c("s3.ko") - 0.3, (n, i, bb) => (n in RONDO ? RING(RONDO[n]) : n === "B5" ? [0, 0] : n === "B0" ? [51.6, 0] : n === "P0" ? [-51.6, 0] : n === "REF" ? [-6, 9] :
    bb ? [Math.cos(i * 0.9) * 12, -Math.abs(Math.sin(i * 0.9)) * 12 - 5] : [-14 - (i % 3) * 3, (i % 2 ? 1 : -1) * (9 + i)]));
  // s4: one pass through all eleven: ten Bellinghams staggered across the lane, P9 runs on to it and finishes
  const LANE = [6, 10, 14, 18, 22, 26, 30, 34, 38, 42];
  jumpAll(c("s4.one") - 0.3, (n, i, bb) => (n === "P8" ? [0, 0] : n === "P9" ? [24, 7] : n === "B0" ? [51.6, 0] : n === "P0" ? [-51.6, 0] : n === "REF" ? [16, -10] :
    bb ? [LANE[i - 1], (i % 2 ? 1 : -1) * 0.9] : [-6 - i, (i % 2 ? 1 : -1) * (6 + i)]));
  at("P9", PASS0, 24, 7); at("P9", PASS1, 45.4, 0.6, "s"); at("P9", G1 + 0.8, 47, 0.8, "o");
  // s5: face to face on halfway
  jumpAll(s("s5") - 0.3, (n, i, bb) => (n === "B5" ? [0.7, 0] : n === "P8" ? [-0.7, 0] : n === "REF" ? [0, -3] : bb ? [6 + i, (i % 2 ? 1 : -1) * (5 + i)] : [-6 - i, (i % 2 ? 1 : -1) * (5 + i)]));
  // s6: Bellinghams stroll, then the late run onto a corner (Bellinghams attack -x)
  const BOX = [[-49.5, -4], [-49, 0.5], [-49.4, 4.4], [-46.6, -2.6], [-46.4, 3], [-43.6, -4], [-43.4, 1.2], [-44, 4.6]];
  jumpAll(c("s6.ans") - 0.3, (n, i, bb) => (n === "B5" ? [-18, 1] : n === "P0" ? [-51.6, 0] : n === "B0" ? [40, 0] : n === "REF" ? [-24, 10] :
    bb ? [-14 + i, (i % 2 ? 1 : -1) * (4 + i)] : [-24 + i * 1.5, (i % 2 ? -1 : 1) * (4 + i)]));
  at("B5", c("s6.stop") + 0.2, -18, 1); at("B5", c("s6.late") - 0.2, -21, 1.2, "l");                  // strolling
  jumpAll(c("s6.late") - 0.25, (n, i, bb) => (n === "B5" ? [-34, 1] : n === "P0" ? [-51.6, 0] : n === "B10" ? [-52, 33.4] : n === "REF" ? [-36, 10] :
    n === "B0" ? [40, 0] : bb ? [-36 + i, (i % 2 ? 1 : -1) * (12 + i)] : BOX[(i - 1) % 8]));
  at("B5", HEAD - 0.6, -40, 0.6, "i"); at("B5", HEAD, -46, 0.1, "l"); at("B5", G2 + 0.7, -45, 0.6, "o");
  // s7: minute 92 - Bellingham at the edge of the box, top corner, arms wide
  jumpAll(c("s7.min") - 0.3, (n, i, bb) => (n === "B5" ? [-31, 2.4] : n === "P0" ? [-51.6, 0] : n === "B0" ? [40, 0] : n === "REF" ? [-24, -8] :
    bb ? [-26 + (i % 4) * 2, (i % 2 ? 1 : -1) * (7 + i)] : [-40 + (i % 4) * 2.5, (i % 2 ? -1 : 1) * (2 + i * 0.6)]));
  at("B5", SHOT - 0.4, -31, 2.4); at("B5", SHOT, -33.4, 2.0, "i"); at("B5", G3 + 0.8, -38, 4.5, "o"); at("B5", s("s8") - 0.1, -39, 5.5, "s");
  at("REF", VAR - 0.4, -24, -8); at("REF", VAR + 0.3, -34, 1.5, "s");
  // loop
  names.forEach((n) => { const [x, z] = HOOKPOS(n, n === "REF" ? -1 : +n.slice(1), n[0] === "B"); at(n, LOOPJ, x - (n === "B5" ? 5.4 : 0) * (END - LOOPJ) / CUT, z, "j"); at(n, END, x, z, "l"); });

  const A = {};
  for (const n of names) {
    const bb = n[0] === "B", i = n === "REF" ? -1 : +n.slice(1), ev = [];
    if (n === "B5") ev.push(["spin", CUT - 0.5, 0.6], ["dizzy", c("s3.cant") - 0.2, 1.8], ["spin", c("s3.cant") - 0.4, 1.0],
      ["jump", HEAD - 0.25, 0.5], ["wide", G2 + 0.15, 1.6], ["wide", G3 + 0.15, VAR - G3 - 0.3]);
    if (bb && i >= 1 && n !== "B5") ev.push(["spin", PASS0 + (LANE[i - 1] / 46) * (PASS1 - PASS0), 0.6]);
    if (n === "P9") ev.push(["armsUp", G1 + 0.1, 1.6]);
    if (n === "B0") ev.push(["dive", G1 - 0.25, 1, -1], ["up", G1 + 1.2]);
    if (n === "P0") ev.push(["dive", HEAD + 0.05, 1, 1], ["up", G2 + 1.2], ["dive", SHOT + 0.25, 1, -1], ["up", G3 + 1.4]);
    if (n === "REF") ev.push(["armsUp", VAR + 0.35, 1.2]);
    A[n] = { path: W[n], ev, h: bb ? 1.86 : 1.74, unit: 360, stride: bb ? 2.1 : 1.9 };
  }

  // ---------------- ball ----------------
  const ball = [
    { t0: 0, k: "at", who: "P8", dx: 0.5, dz: 0.1 },
    { t0: 0.45, t1: 0.95, k: "fly", a: [-0.9, 0, -0.1], b: [-1.6, 0, -2.0], h: 0.05 },
    { t0: 0.95, k: "at", who: "P8", dx: -0.3, dz: -0.4 },
    { t0: CUT + 0.01, k: "rest", p: [0, 0, 0] },
  ];
  // rondo: passes around the square, faster and faster
  const rp = (k) => { const r = RING(k % 4); return [r[0], 0, r[1]]; };
  const oles = [];
  let tp = c("s3.p1") - 0.3, k = 0;
  while (tp < c("s3.cant") + 1.2) { const d = Math.max(0.2, 0.55 - k * 0.04), a = rp(k), b = rp(k + 1 + (k % 2));
    ball.push({ t0: tp, t1: tp + d, k: "fly", a, b, h: 0.12 }); at("B5", tp + d * 0.95, b[0] * 0.6, b[2] * 0.6, "o"); if (oles.length < 6 && k % 1 === 0) oles.push([tp + d, k]); tp += d; k += 1 + (k % 2); }
  W.B5.sort((p, q) => p[0] - q[0]);
  ball.push({ t0: tp, k: "rest", p: rp(k) });
  ball.push({ t0: c("s4.one") - 0.3, k: "at", who: "P8", dx: 0.5, dz: 0.1 });
  ball.push({ t0: PASS0, t1: PASS1, k: "fly", a: [0.5, 0, 0.1], b: [45.8, 0, 0.6], h: 0.02, ease: "o" });
  ball.push({ t0: PASS1, t1: G1, k: "fly", a: [45.8, 0, 0.6], b: [52.8, 0.8, -2.2], h: 0.3 });
  ball.push({ t0: G1, k: "rest", p: [53.2, 0.1, -2.2] });
  ball.push({ t0: s("s5") - 0.3, k: "rest", p: [0, 0, 0.3] });
  ball.push({ t0: c("s6.late") - 0.25, k: "rest", p: [-51.7, 0, 33.2] });
  ball.push({ t0: CK, t1: HEAD, k: "fly", a: [-51.7, 0, 33.2], b: [-46, 2.7, 0.1], h: 7 });
  ball.push({ t0: HEAD, t1: G2, k: "fly", a: [-46, 2.7, 0.1], b: [-53.1, 1.2, 1.4], h: 0.2 });
  ball.push({ t0: G2, k: "rest", p: [-53.3, 0.1, 1.4] });
  ball.push({ t0: c("s7.min") - 0.3, k: "at", who: "B5", dx: -0.55, dz: 0.1 });
  ball.push({ t0: SHOT, t1: G3, k: "fly", a: [-34, 0, 2.0], b: [-52.7, 2.25, -3.0], h: 1.6, curve: 1.6 });
  ball.push({ t0: G3, k: "rest", p: [-53.2, 0.1, -3.0] });
  ball.push({ t0: LOOPJ, k: "at", who: "P8", dx: 0.5, dz: 0.1 });

  // ---------------- camera ----------------
  const sh = [], add = (o) => sh.push(o);
  const HOOKCAM = { k: "path", P: [[1.4, 0.85, 0.5], [1.4, 0.85, 0.5]], T: [[-5, 1.4, 0], [-5, 1.4, 0]], fov: [46, 46], roll: 5, blur: 2.2 };
  add({ t0: 0, ...HOOKCAM });
  add({ t0: CUT, k: "path", P: [[0, 1.2, 12], [0, 1.25, 11]], T: [[0, 1.7, 0], [0, 1.7, 0]], fov: [50, 46], blur: 1.4 });
  add({ t0: c("s2.tb") + 0.1, blend: 0.5, k: "path", P: [[4.8, 1.35, 8.5], [4.8, 1.35, -7.5]], T: [[1.6, 1.4, 8.5], [1.6, 1.4, -7.5]], fov: [48, 48], blur: 2.0 });
  add({ t0: c("s2.tp") + 0.05, blend: 0.4, whip: true, k: "path", P: [[-4.6, 1.25, -8.5], [-4.6, 1.25, 7.5]], T: [[-1.6, 1.3, -8.5], [-1.6, 1.3, 7.5]], fov: [48, 48], roll: [3, 3], blur: 2.0 });
  add({ t0: c("s3.ko") - 0.1, blend: 0.6, whip: true, k: "path", P: [[0, 7.0, 9.6], [0, 5.4, 7.8]], T: [[0, 0.4, -0.3], [0, 0.6, -0.3]], fov: [54, 50], blur: 0.6 });
  add({ t0: c("s3.cant") - 0.1, blend: 0.5, k: "follow", who: "B5", off: [[2.4, 1.5, 1.6], [2.0, 1.5, 1.4]], look: [0, 1.6, 0], fov: [44, 40], blur: 2.4 });
  add({ t0: c("s4.one") - 0.1, blend: 0.45, whip: true, k: "path", P: [[-3.2, 1.5, 2.2], [-3.0, 1.5, 2.0]], T: [[3, 1.0, 0], [3, 1.0, 0]], fov: [50, 48], blur: 1.8 });
  add({ t0: PASS0 + 0.1, blend: 0.3, k: "follow", who: "ball", off: [[-4, 1.3, 3.2], [-4, 1.3, 3.2]], look: [6, 0.6, -0.4], fov: [56, 56], rideY: true, blur: 1.8 });
  add({ t0: PASS1 + 0.05, blend: 0.25, k: "path", P: [[46.5, 1.6, 8.5], [47.5, 1.8, 8]], T: [[53, 1.1, -1.5], [52.5, 1.3, -1.5]], fov: [48, 44], blur: 1.4 });
  add({ t0: s("s5") + 0.05, blend: 0.4, whip: true, k: "path", P: [[0, 1.55, 4.2], [0, 1.6, 3.4]], T: [[0, 1.65, 0], [0, 1.7, 0]], fov: [48, 42], blur: 2.4 });
  add({ t0: c("s6.ans") - 0.1, blend: 0.45, whip: true, k: "follow", who: "B5", off: [[0.3, 1.5, 6.0], [0.3, 1.5, 5.4]], look: [-0.6, 1.4, -1], fov: [50, 48], blur: 2.2 });
  add({ t0: c("s6.late") - 0.2, blend: 0.45, k: "path", P: [[-36, 4.5, 11], [-38, 4.0, 10]], T: [[-46, 0.8, 0.6], [-47, 0.8, 0.6]], fov: [52, 50], blur: 0.8 });
  add({ t0: HEAD - 0.25, blend: 0.25, k: "path", P: [[-43.0, 0.7, 2.4], [-43.4, 0.75, 2.2]], T: [[-46.5, 2.5, 0.1], [-47, 2.3, 0.4]], fov: [50, 46], roll: [4, 6], blur: 1.6 });
  add({ t0: G2 + 0.35, blend: 0.3, k: "path", P: [[-39.5, 1.6, 5.2], [-40, 1.6, 5.4]], T: [[-45, 1.5, 0.6], [-45, 1.5, 0.6]], fov: [50, 48], blur: 1.6 });
  add({ t0: c("s7.min") - 0.1, blend: 0.45, whip: true, k: "path", P: [[-27.5, 1.5, 3.8], [-28.2, 1.5, 3.5]], T: [[-33, 1.5, 2.2], [-33, 1.5, 2.2]], fov: [44, 38], blur: 2.4 });
  add({ t0: SHOT + 0.05, blend: 0.25, k: "path", P: [[-46.5, 1.6, -8.5], [-47.5, 1.8, -8]], T: [[-53, 1.6, -2], [-52.5, 1.6, -2]], fov: [48, 44], blur: 1.4 });
  add({ t0: G3 + 0.6, blend: 0.4, k: "path", P: [[-33.4, 1.6, 8.4], [-36.4, 1.7, 11.4], [-41.6, 1.8, 10.8]], T: [[-38.6, 1.5, 4.8], [-38.8, 1.5, 5.0], [-39, 1.5, 5.4]], fov: [48, 44], blur: 2.0 });
  add({ t0: VAR - 0.1, blend: 0.35, k: "path", P: [[-30.5, 1.6, -3.5], [-30.8, 1.6, -3.2]], T: [[-34.5, 1.8, 1.4], [-34.5, 1.8, 1.4]], fov: [46, 42], roll: [-3, -4], blur: 2.0 });
  add({ t0: c("s8.loop") - 0.3, blend: 0.3, whip: true, ...HOOKCAM });
  sh.forEach((x, i) => { x.t1 = x.t1 ?? (sh[i + 1] ? sh[i + 1].t0 : END); });
  sh[sh.length - 1].t1 = END;

  // ---------------- overlays ----------------
  const chip = (id, t0, t1, kk, v, x, y, cls = "", from = "right") => ({ id, t0, t1, from, cls: "chip " + cls, style: `left:${x}px;top:${y}px`,
    html: `<div class="ck">${kk}</div><div class="cv">${v}</div>` });
  const slam = (id, t0, t1, html, top, size = 128) => ({ id, t0, t1, slam: true, cls: "slam", style: `top:${top}px;font-size:${size}px`, html });
  const lower = (id, t0, who, min) => chip(id, t0, t0 + 1.4, "GOAL · " + min, who, 60, 560, "dark", "left");
  const PASSES = (t) => Math.round(70 * sstep(c("s3.p1") - 0.3, c("s3.cant") + 0.8, t));
  const overlays = [
    slam("sl-a", -1, s("s2") - 0.05, "11 BELLINGHAMS<br><b>vs.</b> 11 PEDRIS", 340, 100),
    chip("c-fee", c("s2.fee"), c("s2.cl") - 0.05, "TEAM BELLINGHAM · 2023", "€103m", 120, 400, "dark"),
    chip("c-cl", c("s2.cl"), c("s2.tp") - 0.05, "FIRST SEASON", "2 Clásico winners", 80, 400, "dark"),
    chip("c-gb", c("s2.gb"), c("s2.g73") - 0.05, "TEAM PEDRI · 2021", "Golden Boy at 18", 80, 400, "gold"),
    chip("c-73", c("s2.g73"), s("s3") - 0.05, "2020–21", "73 games", 120, 400, "gold"),
    { id: "c-pass", t0: c("s3.p1"), t1: s("s4") - 0.05, from: "right", cls: "chip gold", style: "left:120px;top:400px", html: '<div class="ck">PASSES</div><div class="cv" id="passn">0</div>' },
    chip("c-thru", PASS0, G1 + 0.2, "ONE PASS", "through all 11", 120, 400, "gold"),
    lower("g1", G1 + 0.3, "Pedri (one pass)", "23'"),
    lower("g2", G2 + 0.3, "Bellingham (header)", "61'"),
    lower("g3", G3 + 0.3, "Bellingham", "90+2'"),
    { id: "var", t0: VAR - 0.05, t1: LOOPJ, cls: "var", html: 'VAR CHECK<small>GOAL UNDER REVIEW</small>' },
    chip("c-who", c("s8.who"), LOOPJ, "COMMENT", "Who will win?", 120, 640, "red"),
    { id: "hud", t0: c("s3.ko") - 0.1, t1: LOOPJ, cls: "hud", style: "opacity:0",
      html: `<span class="t">BEL</span><span class="sc"><b id="hs">0</b>–<b id="as">0</b></span><span class="t">PED</span><span class="mn" id="mn">1'</span>` },
    slam("sl-end", END - 0.3, END + 1, "11 BELLINGHAMS<br><b>vs.</b> 11 PEDRIS", 340, 100),
  ];
  const bubbles = [
    { who: "REF", t0: c("s5.follow") + 0.05, t1: s("s6") - 0.1, text: "♥ LIKE + FOLLOW +", cls: "red follow" },
    { who: "P8", t0: c("s5.rb"), t1: s("s6") - 0.1, text: "BARÇA?", cls: "dark" },
    { who: "B5", t0: c("s3.cant") + 0.1, t1: s("s4") - 0.2, text: "???", cls: "" },
  ];
  const bursts = [...oles.slice(0, 5).map(([t, kk]) => ({ who: Object.keys(RONDO)[(kk + 1 + (kk % 2)) % 4], t, text: "OLÉ!" })),
    { who: "B5", t: HEAD, text: "BOOM!" }];
  const minute = (t) => t >= c("s7.min") ? "90+2'" : t >= s("s6") ? "61'" : t >= s("s4") ? "23'" : t >= s("s3") ? "2'" : "1'";

  return {
    actors: A, ball, shots: sh, overlays, bubbles, bursts,
    grade: "contrast(1.14) saturate(1.2) brightness(0.95)",
    nets: { right: [G1], left: [G2, G3] }, shake: [G1, G2, G3],
    crowd: (t) => [G1, G2, G3].some((g) => t > g && t < g + 2.6) ? 0.5 : t > c("s3.p1") && t < s("s4") ? 0.3 : 0.1,
    flashes: (t) => ([G1, G3].some((g) => t > g && t < g + 2) ? 0.3 : 0.05),
    speedlines: (t) => Math.max(0.55 * (1 - sstep(CUT - 0.1, CUT + 0.1, t)), 0.55 * sstep(END - 0.35, END - 0.2, t),
      0.35 * sstep(PASS0, PASS0 + 0.2, t) * (1 - sstep(G1, G1 + 0.3, t))),
    custom: (t, { el }) => {
      el("passn").textContent = String(PASSES(t));
      el("hs").textContent = String(t >= G3 ? 2 : t >= G2 ? 1 : 0) + (t >= VAR && t < LOOPJ ? "?" : "");
      el("as").textContent = String(t >= G1 ? 1 : 0);
      el("mn").textContent = t >= VAR ? "VAR" : minute(t);
      let pop = 0; for (const g of [G1, G2, G3]) if (t >= g && t < g + 0.3) pop = Math.sin(((t - g) / 0.3) * Math.PI);
      el("hud").style.transform = `scale(${1 + pop * 0.15})`;
      const v = el("var"); if (t >= VAR) v.style.borderColor = Math.floor(t * 4) % 2 ? "#4fd1ff" : "#f4f4f2";
    },
  };
}
