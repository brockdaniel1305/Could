// S2E04 "Could 11 Messis beat 11 Haalands?" - skill vs power in the night stadium, new athletic broadcast style.
// Thread: each side answers the other's strength (keep-ball -> corner header -> nutmegs -> shots from everywhere -> free kick),
// 2-2, penalties, the last kick is left to the comments. Messis attack +x (Haaland goal at x = 52.5), Haalands attack -x.
import { path, sstep, clamp, lerp } from "./engine.js";

export default function plot(T) {
  const c = (k) => { if (!(k in T.cue)) throw new Error("cue " + k); return T.cue[k]; };
  const s = (k) => T.start[k];
  const END = T.duration, CUT = 1.3, LOOPJ = c("s9.loop") - 0.5;

  // goal moments
  const CK = c("s4.nil") - 0.9, HEAD = c("s4.nil") - 0.35, G1 = c("s4.nil") - 0.1;          // 0-1 header
  const N = [c("s5.n1"), c("s5.n2"), c("s5.n3")], SH1 = c("s5.n3") + 0.55, G2 = c("s5.one") - 0.05;   // nutmegs, 1-1
  const B1 = c("s7.shoots") + 0.05, B2 = c("s7.every") + 0.25, G3 = c("s7.two") - 0.1;           // shots, 1-2
  const FK = c("s8.eq") - 0.6, G4 = c("s8.eq") - 0.1;                                          // free kick, 2-2
  const RUN = c("s9.who") - 0.2, FREEZE = c("s9.who") + 0.35;                                  // last penalty, frozen

  // ---------------- actors (phase tables) ----------------
  const W = {};
  const names = []; for (let i = 0; i < 11; i++) names.push("M" + i, "H" + i);
  names.forEach((n) => (W[n] = []));
  const at = (n, t, x, z, e) => W[n].push([t, x, z, e]);
  const jumpAll = (t, f) => names.forEach((n) => { const p = f(n, +n.slice(1), n[0] === "M"); if (p) at(n, t, p[0], p[1], "j"); });
  // hook: Haaland #9 (H9) charges at the camera, Messi (M9) slips the ball through his legs
  const HOOKPOS = (n, i, m) => (n === "H9" ? [5, 0] : n === "M9" ? [0.4, 0] : m ? [-14 - i * 1.5, (i % 2 ? 1 : -1) * (3 + i)] : [16 + i * 1.6, (i % 2 ? -1 : 1) * (3 + i)]);
  names.forEach((n) => { const [x, z] = HOOKPOS(n, +n.slice(1), n[0] === "M"); at(n, 0, x, z); });
  at("H9", CUT, -1, 0, "l"); at("M9", 0.25, 0.4, 0); at("M9", 0.7, 2.4, 1.1, "s"); at("M9", CUT, 4.6, 0.2, "s");
  // line-ups facing each other on halfway (cut at 1.3 s)
  const LZ = (i) => -9 + i * 1.8;
  jumpAll(CUT + 0.01, (n, i, m) => [m ? -1.6 : 1.6, LZ(i)]);
  // kick-off: Messis in a passing ring, H9 chases inside it, the other Haalands watch from outside
  const RING = (i) => [Math.cos((i / 10) * 2 * Math.PI) * 4.6, Math.sin((i / 10) * 2 * Math.PI) * 4.6];
  jumpAll(c("s3.ko") - 0.3, (n, i, m) => (n === "M0" ? [-51.5, 0] : n === "H0" ? [51.5, 0] : m ? RING(i - 1) : n === "H9" ? [0, 0] : [Math.cos(i * 0.7) * 8.5, Math.sin(i * 0.7) * 8.5]));
  // corner: eleven Haalands in Messi's box, Messis marking them
  const BOX = [[-49.5, -4], [-49, 0.5], [-49.4, 4.4], [-46.6, -2.6], [-46, 0], [-46.4, 3], [-43.6, -4], [-43.4, 1.2], [-44, 4.6]];
  jumpAll(c("s4.corner") - 0.3, (n, i, m) => {
    if (n === "M0") return [-51.6, 0]; if (n === "H0") return [30, 0]; if (n === "H10") return [-52, 33.4];
    const b = BOX[(i - 1) % 9]; return m ? [b[0] + 0.9, b[1] + 0.7] : b; });
  // nutmeg run: three Haalands strung along Messi's line, the rest out of the way
  const NUTX = [4, 13, 22], NUT = { H4: 0, H6: 1, H2: 2 };
  jumpAll(c("s5.ans") - 0.3, (n, i, m) => {
    if (n === "M9") return [-6, 0]; if (n === "H0") return [51.6, 0]; if (n === "M0") return [-51.6, 0];
    if (n in NUT) return [NUTX[NUT[n]], 0.1]; return m ? [-20 + i * 1.5, (i % 2 ? 1 : -1) * (8 + i)] : [30 + i * 1.2, (i % 2 ? -1 : 1) * (10 + i)]; });
  at("M9", c("s5.legs"), -6, 0); NUTX.forEach((x, k) => { at("M9", N[k] - 0.18, x - 1.0, 0.1, k ? "l" : "i"); at("M9", N[k] + 0.12, x + 0.6, 1.2, "l"); at("M9", N[k] + 0.4, x + 2.2, 0.2, "l"); });
  at("M9", SH1, 25.4, 0.2, "l"); at("M9", SH1 + 0.5, 27, 0.3, "o");
  // second half: Haaland shoots from halfway, then from near the corner flag
  jumpAll(c("s7.half") - 0.3, (n, i, m) => (n === "H9" ? [-2, 0] : n === "M0" ? [-51.6, 0] : n === "H0" ? [51.6, 0] : m ? [-30 + i * 2.2, (i % 2 ? 1 : -1) * (5 + i)] : [-8 + i * 1.6, (i % 2 ? -1 : 1) * (7 + i)]));
  at("H9", B1 - 0.5, -2, 0); at("H9", B1, -4, 0, "i"); at("H9", B1 + 0.6, -5.5, 0, "o");
  at("H9", B2 - 0.4, -46.5, -28.5, "j"); at("H9", B2, -47.8, -29.5, "i"); at("H9", B2 + 0.6, -48.6, -30, "o");
  // free kick: Messi 20 m out, five Haalands in the wall
  jumpAll(c("s8.min") - 0.3, (n, i, m) => (n === "M9" ? [30.5, -2.6] : n === "H0" ? [51.6, 0.6] : n === "M0" ? [-51.6, 0] :
    !m && i >= 1 && i <= 5 ? [41.2, -3.0 + (i - 1) * 0.9] : m ? [26 - i, (i % 2 ? 1 : -1) * (6 + i)] : [36 + i, (i % 2 ? -1 : 1) * (8 + i)]));
  at("M9", FK - 0.4, 30.5, -2.6); at("M9", FK, 31.4, -2.0, "i"); at("M9", FK + 0.4, 32.2, -1.8, "o");
  // penalties: Haaland in goal, Messi at the spot; the run-up freezes on "Who scores?"
  jumpAll(c("s9.pens") - 0.3, (n, i, m) => (n === "H9" ? [52, 0] : n === "M9" ? [39.4, 0.6] : n === "H0" ? [56, 12] :
    m ? [30 + (i % 5) * 1.1, -6 - (i > 5 ? 1.4 : 0)] : [30 + (i % 5) * 1.1, 6 + (i > 5 ? 1.4 : 0)]));
  at("M9", RUN, 39.4, 0.6); at("M9", FREEZE, 40.7, 0.25, "i");
  // loop: back into the hook positions
  names.forEach((n) => { const [x, z] = HOOKPOS(n, +n.slice(1), n[0] === "M"); const v = n === "H9" ? -4.6 : 0;
    at(n, LOOPJ, x - v * (END - LOOPJ), z, "j"); at(n, END, x, z, "l"); });

  const A = {};
  const FROZEN = (t) => t >= FREEZE && t < LOOPJ;
  for (const n of names) {
    const m = n[0] === "M", i = +n.slice(1), ev = [];
    if (n === "H9") ev.push(["dizzy", c("s3.none") - 0.3, 1.5], ["spin", c("s3.none") - 0.3, 1.2], ["jump", G3 + 0.1, 1.5], ["armsUp", G3 + 0.1, 1.6]);
    if (n in NUT) { const k = NUT[n]; ev.push(["spin", N[k] + 0.05, 0.8], ["dizzy", N[k] + 0.1, 1.4]); }
    if (n === "H8") ev.push(["jump", HEAD - 0.25, 0.5], ["armsUp", G1 + 0.1, 1.6]);
    if (n === "M0") ev.push(["dive", HEAD + 0.05, 1, 1], ["up", G1 + 1.2], ["dive", G3 - 0.2, 1, -1], ["up", G3 + 1.4]);
    if (n === "H0") ev.push(["dive", G2 - 0.25, 1, -1], ["up", G2 + 1.3], ["dive", G4 - 0.25, 1, 1], ["up", G4 + 1.4]);
    if (!m && i >= 1 && i <= 5) ev.push(["jump", FK + 0.1, 0.5]);
    if (n === "M9") ev.push(["armsUp", G2 + 0.15, s("s7") - G2 - 0.2], ["armsUp", G4 + 0.1, 1.2]);
    A[n] = { path: W[n], ev, h: m ? 1.70 : 1.95, unit: 360, stride: m ? 1.9 : 2.3,
      look: n === "M9" ? (t) => (t > c("s9.duel") && t < FREEZE ? 0.4 * Math.sin(t * 3) : 0) : undefined };
  }

  // ---------------- ball ----------------
  const ball = [
    { t0: 0, k: "at", who: "M9", dx: 0.5, dz: 0.1 },
    { t0: 0.25, t1: 0.75, k: "fly", a: [0.9, 0, 0.1], b: [3.6, 0, 0.05], h: 0.05 },                // through Haaland's legs
    { t0: 0.75, k: "at", who: "M9", dx: 0.6, dz: -0.1 },
    { t0: CUT + 0.01, k: "rest", p: [0, 0, 0] },
  ];
  // keep-ball: passes around the ring, faster and faster, H9 a step behind
  const ringP = (k) => { const r = RING(k % 10); return [r[0], 0, r[1]]; };
  let tp = c("s3.keep"), k = 0;
  while (tp < c("s3.none") + 0.6) { const d = Math.max(0.14, 0.45 - k * 0.03), a = ringP(k), b = ringP(k + 3 + (k % 3));
    ball.push({ t0: tp, t1: tp + d, k: "fly", a, b, h: 0.15 }); at("H9", tp + d * 0.9, b[0] * 0.55, b[2] * 0.55, "s"); tp += d; k += 3 + (k % 3); }
  W.H9.sort((p, q) => p[0] - q[0]);
  ball.push({ t0: tp, k: "rest", p: ringP(k) });
  ball.push({ t0: CK - 0.3, k: "rest", p: [-51.7, 0, 33.2] });
  ball.push({ t0: CK, t1: HEAD, k: "fly", a: [-51.7, 0, 33.2], b: [-46, 2.7, 0], h: 7 });
  ball.push({ t0: HEAD, t1: G1, k: "fly", a: [-46, 2.7, 0], b: [-53.1, 1.4, 1.6], h: 0.2 });
  ball.push({ t0: G1, k: "rest", p: [-53.3, 0.1, 1.6] });
  ball.push({ t0: c("s5.ans") - 0.3, k: "at", who: "M9", dx: 0.55, dz: 0.1 });
  N.forEach((t, j) => { ball.push({ t0: t - 0.18, t1: t + 0.4, k: "fly", a: [NUTX[j] - 0.45, 0, 0.12], b: [NUTX[j] + 2.75, 0, 0.2], h: 0.03 }); ball.push({ t0: t + 0.4, k: "at", who: "M9", dx: 0.55, dz: 0.05 }); });
  ball.push({ t0: SH1, t1: G2, k: "fly", a: [25.9, 0, 0.25], b: [52.8, 0.6, -2.2], h: 1.4 });
  ball.push({ t0: G2, k: "rest", p: [53.2, 0.1, -2.2] });
  ball.push({ t0: c("s7.half") - 0.3, k: "rest", p: [-2.6, 0, 0.1] });
  ball.push({ t0: B1, t1: B1 + 0.75, k: "fly", a: [-4.6, 0, 0.1], b: [-52.5, 2.44, 0.6], h: 5 });            // crossbar
  ball.push({ t0: B1 + 0.75, t1: B1 + 1.1, k: "fly", a: [-52.5, 2.44, 0.6], b: [-46, 0, 2.5], h: 1 });
  ball.push({ t0: B2 - 0.35, k: "rest", p: [-48.3, 0, -29.6] });
  ball.push({ t0: B2, t1: G3, k: "fly", a: [-48.3, 0, -29.6], b: [-53.1, 1.6, 2.4], h: 3.5, curve: 2 });
  ball.push({ t0: G3, k: "rest", p: [-53.3, 0.1, 2.4] });
  ball.push({ t0: c("s8.min") - 0.3, k: "rest", p: [31.6, 0, -2.1] });
  ball.push({ t0: FK, t1: G4, k: "fly", a: [31.6, 0, -2.1], b: [52.7, 2.25, 3.0], h: 3.4, curve: 2.4 });
  ball.push({ t0: G4, k: "rest", p: [53.2, 0.1, 3.0] });
  ball.push({ t0: c("s9.pens") - 0.3, k: "rest", p: [41.5, 0, 0] });
  ball.push({ t0: LOOPJ, k: "at", who: "M9", dx: 0.5, dz: 0.1 });

  // ---------------- camera ----------------
  const sh = [], add = (o) => sh.push(o);
  const HOOKCAM = { k: "path", P: [[-4.4, 1.0, 0.7], [-4.4, 1.0, 0.7]], T: [[2.2, 1.5, 0], [2.2, 1.5, 0]], fov: [46, 46], roll: 4, blur: 2.2 };
  add({ t0: 0, ...HOOKCAM });
  add({ t0: CUT, k: "path", P: [[0, 1.2, 12], [0, 1.25, 11]], T: [[0, 1.7, 0], [0, 1.7, 0]], fov: [50, 46], blur: 1.4 });           // the two lines
  add({ t0: c("s2.tm") + 0.1, blend: 0.5, k: "path", P: [[-4.6, 1.35, 8.5], [-4.6, 1.35, -7.5]], T: [[-1.6, 1.25, 8.5], [-1.6, 1.25, -7.5]], fov: [48, 48], blur: 2.0 });
  add({ t0: c("s2.th") + 0.05, blend: 0.4, whip: true, k: "path", P: [[4.8, 1.25, -8.5], [4.8, 1.25, 7.5]], T: [[1.6, 1.9, -8.5], [1.6, 1.9, 7.5]], fov: [48, 48], roll: [-3, -3], blur: 2.0 });
  add({ t0: c("s2.same") - 0.1, blend: 0.6, k: "path", P: [[0, 9, 18], [0, 16, 22]], T: [[0, 0.5, 0], [0, 0, 0]], fov: [52, 56], blur: 0.3 });
  add({ t0: c("s3.ko") - 0.1, blend: 0.6, whip: true, k: "path", P: [[0.4, 17, 0.05], [0.4, 15, 0.05]], T: [[0.45, 0, 0], [0.45, 0, 0]], fov: [64, 62], blur: 0.2 });
  add({ t0: c("s3.none") - 0.2, blend: 0.5, k: "follow", who: "H9", off: [[3.2, 1.5, 1.2], [2.6, 1.5, 1.0]], look: [0, 1.7, 0], fov: [44, 40], blur: 2.4 });
  add({ t0: c("s4.corner") - 0.1, blend: 0.45, whip: true, k: "path", P: [[-44.5, 0.55, 5.5], [-44.3, 0.6, 5.0]], T: [[-48.5, 2.6, -1], [-48.5, 2.6, -1]], fov: [56, 52], roll: [4, 6], blur: 1.6 });
  add({ t0: HEAD - 0.2, blend: 0.25, k: "path", P: [[-40.5, 3.2, 7.5], [-41.5, 3.0, 7.0]], T: [[-49, 1.6, 0.5], [-50, 1.5, 1.0]], fov: [50, 46], blur: 1.0 });
  add({ t0: c("s5.ans") - 0.1, blend: 0.45, whip: true, k: "follow", who: "M9", off: [0.2, 1.5, 6.4], look: [0.5, 1.25, -0.5], fov: [56, 56], blur: 2.2 });
  add({ t0: SH1 + 0.1, blend: 0.3, k: "path", P: [[46.5, 1.4, 6.5], [47.5, 1.6, 6.8]], T: [[53, 1.0, -1.5], [52.5, 1.2, -1.5]], fov: [48, 44], blur: 1.4 });
  add({ t0: s("s6") + 0.05, blend: 0.4, k: "path", P: [[30.8, 1.5, 1.4], [30.4, 1.5, 1.2]], T: [[28, 1.6, 0.3], [28, 1.65, 0.3]], fov: [44, 38], blur: 2.4 });
  add({ t0: c("s7.half") - 0.1, blend: 0.45, whip: true, k: "path", P: [[2.4, 1.4, 1.2], [1.8, 1.4, 1.0]], T: [[-12, 1.5, -0.4], [-12, 1.5, -0.4]], fov: [46, 42], blur: 2.2 });
  add({ t0: B1 + 0.15, blend: 0.25, k: "follow", who: "ball", off: [[6, 1.2, 0.8], [6, 1.2, 0.8]], look: [-8, 0.2, -0.6], rideY: true, fov: [52, 52], blur: 1.6 });
  add({ t0: B2 - 0.4, k: "path", P: [[-44.2, 1.5, -26.0], [-44.6, 1.5, -26.2]], T: [[-48.5, 1.4, -30], [-48.5, 1.4, -30]], fov: [52, 50], roll: [4, 6], blur: 1.6 });
  add({ t0: B2 + 0.12, blend: 0.2, k: "follow", who: "ball", off: [[3, 1.4, -4], [3, 1.4, -4]], look: [-2, 0.2, 4], rideY: true, fov: [56, 56], blur: 1.6 });
  add({ t0: c("s8.min") - 0.1, blend: 0.45, whip: true, k: "path", P: [[28.2, 1.25, -3.4], [28.6, 1.25, -3.2]], T: [[45, 2.4, -0.6], [45, 2.3, -0.4]], fov: [48, 44], blur: 1.6 });
  add({ t0: FK + 0.2, blend: 0.2, k: "path", P: [[28.6, 1.3, -3.2], [29.2, 1.4, -3.0]], T: [[50, 2.4, 1.4], [52, 2.3, 2.6]], fov: [42, 36], blur: 1.4 });
  add({ t0: c("s9.pens") - 0.1, blend: 0.45, whip: true, k: "path", P: [[36.8, 1.35, 1.2], [37.4, 1.35, 1.0]], T: [[52.5, 1.6, 0], [52.5, 1.6, 0]], fov: [46, 42], blur: 1.6 });
  add({ t0: c("s9.duel") - 0.1, blend: 0.3, k: "path", P: [[48.2, 1.7, 0.4], [48.6, 1.75, 0.35]], T: [[52, 1.9, 0], [52, 1.95, 0]], fov: [42, 36], blur: 2.6 });
  add({ t0: c("s9.duel") + 0.8, blend: 0.3, k: "path", P: [[43.6, 1.45, 0.6], [43.3, 1.45, 0.55]], T: [[39.4, 1.45, 0.6], [39.4, 1.5, 0.6]], fov: [40, 34], blur: 2.6 });
  add({ t0: RUN, blend: 0.3, k: "path", P: [[37.2, 1.4, 0.9], [37.7, 1.4, 0.8]], T: [[52.5, 1.6, -0.2], [52.5, 1.6, -0.2]], fov: [48, 44], roll: [0, 3], blur: 1.4 });
  add({ t0: c("s9.loop") - 0.3, blend: 0.3, whip: true, ...HOOKCAM });
  sh.forEach((x, i) => { x.t1 = x.t1 ?? (sh[i + 1] ? sh[i + 1].t0 : END); });
  sh[sh.length - 1].t1 = END;

  // ---------------- overlays ----------------
  const chip = (id, t0, t1, k, v, x, y, cls = "", from = "right") => ({ id, t0, t1, from, cls: "chip " + cls, style: `left:${x}px;top:${y}px`,
    html: `<div class="ck">${k}</div><div class="cv">${v}</div>` });
  const slam = (id, t0, t1, html, top, size = 128) => ({ id, t0, t1, slam: true, cls: "slam", style: `top:${top}px;font-size:${size}px`, html });
  const lower = (id, t0, who, min) => chip(id, t0, t0 + 2.2, "GOAL · " + min, who, 60, 1020, "dark", "left");
  const PASSES = (t) => Math.round(90 * sstep(c("s3.keep"), c("s3.none") + 0.2, t));
  const overlays = [
    slam("sl-a", -1, s("s2") - 0.05, "11 MESSIS<br><b>vs.</b> 11 HAALANDS", 340, 108),
    chip("c-m", c("s2.tm"), c("s2.th") - 0.05, "TEAM MESSI", "1.70 m", 120, 400, "dark"),
    chip("c-h", c("s2.th"), c("s2.same") - 0.05, "TEAM HAALAND", "1.95 m", 120, 400, "gold"),
    chip("c-stats", c("s2.same"), s("s3") - 0.05, "MESSI: 91 GOALS IN 2012", "HAALAND: 36 PL GOALS (2022–23)", 40, 400, "dark"),
    { id: "c-pass", t0: c("s3.keep"), t1: s("s4") - 0.05, from: "right", cls: "chip gold", style: "left:120px;top:400px", html: '<div class="ck">PASSES</div><div class="cv" id="passn">0</div>' },
    lower("g1", G1 + 0.3, "Haaland (header)", "17'"),
    { id: "c-nut", t0: N[0], t1: SH1, from: "right", cls: "chip red", style: "left:120px;top:400px", html: '<div class="ck">NUTMEGS</div><div class="cv" id="nutn">1</div>' },
    lower("g2", G2 + 0.3, "Messi", "38'"),
    lower("g3", G3 + 0.3, "Haaland (from the flag)", "71'"),
    lower("g4", G4 + 0.3, "Messi (free kick)", "92'"),
    chip("c-who", c("s9.who"), LOOPJ, "COMMENT", "Who scores?", 120, 400, "red"),
    { id: "hud", t0: c("s3.ko") - 0.1, t1: LOOPJ, cls: "hud", style: "opacity:0",
      html: `<span class="t">MES</span><span class="sc"><b id="hs">0</b>–<b id="as">0</b></span><span class="t">HAA</span><span class="mn" id="mn">1'</span>` },
    slam("sl-end", END - 0.3, END + 1, "11 MESSIS<br><b>vs.</b> 11 HAALANDS", 340, 108),
  ];
  const bubbles = [{ who: "M9", t0: c("s6.follow") + 0.1, t1: s("s7") - 0.1, text: "FOLLOW +", cls: "red follow" },
    { who: "H9", t0: c("s3.none"), t1: s("s4") - 0.2, text: "???", cls: "" }];
  const bursts = [...N.map((t, j) => ({ who: Object.keys(NUT)[j], t: t + 0.05, text: "NUTMEG!" })), { who: "H9", t: B1, text: "BOOM!" }, { who: "H9", t: B2, text: "BOOM!" }];

  const minute = (t) => t >= c("s9.pens") ? "PEN" : t >= s("s8") ? "92'" : t >= s("s7") ? `${Math.round(lerp(55, 74, clamp((t - s("s7")) / 6, 0, 1)))}'` : t >= s("s5") ? "38'" : t >= s("s4") ? "17'" : "2'";
  return {
    actors: A, ball, shots: sh, overlays, bubbles, bursts,
    grade: "contrast(1.14) saturate(1.2) brightness(0.95)", charGrade: "",
    nets: { left: [G1, G3], right: [G2, G4] }, shake: [G1, G2, B1, G3, G4],
    crowd: (t) => [G1, G2, G3, G4].some((g) => t > g && t < g + 2.6) ? 0.5 : t < s("s3") ? 0.2 : 0.1,
    flashes: (t) => ([G2, G4].some((g) => t > g && t < g + 2) ? 0.3 : 0.05),
    speedlines: (t) => Math.max(0.55 * (1 - sstep(CUT - 0.1, CUT + 0.1, t)), 0.55 * sstep(END - 0.35, END - 0.2, t),
      0.35 * sstep(N[0] - 0.4, N[0], t) * (1 - sstep(SH1, SH1 + 0.3, t))),
    custom: (t, { el }) => {
      el("passn").textContent = String(PASSES(t));
      el("nutn").textContent = String(t >= N[2] ? 3 : t >= N[1] ? 2 : 1);
      el("hs").textContent = String(t >= G4 ? 2 : t >= G2 ? 1 : 0); el("as").textContent = String(t >= G3 ? 2 : t >= G1 ? 1 : 0);
      el("mn").textContent = minute(t);
      let pop = 0; for (const g of [G1, G2, G3, G4]) if (t >= g && t < g + 0.3) pop = Math.sin(((t - g) / 0.3) * Math.PI);
      el("hud").style.transform = `scale(${1 + pop * 0.15})`;
    },
  };
}
