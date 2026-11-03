// S2E02 "Could Virgil van Dijk stop the running of the bulls?" - one continuous 3D Pamplona morning.
// Thread: Van Dijk never runs; he defends bulls like strikers (show it outside, read the one-two, step up for offside).
// Five bulls, zero dribbles - then bull number six is called Pépé (the player who ended his real 50-game run in 2019).
// Street along x (bulls run towards +x, the bullring is at x ~ 74), fences at z = +-3, Van Dijk waits at x = 0.
import { path, sstep, clamp, lerp } from "./engine.js";
import { buildPamplona, pamplonaBounds } from "./pamplona3d.js";

export default function plot(T) {
  const c = (k) => { if (!(k in T.cue)) throw new Error("cue " + k); return T.cue[k]; };
  const s = (k) => T.start[k];
  const END = T.duration;

  const S2J = s("s2") - 0.05;               // jump from the hook to the corral (inside the whip)
  const LOOPJ = c("s9.loop") - 0.5;          // jump back to the hook picture (inside the last whip)
  const SHOW = c("s4.show"), FENCE = c("s4.fence");
  const STEP = c("s5.step"), HIT = STEP + 0.75;
  const UP = c("s6.up"), OFF = c("s6.off");
  const PEPE = c("s7.pepe");

  // ---------------- actors ----------------
  const A = {};
  const ZZ = [0, -1.2, 1.0, -0.2, 1.6, -1.6, 0.4];
  const HOOK = (i) => [-11 - i * 2.2, ZZ[i]];
  // Van Dijk
  A.v = { h: 1.95, unit: 330, stride: 1.9, path: [
    // (yawns right after the cut in the hook)
    [0, 0, 0], [SHOW - 0.1, 0, 0], [SHOW + 0.6, 0.6, -0.7, "s"], [FENCE, 1.0, -0.6, "o"],          // shows bull 1 outside
    [STEP - 0.05, 1.0, -0.6], [STEP + 0.35, 1.2, 0, "o"],                                           // steps into the one-two
    [UP - 0.05, 1.2, 0], [UP + 0.4, -0.5, 0, "o"],                                                  // steps up: offside
    [PEPE - 0.05, -0.5, 0], [PEPE + 0.15, -0.5, -0.45, "o"], [PEPE + 0.35, -0.5, 0.55, "s"],      // bites on the step-over
    [PEPE + 1.4, -0.3, 0.3, "s"],
    [s("s9") - 0.05, 0, 0, "j"],
  ], ev: [["yawn", 1.5, 0.9], ["yawn", c("s3.nobody") + 0.2, 1.0], ["spin", PEPE + 0.5, 0.8], ["armR", OFF - 0.15, 1.6], ["armR", c("s9.follow"), 1.8]],
    look: (t) => (t > PEPE + 0.4 && t < c("s8.y19") ? 1 : t > c("s7.six") && t < PEPE ? -0.6 : 0) };

  // bulls: hook charge -> corral -> pack run -> staged one by one -> duels
  const STAGE = [0, -14, -18, -22, -26, -30, -36];
  for (let i = 1; i <= 6; i++) {
    const [hx, hz] = HOOK(i), z = ZZ[i] * 0.8, p = [[0, hx, hz], [S2J, hx + 5, hz, "l"], [S2J, -85 - i * 1.6, ZZ[i], "j"],
      [c("s2.six"), -85 - i * 1.6, ZZ[i]], [c("s3.vvd"), -42 - i * 2.5, z, "l"], [c("s4.one") - 0.6, STAGE[i], z, "o"]], ev = [];
    if (i === 1) { p.push([c("s4.one") - 0.4, STAGE[1], 0.3], [SHOW + 0.55, -2, 0.3, "i"], [FENCE - 0.05, 2.2, 2.45, "l"], [FENCE + 0.2, 2.3, 2.5, "o"]);
      ev.push(["dizzy", FENCE, 2.2], ["fall", FENCE + 0.15, 0.4, 1]); }
    if (i === 2 || i === 3) { const zs = i === 2 ? -1.8 : 1.8;
      p.push([c("s5.two") - 0.35, STAGE[i], zs], [HIT, 0.3, zs * -0.25, "i"], [HIT + 0.25, -0.4, zs * 0.4, "o"], [s("s6") - 0.15, 9, zs * 0.9, "s"]);   // stagger off, dizzy
      ev.push(["dizzy", HIT, s("s6") - HIT], ["fall", s("s6") - 0.1, 0.4, i === 2 ? -1 : 1]); }
    if (i === 4 || i === 5) { const zs = i === 4 ? -0.9 : 0.9;
      p.push([c("s6.four") - 0.25, STAGE[i], zs], [OFF - 0.2, -6.5, zs, "i"], [OFF + 0.35, -4.6, zs, "o"]); }
    if (i === 6) p.push([c("s7.six") - 0.1, STAGE[6], 0], [PEPE - 0.1, -3, 0, "o"], [PEPE + 0.15, -2.7, 0.75, "s"], [PEPE + 0.35, -2.4, -0.7, "s"],
      [PEPE + 1.0, 3, -1.4, "l"], [c("s8.y19"), 5.5, -1.2, "l"], [c("s8.never"), 50, 0, "l"], [c("s8.never") + 1.0, 62, 0, "o"]);
    if (i === 6) ev.push(["jump", c("s8.never") + 1.0, 2.5]);
    p.push([LOOPJ, hx, hz, "j"]); ev.push(["up", LOOPJ]);
    A["b" + i] = { path: p, ev, h: 1.55, unit: 230, stride: 3.0, view: "front", dust: true };
  }
  A.b1.facing = (t) => 1;

  // runners: flee past the camera in scene 2 and past Van Dijk in scene 3; m7 stands at the fence as linesman
  const MZ = [-1.8, 1.5, -0.6, 2.0, 0.6, -2.2, 1.0];
  for (let i = 0; i < 7; i++) A["m" + i] = { path: [[s("s2"), -44 + i * 1.3, MZ[i]], [c("s4.one"), -44 + i * 1.3 + 7 * (c("s4.one") - s("s2")), MZ[i], "l"]],
    h: 1.8, unit: 345, stride: 2.0, only: [s("s2"), c("s4.one")] };
  A.m7 = { path: [[0, -7, -2.2]], h: 1.8, unit: 345, only: [s("s6"), c("s7.six")], ev: [["armR", OFF - 0.1, 1.5]] };

  // ---------------- props ----------------
  const props = {
    lflag: { at: (t) => [-6.65, 1.0 + 0.75 * sstep(OFF - 0.15, OFF + 0.1, t) * (1 - sstep(OFF + 1.3, OFF + 1.6, t)), -2.2], h: 1.0, unit: 200,
             only: [s("s6"), c("s7.six")] },
  };

  // ---------------- camera ----------------
  // Every frame full: low angles under the bunting, close-ups, shots through the fence planks (foreground pass blurs them),
  // a top-down for the one-two, push-ins and dutch angles. The camera never leaves the street below roof height (camBounds).
  const sh = [];
  const add = (o) => sh.push(o);
  const OPEN = { P: [3.0, 0.9, 0.5], T: [-4, 2.0, 0] };
  // YouTube hook: frame 0 is the threat - riding in front of a charging bull (speed lines, dust); hard cut at 1.3 s to Van Dijk, unbothered
  const CUT = 1.3, HOOKCAM = { k: "follow", who: "b1", off: [2.9, 0.75, 0.45], look: [-2, 1.35, 0], fov: [46, 46], roll: 6, blur: 2.4 };
  add({ t0: 0, ...HOOKCAM });
  add({ t0: CUT, k: "path", P: [[2.4, 0.95, 0.45], [2.2, 1.0, 0.42]], T: [[-4, 2.0, 0], [-4, 2.0, 0]], fov: [44, 40], ease: "i", blur: 1.8 });
  // s2: rise up the street towards the church as the gate opens; head-on with a bull; under a bull; the runners
  add({ t0: s("s2") + 0.1, blend: 0.45, whip: true, k: "path", P: [[-64, 2.5, 0.3], [-65, 10, 0.3], [-64, 19, 0.3]], T: [[-90, 4, 0], [-90, 6, 0], [-88, 2, 0]], fov: [56, 60], blur: 0.4 });
  add({ t0: c("s2.six") + 0.25, blend: 0.5, k: "follow", who: "b1", off: [[3.4, 1.1, 0.7], [3.0, 1.0, 0.6]], look: [-2, 1.2, 0], fov: [44, 40], blur: 2.2 });
  add({ t0: c("s2.ton") - 0.05, blend: 0.4, k: "follow", who: "b3", off: [[2.0, 0.35, -1.4], [1.7, 0.35, -1.2]], look: [-1, 1.5, 0.2], fov: [48, 44], roll: [8, 11], blur: 2.4 });
  add({ t0: c("s2.run") - 0.2, blend: 0.4, k: "follow", who: "m3", off: [[4.2, 1.3, 0.5], [3.6, 1.25, 0.4]], look: [-3, 1.5, 0], fov: [52, 48], blur: 2.2 });
  // s3: slow orbit around Van Dijk while the runners flee past him, then push in for the yawn
  add({ t0: s("s3"), blend: 0.6, k: "path", P: [[3.2, 1.5, -1.8], [3.4, 1.5, 0], [3.0, 1.55, 1.7]], T: [[0, 1.4, 0], [0, 1.45, 0], [0, 1.5, 0]], fov: [50, 48], blur: 2.4 });
  add({ t0: c("s3.nobody") - 0.2, blend: 0.5, k: "path", P: [[1.9, 1.8, 0.5], [1.55, 1.8, 0.4]], T: [[0, 1.75, 0], [0, 1.75, 0]], fov: [40, 36], blur: 2.8 });
  // s4: through the planks of the near fence (blurred foreground), then a close crash into the far fence
  add({ t0: c("s4.one") - 0.2, blend: 0.6, k: "path", P: [[6.2, 2.4, -1.6], [5.4, 2.2, -1.4]], T: [[-3, 1.0, 0.6], [-2, 1.0, 0.8]], fov: [54, 50], roll: [-3, -4], blur: 1.8 });
  add({ t0: FENCE - 0.15, blend: 0.3, k: "path", P: [[4.6, 1.5, 0.2], [4.3, 1.45, 0.4]], T: [[2.3, 0.9, 2.5], [2.3, 0.9, 2.5]], fov: [42, 34], roll: [-4, -8], blur: 2.0 });
  // s5: straight down on the one-two, then zoom in on the collision
  add({ t0: c("s5.two") - 0.1, blend: 0.6, k: "path", P: [[5.0, 6.5, 0.2], [4.4, 6.0, 0.2]], T: [[-4, 0, 0], [-3, 0, 0]], fov: [56, 54], blur: 0.4 });
  add({ t0: STEP + 0.3, blend: 0.4, k: "path", P: [[1.6, 3.0, 1.2], [1.3, 2.7, 1.0]], T: [[0.2, 0.3, 0], [0.2, 0.3, 0]], fov: [54, 48], roll: [6, 9], blur: 1.2 });
  // s6: worm's-eye behind Van Dijk, push in as he steps up, then the two puzzled bull faces
  add({ t0: c("s6.four") - 0.1, blend: 0.5, k: "path", P: [[3.2, 0.6, 0.7], [2.6, 0.65, 0.65]], T: [[-6, 2.2, 0.2], [-6, 2.2, 0.2]], fov: [54, 50], roll: [4, 5], blur: 1.6 });
  add({ t0: OFF + 0.4, blend: 0.35, k: "path", P: [[-1.1, 1.5, -1.3], [-1.4, 1.5, -1.3]], T: [[-4.6, 1.3, 0.1], [-4.6, 1.3, 0.1]], fov: [56, 52], blur: 2.2 });
  // s7: high over the beaten bulls; over Van Dijk's shoulder as number six comes; close on the name; through the fence for the step-over
  add({ t0: c("s7.five") - 0.1, blend: 0.6, k: "path", P: [[3.5, 6.5, 5.4], [0.5, 6.2, 5.4]], T: [[2, 0.2, 0], [1, 0.2, 0]], fov: [60, 58], blur: 0.3 });
  add({ t0: c("s7.six") - 0.1, blend: 0.5, k: "path", P: [[1.4, 1.5, 0.9], [1.1, 1.45, 0.85]], T: [[-8, 1.2, -0.2], [-8, 1.2, -0.2]], fov: [46, 40], blur: 2.0 });
  add({ t0: c("s7.name") - 0.1, blend: 0.4, k: "follow", who: "b6", off: [[2.6, 1.3, 0.45], [2.2, 1.25, 0.4]], look: [-1, 1.2, 0], fov: [40, 36], blur: 2.4 });
  add({ t0: PEPE - 0.35, blend: 0.3, k: "path", P: [[4.0, 2.2, -2.6], [3.2, 2.2, -2.6]], T: [[-1.8, 0.9, 0.4], [-0.6, 0.9, 0.4]], fov: [58, 56], blur: 1.6 });
  // s8: chase Pépé up the street and into the ring, low angle with the full stands behind
  add({ t0: c("s8.y19") - 0.1, blend: 0.5, k: "follow", who: "b6", off: [[-3.6, 1.6, 2.2], [-4.2, 1.8, 2.4]], look: [5, 1.3, 0], fov: [52, 50], roll: [-4, -6], blur: 1.8 });
  add({ t0: c("s8.never") - 0.2, blend: 0.6, k: "path", P: [[55.5, 2.2, 6.5], [56.2, 2.3, 7]], T: [[62, 1.2, 0], [62.5, 1.3, 0]], fov: [50, 46], roll: [3, 4], blur: 1.6 });
  // s9: Van Dijk, then the whip back into the opening picture
  add({ t0: s("s9") + 0.05, blend: 0.45, whip: true, k: "path", P: [[2.7, 1.4, 0.3], [2.4, 1.4, 0.3]], T: [[0, 1.65, 0], [0, 1.65, 0]], fov: [48, 44], blur: 2.4 });
  add({ t0: c("s9.loop") - 0.3, blend: 0.3, whip: true, ...HOOKCAM });   // loop: back to the charging bull of frame 0
  sh.forEach((x, i) => { x.t1 = x.t1 ?? (sh[i + 1] ? sh[i + 1].t0 : END); });
  sh[sh.length - 1].t1 = END;

  // ---------------- bubbles ----------------
  const bubbles = [
    { who: "b1", t0: c("s4.one"), t1: SHOW + 0.3, text: "#1", cls: "dark" },
    { who: "b2", t0: c("s5.two"), t1: STEP, text: "#2", cls: "dark" }, { who: "b3", t0: c("s5.two") + 0.1, t1: STEP, text: "#3", cls: "dark" },
    { who: "b4", t0: c("s6.four"), t1: UP, text: "#4", cls: "dark" }, { who: "b5", t0: c("s6.four") + 0.1, t1: UP, text: "#5", cls: "dark" },
    { who: "b4", t0: OFF + 0.35, t1: c("s7.six"), text: "?", cls: "" }, { who: "b5", t0: OFF + 0.5, t1: c("s7.six"), text: "?", cls: "" },
    { who: "b6", t0: c("s7.name"), t1: PEPE + 1.6, text: "PÉPÉ", cls: "dark name" },
    { who: "m1", t0: c("s2.run"), t1: c("s2.run") + 1.3, text: "AAH!", cls: "red" }, { who: "m4", t0: c("s2.run") + 0.3, t1: c("s2.run") + 1.5, text: "AAH!", cls: "red" },
    { who: "v", t0: c("s9.follow") + 0.1, t1: LOOPJ - 0.05, text: "FOLLOW +", cls: "red follow" },
  ];

  // ---------------- overlays ----------------
  const chip = (id, t0, t1, k, v, x, y, cls = "", from = "right") => ({ id, t0, t1, from, cls: "chip " + cls, style: `left:${x}px;top:${y}px`,
    html: `<div class="ck">${k}</div><div class="cv">${v}</div>` });
  const slam = (id, t0, t1, html, top, size = 128) => ({ id, t0, t1, slam: true, cls: "slam", style: `top:${top}px;font-size:${size}px`, html });
  const overlays = [
    slam("sl-hook", -1, 1.3, "6 BULLS", 360, 150),
    slam("sl-hook-b", 1.3, s("s2") - 0.05, "<b>vs.</b> PRIME<br>VAN DIJK", 360, 118),
    chip("c-bulls", c("s2.ton"), c("s2.run") - 0.1, "PAMPLONA · 6 BULLS", "500+ kg each", 110, 400, "gold"),
    chip("c-prime", c("s3.vvd"), c("s3.fifty") - 0.05, "PRIME VAN DIJK", "Liverpool · No. 4", 120, 400, "dark"),
    chip("c-fifty", c("s3.fifty"), s("s4") - 0.05, "MAR 2018 – AUG 2019 · PREMIER LEAGUE", "50 games · 0 dribbled past", 40, 400, "gold"),
    chip("c-zero", c("s7.five"), c("s7.six") - 0.1, "5 BULLS", "0 dribbles", 120, 400, "dark"),
    chip("c-y19", c("s8.y19"), s("s9") - 0.05, "AUG 2019 · LIVERPOOL 3–1 ARSENAL", "Pépé ends the run at 50", 50, 400, "gold"),
    chip("c-dont", c("s9.dont"), LOOPJ, "SAFETY", "Don't run with bulls", 120, 1040, "red", "left"),
    slam("sl-hook2", END - 0.3, END + 1, "6 BULLS", 360, 150),
  ];

  return {
    buildWorld: buildPamplona, camBounds: pamplonaBounds, fgBlur: 6,
    actors: A, shots: sh, props, bubbles, overlays,
    shake: [FENCE, HIT],
    bursts: [{ who: "b1", t: FENCE, text: "BAM!" }, { who: "b2", t: HIT, text: "BONK!" }],
    speedlines: (t) => Math.max(0.6 * (1 - sstep(1.2, 1.4, t)), 0.6 * sstep(END - 0.35, END - 0.2, t), 0.3 * (1 - sstep(s("s2") - 0.6, s("s2"), t)), sstep(c("s4.one"), c("s4.one") + 0.3, t) * (1 - sstep(SHOW + 0.3, SHOW + 0.6, t)) * 0.4,
      sstep(c("s6.four"), c("s6.four") + 0.3, t) * (1 - sstep(OFF - 0.3, OFF, t)) * 0.4),
    crowd: (t) => (t > c("s8.never") - 0.3 && t < s("s9") ? 0.45 : t > c("s2.run") - 0.5 && t < s("s4") ? 0.2 : 0.07),
  };
}
