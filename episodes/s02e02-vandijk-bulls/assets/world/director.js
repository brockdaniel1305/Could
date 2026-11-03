// S2E02 "Could Virgil van Dijk stop the running of the bulls?" - one continuous 3D Pamplona morning.
// Thread: Van Dijk never runs; he defends bulls like strikers (show it outside, read the one-two, step up for offside).
// Five bulls, zero dribbles - then bull number six is called Pépé (the player who ended his real 50-game run in 2019).
// Street along x (bulls run towards +x, the bullring is at x ~ 74), fences at z = +-3, Van Dijk waits at x = 0.
import { path, sstep, clamp, lerp } from "./engine.js";
import { buildPamplona } from "./pamplona3d.js";

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
  const HOOK = (i) => [-15 - i * 2.4, ZZ[i]];
  // Van Dijk
  A.v = { h: 1.95, unit: 330, stride: 1.9, path: [
    [0, 0, 0], [SHOW - 0.1, 0, 0], [SHOW + 0.6, 0.6, -0.7, "s"], [FENCE, 1.0, -0.6, "o"],          // shows bull 1 outside
    [STEP - 0.05, 1.0, -0.6], [STEP + 0.35, 1.2, 0, "o"],                                           // steps into the one-two
    [UP - 0.05, 1.2, 0], [UP + 0.4, -0.5, 0, "o"],                                                  // steps up: offside
    [PEPE - 0.05, -0.5, 0], [PEPE + 0.15, -0.5, -0.45, "o"], [PEPE + 0.35, -0.5, 0.55, "s"],      // bites on the step-over
    [PEPE + 1.4, -0.3, 0.3, "s"],
    [s("s9") - 0.05, 0, 0, "j"],
  ], ev: [["yawn", c("s3.nobody") + 0.2, 1.0], ["spin", PEPE + 0.5, 0.8], ["armR", OFF - 0.15, 1.6], ["armR", c("s9.follow"), 1.8]],
    look: (t) => (t > PEPE + 0.4 && t < c("s8.y19") ? 1 : t > c("s7.six") && t < PEPE ? -0.6 : 0) };

  // bulls: hook charge -> corral -> pack run -> staged one by one -> duels
  const STAGE = [0, -14, -18, -22, -26, -30, -36];
  for (let i = 1; i <= 6; i++) {
    const [hx, hz] = HOOK(i), z = ZZ[i] * 0.8, p = [[0, hx, hz], [S2J, hx + 8, hz, "l"], [S2J, -85 - i * 1.6, ZZ[i], "j"],
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
    A["b" + i] = { path: p, ev, h: 1.55, unit: 230, stride: 3.0, view: "front" };
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
  const sh = [];
  const add = (o) => sh.push(o);
  const OPEN = { P: [4.3, 1.5, 0.6], T: [-5, 1.6, 0] };
  add({ t0: 0, k: "path", P: [OPEN.P, [4.7, 1.6, 0.8]], T: [OPEN.T, [-5, 1.6, 0]], ease: "i", blur: 1.6 });
  // s2: whip to the corral end from above the rooftops, ride above the pack, then low as the runners flee past
  add({ t0: s("s2") + 0.1, blend: 0.45, whip: true, k: "path", P: [[-62, 18, 0.4], [-57, 24, 0.4]], T: [[-82, 0, 0], [-76, 0, 0]], blur: 0 });
  add({ t0: c("s2.six") + 0.1, blend: 0.6, k: "follow", who: "b3", off: [[10, 10, 9], [12, 8, 8]], look: [-4, 0, 0], blur: 0.3, flat: true });
  add({ t0: c("s2.run") - 0.3, blend: 0.45, k: "path", P: [[-11, 2.3, 0.3], [-9.5, 2.3, 0.3]], T: [[-30, 1.2, 0], [-28, 1.2, 0]], blur: 1.6 });
  // s3: push in on Van Dijk, the bulls far behind him
  add({ t0: s("s3"), blend: 0.6, k: "path", P: [[6.5, 1.7, 1.3], [3.6, 1.6, 0.7]], T: [[-4, 1.5, 0], [-2, 1.5, 0]], blur: 1.8 });
  // s4: elevated side view across the street (the far fence and balconies behind)
  add({ t0: c("s4.one") - 0.2, blend: 0.6, k: "path", P: [[-1.5, 4.2, -5.2], [0.5, 4.0, -5.0]], T: [[-1, 0.6, 1.5], [1, 0.6, 1.5]], blur: 0.8 });
  // s5: from above for the one-two
  add({ t0: c("s5.two") - 0.1, blend: 0.6, k: "path", P: [[1.6, 7.5, 3.4], [1.4, 6.2, 2.8]], T: [[0.3, 0, 0], [0.4, 0, 0]], fov: [50, 50], blur: 0.3 });
  // s6: low behind Van Dijk looking at the two charging bulls
  add({ t0: c("s6.four") - 0.1, blend: 0.5, k: "path", P: [[6, 3.0, 1.2], [5, 2.8, 1.0]], T: [[-8, 1.2, -0.3], [-8, 1.2, -0.3]], blur: 1.4 });
  // s7: wide over the five beaten bulls, low for number six, side view for the step-over
  add({ t0: c("s7.five") - 0.1, blend: 0.6, k: "path", P: [[7, 5, 7], [5, 4.2, 6]], T: [[0, 0.5, 0], [0, 0.5, 0]], blur: 0.4 });
  add({ t0: c("s7.six") - 0.1, blend: 0.5, k: "path", P: [[4.2, 2.6, 1.6], [3.4, 2.5, 1.3]], T: [[-8, 1.3, -0.2], [-8, 1.3, -0.2]], blur: 1.6 });
  add({ t0: PEPE - 0.35, blend: 0.3, k: "path", P: [[-0.5, 4.0, -5.0], [1.5, 4.0, -5.0]], T: [[-0.5, 0.6, 1.5], [1.5, 0.6, 1.5]], blur: 0.8 });
  // s8: ride with Pépé into the bullring
  add({ t0: c("s8.y19") - 0.1, blend: 0.5, k: "follow", who: "b6", off: [[-7, 2.6, 4], [-8, 3, 5]], look: [6, 1.2, 0], blur: 1.2 });
  add({ t0: c("s8.never") - 0.2, blend: 0.6, k: "path", P: [[54, 3, 8], [55, 3.4, 9]], T: [[62, 1.4, 0], [63, 1.8, 0]], blur: 1.0 });
  // s9: back to Van Dijk, then the loop
  add({ t0: s("s9") + 0.05, blend: 0.45, whip: true, k: "path", P: [[4.2, 1.6, 0.1], [3.7, 1.6, 0.1]], T: [[-2, 1.6, 0.3], [-2, 1.6, 0.3]], blur: 1.6 });
  add({ t0: c("s9.loop") - 0.35, blend: 0.3, whip: true, k: "path", P: [[5.2, 1.7, 1.0], OPEN.P], T: [[-5, 1.6, 0], OPEN.T], ease: "o", blur: 1.6 });
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
    slam("sl-hook", -1, s("s2") - 0.05, "VAN DIJK<br><b>vs.</b> 6 BULLS", 360, 128),
    chip("c-bulls", c("s2.ton"), c("s2.run") - 0.1, "PAMPLONA · 6 BULLS", "500+ kg each", 110, 400, "gold"),
    chip("c-fifty", c("s3.fifty"), s("s4") - 0.05, "PREMIER LEAGUE", "50 games · 0 dribbled past", 60, 400, "dark"),
    chip("c-zero", c("s7.five"), c("s7.six") - 0.1, "5 BULLS", "0 dribbles", 120, 400, "dark"),
    chip("c-y19", c("s8.y19"), s("s9") - 0.05, "AUG 2019 · LIVERPOOL 3–1 ARSENAL", "Pépé ends the run at 50", 50, 400, "gold"),
    chip("c-dont", c("s9.dont"), LOOPJ, "SAFETY", "Don't run with bulls", 120, 560, "red", "left"),
    slam("sl-hook2", END - 0.35, END + 1, "VAN DIJK<br><b>vs.</b> 6 BULLS", 360, 128),
  ];

  return {
    buildWorld: buildPamplona,
    actors: A, shots: sh, props, bubbles, overlays,
    shake: [FENCE, HIT],
    crowd: (t) => (t > c("s8.never") - 0.3 && t < s("s9") ? 0.45 : t > c("s2.run") - 0.5 && t < s("s4") ? 0.2 : 0.07),
  };
}
