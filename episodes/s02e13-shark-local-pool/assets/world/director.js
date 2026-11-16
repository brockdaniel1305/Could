// S2E13 "Could a shark end up in your local swimming pool?" - an honest thought experiment: we check every way in.
// Way 1 pipes (2D cross-section, the shark corks the pipe) -> no. Way 2 the sea (2D map: a great white tastes fresh water and turns
// back; a bull shark travels thousands of km up the Amazon). Way 3 floods (3D flooded street, the fake highway photo, the golf
// course lake in Queensland 1996-2013). The scenario (3D): the river next to an outdoor pool floods over the fence, a bull shark
// swims in, the water drops - it's stuck. Verdict: great white no, bull shark possible. Safety line. New sign: NO SHARKS.
import { path, sstep, clamp, lerp } from "./engine.js";
import { buildPool, POOL, STREET_X as SX, GOLF_X as GX } from "./pool3d.js";

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
  at("BULL", 0, -7, 0.6); at("BULL", CUT, -3, 0.4, "l"); lapPool("BULL", CUT + 0.1, s("s6") - 0.1, Math.PI);
  at("BULL", s("s6"), 500, 500, "j"); at("BULL", c("s8.so") - 0.15, -4, POOL.river + 1, "j");
  at("BULL", RISE0 + 0.6, -4, POOL.river + 2, "l"); at("BULL", RISE1, -3, -W / 2 - 3, "l"); at("BULL", FALL0 + 0.4, -1.5, -0.6, "l");
  lapPool("BULL", FALL0 + 0.5, LOOPJ - 0.1, 0.8, 7.5, 2.4);
  at("BULL", LOOPJ, -7 - 4 * (END - LOOPJ) / CUT, 0.6, "j"); at("BULL", END, -7, 0.6, "l");
  // the flooded street and the golf lake
  at("BULL2", 0, 500, 500); at("BULL2", s("s6") - 0.05, SX + 1.5, -26, "j"); at("BULL2", s("s7") - 0.1, SX - 1, 18, "l");
  for (let t = s("s7"); t <= s("s8"); t += 0.25) { const a = (t - s("s7")) * 0.7; at("BULL2", t, GX + Math.cos(a) * 14, -6 + Math.sin(a) * 7, "l"); }
  at("BULL2", s("s8") + 0.01, 500, 500, "j"); at("BULL2", END, 500, 500);
  at("GW", 0, 600, 600); at("GW", END, 600, 600);
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
    GW: { path: W8.GW, ev: [], h: 0.75, unit: 170, stride: 99 },
    LG: { path: W8.LG, ev: [["armR", c("s5.follow"), 1.4], ["armsUp", c("s8.guard") + 1.0, 1.4], ["jump", c("s8.guard") + 1.0, 0.5], ["armR", c("s10.who") - 0.2, 1.6]],
      h: 1.85, unit: 360, stride: 1.9, yAt: onChair },
    GOLF: { path: W8.GOLF, ev: [["armsUp", c("s7.golf") + 1.4, 1.2]], h: 1.8, unit: 360, stride: 1.9 },
    FLOAT1: { path: W8.FLOAT1, ev: [], h: 0.6, unit: 110, stride: 99, yAt: (t) => poolY(t) + Math.sin(t * 2) * 0.03 },
    FLOAT2: { path: W8.FLOAT2, ev: [], h: 0.6, unit: 110, stride: 99, yAt: (t) => poolY(t) + Math.sin(t * 2 + 1) * 0.03 },
  };

  // ---------------- props ----------------
  const PS = {}; const pos = (n, t) => { const p = (PS[n] = PS[n] || path(A[n].path))(t); return [p.x, p.z]; };
  const CUPFLY = c("s8.guard") + 1.0;
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
  };

  // ---------------- camera ----------------
  const sh = [], add = (o) => sh.push(o);
  const HOOKCAM = { k: "path", P: [[-3, 1.6, 9.5], [-2.6, 1.55, 9.0]], T: [[-6, 0.0, 0.2], [-4.5, 0.0, 0.2]], fov: [48, 46], roll: -2, blur: 1.6 };
  add({ t0: 0, ...HOOKCAM });
  add({ t0: CUT, whip: true, k: "path", P: [[10, 6.5, 20], [7, 5.5, 17]], T: [[0, 0, -2], [0, 0, -2]], fov: [50, 48], blur: 0.8 });
  add({ t0: s("s2") + 0.05, whip: true, k: "path", P: [[-9.4, 0.8, 4.2], [-9.2, 0.75, 3.8]], T: [[-12.5, -0.6, 0.6], [-12.5, -0.6, 0.6]], fov: [50, 48], blur: 2.0 });
  add({ t0: s("s3") + 0.05, whip: true, k: "path", P: [[0, 16, 2], [0, 15, 1.5]], T: [[0, 0, -16], [0, 0, -16]], fov: [50, 48], blur: 1.0 });
  add({ t0: s("s5") + 0.05, whip: true, k: "path", P: [[6.2, 2.6, 13.4], [6.0, 2.7, 12.8]], T: [[4, 2.9, CHAIR[1]], [4, 3.0, CHAIR[1]]], fov: [46, 42], blur: 2.0 });
  add({ t0: s("s6") + 0.05, whip: true, k: "path", P: [[SX + 4, 3.0, 24], [SX + 3, 2.8, 18]], T: [[SX, 1.2, 0], [SX, 1.2, -4]], fov: [50, 48], blur: 1.4 });
  add({ t0: s("s7") + 0.05, whip: true, k: "path", P: [[GX + 14, 3.4, 26], [GX + 12, 3.0, 23]], T: [[GX + 2, 0.5, 0], [GX + 2, 0.5, 0]], fov: [50, 48], blur: 1.4 });
  add({ t0: s("s8") + 0.05, whip: true, k: "path", P: [[2, 9, 22], [1, 8.5, 21]], T: [[-1, -0.2, -9], [-1, -0.2, -8]], fov: [52, 52], blur: 0.8 });
  add({ t0: FALL1 - 0.2, blend: 0.4, k: "path", P: [[-6.5, 1.7, 13.5], [-6, 1.7, 12.5]], T: [[-1.5, 0.6, 2], [-1.5, 0.6, 1.5]], fov: [50, 48], blur: 1.6 });
  add({ t0: s("s9") + 0.05, whip: true, k: "path", P: [[0, 7, 16], [0, 6, 14]], T: [[0, -0.2, 0], [0, -0.2, 0]], fov: [50, 48], blur: 1.0 });
  add({ t0: s("s10") + 0.05, whip: true, k: "path", P: [[-5.4, 1.9, 16.2], [-5.6, 1.9, 15.4]], T: [[-6.8, 1.7, W / 2 + 1.4], [-6.8, 1.7, W / 2 + 1.4]], fov: [48, 46], blur: 2.0 });
  add({ t0: c("s10.loop") - 0.3, blend: 0.3, whip: true, ...HOOKCAM });
  sh.forEach((x, i) => { x.t1 = x.t1 ?? (sh[i + 1] ? sh[i + 1].t0 : END); });
  sh[sh.length - 1].t1 = END;

  // ---------------- 2D explainer panels ----------------
  const SHARK = (body, belly, id) => `<g id="${id}"><path d="M-150,0 Q-60,-62 90,-30 Q140,-20 170,-2 Q140,22 90,26 Q-60,52 -150,0 Z" fill="${body}" stroke="#14141f" stroke-width="6" stroke-linejoin="round"/>` +
    `<path d="M-120,12 Q-40,40 90,22 Q40,8 -120,12 Z" fill="${belly}"/><path d="M-20,-46 Q10,-120 50,-118 Q30,-80 40,-34 Z" fill="${body}" stroke="#14141f" stroke-width="6" stroke-linejoin="round"/>` +
    `<path d="M-150,0 L-215,-60 Q-200,0 -215,56 Z" fill="${body}" stroke="#14141f" stroke-width="6" stroke-linejoin="round"/><circle cx="110" cy="-10" r="7" fill="#14141f"/>` +
    `<path d="M70,-14 Q74,0 70,12 M58,-16 Q62,0 58,14 M46,-16 Q50,0 46,16" fill="none" stroke="#14141f" stroke-width="4"/>` +
    `<path d="M120,10 Q140,18 160,6" fill="none" stroke="#14141f" stroke-width="4"/><path d="M126,12 l4,7 l4,-6 l4,7 l4,-6 l4,6" fill="#fff" stroke="#14141f" stroke-width="2"/></g>`;
  const PIPE = `<svg viewBox="0 0 980 760" width="100%" height="100%"><rect width="980" height="760" fill="#e9eef5"/>` +
    `<rect x="760" y="80" width="220" height="640" fill="#7fd3ef"/><rect x="740" y="80" width="30" height="640" fill="#c9d6d8" stroke="#14141f" stroke-width="5"/>` +
    `<rect x="40" y="356" width="720" height="48" fill="#9aa5b1" stroke="#14141f" stroke-width="6"/><rect x="40" y="368" width="720" height="24" fill="#2f8fb0" opacity="0.6"/>` +
    `<g id="dim" opacity="0"><path d="M330,320 L330,440 M318,356 L342,356 M318,404 L342,404" stroke="#d8202c" stroke-width="5"/><text x="350" y="336" font-family="Inter" font-weight="900" font-size="48" fill="#d8202c">10 cm</text></g>` +
    `<g id="pshark" transform="translate(-260,380) scale(1.25)">${SHARK("#7c8794", "#e9eef5", "s1")}</g>` +
    `<g id="pno" opacity="0"><circle cx="500" cy="600" r="70" fill="#d8202c"/><path d="M465,565 L535,635 M535,565 L465,635" stroke="#fff" stroke-width="16" stroke-linecap="round"/></g>` +
    `<text x="790" y="130" font-family="Inter" font-weight="900" font-size="36" fill="#14141f">POOL</text></svg>`;
  const SEA = `<svg viewBox="0 0 980 760" width="100%" height="100%"><rect width="980" height="760" fill="#2f8fb0"/>` +
    `<path d="M0,0 L980,0 L980,430 Q760,470 600,420 Q470,380 330,440 Q180,500 0,470 Z" fill="#e8d7a6" stroke="#14141f" stroke-width="6"/>` +
    `<path d="M470,395 Q440,300 520,230 Q600,160 560,60 Q545,20 590,0" fill="none" stroke="#7fd3ef" stroke-width="34" stroke-linecap="round"/>` +
    `<text x="40" y="560" font-family="Inter" font-weight="900" font-size="40" fill="#fff">SEA · SALT</text><text x="640" y="200" font-family="Inter" font-weight="900" font-size="36" fill="#14141f">RIVER · FRESH</text>` +
    `<g id="gw" transform="translate(120,600) scale(0.55)">${SHARK("#7c8794", "#e9eef5", "s2")}</g>` +
    `<g id="yuck" opacity="0"><text x="430" y="290" font-family="Inter" font-weight="900" font-size="54" fill="#d8202c">BLEH!</text></g>` +
    `<g id="dead" opacity="0"><rect x="560" y="300" width="300" height="90" rx="10" fill="#ffd23f" stroke="#14141f" stroke-width="6"/><text x="710" y="362" text-anchor="middle" font-family="Inter" font-weight="900" font-size="48" fill="#14141f">DEAD END</text></g></svg>`;
  const AMAZON = `<svg viewBox="0 0 980 760" width="100%" height="100%"><rect width="980" height="760" fill="#2f8fb0"/>` +
    `<path d="M120,60 Q330,20 560,70 Q760,90 900,200 Q960,300 900,420 Q840,560 640,640 Q520,700 420,720 Q300,600 240,470 Q150,330 120,60 Z" fill="#9cc77a" stroke="#14141f" stroke-width="6"/>` +
    `<path id="amz" d="M905,250 Q800,240 720,280 Q640,320 560,290 Q470,255 390,300 Q320,340 250,300" fill="none" stroke="#7fd3ef" stroke-width="22" stroke-linecap="round"/>` +
    `<path id="trail" d="M905,250 Q800,240 720,280 Q640,320 560,290 Q470,255 390,300 Q320,340 250,300" fill="none" stroke="#ffd23f" stroke-width="10" stroke-dasharray="1400" stroke-dashoffset="1400"/>` +
    `<circle cx="250" cy="300" r="12" fill="#d8202c" stroke="#14141f" stroke-width="4"/><text x="150" y="270" font-family="Inter" font-weight="900" font-size="32" fill="#14141f">IQUITOS</text>` +
    `<text x="720" y="150" font-family="Inter" font-weight="900" font-size="34" fill="#14141f">AMAZON</text>` +
    `<g id="bs" transform="translate(905,250) scale(0.32)">${SHARK("#8a8370", "#c9c0a8", "s3")}</g>` +
    `<text id="km" x="490" y="620" text-anchor="middle" font-family="CouldMono, monospace" font-weight="700" font-size="64" fill="#14141f">0 km</text></svg>`;
  const PHOTO = `<svg viewBox="0 0 980 760" width="100%" height="100%"><rect width="980" height="760" fill="#14141f"/>` +
    `<rect x="60" y="60" width="860" height="640" fill="#8a94a1"/><rect x="60" y="360" width="860" height="340" fill="#6d6a4f"/>` +
    `<path d="M60,520 L920,470 L920,560 L60,640 Z" fill="#4a4d55" opacity="0.6"/><rect x="760" y="120" width="20" height="260" fill="#5a5f69"/><rect x="700" y="110" width="140" height="70" fill="#1f9d55"/>` +
    `<g transform="translate(420,470) scale(1.1)"><path d="M-170,6 Q-40,-30 150,6 Z" fill="#7c8794" stroke="#14141f" stroke-width="5"/><path d="M70,-14 Q40,-150 -30,-150 Q10,-90 -40,-6 Z" fill="#7c8794" stroke="#14141f" stroke-width="6"/></g>` +
    `<text x="80" y="110" font-family="Inter" font-weight="900" font-size="34" fill="#f4f4f2">VIRAL "SHARK ON THE HIGHWAY"</text>` +
    `<g id="stamp" opacity="0" transform="translate(490,380) rotate(-14)"><rect x="-230" y="-80" width="460" height="160" rx="16" fill="none" stroke="#d8202c" stroke-width="16"/>` +
    `<text x="0" y="48" text-anchor="middle" font-family="Inter" font-weight="900" font-size="140" fill="#d8202c">FAKE</text></g></svg>`;

  // ---------------- overlays ----------------
  const chip = (id, t0, t1, kk, v, x, y, cls = "", from = "right") => ({ id, t0, t1, from, cls: "chip " + cls, style: `left:${x}px;top:${y}px`,
    html: `<div class="ck">${kk}</div><div class="cv">${v}</div>` });
  const slam = (id, t0, t1, html, top, size = 128) => ({ id, t0, t1, slam: true, cls: "slam", style: `top:${top}px;font-size:${size}px`, html });
  const overlays = [
    slam("sl-a", -1, c("s1.check") - 0.05, "COULD A SHARK END UP<br><b>IN YOUR POOL?</b>", 330, 76),
    { id: "check", t0: c("s1.check"), t1: s("s9") - 0.05, cls: "check", html: '<div class="h">EVERY WAY IN</div><div id="ck1"></div><div id="ck2"></div><div id="ck3"></div>' },
    { id: "p-pipe", t0: c("s2.w1") + 0.1, t1: s("s3") - 0.05, cls: "panel", html: PIPE + '<div class="cap">WAY 1 · THE PIPES</div>' },
    { id: "p-sea", t0: c("s3.w2") + 0.1, t1: s("s4") - 0.05, cls: "panel", html: SEA + '<div class="cap">WAY 2 · THE SEA · GREAT WHITE</div>' },
    { id: "p-amz", t0: s("s4"), t1: s("s5") - 0.05, cls: "panel", html: AMAZON + '<div class="cap">BULL SHARK · UP THE AMAZON</div>' },
    { id: "p-photo", t0: c("s6.fake") - 0.05, t1: s("s7") - 0.05, cls: "panel", html: PHOTO + '<div class="cap" style="color:#f4f4f2">THE FAMOUS PHOTO</div>' },
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
      // pipes: the shark swims in and corks the pipe
      const px = lerp(-260, 150, sstep(c("s2.w1") + 0.3, c("s2.cm") + 0.9, t)), squish = t > c("s2.cm") + 0.9 ? 1 + Math.sin(t * 18) * 0.04 : 1;
      el("pshark").setAttribute("transform", `translate(${px},380) scale(${(1.25 * squish).toFixed(3)},${(1.25 / squish).toFixed(3)})`);
      el("dim").setAttribute("opacity", t > c("s2.cm") ? "1" : "0"); el("pno").setAttribute("opacity", t > c("s2.not") + 0.2 ? "1" : "0");
      // sea: the great white swims into the river mouth, tastes fresh water and turns back
      const g1 = sstep(c("s3.w2") + 0.2, c("s3.salt") + 0.6, t), g2 = sstep(c("s3.salt") + 1.2, c("s3.dead") + 0.4, t);
      const gx = g1 < 1 ? lerp(120, 450, g1) : lerp(450, 140, g2), gy = g1 < 1 ? lerp(600, 410, g1) : lerp(410, 610, g2);
      el("gw").setAttribute("transform", `translate(${gx},${gy}) scale(${g2 > 0 ? -0.55 : 0.55},0.55)`);
      el("yuck").setAttribute("opacity", t > c("s3.salt") + 0.7 && t < c("s3.dead") + 0.6 ? "1" : "0"); el("dead").setAttribute("opacity", t > c("s3.dead") ? "1" : "0");
      // Amazon: the bull shark travels upriver, the counter runs
      const f = sstep(c("s4.bull") + 0.4, c("s4.amazon") + 1.6, t), pth = el("amz");
      if (pth && pth.getTotalLength) { const L = pth.getTotalLength(), p = pth.getPointAtLength(L * f); el("bs").setAttribute("transform", `translate(${p.x.toFixed(1)},${p.y.toFixed(1)}) scale(-0.32,0.32)`);
        el("trail").setAttribute("stroke-dashoffset", String(1400 - 1400 * f)); }
      el("km").textContent = Math.round(4000 * f).toLocaleString("en-US") + " km";
      el("stamp").setAttribute("opacity", t > c("s6.fake") + 2.0 ? "1" : "0");
      el("lvl").style.height = (10 + flood(t) / 1.7 * 80).toFixed(1) + "%";
      el("v2").style.opacity = t > c("s9.bs") ? "1" : "0"; el("v3").style.opacity = t > c("s9.safe") ? "1" : "0";
    },
  };
}
