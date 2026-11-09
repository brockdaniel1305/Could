// S2E08 "Could 11 Yamals beat 11 young Messis?" - is Yamal the next Messi? Night stadium, broadcast style.
// Thread: they've met before (2007: Messi bathed baby Yamal). Yamal curls the opener (1-0), all eleven Yamals celebrate in the corner
// while the Messis score into the empty goal (1-1); half-time homework; Messi dribbles past all eleven - bath time, again (1-2);
// last minute Yamal free kick, freeze -> comments decide.
// Yamals attack +x (Messi goal at x = 52.5), Messis attack -x (Yamal goal at x = -52.5).
import { path, sstep, clamp, lerp } from "./engine.js";

export default function plot(T) {
  const c = (k) => { if (!(k in T.cue)) throw new Error("cue " + k); return T.cue[k]; };
  const s = (k) => T.start[k];
  const END = T.duration, CUT = 1.3, LOOPJ = c("s10.loop") - 0.5;

  const BATH = c("s4.bath"), BATHE = s("s5") - 0.1;                                             // 2007 flashback
  const SHOT1 = c("s5.one") - 0.7, G1 = c("s5.one") - 0.1;                                      // Yamal's curler, 1-0
  const K2 = c("s6.on") + 0.35, G2 = c("s6.eq") - 0.1;                                          // Messi from halfway into the empty goal, 1-1
  const RUN0 = c("s9.sh") + 0.1, RUN1 = c("s9.bt") - 0.45, G3 = c("s9.bt") - 0.15;              // the solo, 1-2
  const FKK = c("s10.who") - 0.1;                                                                // free kick, freeze
  const CORNER = [48.6, 30.6];

  const W = {}, names = [];
  for (let i = 0; i < 11; i++) names.push("Y" + i, "M" + i);
  names.push("REF");
  names.forEach((n) => (W[n] = []));
  const at = (n, t, x, z, e) => W[n].push([t, x, z, e]);
  const idx = (n) => (n === "REF" ? -1 : +n.slice(1));
  const jumpAll = (t, f) => names.forEach((n) => { const p = f(n, idx(n), n[0] === "Y"); if (p) at(n, t, p[0], p[1], "j"); });
  const LZ = (i) => -9 + i * 1.8;
  const ROWS = (i, side) => [side * (1.9 + (i % 5) * 1.35), -3.2 - (i > 5 ? 1.7 : 0) - (i % 2) * 0.3];

  // hook: Yamal Y10 dribbles at the camera, young Messi M10 chasing
  const HOOKPOS = (n, i, yy) => (n === "Y10" ? [-6.4, 0.2] : n === "M10" ? [-8.6, 0.9] : n === "REF" ? [-14, 10] :
    yy ? [-16 - i * 1.4, (i % 2 ? 1 : -1) * (5 + i)] : [-22 - i * 1.3, (i % 2 ? -1 : 1) * (4 + i)]);
  names.forEach((n) => { const [x, z] = HOOKPOS(n, idx(n), n[0] === "Y"); at(n, 0, x, z); });
  at("Y10", CUT, -2.6, 0.25, "l"); at("M10", CUT, -4.9, 0.8, "l");
  jumpAll(CUT + 0.01, (n, i, yy) => (n === "REF" ? [0, -9.5] : [yy ? -1.6 : 1.6, LZ(i)]));
  // s2 + s3: the two teams side by side, Yamal and Messi in front, the referee between them
  jumpAll(s("s2") - 0.05, (n, i, yy) => (n === "Y10" ? [-0.95, 0] : n === "M10" ? [0.95, 0.1] : n === "REF" ? [0, -1.6] : ROWS(i, yy ? -1 : 1)));
  // s4: face to face ... then 2007: Messi behind the bathtub, everybody else out of the picture
  jumpAll(s("s4") - 0.05, (n, i, yy) => (n === "Y10" ? [-0.75, 0] : n === "M10" ? [0.75, 0] : n === "REF" ? [0, -6] : ROWS(i, yy ? -1 : 1).map((v, k) => (k ? v - 2 : v * 1.4))));
  jumpAll(BATH - 0.05, (n, i, yy) => (n === "M10" ? [0.15, -0.75] : n === "REF" ? [-30, 20] : [yy ? -30 - i : 30 + i, 18]));
  // s5: Yamal on the right wing cuts inside and curls it into the far top corner
  jumpAll(s("s5") - 0.1, (n, i, yy) => (n === "Y10" ? [0.4, 0.3] : n === "M10" ? [3, 2] : n === "REF" ? [-5, 8] : n === "Y0" ? [-51.6, 0] : n === "M0" ? [51.6, 0] :
    yy ? [-4 - (i % 4) * 6, ((i % 3) - 1) * 12] : [5 + (i % 4) * 6, ((i % 3) - 1) * 12]));
  jumpAll(c("s5.curl") - 0.2, (n, i, yy) => (n === "Y10" ? [33.4, 15.2] : n === "M0" ? [51.6, 0] : n === "Y0" ? [-51.6, 0] : n === "REF" ? [30, -6] :
    yy ? [24 + (i % 4) * 4, ((i % 3) - 1) * 10 - 2] : [40 + (i % 3) * 3, ((i % 4) - 1.5) * 4.5]));
  at("Y10", SHOT1 - 0.45, 34.8, 13.6); at("Y10", SHOT1, 37.4, 10.6, "i"); at("Y10", G1 + 0.3, 38.4, 10.6, "o");
  // s6: all eleven Yamals (keeper too) celebrate in the corner - Messi kicks off and scores from halfway into the empty goal
  const DANCE = (i) => [CORNER[0] - 1.2 - Math.cos(i * 1.7) * (1 + (i % 3) * 0.8), CORNER[1] - 1.2 - Math.sin(i * 1.7) * (1 + (i % 3) * 0.8)];
  jumpAll(s("s6") - 0.1, (n, i, yy) => (yy ? DANCE(i) : n === "M10" ? [0.6, 0] : n === "M9" ? [-0.6, 1.4] : n === "M0" ? [51.6, 0] : n === "REF" ? [10, -6] :
    [4 + (i % 4) * 3, ((i % 3) - 1) * 9]));
  at("M10", K2 - 0.3, 0.6, 0); at("M10", K2, -0.6, 0.05, "i"); at("M10", G2 + 0.6, -6, 0.4, "o");
  // s7: face to face on halfway
  jumpAll(s("s7") - 0.3, (n, i, yy) => (n === "Y10" ? [-0.7, 0] : n === "M10" ? [0.7, 0] : n === "REF" ? [0, -3] : yy ? [-6 - i, (i % 2 ? 1 : -1) * (5 + i)] : [6 + i, (i % 2 ? 1 : -1) * (5 + i)]));
  // s8: half-time homework by the touchline
  const HWX = (i) => -3.6 + (i - 1) * 0.9;
  jumpAll(s("s8") - 0.1, (n, i, yy) => (yy && i >= 1 && i <= 9 ? [HWX(i), -30.5 - (i % 2) * 1.1] : n === "Y10" ? [5.6, -31.2] : n === "Y0" ? [-7.4, -31.4] :
    n === "M10" ? [2.4, -26.6] : n === "REF" ? [-9, -27] : [4 + (i % 5) * 1.6, -24 - (i % 2) * 1.4]));
  // s9: Messi dribbles past all eleven Yamals, one after another they go down
  const LANE = [-10, -13.5, -17, -20.5, -24, -27.5, -31, -34.5, -38, -41.5];
  const LANEY = ["Y1", "Y2", "Y3", "Y4", "Y5", "Y6", "Y7", "Y8", "Y9", "Y10"];
  jumpAll(s("s9") - 0.1, (n, i, yy) => (n === "M10" ? [-7.6, 0] : n === "Y0" ? [-51.6, 0] : n === "M0" ? [51.6, 0] : n === "REF" ? [-20, 9] :
    yy ? [LANE[LANEY.indexOf(n)], (i % 2 ? 1 : -1) * 0.9] : [2 + (i % 4) * 4, ((i % 3) - 1) * 10]));
  at("M10", RUN0, -7.6, 0); at("M10", RUN1, -45.8, 0.3, "i"); at("M10", G3 + 0.9, -48.5, 3.2, "o");
  const PASSAT = (x) => RUN0 + ((-7.6 - x) / 38.2) * (RUN1 - RUN0);
  // s10: last minute - Yamal's free kick, a wall of Messis
  const WALL = (k) => [39.8 + k * 0.15, 3.5 - (k - 2) * 0.62];
  jumpAll(s("s10") - 0.3, (n, i, yy) => (n === "Y10" ? [29.4, 7.0] : n === "M0" ? [51.8, 0] : n === "Y0" ? [-51.6, 0] : n === "REF" ? [33, 12] :
    !yy && i >= 1 && i <= 5 ? WALL(i - 1) : yy ? [38 + (i % 4) * 2.2, -4 - (i % 3) * 3] : [44 + (i % 3) * 1.8, -6 + (i % 4) * 4]));
  at("Y10", FKK - 0.45, 29.4, 7.0); at("Y10", FKK, 30.6, 6.25, "i");
  // loop
  names.forEach((n) => { const [x, z] = HOOKPOS(n, idx(n), n[0] === "Y"); const dx = n === "Y10" ? 3.8 : n === "M10" ? 3.7 : 0;
    at(n, LOOPJ, x - dx * (END - LOOPJ) / CUT, z, "j"); at(n, END, x, z, "l"); });
  for (const n of names) W[n].sort((p, q) => p[0] - q[0]);

  const A = {};
  for (const n of names) {
    const yy = n[0] === "Y", i = idx(n), ev = [];
    if (n === "Y10") ev.push(["charge", 0, CUT], ["armsUp", c("s2.wc"), c("s2.arg") - c("s2.wc") + 0.4], ["charge", SHOT1 - 0.6, 0.6], ["charge", FKK - 0.45, 0.45]);
    if (n === "M10") ev.push(["charge", 0, CUT], ["cross", c("s2.arg"), 1.3], ["armsUp", G2 + 0.1, 1.2], ["charge", RUN0, RUN1 - RUN0], ["armsUp", G3 + 0.2, 1.6]);
    if (!yy && i >= 1 && i <= 9 && i !== 10) ev.push(["cross", c("s2.arg") + 0.1, 1.2]);
    if (yy) { for (let k = 0; k < 7; k++) ev.push(["jump", s("s6") + 0.1 + k * 0.42 + (i % 3) * 0.1, 0.3]);                 // the corner dance
      ev.push(["spin", s("s6") + 0.4 + (i % 4) * 0.3, 0.6], ["armsUp", s("s6") + 0.2, c("s6.eq") - s("s6")]); }
    if (n === "Y4") ev.push(["spin", G2 + 0.15, 0.4]);
    if (n === "Y7") ev.push(["yawn", c("s8.hw") + 0.2, 1.1]);
    if (LANEY.includes(n)) ev.push(["fall", PASSAT(LANE[LANEY.indexOf(n)]) + 0.05, 0, i % 2 ? 1 : -1], ["up", s("s10") - 0.35]);
    if (n === "Y0") ev.push(["dive", G3 - 0.2, 1, 1], ["up", s("s10") - 0.4]);
    if (n === "M0") ev.push(["dive", G1 - 0.25, 1, 1], ["up", G1 + 1.2], ["dive", FKK + 0.1, 1, -1]);
    if (!yy && i >= 1 && i <= 5) ev.push(["jump", FKK - 0.05, 0.5]);
    if (n === "REF") ev.push(["armsUp", c("s3.n19") + 0.25, 1.0]);
    A[n] = { path: W[n], ev, h: yy ? 1.8 : 1.7, unit: 360, stride: yy ? 2.0 : 1.8 };
  }

  // ---------------- ball ----------------
  const ball = [
    { t0: 0, k: "at", who: "Y10", dx: 0.55, dz: 0.1 },
    { t0: CUT + 0.01, k: "rest", p: [0, 0, 0.6] },
    { t0: s("s2") - 0.05, k: "rest", p: [0, -50, 0] },
    { t0: s("s5") - 0.1, k: "at", who: "Y10", dx: 0.55, dz: 0.1 },
    { t0: SHOT1, t1: G1, k: "fly", a: [37.9, 0, 10.4], b: [52.7, 2.2, -3.0], h: 1.4, curve: -1.6 },
    { t0: G1, k: "rest", p: [53.2, 0.1, -3.0] },
    { t0: s("s6") - 0.1, k: "rest", p: [0, 0, 0] },
    { t0: K2 - 0.05, k: "rest", p: [-0.1, 0, 0.05] },
    { t0: K2, t1: G2, k: "fly", a: [-0.1, 0, 0.05], b: [-52.8, 0.7, 0.5], h: 9 },
    { t0: G2, k: "rest", p: [-53.2, 0.1, 0.5] },
    { t0: s("s7") - 0.3, k: "rest", p: [0, 0, 0.3] },
    { t0: s("s8") - 0.1, k: "rest", p: [0, 0, 0] },
    { t0: s("s9") - 0.1, k: "at", who: "M10", dx: -0.5, dz: 0.1 },
    { t0: RUN1, t1: G3, k: "fly", a: [-46.3, 0, 0.3], b: [-52.8, 0.6, -1.8], h: 0.25 },
    { t0: G3, k: "rest", p: [-53.2, 0.1, -1.8] },
    { t0: s("s10") - 0.3, k: "rest", p: [31, 0, 6] },
    { t0: FKK, t1: FKK + 0.32, k: "fly", a: [31, 0, 6], b: [40.6, 2.7, 2.4], h: 0.6, curve: 0.4 },
    { t0: FKK + 0.32, k: "rest", p: [40.6, 2.7, 2.4] },                                                  // freeze
    { t0: LOOPJ, k: "at", who: "Y10", dx: 0.55, dz: 0.1 },
  ];

  // ---------------- props: the 2007 bathtub, the World Cup, the notebooks ----------------
  const PS = {}; const pos = (n, t) => { const p = (PS[n] = PS[n] || path(A[n].path))(t); return [p.x, p.z]; };
  const props = {
    tub: { h: 1.15, unit: 230, only: [BATH - 0.05, BATHE], p: [0, 0, 0.35] },
    wc: { h: 0.55, unit: 125, only: [c("s2.wc") - 0.05, c("s2.arg") + 0.4], at: (t) => { const k = pos("Y10", t), f = sstep(c("s2.wc"), c("s2.wc") + 0.3, t); return [k[0] + 0.02, lerp(1.2, 2.05, f), k[1] + 0.05]; } },
  };
  for (let k = 0; k < 5; k++) { const who = "Y" + (1 + k * 2);
    props["book" + k] = { h: 0.32, unit: 46, only: [s("s8") - 0.05, s("s9") - 0.1], at: (t) => { const p = pos(who, t); return [p[0] + 0.05, 0.95, p[1] + 0.32]; } }; }

  // ---------------- camera ----------------
  const sh = [], add = (o) => sh.push(o);
  const HOOKCAM = { k: "path", P: [[1.4, 0.85, 0.5], [1.4, 0.85, 0.5]], T: [[-5, 1.4, 0], [-5, 1.4, 0]], fov: [46, 46], roll: 5, blur: 2.2 };
  add({ t0: 0, ...HOOKCAM });
  add({ t0: CUT, k: "path", P: [[0, 1.2, 12], [0, 1.25, 11]], T: [[0, 1.7, 0], [0, 1.7, 0]], fov: [50, 46], blur: 1.4 });
  add({ t0: s("s2") + 0.05, whip: true, k: "path", P: [[-1.6, 1.6, 6.4], [-1.4, 1.6, 5.8]], T: [[-1.4, 1.85, 0], [-1.3, 1.85, 0]], fov: [44, 42], blur: 2.2 });
  add({ t0: c("s2.arg") - 0.05, whip: true, k: "path", P: [[1.8, 1.6, 6.0], [1.8, 1.6, 5.6]], T: [[1.7, 1.6, -1], [1.7, 1.6, -1]], fov: [44, 42], blur: 2.2 });
  add({ t0: c("s3.n19") - 0.05, blend: 0.35, whip: true, k: "path", P: [[0, 1.55, 6.6], [0, 1.55, 6.0]], T: [[0, 1.45, 0], [0, 1.45, 0]], fov: [44, 40], blur: 2.2 });
  add({ t0: c("s3.more") - 0.05, blend: 0.35, k: "path", P: [[1.2, 1.62, 3.6], [1.1, 1.62, 3.0]], T: [[0.95, 1.65, 0], [0.95, 1.68, 0]], fov: [44, 38], blur: 2.4 });
  add({ t0: s("s4") + 0.05, whip: true, k: "path", P: [[0, 1.5, 4.6], [0, 1.5, 4.0]], T: [[0, 1.55, 0], [0, 1.6, 0]], fov: [46, 42], blur: 2.4 });
  add({ t0: BATH - 0.05, whip: true, k: "path", P: [[0.4, 1.35, 4.4], [0.3, 1.3, 3.7]], T: [[0.1, 1.0, 0], [0.1, 1.0, 0]], fov: [46, 42], blur: 2.2 });
  add({ t0: s("s5") + 0.05, whip: true, k: "path", P: [[-3.4, 1.6, 4.2], [-3.0, 1.6, 3.8]], T: [[2, 1.1, -0.4], [2.2, 1.1, -0.4]], fov: [50, 48], blur: 1.6 });
  add({ t0: c("s5.curl") - 0.15, whip: true, k: "follow", who: "Y10", off: [[-4.2, 1.5, 4.8], [-4.4, 1.5, 4.4]], look: [3, 1.0, -2.6], fov: [50, 48], blur: 1.8 });
  add({ t0: SHOT1 + 0.05, blend: 0.25, k: "path", P: [[45.2, 1.8, -12], [45.8, 1.9, -11.5]], T: [[50.5, 1.7, -1.5], [50.5, 1.7, -1.5]], fov: [48, 44], blur: 1.4 });
  add({ t0: s("s6") + 0.05, blend: 0.4, whip: true, k: "path", P: [[42.6, 1.7, 23.0], [43.2, 1.7, 23.6]], T: [[47.4, 1.4, 29.4], [47.4, 1.4, 29.4]], fov: [50, 46], blur: 2.0 });
  add({ t0: K2 - 0.55, whip: true, k: "path", P: [[3.6, 1.5, 1.6], [3.4, 1.6, 1.6]], T: [[-6, 1.4, 0], [-8, 2.6, 0]], fov: [48, 50], blur: 1.6 });
  add({ t0: K2 + 0.35, blend: 0.3, k: "path", P: [[-43.5, 1.6, 7.5], [-44.5, 1.6, 7.0]], T: [[-52.5, 1.3, 0.3], [-52.5, 1.2, 0.3]], fov: [50, 46], blur: 1.4 });
  add({ t0: G2 + 0.15, whip: true, k: "path", P: [[43.2, 1.7, 23.6], [43.6, 1.7, 24.0]], T: [[47.4, 1.4, 29.4], [47.4, 1.4, 29.4]], fov: [46, 42], blur: 2.0 });
  add({ t0: s("s7") + 0.05, blend: 0.4, whip: true, k: "path", P: [[0, 1.55, 5.4], [0, 1.6, 4.6]], T: [[0, 1.65, 0], [0, 1.7, 0]], fov: [48, 42], blur: 2.4 });
  add({ t0: s("s8") + 0.05, whip: true, k: "path", P: [[0, 1.65, -22.6], [0, 1.65, -23.4]], T: [[0, 1.15, -31], [0, 1.15, -31]], fov: [54, 50], blur: 2.0 });
  add({ t0: s("s9") + 0.05, whip: true, k: "follow", who: "M10", off: [[0.7, 1.4, 6.0], [0.6, 1.4, 5.6]], look: [-0.5, 1.2, 0], fov: [50, 50], blur: 1.8 });
  add({ t0: RUN1 - 0.05, blend: 0.25, k: "path", P: [[-46.5, 1.6, 8.5], [-47.5, 1.8, 8]], T: [[-53, 1.1, -1.5], [-52.5, 1.3, -1.5]], fov: [48, 44], blur: 1.4 });
  add({ t0: c("s9.bt") + 0.1, blend: 0.4, k: "path", P: [[-47, 2.6, 4.6], [-46.5, 2.8, 4.8]], T: [[-30, 0.3, 0], [-30, 0.3, 0]], fov: [52, 50], blur: 1.6 });
  add({ t0: s("s10") + 0.05, whip: true, k: "path", P: [[24.4, 1.7, 10.6], [24.9, 1.7, 10.1]], T: [[40, 1.3, 2.6], [40, 1.3, 2.6]], fov: [46, 42], blur: 2.0 });
  add({ t0: c("s10.loop") - 0.3, blend: 0.3, whip: true, ...HOOKCAM });
  sh.forEach((x, i) => { x.t1 = x.t1 ?? (sh[i + 1] ? sh[i + 1].t0 : END); });
  sh[sh.length - 1].t1 = END;

  // ---------------- overlays ----------------
  const chip = (id, t0, t1, kk, v, x, y, cls = "", from = "right") => ({ id, t0, t1, from, cls: "chip " + cls, style: `left:${x}px;top:${y}px`,
    html: `<div class="ck">${kk}</div><div class="cv">${v}</div>` });
  const slam = (id, t0, t1, html, top, size = 128) => ({ id, t0, t1, slam: true, cls: "slam", style: `top:${top}px;font-size:${size}px`, html });
  const lower = (id, t0, who, min, y = 560) => chip(id, t0, t0 + 1.3, "GOAL · " + min, who, 60, y, "dark", "left");
  const FOAM = Array.from({ length: 34 }, (_, k) => { const r = 70 + ((k * 37) % 90), x = ((k * 173) % 1160) - 40, y = 60 + ((k * 89) % 520);
    return `<i style="left:${x}px;top:${y}px;width:${r * 2}px;height:${r * 2}px"></i>`; }).join("");
  const DUCKSVG = '<svg viewBox="-70 -90 140 100" width="260" height="190"><ellipse cx="0" cy="-22" rx="34" ry="22" fill="#ffd23f" stroke="#14141f" stroke-width="5"/><circle cx="20" cy="-50" r="18" fill="#ffd23f" stroke="#14141f" stroke-width="5"/><path d="M34,-52 L52,-46 L34,-40 Z" fill="#f07a1a" stroke="#14141f" stroke-width="4"/><circle cx="24" cy="-55" r="4" fill="#14141f"/></svg>';
  const overlays = [
    slam("sl-a", -1, s("s2") - 0.05, "11 YAMALS<br><b>vs.</b> 11 YOUNG MESSIS", 340, 92),
    chip("c-euro", c("s2.euro"), c("s2.wc") - 0.05, "TEAM YAMAL · EURO 2024", "Champion at 17", 80, 400, "red"),
    chip("c-wc", c("s2.wc"), s("s3") - 0.05, "WORLD CUP 2026 · vs ARG", "Champion at 19", 80, 400, "gold"),
    chip("c-y06", c("s3.y06"), c("s3.n19") - 0.05, "TEAM MESSI", "2006", 120, 400, "dark"),
    chip("c-n19", c("s3.n19"), c("s3.more") - 0.05, "AGE · SHIRT", "19 · No. 19", 120, 400, "dark"),
    { id: "flash", t0: BATH - 0.05, t1: BATHE, cls: "flash", html: "" },
    { id: "flashlbl", t0: BATH, t1: BATHE, cls: "flashlbl", html: "2007" },
    lower("g1", G1 + 0.3, "Yamal (top corner)", "2'"),
    lower("g2", G2 + 0.2, "Messi (empty net)", "3'", 1180),
    { id: "c-ht", t0: c("s8.ht"), t1: s("s9") - 0.05, from: "right", cls: "chip gold", style: "left:80px;top:400px", html: '<div class="ck">HALF-TIME · HOMEWORK</div><div class="cv">Maths, p. 47</div>' },
    { id: "foam", t0: c("s9.bt") - 0.15, t1: s("s10") - 0.05, cls: "foam", html: FOAM },
    { id: "duck", t0: c("s9.bt") + 0.25, t1: s("s10") - 0.05, cls: "duck", html: DUCKSVG },
    slam("splash", c("s9.bt") - 0.1, c("s9.again") - 0.05, "SPLASH!", 520, 150),
    slam("again", c("s9.again"), s("s10") - 0.05, "BATH TIME. AGAIN.", 520, 88),
    chip("c-who", c("s10.who"), LOOPJ, "COMMENT", "Who will win?", 120, 460, "red"),
    { id: "hud", t0: c("s5.ko") - 0.1, t1: LOOPJ, cls: "hud", style: "opacity:0",
      html: `<span class="t">YAM</span><span class="sc"><b id="hs">0</b>–<b id="as">0</b></span><span class="t">MES</span><span class="mn" id="mn">1'</span>` },
    slam("sl-end", END - 0.3, END + 1, "11 YAMALS<br><b>vs.</b> 11 YOUNG MESSIS", 340, 92),
  ];
  const bubbles = [
    { who: "M10", t0: c("s2.arg") + 0.15, t1: s("s3") - 0.05, text: "HEY!", cls: "dark" },
    { who: "REF", t0: c("s3.n19") + 0.3, t1: c("s3.more") - 0.1, text: "BOTH 19?!", cls: "" },
    { who: "M10", t0: c("s3.know") + 0.1, t1: s("s4") - 0.05, text: "😉", cls: "" },
    { who: "Y10", t0: c("s4.met") + 0.2, t1: BATH - 0.1, text: "...?", cls: "" },
    { who: "M10", t0: BATH + 0.6, t1: BATHE - 0.1, text: "SPLASH SPLASH", cls: "small" },
    { who: "Y10", t0: s("s6") + 0.2, t1: G2 - 0.3, text: "304!", cls: "red" },
    { who: "Y4", t0: G2 + 0.3, t1: s("s7") - 0.1, text: "WAIT—", cls: "dark" },
    { who: "REF", t0: c("s7.follow") + 0.05, t1: c("s7.q") - 0.05, text: "♥ LIKE + FOLLOW +", cls: "red follow" },
    { who: "Y10", t0: c("s7.q"), t1: s("s8") - 0.1, text: "YAMAL?", cls: "red" },
    { who: "M10", t0: c("s7.q") + 0.3, t1: s("s8") - 0.1, text: "MESSI?", cls: "dark" },
    { who: "Y5", t0: c("s8.hw") + 0.05, t1: s("s9") - 0.1, text: "MATHS?!", cls: "" },
    { who: "Y7", t0: c("s8.hw") + 0.45, t1: s("s9") - 0.1, text: "HELP", cls: "dark small" },
  ];
  const bursts = [{ who: "Y10", t: SHOT1, text: "CURL!" }, { who: "M10", t: K2, text: "BOOM!" }];
  const minute = (t) => t >= c("s10.last") ? "90'" : t >= s("s9") ? "50'" : t >= s("s8") ? "HT" : t >= s("s6") ? "3'" : "2'";

  return {
    actors: A, ball, shots: sh, overlays, bubbles, bursts, props,
    grade: "contrast(1.14) saturate(1.2) brightness(0.95)",
    nets: { left: [G2, G3], right: [G1] }, shake: [G1, G2, G3],
    crowd: (t) => [G1, G2, G3].some((g) => t > g && t < g + 2.4) ? 0.5 : t > RUN0 && t < G3 ? 0.3 : 0.1,
    flashes: (t) => ([G1, G3].some((g) => t > g && t < g + 2) ? 0.3 : 0.05),
    speedlines: (t) => Math.max(0.55 * (1 - sstep(CUT - 0.1, CUT + 0.1, t)), 0.55 * sstep(END - 0.35, END - 0.2, t),
      0.4 * sstep(RUN0, RUN0 + 0.2, t) * (1 - sstep(RUN1, RUN1 + 0.3, t))),
    custom: (t, { el }) => {
      el("hs").textContent = String(t >= G1 ? 1 : 0);
      el("as").textContent = String(t >= G3 ? 2 : t >= G2 ? 1 : 0);
      el("mn").textContent = minute(t);
      let pop = 0; for (const g of [G1, G2, G3]) if (t >= g && t < g + 0.3) pop = Math.sin(((t - g) / 0.3) * Math.PI);
      el("hud").style.transform = `scale(${1 + pop * 0.15})`;
      const rise = sstep(c("s9.bt") - 0.15, c("s9.bt") + 0.45, t);                                       // the foam rises and wobbles
      el("foam").style.transform = `translateY(${((1 - rise) * 820 + Math.sin(t * 3) * 10).toFixed(1)}px)`;
      const dp = sstep(c("s9.bt") + 0.25, c("s9.bt") + 0.5, t);
      el("duck").style.transform = `translateY(${((1 - dp) * 300 + Math.sin(t * 4) * 8).toFixed(1)}px) rotate(${(Math.sin(t * 3) * 8).toFixed(1)}deg)`;
    },
  };
}
