// S2E12 "Could Usain Bolt beat a T-Rex in a 100 m sprint?" - remake of 002 on a red 100 m straight in the night stadium.
// Race model from 002 (FACTS.md): Bolt's Berlin 2009 10 m splits; T-Rex nose starts 12 m ahead, ~5.4 m/s; lead change ~34.5 m
// at 4.17 s; T-Rex at 63.7 m when Bolt finishes (9.58 s); T-Rex finishes at 16.3 s. Video time is mapped onto race time.
// Gags: lightning pose, pose with tiny arms, starter roared over, nose-first lead, "don't look back", dip finish without arms,
// photo finish needs two photos, the T-Rex does not stop at the line -> round two, no finish line.
// The cameras all sit on the -z side, so +x (the running direction) is screen-LEFT; the T-Rex sprite is mirrored to face left.
import { path, sstep, clamp, lerp } from "./engine.js";
import { buildTrack, laneZ } from "./track3d.js";

export default function plot(T) {
  const c = (k) => { if (!(k in T.cue)) throw new Error("cue " + k); return T.cue[k]; };
  const s = (k) => T.start[k];
  const END = T.duration, CUT = 1.3, LOOPJ = c("s11.loop") - 0.5;
  const X0 = -50, ZB = laneZ(4), ZR = laneZ(5) + 1.2, NOSE = 4.1;
  const G = c("s4.bang"), M35 = c("s8.m35") + 0.6, FIN = c("s9.fin") + 0.1, RFIN = c("s9.dip") + 1.15;

  // ---- race model ----
  const SPLIT_T = [0, 1.89, 2.88, 3.78, 4.64, 5.47, 6.29, 7.10, 7.92, 8.75, 9.58], SPLIT_X = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100];
  const interp = (r, xs, ys) => { if (r <= xs[0]) return ys[0]; for (let i = 1; i < xs.length; i++) if (r <= xs[i]) return lerp(ys[i - 1], ys[i], (r - xs[i - 1]) / (xs[i] - xs[i - 1])); return ys[ys.length - 1]; };
  const raceT = (t) => interp(t, [G, M35, FIN, RFIN], [0, 4.17, 9.58, 16.3]);
  const boltX = (t) => { if (t < FIN) return X0 + interp(raceT(t), SPLIT_T, SPLIT_X);
    return X0 + 100 + 2.4 * (1 - Math.exp(-(t - FIN) / 0.5)); };                                 // eases out just past the line
  const FLEE = c("s10.not") + 0.2;
  const boltZ = (t) => (t < FLEE ? ZB : ZB - (t - FLEE) * 6.2);                                       // ... then runs for his life, sideways
  const rexNose = (t) => { if (t < RFIN) return X0 + 12 + 5.4 * raceT(t); return Math.min(X0 + 103.5, X0 + 100 + (t - RFIN) * 1.7); };
  const rexZ = (t) => (t < FLEE + 0.3 ? ZR : ZR - (t - FLEE - 0.3) * 5.8);
  const W = { B: [], R: [], S: [] };
  const at = (n, t, x, z, e) => W[n].push([t, x, z, e]);
  // hook / intro: at the blocks
  at("B", 0, X0 - 0.2, ZB); at("R", 0, X0 + 12 - NOSE, ZR); at("S", 0, X0 + 6.5, -3.0);
  for (let t = G; t <= LOOPJ; t += 0.1) { at("B", t, boltX(t), boltZ(t), "l"); at("R", t, rexNose(t) - NOSE, rexZ(t), "l"); }
  at("S", END, X0 + 6.5, -3.0);
  at("B", LOOPJ + 0.01, X0 - 0.2, ZB, "j"); at("R", LOOPJ + 0.01, X0 + 12 - NOSE, ZR, "j"); at("B", END, X0 - 0.2, ZB); at("R", END, X0 + 12 - NOSE, ZR);
  for (const n of ["B", "R", "S"]) W[n].sort((p, q) => p[0] - q[0]);

  const POSE = (t0, d) => [["arms", t0, d, 55], ["armR", t0, d]];                                 // lightning pose (one arm high, one out)
  const A = {
    B: { path: W.B, ev: [...POSE(c("s2.prime") + 0.2, s("s3") - c("s2.prime") - 0.3), ["charge", G, FIN - G], ...POSE(c("s10.wins") + 0.1, c("s10.not") - c("s10.wins") - 0.1),
      ["spin", c("s10.not") - 0.1, 0.5]], h: 1.95, unit: 360, stride: 2.6 },
    R: { path: W.R, ev: [["arms", c("s3.arms") - 0.2, 1.4, 170], ["lean", RFIN - 0.55, 1.1, 24], ["charge", G + 0.6, 30]], h: 5.0, unit: 330, stride: 3.6 },
    S: { path: W.S, ev: [["armR", G - 0.3, 0.6], ["fall", c("s4.pers") + 0.45, 0, -1], ["up", s("s6")]], h: 1.8, unit: 360, stride: 1.9 },
  };
  A.B.look = (t) => (t >= c("s10.line") && t < c("s10.not") ? -1 : 0);
  const roar = (t) => [[0, CUT + 0.1], [c("s4.pers") + 0.1, c("s4.pers") + 1.7], [M35 - 0.4, M35 + 1.6], [c("s10.not"), END]].some(([a, b]) => t >= a && t < b);

  // ---------------- camera (all on the -z side) ----------------
  const sh = [], add = (o) => sh.push(o);
  const track = (t0, t1, fn, look, fov, blur = 1.6) => { const P = [], Tg = [];                 // a tracking shot sampled from the race model
    for (let k = 0; k <= 8; k++) { const t = lerp(t0, t1, k / 8), x = fn(t); P.push([x + look[0], look[1], look[2]]); Tg.push([x + look[3], look[4], look[5]]); }
    return { t0, k: "path", ease: "l", P, T: Tg, fov, blur }; };
  const HOOKCAM = { k: "path", P: [[X0 - 4.2, 1.5, -1.7], [X0 - 4.0, 1.5, -1.6]], T: [[X0 + 8, 2.4, 0.6], [X0 + 8, 2.3, 0.6]], fov: [52, 50], roll: -3, blur: 2.0 };
  add({ t0: 0, ...HOOKCAM });
  add({ t0: CUT, whip: true, k: "path", P: [[X0 + 14, 7, -24], [X0 + 10, 6, -21]], T: [[X0 + 6, 0.5, 0], [X0 + 6, 0.5, 0]], fov: [50, 50], blur: 0.8 });
  add({ t0: s("s2") + 0.05, whip: true, k: "path", P: [[X0 - 0.2, 1.62, ZB - 4.4], [X0 - 0.2, 1.62, ZB - 3.6]], T: [[X0 - 0.2, 1.72, ZB], [X0 - 0.2, 1.75, ZB]], fov: [44, 40], blur: 2.4 });
  add({ t0: s("s3") + 0.05, whip: true, k: "path", P: [[X0 + 6.6, 3.0, -9.5], [X0 + 6.8, 3.1, -8.6]], T: [[X0 + 7.4, 3.0, ZR], [X0 + 7.4, 3.2, ZR]], fov: [50, 48], blur: 2.0 });
  add({ t0: s("s4") + 0.05, whip: true, k: "path", P: [[X0 + 4.5, 1.8, -8.8], [X0 + 4.7, 1.9, -8.4]], T: [[X0 + 8, 2.6, -0.4], [X0 + 8.2, 2.8, -0.4]], fov: [50, 48], blur: 1.8 });
  add({ t0: s("s5") + 0.05, blend: 0.4, ...track(s("s5") + 0.05, s("s6"), (t) => (boltX(t) + rexNose(t)) / 2, [-2, 18, -9, -2, 0, 0], [50, 50], 0.8) });
  add({ t0: s("s6") + 0.05, blend: 0.4, ...track(s("s6") + 0.05, M35 - 0.8, (t) => 0.62 * boltX(t) + 0.38 * (rexNose(t) - NOSE), [0, 2.8, -18, 0, 2.0, 0.6], [50, 50]) });
  add({ t0: M35 - 0.8, whip: true, ...track(M35 - 0.8, c("s8.look") + 1.0, boltX, [7.5, 1.6, -3.2, -4, 2.2, 0.8], [50, 50]) });
  add({ t0: c("s8.look") + 1.0, whip: true, k: "path", P: [[X0 + 96.6, 1.8, -11], [X0 + 96.8, 1.9, -10.4]], T: [[X0 + 99.4, 2.2, 0.6], [X0 + 99.4, 2.3, 0.6]], fov: [54, 54], blur: 1.4 });
  add({ t0: c("s10.wins") - 0.05, whip: true, k: "path", P: [[X0 + 95, 2.0, -9.5], [X0 + 95.4, 2.0, -9.0]], T: [[X0 + 101.2, 2.3, 0.2], [X0 + 101.2, 2.4, 0.2]], fov: [52, 50], blur: 1.8 });
  { const t0 = c("s11.r2") - 0.05, P = [], Tg = [];
    for (let k = 0; k <= 8; k++) { const t = lerp(t0, LOOPJ, k / 8), mx = (boltX(t) + rexNose(t) - NOSE) / 2, mz = (boltZ(t) + rexZ(t)) / 2;
      P.push([mx - 15, 4.5, mz - 6]); Tg.push([mx, 1.4, mz]); }
    add({ t0, blend: 0.3, k: "path", ease: "l", P, T: Tg, fov: [50, 50], blur: 1.2 }); }
  add({ t0: c("s11.loop") - 0.3, blend: 0.3, whip: true, ...HOOKCAM });
  sh.forEach((x, i) => { x.t1 = x.t1 ?? (sh[i + 1] ? sh[i + 1].t0 : END); });
  sh[sh.length - 1].t1 = END;

  // ---------------- overlays ----------------
  const chip = (id, t0, t1, kk, v, x, y, cls = "", from = "right") => ({ id, t0, t1, from, cls: "chip " + cls, style: `left:${x}px;top:${y}px`,
    html: `<div class="ck">${kk}</div><div class="cv">${v}</div>` });
  const slam = (id, t0, t1, html, top, size = 128) => ({ id, t0, t1, slam: true, cls: "slam", style: `top:${top}px;font-size:${size}px`, html });
  const overlays = [
    slam("sl-a", -1, s("s2") - 0.05, "BOLT <b>vs.</b> T-REX<br>100 M", 330, 104),
    chip("c-wr", c("s2.wr"), s("s3") - 0.05, "LANE 4 · BERLIN 2009", "9.58 s", 80, 400, "gold"),
    chip("c-kg", c("s3.kg"), c("s3.arms") + 0.6, "LANE 5 · T-REX", "8 tonnes", 80, 400, "dark"),
    chip("c-66", c("s3.arms") + 0.6, s("s4") - 0.05, "LAST RACE", "66 million years ago", 60, 400, "dark"),
    chip("c-lead", c("s5.nose") + 0.6, s("s6") - 0.05, "NOSE FIRST", "T-REX LEADS +12 m", 80, 400, "red"),
    chip("c-vb", c("s7.bolt"), s("s8") - 0.05, "BOLT · TOP SPEED", "44.7 km/h", 80, 400, "gold"),
    chip("c-vr", c("s7.rex"), s("s8") - 0.05, "T-REX · EST.", "~19 km/h", 80, 560, "dark"),
    chip("c-35", M35 - 0.2, c("s8.look") - 0.1, "35 m", "BOLT LEADS", 80, 400, "gold"),
    chip("c-photo", c("s9.dip") + 0.6, s("s10") - 0.05, "PHOTO FINISH", "2 photos needed", 80, 400, "red"),
    chip("c-win", c("s10.wins"), c("s10.not") - 0.05, "WINNER · 9.58 s", "Usain Bolt", 80, 400, "gold"),
    chip("c-r2", c("s11.r2"), LOOPJ, "ROUND 2", "No finish line", 80, 400, "red"),
    chip("c-who", c("s11.who"), LOOPJ, "COMMENT", "Who will win?", 120, 1180, "red"),
    { id: "clock", t0: G - 0.3, t1: LOOPJ, cls: "clock", html: '<small>RACE CLOCK</small><span id="clk">0.00</span>' },
    slam("sl-end", END - 0.3, END + 1, "BOLT <b>vs.</b> T-REX<br>100 M", 330, 104),
  ];
  const bubbles = [
    { who: "R", t0: c("s3.arms") + 0.1, t1: s("s4") - 0.1, text: "⚡?", cls: "" },
    { who: "S", t0: c("s4.pers") + 0.9, t1: s("s5") - 0.1, text: "@#%!", cls: "dark small" },
    { who: "B", t0: c("s6.follow") + 0.05, t1: c("s6.q") - 0.05, text: "♥ LIKE + FOLLOW +", cls: "red follow" },
    { who: "B", t0: c("s6.q"), t1: s("s7") - 0.1, text: "BOLT?", cls: "" },
    { who: "R", t0: c("s6.q") + 0.3, t1: s("s7") - 0.1, text: "T-REX?", cls: "dark" },
    { who: "B", t0: c("s8.look"), t1: c("s8.look") + 1.4, text: "DON'T LOOK BACK", cls: "dark small" },
    { who: "B", t0: c("s10.not") + 0.2, t1: s("s11") + 0.4, text: "NOPE.", cls: "red" },
  ];
  const bursts = [{ who: "S", t: G, text: "BANG!" }, { who: "R", t: c("s4.pers") + 0.15, text: "ROAR!" }];

  return {
    actors: A, shots: sh, overlays, bubbles, bursts, buildWorld: buildTrack, fgMax: 8,
    grade: "contrast(1.12) saturate(1.18) brightness(0.97)",
    shake: [c("s4.pers") + 0.2, M35, c("s10.not")],
    crowd: (t) => (t > G && t < RFIN + 1 ? 0.45 : 0.12), flashes: (t) => (t > FIN && t < FIN + 2 ? 0.3 : 0.05),
    speedlines: (t) => Math.max(0.5 * (1 - sstep(CUT - 0.1, CUT + 0.1, t)), 0.35 * sstep(M35 - 1, M35 - 0.6, t) * (1 - sstep(FIN, FIN + 0.3, t)),
      0.45 * sstep(c("s10.not"), c("s10.not") + 0.3, t) * (1 - sstep(LOOPJ - 0.2, LOOPJ, t))),
    custom: (t, { el }) => {
      const r = t < G ? 0 : Math.min(raceT(t), 9.58); el("clk").textContent = r.toFixed(2);
      const j = el("w3-Rx-jaw"), h = el("w3-Rx-head"), open = roar(t) ? 22 + Math.sin(t * 30) * 4 : 0;
      if (j) j.style.transform = `rotate(${open.toFixed(1)}deg)`;
      if (h) h.style.transform = `rotate(${(roar(t) ? -8 : Math.sin(t * 2) * 2).toFixed(1)}deg)`;
    },
  };
}
