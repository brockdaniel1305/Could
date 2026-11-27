// S2E16 "Could Chelsea beat 11 traffic cones?" - after three defeats in a row Chelsea face eleven orange traffic cones (4-4-2,
// the keeper cone wears gloves). The cones never move. Chelsea attack +x (cone goal x = +52.5), Chelsea's own goal x = -52.5.
// Thread: a Chelsea player runs into a cone (hook) -> the cones win 1-0 by a clearance off a cone into Chelsea's own goal.
import { path, sstep, clamp, lerp } from "./engine.js";

export default function plot(T) {
  const c = (k) => { if (!(k in T.cue)) throw new Error("cue " + k); return T.cue[k]; };
  const s = (k) => T.start[k];
  const END = T.duration, LOOPJ = END - 0.12;

  const CHE = ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10", "C11"];
  const CON = ["K1", "K2", "K3", "K4", "K5", "K6", "K7", "K8", "K9", "K10", "K11"];
  const names = [...CHE, ...CON, "XA", "REF"];
  const W = {}; names.forEach((n) => (W[n] = []));
  const at = (n, t, x, z, e) => W[n].push([t, x, z, e]);
  const jumpAll = (t, f) => names.forEach((n) => { const p = f(n); if (p) at(n, t, p[0], p[1], "j"); });
  const OFF = (n) => [90 + names.indexOf(n) * 2, 70];

  // the cones' 4-4-2 (compact), keeper on the line
  const FORM = { K1: [51.3, 0], K2: [34, -6], K3: [34, -2], K4: [34, 2], K5: [34, 6], K6: [24, -6], K7: [24, -2], K8: [24, 2], K9: [24, 6],
    K10: [14, -2], K11: [14, 2] };
  const cone = (n) => FORM[n];

  // key times
  const HIT0 = 1.0;                                            // hook: runs into the cone
  const CONEHIT = c("s4.cone") + 0.3;
  const P1 = c("s5.p1") - 0.02, C1T = c("s5.c1") - 0.02, P2 = c("s5.p2") - 0.02;
  const PASS = c("s7.hit") - 0.45, PHIT = c("s7.hit") - 0.05;
  const CLR = c("s8.clear") + 0.05, CBOUNCE = CLR + 0.45, GOAL = c("s8.own") + 0.9;
  const DROP = c("s2.cones") + 0.05;

  // ---------- s1 hook: Chelsea's number 7 sprints straight into a cone; then the line-up ----------
  const HOOK = (n) => (n === "C9" ? [5.5, -2] : CON.includes(n) ? cone(n) : n === "REF" ? [6, 9] : OFF(n));
  names.forEach((n) => { const p = HOOK(n); at(n, 0, p[0], p[1]); });
  at("C9", HIT0, 13.4, -2, "l"); at("C9", HIT0 + 0.5, 14.6, -1.6, "o");
  const LINE = (n) => { const i = CHE.indexOf(n); if (i >= 0) return [-2 - (i % 4) * 2.2, -4.5 + Math.floor(i / 4) * 3];
    return CON.includes(n) ? cone(n) : n === "REF" ? [0, -6] : OFF(n); };
  jumpAll(1.5, LINE);

  // ---------- s2 Chelsea, heads down; the cones drop onto the pitch ----------
  jumpAll(s("s2") - 0.05, (n) => { const i = CHE.indexOf(n); return i >= 0 ? [-10 + i * 2, 0] : CON.includes(n) ? cone(n) : OFF(n); });
  jumpAll(c("s2.so") - 0.06, (n) => (CON.includes(n) ? cone(n) : OFF(n)));

  // ---------- s4 kick-off: dribble into the first cone ----------
  jumpAll(s("s4") - 0.05, (n) => { const i = CHE.indexOf(n);
    if (n === "C9") return [0.8, -2]; if (n === "C1") return [-48, 0];
    if (i >= 0) return [-3 - (i % 4) * 5, -10 + (i % 5) * 5];
    return CON.includes(n) ? cone(n) : n === "REF" ? [2, 8] : OFF(n); });
  at("C9", c("s4.drib"), 2.0, -2); at("C9", CONEHIT, 13.4, -2, "l"); at("C9", CONEHIT + 0.5, 14.6, -1.6, "o");

  // ---------- s5 the pinball shot ----------
  jumpAll(s("s5") - 0.05, (n) => (n === "C10" ? [41.0, 2.6] : n === "C9" ? [30, 8] : CON.includes(n) ? cone(n) : n === "REF" ? [36, 12] : OFF(n)));

  // ---------- s6 face to face: Chelsea or the cones? ----------
  jumpAll(s("s6") - 0.05, (n) => (n === "C8" ? [-0.7, 0] : n === "K10" ? [0.75, 0] : n === "REF" ? [0, -3] : CON.includes(n) ? cone(n) : OFF(n)));

  // ---------- s7 Alonso's plan: pass around them ----------
  jumpAll(s("s7") - 0.05, (n) => (n === "XA" ? [-6, 31] : n === "C6" ? [18, 2] : n === "C7" ? [27, -3] : CON.includes(n) ? cone(n) : n === "REF" ? [20, 10] : OFF(n)));

  // ---------- s8 90th minute: clearance off a cone into Chelsea's own goal ----------
  jumpAll(s("s8") - 0.05, (n) => (n === "C2" ? [-46, 0.6] : n === "C1" ? [-51.2, -2.6] : n === "C3" ? [-44, -5] : n === "K11" ? [-41, 0.8] :
    n === "REF" ? [-36, 9] : CON.includes(n) ? cone(n) : OFF(n)));

  // ---------- s9 the cones celebrate (standing still) ----------
  jumpAll(s("s9") - 0.05, (n) => (n === "K11" ? cone(n) : CON.includes(n) ? cone(n) : n === "C2" ? [-40, 6] : OFF(n)));

  // loop back into the hook
  names.forEach((n) => { const p = HOOK(n); at(n, LOOPJ, p[0], p[1], "j"); at(n, END, p[0], p[1]); });
  for (const n of names) W[n].sort((p, q) => p[0] - q[0]);

  // ---------------- actors ----------------
  const A = {};
  for (const n of names) {
    const ev = [];
    const isCone = CON.includes(n);
    if (n === "C9") ev.push(["fall", HIT0, 0, 1], ["up", 1.45], ["fall", CONEHIT, 0, 1], ["dizzy", CONEHIT + 0.3, s("s5") - CONEHIT - 0.35], ["up", s("s5") - 0.1]);
    if (n === "C10") ev.push(["armsUp", P2 + 0.3, 0.3], ["arms", P2 + 0.6, s("s6") - P2 - 0.7, 150]);
    if (n === "XA") ev.push(["armR", c("s7.xa") - 0.1, PHIT - c("s7.xa") + 0.1, 60], ["arms", PHIT + 0.5, s("s8") - PHIT - 0.5, 150]);
    if (n === "C2") ev.push(["dive", GOAL - 0.7, 1], ["up", s("s9") - 0.1]);
    if (n === "C1") ev.push(["dive", GOAL - 0.35, -1], ["up", s("s9") - 0.1]);
    if (n === "C8") ev.push(["arms", c("s6.q") + 0.1, s("s7") - c("s6.q") - 0.2, 40]);
    if (isCone && n !== "K10" || n === "K10") { /* cones never move */ }
    if (isCone) ev.push(["hide", s("s2") + 0.05, DROP + CON.indexOf(n) * 0.07 - s("s2") - 0.05]);
    const k = CON.indexOf(n);
    A[n] = isCone
      ? { path: W[n], ev, h: 0.75, unit: 300, stride: 9, yAt: (t) => { const t0 = DROP + k * 0.07, f = clamp((t - t0) / 0.35, 0, 1);
          return t < s("s2") || t > t0 + 0.6 ? 0 : (1 - f * f) * 7 + (f >= 1 ? Math.abs(Math.sin((t - t0 - 0.35) * 14)) * 0.12 * (1 - sstep(t0 + 0.35, t0 + 0.6, t)) : 0); } }
      : { path: W[n], ev, h: 1.82, unit: 360, stride: 1.9, autoFlip: true };
  }

  // ---------------- ball ----------------
  const ball = [
    { t0: 0, k: "at", who: "C9", dx: 0.5, dz: 0 },
    { t0: HIT0, t1: HIT0 + 0.8, k: "fly", a: [13.6, 0, -2], b: [17, 0, 1.0], h: 0.5, ease: "o" },
    { t0: HIT0 + 0.8, k: "rest", p: [17, 0, 1.0] },
    { t0: 1.5, k: "rest", p: [0, 0, 0] },
    { t0: s("s2") - 0.05, k: "rest", p: [0, -50, 0] },
    { t0: s("s4") - 0.05, k: "rest", p: [1.3, 0, -2] },
    { t0: c("s4.drib"), k: "at", who: "C9", dx: 0.5, dz: 0 },
    { t0: CONEHIT, t1: CONEHIT + 0.8, k: "fly", a: [13.6, 0, -2], b: [17, 0, 1.0], h: 0.5, ease: "o" },
    { t0: CONEHIT + 0.8, k: "rest", p: [17, 0, 1.0] },
    { t0: s("s5") - 0.05, k: "rest", p: [41.6, 0, 2.2] },
    { t0: c("s5.shot"), t1: P1, k: "fly", a: [41.6, 0, 2.2], b: [52.5, 1.2, 3.55], h: 0.6 },
    { t0: P1, t1: C1T, k: "fly", a: [52.5, 1.2, 3.55], b: [51.1, 0.45, 0.6], h: 1.2 },
    { t0: C1T, t1: P2, k: "fly", a: [51.1, 0.45, 0.6], b: [52.5, 1.0, -3.55], h: 0.9 },
    { t0: P2, t1: P2 + 0.8, k: "fly", a: [52.5, 1.0, -3.55], b: [50.5, 0, -9], h: 0.6, ease: "o" },
    { t0: P2 + 0.8, k: "rest", p: [50.5, 0, -9] },
    { t0: s("s6") - 0.05, k: "rest", p: [0, 0, 0.6] },
    { t0: s("s7") - 0.05, k: "at", who: "C6", dx: 0.5, dz: 0 },
    { t0: PASS, t1: PHIT, k: "fly", a: [18.6, 0, 2], b: [23.8, 0.2, 2.0], h: 0.1 },
    { t0: PHIT, t1: PHIT + 0.6, k: "fly", a: [23.8, 0.2, 2.0], b: [20.5, 0, 3.6], h: 0.6, ease: "o" },
    { t0: PHIT + 0.6, k: "rest", p: [20.5, 0, 3.6] },
    { t0: s("s8") - 0.05, k: "at", who: "C2", dx: 0.5, dz: 0 },
    { t0: CLR, t1: CBOUNCE, k: "fly", a: [-45.4, 0, 0.6], b: [-41.2, 0.35, 0.8], h: 0.2 },
    { t0: CBOUNCE, t1: GOAL, k: "fly", a: [-41.2, 0.35, 0.8], b: [-53.4, 0.15, 0.4], h: 1.8, ease: "o" },
    { t0: GOAL, k: "rest", p: [-53.6, 0.12, 0.4] },
    { t0: s("s9") - 0.05, k: "rest", p: [0, -50, 0] },
    { t0: LOOPJ, k: "at", who: "C9", dx: 0.5, dz: 0 },
  ];

  // ---------------- props ----------------
  const PS = {}; const pos = (n, t) => { const p = (PS[n] = PS[n] || path(A[n].path))(t); return [p.x, p.z]; };
  const props = {
    board: { h: 0.5, unit: 130, at: (t) => { const p = pos("XA", t); return [p[0] + 0.45, 1.05, p[1] + 0.15]; }, only: [s("s7") - 0.05, PHIT + 0.5] },
    confetti: { h: 1.4, unit: 600, at: (t) => [51.3, 1.9 - ((t - s("s9")) * 0.5) % 1.4, 0.3], only: [s("s9") + 0.1, LOOPJ] },
  };

  // ---------------- camera ----------------
  const sh = [], add = (o) => sh.push(o);
  const HOOKCAM = { k: "follow", who: "C9", off: [[-2.8, 1.2, 0.8], [-2.6, 1.1, 0.8]], look: [4, 0.6, 0], fov: [52, 50], blur: 1.4 };
  add({ t0: 0, ...HOOKCAM });
  add({ t0: 1.5, whip: true, k: "path", P: [[-12, 4.0, 1.5], [-11, 3.6, 1.2]], T: [[20, 0.2, 0], [20, 0.2, 0]], fov: [50, 48], blur: 0.8 });
  add({ t0: s("s2") + 0.05, whip: true, k: "path", P: [[-8, 1.5, 6.5], [4, 1.5, 6.5]], T: [[-8, 1.1, -2], [4, 1.1, -2]], fov: [50, 50], blur: 1.2, ease: "l" });
  add({ t0: c("s2.so") - 0.05, whip: true, k: "path", P: [[7, 3.4, 0], [9, 3.0, 0]], T: [[27, 0, 0], [27, 0, 0]], fov: [52, 50], blur: 0.8 });
  add({ t0: s("s3") + 0.05, whip: true, k: "path", P: [[48.2, 0.75, 1.8], [48.6, 0.7, 1.4]], T: [[51.3, 0.45, 0], [51.3, 0.45, 0]], fov: [46, 40], blur: 1.8 });
  add({ t0: s("s4") + 0.05, whip: true, k: "follow", who: "C9", off: [[-2.8, 1.2, 0.8], [-2.6, 1.1, 0.8]], look: [4, 0.6, 0], fov: [52, 50], blur: 1.4 });
  add({ t0: CONEHIT + 0.6, blend: 0.3, k: "path", P: [[12.5, 0.9, 1.4], [12.7, 0.8, 1.0]], T: [[14.2, 0.4, -1.8], [14.2, 0.4, -1.8]], fov: [48, 44], blur: 1.6 });
  add({ t0: s("s5") + 0.05, whip: true, k: "path", P: [[45.5, 1.2, 2.2], [45.8, 1.2, 0], [46, 1.2, -2.2]], T: [[52.5, 0.9, 2.8], [52, 0.7, 0], [52.5, 0.9, -2.8]], fov: [54, 52], blur: 1.0 });
  add({ t0: s("s6") + 0.05, whip: true, k: "path", P: [[0, 1.3, 5.2], [0, 1.3, 4.7]], T: [[0, 1.25, 0], [0, 1.25, 0]], fov: [48, 44], blur: 2.0 });
  add({ t0: s("s7") + 0.05, whip: true, k: "path", P: [[-4.8, 1.5, 35.2], [-5.0, 1.5, 34.8]], T: [[-6, 1.2, 31], [-6, 1.2, 31]], fov: [46, 42], blur: 1.8 });
  add({ t0: PASS - 0.25, whip: true, k: "path", P: [[12.0, 1.7, 3.4], [12.8, 1.6, 3.3]], T: [[23, 0.5, 2], [23, 0.5, 2]], fov: [50, 48], blur: 1.2 });
  add({ t0: PHIT + 0.6, whip: true, k: "path", P: [[-4.8, 1.5, 35.4], [-5.0, 1.5, 35.0]], T: [[-6, 1.2, 31], [-6, 1.2, 31]], fov: [44, 40], blur: 1.8 });
  add({ t0: s("s8") + 0.05, whip: true, k: "path", P: [[-34.5, 1.8, 0.9], [-35.5, 1.7, 0.8]], T: [[-48, 0.5, 0.3], [-48, 0.5, 0.3]], fov: [54, 52], blur: 1.0 });
  add({ t0: c("s8.own") - 0.3, blend: 0.3, k: "path", P: [[-39.5, 1.6, 1.4], [-40.5, 1.4, 1.2]], T: [[-53, 0.6, 0.3], [-53, 0.6, 0.3]], fov: [56, 52], blur: 1.4 });
  add({ t0: c("s8.one") - 0.05, whip: true, k: "path", P: [[4, 6.5, 0], [8, 5.5, 0]], T: [[30, 0, 0], [30, 0, 0]], fov: [52, 50], blur: 0.8 });
  add({ t0: s("s9") + 0.05, whip: true, k: "path", P: [[48.4, 0.8, 1.6], [48.8, 0.75, 1.2]], T: [[51.3, 0.5, 0], [51.3, 0.5, 0]], fov: [48, 42], blur: 1.8 });
  add({ t0: LOOPJ, blend: 0.12, ...HOOKCAM });
  sh.forEach((x, i) => { x.t1 = x.t1 ?? (sh[i + 1] ? sh[i + 1].t0 : END); });
  sh[sh.length - 1].t1 = END;

  // ---------------- overlays ----------------
  const chip = (id, t0, t1, kk, v, x, y, cls = "", from = "right") => ({ id, t0, t1, from, cls: "chip " + cls, style: `left:${x}px;top:${y}px`,
    html: `<div class="ck">${kk}</div><div class="cv">${v}</div>` });
  const slam = (id, t0, t1, html, top, size = 96) => ({ id, t0, t1, slam: true, cls: "slam", style: `top:${top}px;font-size:${size}px`, html });
  const overlays = [
    slam("sl-a", -1, s("s2") - 0.05, "CHELSEA<br><b>vs.</b> 11 TRAFFIC CONES", 330, 90),
    chip("c-lost", c("s2.three"), c("s2.so") - 0.05, "CHELSEA · PREMIER LEAGUE", "LOST: 3 IN A ROW", 60, 420, "red"),
    chip("c-opp", c("s2.cones") + 0.2, s("s3") - 0.05, "TODAY'S OPPONENT", "11 TRAFFIC CONES", 80, 420, "gold"),
    chip("c-tac", c("s3.still") - 0.05, s("s4") - 0.05, "CONES · TACTIC", "STAND STILL", 100, 420, "dark"),
    chip("c-ping", P1, s("s6") - 0.05, "SHOT", "POST · CONE · POST", 80, 420, "dark"),
    chip("c-plan", c("s7.plan") - 0.05, PHIT - 0.3, "ALONSO'S PLAN", "PASS AROUND THEM", 80, 420, "gold"),
    chip("c-own", GOAL + 0.2, s("s9") - 0.05, "GOAL · 90' · OWN GOAL", "CONES 1–0 CHELSEA", 60, 420, "red"),
    chip("c-who", c("s9.who"), LOOPJ, "COMMENT · YES or NO", "Would YOUR team<br>beat the cones?", 80, 420, "red"),
    { id: "hud", t0: c("s4.ko") - 0.1, t1: LOOPJ, cls: "hud", style: "opacity:0",
      html: `<span class="t">CHE</span><span class="sc"><b id="hs">0</b>–<b id="as">0</b></span><span class="t">CONES</span><span class="mn" id="mn">1'</span>` },
    slam("sl-end", END - 0.3, END + 1, "CHELSEA<br><b>vs.</b> 11 TRAFFIC CONES", 330, 90),
  ];
  const bubbles = [
    { who: "C5", t0: c("s2.three") + 0.4, t1: c("s2.so") - 0.1, text: "AGAIN?!", cls: "che small" },
    { who: "K1", t0: c("s3.still") + 0.3, t1: s("s4") - 0.1, text: "...", cls: "cone small" },
    { who: "K10", t0: CONEHIT + 0.7, t1: s("s5") - 0.1, text: "...", cls: "cone small" },
    { who: "REF", t0: c("s6.follow") + 0.05, t1: c("s6.q") - 0.05, text: "♥ LIKE + FOLLOW +", cls: "red follow" },
    { who: "C8", t0: c("s6.q"), t1: s("s7") - 0.1, text: "CHELSEA?", cls: "che" },
    { who: "K10", t0: c("s6.q") + 0.3, t1: s("s7") - 0.1, text: "CONES?", cls: "cone" },
    { who: "XA", t0: c("s7.plan") + 0.1, t1: PHIT - 0.3, text: "PASS AROUND THEM!", cls: "small" },
    { who: "XA", t0: PHIT + 0.7, t1: s("s8") - 0.1, text: "...WHY?", cls: "small" },
    { who: "K1", t0: c("s9.cel") + 0.4, t1: c("s9.who") - 0.1, text: "...", cls: "cone small" },
  ];
  const bursts = [{ who: "C9", t: HIT0, text: "BONK!" }, { who: "C9", t: CONEHIT, text: "BONK!" },
    { who: "K1", t: P1, text: "PING!" }, { who: "K1", t: C1T, text: "BOINK!" }, { who: "K1", t: P2, text: "PING!" }, { who: "K7", t: PHIT, text: "BONK!" },
    { who: "K11", t: CBOUNCE, text: "BOINK!" }];
  const minute = (t) => (t >= s("s8") ? "90'" : t >= s("s7") ? "61'" : t >= s("s5") ? "17'" : "1'");

  return {
    actors: A, ball, shots: sh, overlays, bubbles, bursts, props,
    grade: "contrast(1.12) saturate(1.2) brightness(0.96)",
    nets: { right: [], left: [GOAL] }, shake: [HIT0, CONEHIT, P1, P2, GOAL],
    crowd: (t) => (t > GOAL && t < GOAL + 3 ? 0.5 : 0.12),
    flashes: (t) => (t > GOAL && t < GOAL + 2.5 ? 0.3 : 0.06),
    speedlines: (t) => Math.max(0.5 * sstep(0.2, 0.5, t) * (1 - sstep(HIT0, HIT0 + 0.2, t)), 0.5 * sstep(END - 0.35, END - 0.2, t),
      0.4 * sstep(c("s4.drib"), c("s4.drib") + 0.2, t) * (1 - sstep(CONEHIT, CONEHIT + 0.2, t))),
    custom: (t, { el }) => {
      el("hs").textContent = "0";
      el("as").textContent = String(t >= GOAL ? 1 : 0);
      el("mn").textContent = minute(t);
      let pop = 0; if (t >= GOAL && t < GOAL + 0.3) pop = Math.sin(((t - GOAL) / 0.3) * Math.PI);
      el("hud").style.transform = `scale(${1 + pop * 0.15})`;
    },
  };
}
