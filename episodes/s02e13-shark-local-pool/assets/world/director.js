// S2E13 "Could a shark end up in your local swimming pool?" - an honest thought experiment: we check every way in.
// Way 1 pipes (2D cross-section, the shark corks the pipe) -> no. Way 2 the sea (2D map: a great white tastes fresh water and turns
// back; a bull shark travels thousands of km up the Amazon). Way 3 floods (3D flooded street, the fake highway photo, the golf
// course lake in Queensland 1996-2013). The scenario (3D): the river next to an outdoor pool floods over the fence, a bull shark
// swims in, the water drops - it's stuck. Verdict: great white no, bull shark possible. Safety line. New sign: NO SHARKS.
import { path, sstep, clamp, lerp } from "./engine.js";
import { buildPool, POOL, STREET_X as SX, GOLF_X as GX, COAST_X as CX, riverX, PIPE } from "./pool3d.js";

export default function plot(T) {
  const c = (k) => { if (!(k in T.cue)) throw new Error("cue " + k); return T.cue[k]; };
  const s = (k) => T.start[k];
  const END = T.duration, CUT = 1.3, LOOPJ = c("s10.loop") - 0.5;
  const { W } = POOL;

  // ---- the flood (metres above the river surface) ----
  const RISE0 = c("s8.so") + 0.3, RISE1 = c("s8.so") + 2.6, FALL0 = c("s8.drop") + 0.1, FALL1 = c("s8.drop") + 1.7;
  const flood = (t) => (t < RISE0 || t > FALL1 ? 0 : t < RISE1 ? 1.7 * sstep(RISE0, RISE1, t) : t < FALL0 ? 1.7 + Math.sin(t * 3) * 0.04 : 1.7 * (1 - sstep(FALL0, FALL1, t)));
  globalThis.__flood = flood;
  const poolY = (t) => Math.max(POOL.water, flood(t) > 0 ? -0.5 + flood(t) : POOL.water);

  const W8 = { BULL: [], BULL2: [], GW: [], LG: [], GOLF: [], FLOAT1: [], FLOAT2: [] };
  const at = (n, t, x, z, e) => W8[n].push([t, x, z, e]);
  const lapPool = (n, t0, t1, ph = 0, rx = 8.5, rz = 2.6) => { for (let t = t0; t <= t1; t += 0.25) { const a = ph + (t - t0) * 0.9; at(n, t, Math.cos(a) * rx, Math.sin(a) * rz, "l"); } };
  // the bull shark in the pool: hook + loop end, cruising laps; then the flood scenario brings it in from the river
  at("BULL", 0, -7, 0.6); at("BULL", CUT, -3, 0.4, "l"); lapPool("BULL", CUT + 0.1, s("s2") - 0.1, Math.PI); at("BULL", s("s2"), 500, 500, "j");
  at("BULL", s("s6"), 500, 500, "j"); at("BULL", c("s8.so") - 0.15, -4, POOL.river + 1, "j");
  at("BULL", RISE0 + 0.6, -4, POOL.river + 2, "l"); at("BULL", RISE1, -3, -W / 2 - 3, "l"); at("BULL", FALL0 + 0.4, -1.5, -0.6, "l");
  lapPool("BULL", FALL0 + 0.5, LOOPJ - 0.1, 0.8, 7.5, 2.4);
  at("BULL", LOOPJ, -7 - 4 * (END - LOOPJ) / CUT, 0.6, "j"); at("BULL", END, -7, 0.6, "l");
  // the flooded street and the golf lake
  at("BULL2", 0, 500, 500); at("BULL2", s("s6") - 0.05, SX + 1.5, -26, "j"); at("BULL2", s("s7") - 0.1, SX - 1, 18, "l");
  for (let t = s("s7"); t <= s("s8"); t += 0.25) { const a = (t - s("s7")) * 0.7; at("BULL2", t, GX + Math.cos(a) * 14, -6 + Math.sin(a) * 7, "l"); }
  at("BULL2", s("s8") + 0.01, 500, 500, "j"); at("BULL2", END, 500, 500);
  // the sea: a great white swims into the river mouth, tastes fresh water, turns back
  const GT0 = s("s3"), GT1 = c("s3.salt") + 0.6, GT2 = c("s3.salt") + 1.3, GT3 = s("s4") + 0.3;
  at("GW", 0, 600, 600); at("GW", GT0 - 0.05, 600, 600); at("GW", GT0, CX + 16, 40, "j"); at("GW", GT1, CX + 1.5, 5, "l");
  at("GW", GT2 - 0.3, CX + 1.2, 4.2, "l"); at("GW", GT2, CX + 2.2, 5.5, "l"); at("GW", GT3, CX + 20, 42, "l"); at("GW", GT3 + 0.05, 600, 600, "j"); at("GW", END, 600, 600);
  // the Amazon: a bull shark swims from the sea into the river and on upstream (camera follows); arrives at the IQUITOS sign
  const B0 = s("s4") - 0.4, B1 = c("s4.bull") + 0.5, B2 = s("s5") - 0.2, ZEND = -385;
  W8.BULL3 = []; at("BULL3", 0, 700, 700); at("BULL3", B0 - 0.05, 700, 700); at("BULL3", B0, CX + 9, 30, "j"); at("BULL3", B1, riverX(9), 9, "l");
  const zAt = (t) => lerp(9, ZEND, Math.pow(sstep(B1, B2, t), 1.15));
  for (let t = B1 + 0.1; t <= B2; t += 0.1) { const z = zAt(t); at("BULL3", t, riverX(z) + 0.6 * Math.sin(t * 3), z, "l"); }
  at("BULL3", B2 + 0.5, riverX(ZEND - 1), ZEND - 1, "l"); at("BULL3", B2 + 0.55, 700, 700, "j"); at("BULL3", END, 700, 700);
  // the lifeguard: on the chair, then the "very strange morning" walk-in with a coffee
  const CHAIR = [4, W / 2 + 2.2];
  at("LG", 0, CHAIR[0], CHAIR[1]); at("LG", FALL0, CHAIR[0], CHAIR[1]); at("LG", FALL0 + 0.05, -10, 9.4, "j"); at("LG", c("s8.guard") + 0.9, -3.4, 7.2, "l");
  at("LG", s("s10") - 0.05, -4.6, 8.4, "j"); at("LG", LOOPJ, CHAIR[0], CHAIR[1], "j"); at("LG", END, CHAIR[0], CHAIR[1]);
  at("GOLF", 0, GX + 8, 14); at("GOLF", END, GX + 8, 14);
  for (const [n, x, z, ph] of [["FLOAT1", -3.5, -2.8, 0], ["FLOAT2", 3.2, 3.0, 2]]) for (let t = 0; t <= END; t += 0.5) at(n, t, x + Math.sin(t * 0.3 + ph) * 1.2, z + Math.cos(t * 0.25 + ph) * 0.4, "l");
  for (const n of Object.keys(W8)) W8[n].sort((p, q) => p[0] - q[0]);

  const onChair = (t) => (t < FALL0 || t >= LOOPJ ? 2.45 : 0);
  const A = {
    BULL: { path: W8.BULL, ev: [], h: 0.75, unit: 170, stride: 99, autoFlip: true, yAt: (t) => (t > c("s8.so") - 0.2 && t < RISE0 + 0.6 ? -0.5 : poolY(t)) },
    BULL2: { path: W8.BULL2, ev: [], h: 0.75, unit: 170, stride: 99, autoFlip: true, yAt: (t) => (t < s("s7") ? 1.0 : 0.03) },
    GW: { path: W8.GW, ev: [], h: 0.85, unit: 170, stride: 99, autoFlip: true, yAt: () => 0.05 },
    BULL3: { path: W8.BULL3, ev: [], h: 0.8, unit: 170, stride: 99, autoFlip: true, yAt: () => 0.06 },
    LG: { path: W8.LG, ev: [["armR", c("s5.follow"), 1.4], ["armsUp", c("s8.guard") + 1.0, 1.4], ["jump", c("s8.guard") + 1.0, 0.5], ["armR", c("s10.who") - 0.2, 1.6]],
      h: 1.85, unit: 360, stride: 1.9, yAt: onChair },
    GOLF: { path: W8.GOLF, ev: [["armsUp", c("s7.golf") + 1.4, 1.2]], h: 1.8, unit: 360, stride: 1.9 },
    FLOAT1: { path: W8.FLOAT1, ev: [], h: 0.6, unit: 110, stride: 99, yAt: (t) => poolY(t) + Math.sin(t * 2) * 0.03 },
    FLOAT2: { path: W8.FLOAT2, ev: [], h: 0.6, unit: 110, stride: 99, yAt: (t) => poolY(t) + Math.sin(t * 2 + 1) * 0.03 },
  };

  // ---------------- props ----------------
  const PS = {}; const pos = (n, t) => { const p = (PS[n] = PS[n] || path(A[n].path))(t); return [p.x, p.z]; };
  const CUPFLY = c("s8.guard") + 1.0;
  const zAtKm = (t) => (t < B1 ? 9 : zAt(Math.min(t, B2)));
  const PJ = c("s2.cm") + 0.6, PZ = -18.95, SHKF = -1;     // pipe: jam time, the shark's centre when its nose is in the pipe mouth, facing
  const props = {
    cup: { h: 0.32, unit: 110, only: [FALL0, s("s9")], at: (t) => { const l = pos("LG", Math.min(t, CUPFLY)); if (t < CUPFLY) return [l[0] + 0.4, 1.0, l[1] + 0.2];
      const f = clamp((t - CUPFLY) / 0.9, 0, 1); return [lerp(l[0] + 0.4, l[0] + 2.4, f), 1.0 + Math.sin(f * Math.PI) * 2.4 - f * 1.2, lerp(l[1] + 0.2, l[1] - 2.0, f)]; },
      rot: (t) => (t > CUPFLY ? (t - CUPFLY) * 700 : 0) },
    club: { h: 1.0, unit: 160, p: [GX + 8.45, 0.05, 14.2] },
    rules: { h: 1.9, unit: 230, p: [-7.6, 0, W / 2 + 1.6], only: [-1, c("s10.who") + 0.2] },
    rules2: { h: 2.35, unit: 280, p: [-7.6, 0, W / 2 + 1.6], only: [c("s10.who") + 0.2, LOOPJ] },
    haz: { h: 1.6, unit: 190, p: [GX + 3.5, 0, 15.5], only: [-1, c("s7.golf") + 1.3] },
    haz2: { h: 1.6, unit: 190, p: [GX + 3.5, 0, 15.5], only: [c("s7.golf") + 1.3, END + 1] },
    speed: { h: 2.4, unit: 240, p: [SX + 7.4, 0, 9] },
    // way 1: a whole bull shark noses into the 10 cm pipe mouth, gets stuck, wiggles, backs off dizzy
    SHK: { h: 1.0, unit: 128, only: [s("s2"), s("s3")], at: (t) => { const z = t < PJ ? lerp(-31, PZ, sstep(s("s2"), PJ, t)) : t < c("s2.not") + 0.4 ? PZ : lerp(PZ, PZ - 2.2, sstep(c("s2.not") + 0.4, c("s2.not") + 1.2, t));
      return [PIPE.x - 0.1, -0.5, z]; },
      sc: (t) => { const q = t > PJ && t < c("s2.not") + 0.4 ? Math.sin(t * 22) * 0.06 : 0; return [SHKF * (1 - q), 1 + q]; },
      rot: (t) => (t > PJ && t < c("s2.not") + 0.4 ? Math.sin(t * 15) * 4 : t > c("s2.not") + 0.4 ? -8 * Math.sin(t * 6) : 0) },
    pipe10: { h: 1.7, unit: 220, p: [PIPE.x + 2.1, 0.62, -17.5], only: [c("s2.cm") - 0.05, s("s3")] },
    salt: { h: 2.2, unit: 230, p: [CX + 13, 0, 10.5] },
    fresh: { h: 2.2, unit: 230, p: [CX - 8, 0, -1] },
    deadend: { h: 2.0, unit: 200, p: [CX + 6, 0, 3], only: [c("s3.dead") - 0.05, s("s4") + 0.6] },
    amz: { h: 2.6, unit: 230, p: [riverX(-14) + 7, 0, -14] },
    iq: { h: 2.6, unit: 260, p: [riverX(ZEND - 10) + 4.5, 0, ZEND - 10] },
    // the "shark on the highway": a cardboard fin glides by, gets pulled up on its stick
    hwy: { h: 2.6, unit: 230, p: [SX - 6.6, 1.0, -2] },
    cutfin: { h: 1.25, unit: 230, only: [c("s6.fake") - 0.3, c("s6.fake") + 1.3], at: (t) => [lerp(SX - 7, SX + 0.5, sstep(c("s6.fake") - 0.3, c("s6.fake") + 1.3, t)), 0.92, 3] },
    cut: { h: 1.25, unit: 230, only: [c("s6.fake") + 1.3, s("s7")], at: (t) => [SX + 0.5, 0.92 + 0.8 * sstep(c("s6.fake") + 1.3, c("s6.fake") + 1.8, t), 3],
      rot: (t) => -70 * sstep(c("s6.fake") + 2.3, c("s6.fake") + 2.7, t) },
  };

  // ---------------- camera ----------------
  const sh = [], add = (o) => sh.push(o);
  const HOOKCAM = { k: "path", P: [[-3, 1.6, 9.5], [-2.6, 1.55, 9.0]], T: [[-6, 0.0, 0.2], [-4.5, 0.0, 0.2]], fov: [48, 46], roll: -2, blur: 1.6 };
  add({ t0: 0, ...HOOKCAM });
  add({ t0: CUT, whip: true, k: "path", P: [[10, 6.5, 20], [7, 5.5, 17]], T: [[0, 0, -2], [0, 0, -2]], fov: [50, 48], blur: 0.8 });
  // way 1: along the pipe from the pool to the river, then close on the pipe mouth
  add({ t0: s("s2") + 0.05, whip: true, k: "path", P: [[PIPE.x + 6, 7, -3], [PIPE.x + 5, 5.5, -9]], T: [[PIPE.x, 0, -15], [PIPE.x, -0.2, -19]], fov: [52, 50], blur: 1.0 });
  add({ t0: c("s2.cm") - 0.05, blend: 0.5, k: "path", P: [[PIPE.x + 7.5, 1.1, -24.5], [PIPE.x + 7, 1.0, -24]], T: [[PIPE.x - 0.3, -0.1, -19.3], [PIPE.x - 0.3, -0.1, -19.3]], fov: [44, 42], blur: 2.0 });
  // way 2: the sea and the river mouth, then the bull shark chase up the Amazon
  add({ t0: s("s3") + 0.05, whip: true, k: "path", P: [[CX + 13, 5.5, 23], [CX + 11, 5, 20]], T: [[CX + 1, 0, 2], [CX + 1, 0, 2]], fov: [50, 48], blur: 1.0 });
  add({ t0: B0 + 0.4, blend: 0.6, who: "BULL3", off: [[5, 8, 15], [0, 6.5, 13]], look: [0, 0.5, -12], fov: [52, 56], blur: 1.0 });
  add({ t0: s("s5") + 0.05, whip: true, k: "path", P: [[6.2, 2.6, 13.4], [6.0, 2.7, 12.8]], T: [[4, 2.9, CHAIR[1]], [4, 3.0, CHAIR[1]]], fov: [46, 42], blur: 2.0 });
  add({ t0: s("s6") + 0.05, whip: true, k: "path", P: [[SX + 4, 3.0, 24], [SX + 3, 2.8, 18]], T: [[SX, 1.2, 0], [SX, 1.2, -4]], fov: [50, 48], blur: 1.4 });
  add({ t0: c("s6.fake") - 0.3, whip: true, k: "path", P: [[SX + 4, 2.4, 13], [SX + 3.2, 2.2, 11.5]], T: [[SX - 2, 1.4, 1], [SX - 1, 1.5, 1]], fov: [48, 46], blur: 1.4 });
  add({ t0: s("s7") + 0.05, whip: true, k: "path", P: [[GX + 14, 3.4, 26], [GX + 12, 3.0, 23]], T: [[GX + 2, 0.5, 0], [GX + 2, 0.5, 0]], fov: [50, 48], blur: 1.4 });
  add({ t0: s("s8") + 0.05, whip: true, k: "path", P: [[2, 9, 22], [1, 8.5, 21]], T: [[-1, -0.2, -9], [-1, -0.2, -8]], fov: [52, 52], blur: 0.8 });
  add({ t0: FALL1 - 0.2, blend: 0.4, k: "path", P: [[-6.5, 1.7, 13.5], [-6, 1.7, 12.5]], T: [[-1.5, 0.6, 2], [-1.5, 0.6, 1.5]], fov: [50, 48], blur: 1.6 });
  add({ t0: s("s9") + 0.05, whip: true, k: "path", P: [[0, 7, 16], [0, 6, 14]], T: [[0, -0.2, 0], [0, -0.2, 0]], fov: [50, 48], blur: 1.0 });
  add({ t0: s("s10") + 0.05, whip: true, k: "path", P: [[-5.4, 1.9, 16.2], [-5.6, 1.9, 15.4]], T: [[-6.8, 1.7, W / 2 + 1.4], [-6.8, 1.7, W / 2 + 1.4]], fov: [48, 46], blur: 2.0 });
  add({ t0: c("s10.loop") - 0.3, blend: 0.3, whip: true, ...HOOKCAM });
  sh.forEach((x, i) => { x.t1 = x.t1 ?? (sh[i + 1] ? sh[i + 1].t0 : END); });
  sh[sh.length - 1].t1 = END;

  // ---------------- overlays ----------------
  const chip = (id, t0, t1, kk, v, x, y, cls = "", from = "right") => ({ id, t0, t1, from, cls: "chip " + cls, style: `left:${x}px;top:${y}px`,
    html: `<div class="ck">${kk}</div><div class="cv">${v}</div>` });
  const slam = (id, t0, t1, html, top, size = 128) => ({ id, t0, t1, slam: true, cls: "slam", style: `top:${top}px;font-size:${size}px`, html });
  const overlays = [
    slam("sl-a", -1, c("s1.check") - 0.05, "COULD A SHARK END UP<br><b>IN YOUR POOL?</b>", 330, 76),
    { id: "check", t0: c("s1.check"), t1: s("s9") - 0.05, cls: "check", html: '<div class="h">EVERY WAY IN</div><div id="ck1"></div><div id="ck2"></div><div id="ck3"></div>' },
    slam("sl-x1", c("s2.not") + 0.25, s("s3") - 0.05, '<b style="color:#ff5a4f">✗ TOO BIG</b>', 560, 110),
    { id: "kmc", t0: c("s4.bull") + 0.4, t1: s("s5") - 0.05, cls: "kmc", html: '<span id="km">0 km</span>' },
    { id: "stamp", t0: c("s6.fake") + 2.0, t1: s("s7") - 0.05, slam: true, cls: "stamp", html: "FAKE" },
    chip("c-street", c("s6.street") + 0.2, c("s6.fake") - 0.1, "REAL VIDEOS · QUEENSLAND & FLORIDA", "Bull sharks in flooded streets", 60, 1180, "dark"),
    chip("c-golf", c("s7.golf") + 0.4, c("s7.years") - 0.05, "CARBROOK GOLF CLUB · AUSTRALIA", "1996 → 2013", 60, 1180, "gold"),
    chip("c-17", c("s7.years"), s("s8") - 0.05, "BULL SHARKS IN A GOLF LAKE", "17 years", 60, 1360 - 180, "red"),
    { id: "gauge", t0: s("s8"), t1: c("s8.guard") - 0.1, cls: "gauge", html: '<b>RIVER</b><i id="lvl" style="height:10%"></i>' },
    { id: "verdict", t0: c("s9.gw"), t1: s("s10") - 0.05, cls: "verdict",
      html: '<div id="v1">GREAT WHITE <span class="x">✗ NO</span></div><div id="v2" style="opacity:0">BULL SHARK <span class="ok">✓ POSSIBLE</span></div><small id="v3" style="opacity:0">FLOOD? STAY OUT OF THE WATER.</small>' },
    chip("c-who", c("s10.who"), LOOPJ, "COMMENT", "Would you still go swimming?", 60, 420, "red"),
    slam("sl-end", END - 0.3, END + 1, "COULD A SHARK END UP<br><b>IN YOUR POOL?</b>", 330, 76),
  ];
  const bubbles = [
    { who: "LG", t0: 0.2, t1: CUT + 0.2, text: "!!", cls: "red" },
    { who: "LG", t0: c("s5.follow") + 0.05, t1: s("s6") - 0.1, text: "♥ LIKE + FOLLOW +", cls: "red follow" },
    { who: "GW", t0: c("s3.salt") + 0.7, t1: c("s3.dead") - 0.1, text: "BLEH! FRESH WATER", cls: "dark" },
    { who: "GOLF", t0: c("s7.golf") + 1.5, t1: s("s8") - 0.1, text: "FORE?!", cls: "dark" },
    { who: "LG", t0: CUPFLY, t1: s("s9") - 0.1, text: "NOPE.", cls: "red" },
  ];
  const bursts = [{ who: "LG", t: CUPFLY + 0.05, text: "SPLASH!" }];

  return {
    actors: A, shots: sh, overlays, bubbles, bursts, props, buildWorld: buildPool, fgMax: 6,
    grade: "contrast(1.08) saturate(1.15) brightness(1.02)",
    custom: (t, { el }) => {
      const mark = (state) => (state === 1 ? '<span class="x">✗</span>' : state === 2 ? '<span class="ok">✓</span>' : '<span class="q">?</span>');
      const k1 = t >= c("s2.not") ? 1 : 0, k2 = t >= c("s3.dead") ? 1 : 0, k3 = t >= c("s8.drop") ? 2 : 0;
      el("ck1").innerHTML = mark(k1) + "PIPES"; el("ck2").innerHTML = mark(k2) + "SEA (GREAT WHITE)"; el("ck3").innerHTML = mark(k3) + "FLOOD (BULL SHARK)";
      const f = clamp((zAtKm(t) - 9) / (ZEND - 9), 0, 1);
      el("km").textContent = Math.round(4000 * f).toLocaleString("en-US") + " km";
      el("lvl").style.height = (10 + flood(t) / 1.7 * 80).toFixed(1) + "%";
      el("v2").style.opacity = t > c("s9.bs") ? "1" : "0"; el("v3").style.opacity = t > c("s9.safe") ? "1" : "0";
    },
  };
}
