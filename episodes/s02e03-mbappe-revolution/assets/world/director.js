// S2E03 "Could Real Madrid's Kylian Mbappé lead the French Revolution?" - Paris 1789 (3D) and, for the finale, the Bernabéu.
// Thread: his speed makes him the leader (Bastille in one sprint, seven prisoners = seven fans) until Napoleon's horse is faster,
// so he goes back to his real dictatorship: Real Madrid, where he takes the penalties.
// Paris street runs along x from -2110 (cathedral) to -1975 (square), Bastille gate at x ~ -1964; the stadium sits at the origin.
import { path, sstep, clamp, lerp } from "./engine.js";
import { buildParis, parisBounds, PARIS } from "./paris3d.js";
import { buildStadium } from "./stadium3d.js";

export default function plot(T) {
  const c = (k) => { if (!(k in T.cue)) throw new Error("cue " + k); return T.cue[k]; };
  const s = (k) => T.start[k];
  const END = T.duration;
  const CUT = 1.3, LOOPJ = c("s8.loop") - 0.5;
  const GATE = c("s4.sprint") + 1.6;              // Mbappé bursts through the Bastille gate
  const RACE = c("s6.kmh") - 0.3, KICK = c("s7.him") - 0.35, GOAL = KICK + 0.4;
  const gx = PARIS.bastille[0] - 18.2;

  // ---------------- two worlds in one scene: Paris (day) and the stadium (night) ----------------
  function buildWorld(THREE, scene) {
    const p = buildParis(THREE, scene);
    const before = new Set(); scene.traverse((o) => { if (o.isLight) before.add(o); });
    const st = buildStadium(THREE, scene);
    const stadiumLights = []; scene.traverse((o) => { if (o.isLight && !before.has(o) && !p.lights.includes(o)) stadiumLights.push(o); });
    const night = { bg: scene.background, fog: scene.fog };
    return { ...st, crowd: (t, amp) => { p.crowd(t, amp); st.crowd(t, amp); }, door: p.door,
      envAt: (cam) => { const paris = cam.position.x < -1000;
        scene.background = paris ? p.sky : night.bg; scene.fog = paris ? p.fog : night.fog;
        p.lights.forEach((l) => (l.visible = paris)); stadiumLights.forEach((l) => (l.visible = !paris)); } };
  }

  // ---------------- actors ----------------
  const A = {};
  const HX = -2075, HV = 9;                        // hook: Mbappé sprinting up the street at 9 m/s
  const hookIn = (x0) => [[LOOPJ, x0 - HV * (END - LOOPJ), 0, "j"], [END, x0, 0, "l"]];
  A.m = { h: 1.78, unit: 330, stride: 2.1, path: [
    [0, HX, 0], [CUT, HX + HV * CUT, 0, "l"], [s("s2"), HX + HV * s("s2"), 0, "l"],
    [s("s3") - 0.4, -2030, 0, "j"],                                                     // stands for the CV close-up
    [s("s4") + 0.2, -2030, 0], [c("s4.sprint"), -1992, 0.2, "i"], [GATE, -1965.5, 0, "l"], [GATE + 0.2, -1962, 0, "o"],   // the sprint, through the gate
    [c("s5.seven") + 1.2, -1962, 0], [c("s5.seven") + 1.2, -1966, 0.2, "j"], [c("s5.fans") - 0.2, -1971.5, 0.2, "s"],   // walks out with the prisoners
    [s("s6") + 0.15, -1971.5, 0.2], [s("s6") + 0.15, -2052, -0.3, "j"], [RACE, -2052, -0.3], [RACE + 0.5, -2049, -0.3, "i"],
    [s("s7"), -2049 + 10.5 * (s("s7") - RACE - 0.5), -0.3, "l"],                                                           // 38 km/h
    [s("s7") + 0.1, 0, 0, "j"], [s("s7") + 0.1, 28, 3], [c("s7.who"), 39.6, 0.4, "s"], [c("s7.who") + 1.2, 39.6, 0.4],     // Bernabéu, to the spot
    [KICK - 0.3, 40.2, 0.2], [KICK, 41.0, 0.1, "i"], [GOAL + 0.6, 42.4, 0.1, "o"],
    ...hookIn(HX),
  ], ev: [["cross", c("s3.wc") - 0.1, s("s4") - c("s3.wc") - 0.1], ["cross", c("s5.fans"), s("s6") - c("s5.fans")], ["cross", GOAL + 0.7, LOOPJ - GOAL - 0.7]],
    look: (t) => (t > c("s6.second") && t < s("s7") ? 1 : 0) };
  // the mob: behind him in the hook, in the square in front of the Bastille in scene 4/5
  for (let i = 0; i < 8; i++) {
    const hx = HX - 2.4 - i * 1.1, hz = (i % 2 ? 1 : -1) * (0.8 + (i % 4) * 0.5);
    const sqx = -1977 + (i % 4) * -1.6, sqz = (i < 4 ? -1 : 1) * (5.0 + (i % 3) * 1.2);
    A["c" + i] = { h: 1.75, unit: 320, stride: 2.0, path: [[0, hx, hz], [s("s2"), hx + 8.6 * s("s2"), hz, "l"],
      [s("s4") - 0.3, sqx, sqz, "j"], [c("s4.sprint") + 0.4, sqx, sqz], [GATE - 0.2, sqx + 2.2, sqz * 0.8, "s"],
      [s("s6") + 0.15, sqx + 2.2, sqz * 0.8], ...hookIn(hx).map((w) => [w[0], w[1], hz, w[3]])],
      ev: [["jump", s("s4") + 0.4 + i * 0.1, 1.6], ["jump", GATE + 0.1, 2.0], ["jump", c("s5.fans"), 1.8], ["hide", s("s6") + 0.2, LOOPJ - s("s6") - 0.2]] };
  }
  // seven prisoners come out of the gate and cross their arms like him
  for (let i = 0; i < 7; i++) {
    const tz = -3 + i * 1.0, tx = -1973 - (i % 2) * 1.4;
    A["p" + i] = { h: 1.72, unit: 320, stride: 1.8, path: [[0, gx + 1.5, 0], [c("s5.seven") + i * 0.12, gx + 1.5, 0], [c("s5.seven") + 0.9 + i * 0.12, tx, tz, "o"]],
      ev: [["cross", c("s5.fans") + i * 0.05, s("s6") - c("s5.fans")]], only: [c("s5.seven") - 0.05, s("s6") + 0.2] };
  }
  // Napoleon waits at the side of the street, then the race
  A.nap = { h: 2.6, unit: 560, stride: 3.2, autoFlip: true, path: [[0, -2056, 1.6], [RACE, -2056, 1.6], [RACE + 0.4, -2054, 1.6, "i"],
    [s("s7"), -2054 + 12.5 * (s("s7") - RACE - 0.4), 1.6, "l"]], only: [s("s6"), s("s7")] };
  // Real Madrid: keeper and three team-mates around the penalty spot
  A.r0 = { h: 1.9, unit: 345, path: [[0, 52, 0]], ev: [["dive", KICK + 0.12, 1, -1]], only: [s("s7"), LOOPJ] };
  [[39.2, 2.2], [38.6, -1.8], [40.4, -2.6]].forEach(([x, z], j) => {
    A["r" + (j + 1)] = { h: 1.85, unit: 345, path: [[0, x, z], [c("s7.who") + 0.7, x, z], [c("s7.who") + 1.3, x - 2.2, z * 1.6, "s"]],
      ev: [["jump", GOAL + 0.2, 1.4], ["armsUp", GOAL + 0.2, 1.6]], only: [s("s7"), LOOPJ] }; });

  // ---------------- ball ----------------
  const ball = [
    { t0: 0, k: "at", who: "m", dx: 0.55, dz: 0.15 },
    { t0: s("s3") - 0.4, k: "rest", p: [-2029.5, 0, 0.3] },
    { t0: s("s4") + 0.2, k: "at", who: "m", dx: 0.6, dz: 0.1 },
    { t0: GATE - 0.1, k: "rest", p: [-1964.6, 0, 0.6] },
    { t0: s("s6") + 0.15, k: "at", who: "m", dx: 0.6, dz: 0.12 },
    { t0: s("s7") + 0.1, k: "at", who: "m", dx: 0.6, dz: 0.1 },
    { t0: c("s7.who") + 0.8, k: "rest", p: [41.5, 0, 0] },
    { t0: KICK, t1: GOAL, k: "fly", a: [41.5, 0, 0], b: [52.7, 1.5, 2.3], h: 0.6 },
    { t0: GOAL, k: "rest", p: [53.2, 0.1, 2.3] },
    { t0: LOOPJ, k: "at", who: "m", dx: 0.55, dz: 0.15 },
  ];

  // ---------------- camera ----------------
  const sh = [], add = (o) => sh.push(o);
  const HOOKCAM = { k: "follow", who: "m", off: [3.3, 0.85, 0.45], look: [-2, 1.35, 0], fov: [46, 46], roll: 5, blur: 2.2 };
  add({ t0: 0, ...HOOKCAM });
  add({ t0: CUT, k: "path", P: [[-1996, 0.5, 1.2], [-1994.5, 0.55, 1.1]], T: [[-1950, 16, 0], [-1950, 15, 0]], fov: [54, 48], roll: [-4, -5], blur: 0.6 });   // Bastille looming
  // s2: rise over barricades and roofs, looking up the street to the Bastille
  add({ t0: s("s2") + 0.1, blend: 0.45, whip: true, k: "path", P: [[-2096, 2.2, 0.3], [-2094, 11, 0.3], [-2090, 21, 0.3]], T: [[-2060, 5, 0], [-2040, 6, 0], [-1990, 4, 0]], fov: [56, 58], blur: 0.3 });
  // s3: push in on Mbappé, arms crossed
  add({ t0: s("s3"), blend: 0.5, k: "path", P: [[-2026.6, 1.4, 0.6], [-2027.6, 1.55, 0.45]], T: [[-2030, 1.45, 0], [-2030, 1.6, 0]], fov: [48, 38], blur: 2.4 });
  // s4: over the crowd at the Bastille, then ride the sprint over the drawbridge
  add({ t0: s("s4") + 0.1, blend: 0.5, whip: true, k: "path", P: [[-1988, 3.6, 7], [-1986, 3.2, 6]], T: [[-1964, 5, 0], [-1964, 4.5, 0]], fov: [54, 50], blur: 0.6 });
  add({ t0: c("s4.sprint") - 0.25, blend: 0.3, k: "follow", who: "m", off: [[-1.4, 2.0, 3.0], [-2.2, 2.0, 2.8]], look: [3, 1.6, -0.6], fov: [56, 52], roll: [-3, -5], blur: 2.0 });
  add({ t0: GATE - 0.35, blend: 0.25, k: "path", P: [[-1984, 2.2, 5.5], [-1983, 2.3, 5.2]], T: [[-1964, 3, 0], [-1964, 3.2, 0]], fov: [52, 48], blur: 0.8 });
  // s5: low in front of the gate as the prisoners come out
  add({ t0: s("s5") + 0.05, blend: 0.4, k: "path", P: [[-1982.5, 1.25, 0.3], [-1979.5, 1.35, 0.3]], T: [[-1968, 2.0, 0], [-1968, 2.1, 0]], fov: [54, 48], blur: 1.6 });
  // s6: whip to Napoleon, low; then side tracking for the race
  add({ t0: c("s6.prob") + 0.2, blend: 0.4, whip: true, k: "path", P: [[-2052.6, 0.7, 2.9], [-2052.9, 0.75, 2.8]], T: [[-2056, 2.6, 1.6], [-2056, 2.6, 1.6]], fov: [50, 44], roll: [5, 7], blur: 1.8 });
  add({ t0: RACE - 0.1, blend: 0.4, k: "follow", who: "m", off: [[0.8, 3.0, -2.6], [1.4, 2.9, -2.6]], look: [0.9, 1.0, 1.0], fov: [56, 54], blur: 1.6 });
  // s7: whip to the Bernabéu, behind the penalty taker, then the celebration
  add({ t0: s("s7") + 0.15, blend: 0.45, whip: true, k: "path", P: [[24, 6, 12], [30, 4, 9]], T: [[40, 1, 0], [42, 1, 0]], fov: [54, 50], blur: 0.6 });
  add({ t0: c("s7.who") - 0.1, blend: 0.6, k: "path", P: [[37.2, 1.6, 1.0], [37.8, 1.55, 0.8]], T: [[52.5, 1.3, 0], [52.5, 1.3, 0.2]], fov: [48, 40], blur: 1.4 });
  add({ t0: GOAL + 0.35, blend: 0.3, k: "path", P: [[45.2, 1.45, 0.4], [44.6, 1.5, 0.35]], T: [[42.4, 1.5, 0.1], [42.4, 1.55, 0.1]], fov: [46, 40], blur: 2.4 });
  // s8: back into the opening sprint (loop)
  add({ t0: c("s8.loop") - 0.3, blend: 0.3, whip: true, ...HOOKCAM });
  sh.forEach((x, i) => { x.t1 = x.t1 ?? (sh[i + 1] ? sh[i + 1].t0 : END); });
  sh[sh.length - 1].t1 = END;

  // ---------------- bubbles, bursts, overlays ----------------
  const bubbles = [
    { who: "m", t0: c("s5.follow"), t1: s("s6") - 0.1, text: "FOLLOW +  #8", cls: "red follow" },
    { who: "m", t0: c("s6.second") + 0.2, t1: s("s7"), text: "?!", cls: "" },
    { who: "r1", t0: c("s7.who"), t1: c("s7.who") + 1.1, text: "?", cls: "" }, { who: "r2", t0: c("s7.who") + 0.1, t1: c("s7.who") + 1.1, text: "?", cls: "" },
  ];
  const chip = (id, t0, t1, k, v, x, y, cls = "", from = "right") => ({ id, t0, t1, from, cls: "chip " + cls, style: `left:${x}px;top:${y}px`,
    html: `<div class="ck">${k}</div><div class="cv">${v}</div>` });
  const slam = (id, t0, t1, html, top, size = 128) => ({ id, t0, t1, slam: true, cls: "slam", style: `top:${top}px;font-size:${size}px`, html });
  const overlays = [
    slam("sl-a", -1, CUT, "DICTATOR<br>MBAPPÉ", 340, 138),
    slam("sl-b", CUT, s("s2") - 0.05, "<b>vs.</b> 1789", 360, 150),
    chip("c-leader", c("s2.want"), c("s2.dict") - 0.05, "PARIS · 1789", "Leader wanted", 120, 400, "gold"),
    chip("c-dict", c("s2.dict"), s("s3") - 0.05, "PARIS · 1789", "Dictator found", 120, 400, "red"),
    chip("c-wc", c("s3.wc"), s("s4") - 0.05, "WORLD CUP 2018", "Champion at 19", 120, 400, "dark"),
    chip("c-spd", c("s3.speed"), s("s4") - 0.05, "TOP SPEED", "≈ 38 km/h", 420, 560, "red", "left"),
    chip("c-hours", c("s4.hours"), c("s4.sprint") + 0.4, "14 JULY 1789 · THE CROWD", "took hours", 80, 400, "dark"),
    chip("c-fans", c("s5.fans"), s("s6") - 0.05, "MBAPPÉ FANS", "7", 120, 400, "gold"),
    chip("c-m", c("s6.kmh"), c("s6.second") - 0.1, "MBAPPÉ", "≈ 38 km/h", 60, 400, "dark"),
    chip("c-h", c("s6.kmh") + 0.3, c("s6.second") - 0.1, "NAPOLEON'S HORSE", "≈ 45 km/h", 380, 560, "red", "left"),
    chip("c-2nd", c("s6.second"), s("s7") - 0.05, "FASTEST IN FRANCE", "No. 2", 120, 400, "gold"),
    chip("c-rm", c("s7.rm"), c("s7.who") - 0.05, "REAL MADRID", "Dictator since 2024", 120, 400, "dark"),
    chip("c-pen", c("s7.who"), GOAL + 0.3, "PENALTY TAKER", "?", 120, 400, "gold"),
    chip("c-next", c("s8.next"), LOOPJ, "COMMENT", "Who dictates the next revolution?", 40, 400, "red"),
    slam("sl-end", END - 0.3, END + 1, "DICTATOR<br>MBAPPÉ", 340, 138),
  ];

  return {
    buildWorld, camBounds: (P) => (P.x < -1000 ? parisBounds(P) : P), fgBlur: 6,
    actors: A, ball, shots: sh, bubbles, overlays,
    nets: { right: [GOAL] }, shake: [GATE, GOAL],
    bursts: [{ who: "m", t: GATE, text: "BAM!" }],
    crowd: (t) => (t < s("s2") ? 0.25 : t > s("s4") && t < s("s6") ? 0.4 : t > GOAL && t < s("s8") + 2 ? 0.5 : 0.08),
    flashes: (t) => (t > GOAL && t < GOAL + 2 ? 0.3 : 0.05),
    speedlines: (t) => Math.max(0.6 * (1 - sstep(CUT - 0.1, CUT + 0.1, t)), 0.6 * sstep(END - 0.35, END - 0.2, t),
      0.45 * sstep(c("s4.sprint") - 0.2, c("s4.sprint"), t) * (1 - sstep(GATE, GATE + 0.3, t)),
      0.35 * sstep(RACE, RACE + 0.3, t) * (1 - sstep(c("s6.second"), c("s6.second") + 0.3, t))),
    custom: (t, { st }) => { if (st.door) st.door(t >= LOOPJ ? 0 : sstep(GATE - 0.05, GATE + 0.15, t)); },
  };
}
