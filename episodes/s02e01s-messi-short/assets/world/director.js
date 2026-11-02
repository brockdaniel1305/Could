// S2E01 SHORT (~50 s, derived from v3): cues the short narration drops are aliased below.
// S2E01 v2 "Could prime Messi beat Real Madrid on his own?" - the whole match as one continuous 3D world.
// Thread: playing alone has three problems (no team-mates, no keeper, stamina) and Messi solves them one by one;
// the final goal pays off all three (walked all game -> one sprint -> pass to himself).
// Pitch: x -52.5 (Messi's goal, LEFT) .. +52.5 (Real's goal, RIGHT), z -34 (far side) .. +34 (near side, camera side).
import { path, sstep, clamp, lerp } from "./engine.js";

export default function plot(T) {
  const s = (k) => T.start[k];
  const ALIAS = {   // moments the short narration no longer names
    "s2.fans": () => T.cue["s2.eleven"], "s3.through": () => T.cue["s3.through"],
    "s5.past": () => T.cue["s5.half"] + 1.5, "s6.foul": () => T.cue["s6.fk"] - 0.35,
    "s7.subs": () => s("s7") - 3.0, "s7.bench": () => s("s7"), "s7.box": () => T.cue["s7.corner"] - 0.4,
    "s8.last": () => T.cue["s8.three"] + 0.3, "s8.walked": () => T.cue["s8.three"], "s8.saved": () => T.cue["s8.three"],
  };
  const c = (k) => { if (k in T.cue) return T.cue[k]; if (ALIAS[k]) return ALIAS[k](); throw new Error("cue " + k); };
  const END = T.duration;

  // ---------------- key moments ----------------
  const KO = s("s3") + 0.05;                 // kick-off whistle
  const TAP1 = c("s3.himself") - 0.1;        // first "pass to himself"
  const SHOT1 = c("s3.through") + 0.95;      // saved
  const PUNT = c("s4.counter") + 0.3;
  const R_SHOT = c("s4.fifty") + 0.15, G1 = R_SHOT + 1.4;            // 1-0 Real (from fifty metres)
  const SOLO = c("s5.half"), G2 = c("s5.one") - 0.05;                // 1-1
  const SPRINT = c("s6.sprint"), FOUL = c("s6.foul") - 0.05;
  const FK = c("s6.top") - 0.45, G3 = FK + 0.75;                      // 1-2 free kick
  const CK = c("s7.two") - 1.0, HEAD = CK + 0.6, G4 = HEAD + 0.3;     // 2-2 corner
  const LAST = c("s8.last") - 0.9, TAP2 = c("s8.self") - 0.05, SHOT2 = c("s8.goal") - 0.5, G5 = c("s8.goal") - 0.02; // 2-3
  const FT = c("s10.loop") - 1.5;   // loop teleports at FT + 1 (inside the whip back to the opening)
  const FKSET = c("s6.fk") - 0.05, CKSET = c("s7.corner") - 0.5, S8SET = s("s8") - 0.5, S6SET = s("s6") - 0.2;

  // ---------------- actors ----------------
  const A = {};
  // Messi
  const mPath = [
    [0, 0, 0], [KO, 0, 0],
    [TAP1, 0, 0], [TAP1 + 0.38, 2.9, 1.5, "o"], [TAP1 + 0.7, 5.6, -0.7, "l"],            // around the defender, the ball goes the other way
    [SHOT1, 17.2, -0.2, "l"], [SHOT1 + 1.2, 19, 0, "o"],                                // through ... shot ... saved
    [G1 - 0.6, 12, 2, "s"],                                                               // walking back, far from his own goal
    [G1 + 0.9, 12, 2], [G1 + 0.9, 0, 0],                                                  // (teleport during the whip) kick-off spot
    [SOLO, 0, 0], [SOLO + 0.45, 3, 0, "i"], [SOLO + 3.05, 41, 0, "l"],                   // solo run past ten
    [SOLO + 3.4, 44.6, 1.6, "l"], [SOLO + 3.8, 49.2, 0.2, "l"], [G2 + 0.6, 49.8, 0.4, "o"],
    [G2 + 0.8, 49.8, 0.4], [c("s6.walk") - 0.3, 21, 0.2, "s"],                              // runs the whole pitch back
    [c("s6.walk"), 19.5, 0.4, "o"], [SPRINT - 0.05, 14.2, 1, "l"],                       // walks
    [FOUL, 28.2, 0.6, "l"],                                                               // one sprint ... foul
    [FKSET, 28.2, 0.6], [FKSET, 27.2, 1.1],                                        // (teleport) free-kick run-up spot
    [FK - 0.35, 27.2, 1.1], [FK, 28.5, 0.5, "i"], [FK + 0.5, 29.2, 0.4, "o"],
    [CKSET, 29.2, 0.4], [CKSET, -44, 4],                       // (teleport) back defending the corner
    [c("s7.box") + 0.2, -44, 4], [c("s7.mark") - 0.2, -44.3, 1.5, "s"],                  // marks exactly one
    [S8SET, -44.3, 1.5], [S8SET, 0, 0],                                             // (teleport) kick-off after 2-2
    [LAST, 0, 0], [LAST + 1.25, 18, 0, "i"], [TAP2, 26.4, 0, "o"],                       // last attack, slow motion
    [TAP2 + 0.5, 29.4, 1.6, "o"], [TAP2 + 0.9, 32.2, -0.9, "l"], [SHOT2, 32.6, -1.0, "o"],
    [SHOT2 + 0.9, 33.5, -0.8, "o"],
    [s("s9") - 0.05, 33.5, -0.8], [s("s9") - 0.05, 40, 31.2],                            // (teleport) in front of the near stand
    [s("s10"), 40, 31.2], [FT + 1.0, 37.5, 31.2, "l"], [FT + 1.0, 0, 0],                                               // (teleport behind the board) loop start
  ];
  A.m = { path: mPath, h: 1.7, unit: 330, stride: 1.8, ev: [
    ["armsUp", G2 + 0.15, 1.2], ["fall", FOUL + 0.05, 0.4, 1], ["up", FOUL + 0.45], ["armsUp", G3 + 0.1, 1.3],
    ["armsUp", s("s9") - 0.05, s("s10") - s("s9") + 0.05],
  ], look: (t) => (t > c("s3.none") && t < c("s3.self") ? Math.sin((t - c("s3.none")) * 4) : t > c("s8.three") && t < c("s8.last") ? -0.6 : 0) };

  // Real: r0 keeper, r1..r10 outfield (#2 3 4 5 6 8 10 11 7 9), q0..q2 fresh substitutes
  const ringAng = (i) => Math.PI / 2 + Math.PI / 11 + (i * 2 * Math.PI) / 11; // a gap straight towards the camera
  const ring = (i) => [Math.cos(ringAng(i)) * 3.1, Math.sin(ringAng(i)) * 3.1];
  // lineup: a row behind Messi's shoulder (x 3..18), the "11 v 1" picture
  const LX = (i) => 3 + i * 1.5;
  // the ring slot at angle 0 (straight ahead of Messi, x +3.1) belongs to the defender he beats with the pass to himself
  const slotOf = [8, 0, 1, 2, 3, 4, 5, 6, 7, 9, 10]; // r_i -> ring slot; r0 (keeper) takes slot 8 (x>0 side), r5 -> 4 ...
  // which outfield player is straight ahead (angle 0 = slot with cos 1): slot index where ringAng = 0 -> i = 11/4 ~ not integer, use nearest
  let ahead = 0, best = -9; for (let i = 0; i < 11; i++) { const [x, z] = ring(i); if (x - Math.abs(z) > best) { best = x - Math.abs(z); ahead = i; } }
  const SOLO_X = [4, 8, 12, 16, 20, 24, 28, 32, 36, 39.5];
  const soloT = (x) => SOLO + 0.45 + (x - 3) / ((41 - 3) / 2.6);
  const BOX = [[-49.5, -4], [-49, 0.5], [-49.4, 4.6], [-46.8, -2.6], [-46, 0], [-46.4, 3.4], [-43.6, -4.2], [-43.2, 1], [-43.8, 5]];
  const WALL = [[38.2, -1.2], [38.2, -0.4], [38.2, 0.4], [38.2, 1.2]];
  const subsOn = c("s7.subs") + 0.5;

  for (let i = 0; i < 11; i++) {
    const name = "r" + i, slot = slotOf[i], [rx, rz] = ring(slot);
    const p = [[0, LX(i), 0]], ev = [];
    if (i === 0) {
      // keeper: in the line-up, then in Real's goal for the whole match
      p.push([KO, LX(0), 0], [KO + 1.2, rx, rz, "s"], [SHOT1 - 0.4, rx, rz], [SHOT1 - 0.4, 51.2, 0],
        [SHOT1 + 0.3, 51.2, 0], [SHOT1 + 0.42, 51.3, 0.1, "o"],
        [c("s5.keeper") - 0.2, 51, 0], [c("s5.keeper") + 0.15, 45.6, 0.6, "o"],
        [FKSET, 45.6, 0.6], [FKSET, 51.8, -0.6], [LAST, 51.8, -0.6], [LAST, 50.6, 0], [FT + 1, 50.6, 0], [FT + 1, LX(0), 0]);
      ev.push(["armsUp", SHOT1 + 0.35, 1.4], ["dive", c("s5.keeper") + 0.35, 1, -1], ["up", G2 + 1.2],
        ["dive", G3 - 0.3, 1, -1], ["up", G3 + 1.5], ["dive", SHOT2 + 0.15, 1, 1], ["up", FT + 1]);
    } else {
      // press into the ring, then spread out
      p.push([KO, LX(i), 0], [c("s3.press") + 0.25 + i * 0.04, LX(i), 0], [c("s3.none") - 0.1, rx, rz, "s"]);
      if (i === 9) p.push([TAP1 - 0.7, rx, rz], [TAP1 - 0.15, 4.6, -2.4, "s"]); // steps out of the lane (and out of shot)
      if (slot === ahead) p.push([TAP1 + 0.1, rx, rz], [TAP1 + 0.35, rx - 0.3, rz + 0.5, "s"]); // lunges at the ball, too late
      ev.push(["spin", c("s3.through") - 0.3, 0.8]);
      p.push([c("s3.through") + 0.9, rx + (i % 2 ? 1 : -1), rz * 1.4]);
      if (i !== 9) p.push([G1 - 0.4, 14 + i, rz * 2.5, "s"]);
      // the fifty-metre shooter is r9 (#7)
      if (i === 9) p.push([c("s4.empty") - 0.6, 4, 4], [c("s4.empty") - 0.3, 0, 4, "o"], [G1 + 0.3, 0, 4], [G1 + 0.9, -8, 3, "o"]);
      // solo run: ten defenders strung along Messi's line
      const sx = SOLO_X[i - 1], sz = (i % 2 ? -1 : 1) * 1.4, ti = soloT(sx);
      p.push([G1 + 0.9, sx + 1.5, sz * 1.6, "j"], [ti - 0.45, sx + 1.5, sz * 1.6], [ti - 0.05, sx, sz * 0.45, "o"]);
      ev.push(["spin", ti - 0.05, 0.7], ["fall", ti + 0.65, 0.4, i % 2 ? 1 : -1], ["up", S6SET]);
      p.push([S6SET - 0.01, sx, sz * 0.45]);
      // s6: keep-ball around the walking Messi, then the wall
      const kb = [[9, -3.4], [17, -4.5], [13, -6.5], [22, -2.5], [8, -6], [24, -6], [16, -9], [12, -10], [27, -4], [20, -11]][i - 1];
      p.push([S6SET, kb[0] + 8, kb[1], "j"], [c("s6.walk"), kb[0], kb[1], "s"]);
      if (c("s6.bored") && [3, 4, 6, 7].includes(i)) p.push([c("s6.bored") + 0.1, kb[0], kb[1]], [SPRINT, kb[0] + (kb[0] > 15 ? 3 : -3), kb[1] * 1.6, "s"]);
      if (i === 2) p.push([SPRINT + 0.2, 31.5, 3.6], [FOUL - 0.1, 28.6, 1.0, "o"], [FKSET, 34, 7.5, "j"]);   // the slide tackle
      if (i >= 3 && i <= 6) p.push([FKSET, WALL[i - 3][0], WALL[i - 3][1], "j"]);
      if (i === 2) ev.push(["fall", FOUL - 0.2, 0.3, -1], ["up", FKSET]);
      if (i >= 3 && i <= 6) ev.push(["jump", FK + 0.05, 0.5]);
      // s7: three of them go off for the substitutes (r6, r7, r8), the rest attack the corner
      if (i >= 6 && i <= 8) { p.push([CKSET, 0, 60, "j"]); ev.push(["hide", CKSET, 999]); }   // short: subbed off unseen
      else if (i === 10) p.push([CKSET, -52, 33.4, "j"]);          // corner taker
      else { const b = BOX[[0, 1, 2, 4, 3, 0, 0, 0, 5][i - 1]]; p.push([CKSET, b[0] + 12, b[1] * 1.6, "j"], [c("s7.box") - 0.1, b[0] + 12, b[1] * 1.6], [c("s7.mark") - 0.5, b[0], b[1], "s"]); }
      if (i === 4) ev.push(["jump", HEAD - 0.25, 0.5], ["armsUp", G4 + 0.1, 1.6]);
      // s8: everyone still jogging back from the corner, one defender left (r2)
      if (i === 2) p.push([S8SET, 30.5, 0, "j"], [TAP2 + 0.1, 29.6, 0], [TAP2 + 0.5, 29.4, -0.3, "o"]);
      else if (!(i >= 6 && i <= 8)) p.push([S8SET, -30 + i * 2.5, (i % 3 - 1) * 9, "j"], [SHOT2 + 2, -10 + i * 2.5, (i % 3 - 1) * 9, "l"]);
      if (i === 2) ev.push(["spin", TAP2 + 0.25, 0.9], ["fall", TAP2 + 1.15, 0.4, 1], ["up", FT + 1]);
      p.push([FT + 1, LX(i), 0, "j"]);
      ev.push(["up", FT + 1]);
    }
    A[name] = { path: p, ev, h: 1.85, unit: 345, stride: 2.0 };
  }
  // substitutes: jog on from the touchline at the half-way board
  for (let j = 0; j < 3; j++) {
    const b = BOX[[6, 7, 8][j]];
    A["q" + j] = { path: [[0, -1 + j * 2, 37.5], [subsOn, -1 + j * 2, 37.5], [subsOn + 1.6, -3 + j * 2.5, 30, "s"],
      [CKSET, -3 + j * 2.5, 30], [CKSET, b[0] + 10, b[1] + 6, "j"], [c("s7.box") - 0.1, b[0] + 10, b[1] + 6], [c("s7.mark") - 0.5, b[0], b[1], "s"],
      [S8SET, -40 + j * 3, -6 + j * 6, "j"], [SHOT2 + 2, -18 + j * 3, -6 + j * 6, "l"]],
      ev: [["jump", subsOn + 1.6, 0.7]], h: 1.85, unit: 345, stride: 2.0, only: [CKSET, s("s9")] };
  }

  // ---------------- ball ----------------
  const P = (name, t) => { const f = path(A[name].path)(t); return [f.x, 0, f.z]; };
  const mAt = (t, dx = 0.55, dz = 0.15) => { const p = P("m", t); return [p[0] + dx, 0, p[2] + dz]; };
  const ball = [
    { t0: 0, k: "juggle", who: "m" },
    { t0: c("s2.nomates") - 0.2, k: "at", who: "m", dx: 0.45, dz: 0.2 },
    { t0: TAP1, t1: TAP1 + 0.72, k: "fly", a: mAt(TAP1, 0.45, 0.2), b: mAt(TAP1 + 0.72, 0.5, 0.1), h: 0.25, curve: -2.2 },
    { t0: TAP1 + 0.72, k: "at", who: "m", dx: 0.55, dz: 0.1 },
    { t0: SHOT1, t1: SHOT1 + 0.42, k: "fly", a: mAt(SHOT1), b: [51.3, 1.0, 0.25], h: 1.2 },
    { t0: SHOT1 + 0.42, k: "at", who: "r0", dx: 0.15, dz: 0.3, y: 1.05 },
    { t0: PUNT, t1: PUNT + 1.15, k: "fly", a: [51.2, 1.0, 0.3], b: [0.4, 0, 4.1], h: 26 },
    { t0: PUNT + 1.15, k: "at", who: "r9", dx: 0.5, dz: 0.15 },
    { t0: R_SHOT, t1: G1, k: "fly", a: [0.4, 0, 4.15], b: [-53.1, 1.4, 0.6], h: 11, ease: "o" },
    { t0: G1, k: "rest", p: [-53.3, 0.1, 0.6] },
    { t0: G1 + 0.9, k: "at", who: "m", dx: 0.55, dz: 0.15 },
    { t0: SOLO + 3.85, t1: G2, k: "fly", a: mAt(SOLO + 3.85), b: [53.0, 0.3, 0.3], h: 0.3 },
    { t0: G2, k: "rest", p: [53.2, 0.1, 0.3] },
    // keep-ball around the walking Messi (s6), the lazy pass he intercepts
    { t0: s("s6") + 0.2, k: "rest", p: [30, 0, 0] },
  ];
  // lazy passes between r1 (9,-3.4) r2 (18,3.2) r4 (22,-2.5) r5 (8,4.2) while Messi walks
  const KB = [["r1", "r5"], ["r5", "r2"], ["r2", "r4"], ["r4", "r1"], ["r1", "r2"]];
  let tk = c("s6.walk") + 0.2;
  const pos = (n, t) => { const f = path(A[n].path)(t); return [f.x + 0.4, 0, f.z + 0.2]; };
  for (const [a, b] of KB) {
    if (tk + 0.9 > SPRINT - 0.4) break;
    ball.push({ t0: tk, t1: tk + 0.9, k: "fly", a: pos(a, tk), b: pos(b, tk + 0.9), h: 0.2 });
    ball.push({ t0: tk + 0.9, k: "at", who: b, dx: 0.4, dz: 0.2 });
    tk += 1.25;
  }
  const lastFrom = ball[ball.length - 1].who || "r1";
  ball.push({ t0: SPRINT - 0.35, t1: SPRINT + 0.05, k: "fly", a: pos(lastFrom, SPRINT - 0.35), b: mAt(SPRINT + 0.05), h: 0.3 });
  ball.push({ t0: SPRINT + 0.05, k: "at", who: "m", dx: 0.6, dz: 0.1 });
  ball.push({ t0: FOUL + 0.05, t1: FOUL + 0.6, k: "fly", a: mAt(FOUL + 0.05), b: [30.5, 0, 0.2], h: 0.4 });
  ball.push({ t0: FKSET, k: "rest", p: [28.9, 0, 0.35] });
  ball.push({ t0: FK, t1: G3, k: "fly", a: [28.9, 0, 0.35], b: [52.7, 2.2, -3.1], h: 3.2, curve: 2.6 });
  ball.push({ t0: G3, k: "rest", p: [53.3, 0.1, -3] });
  ball.push({ t0: CKSET, k: "rest", p: [-51.7, 0, 33.2] });
  ball.push({ t0: CK, t1: HEAD, k: "fly", a: [-51.7, 0, 33.2], b: [-46.6, 2.1, 0.1], h: 7 });
  ball.push({ t0: HEAD, t1: G4, k: "fly", a: [-46.6, 2.1, 0.1], b: [-53.1, 1.2, 1.4], h: 0.2 });
  ball.push({ t0: G4, k: "rest", p: [-53.3, 0.1, 1.4] });
  ball.push({ t0: S8SET, k: "at", who: "m", dx: 0.55, dz: 0.15 });
  ball.push({ t0: TAP2, t1: TAP2 + 0.9, k: "fly", a: mAt(TAP2), b: mAt(TAP2 + 0.9, 0.5, 0.1), h: 0.2, curve: -2.4 });
  ball.push({ t0: TAP2 + 0.9, k: "at", who: "m", dx: 0.55, dz: 0.1 });
  ball.push({ t0: SHOT2, t1: G5, k: "fly", a: mAt(SHOT2), b: [53.0, 1.0, 2.1], h: 0.8 });
  ball.push({ t0: G5, k: "rest", p: [53.2, 0.1, 2.1] });
  ball.push({ t0: FT + 1, k: "juggle", who: "m" });

  // ---------------- camera ----------------
  // path shots: P/T lists of points over [t0, t1]; follow shots ride an actor or the ball. "blend" = seconds of smooth move INTO the shot.
  const sh = [];
  const add = (o) => sh.push(o);
  const OPEN = { P: [0.2, 1.25, 3.9], T: [0.2, 1.05, 0] };
  add({ t0: 0, k: "path", P: [OPEN.P, [1.5, 2.2, 7.5], [3, 3.8, 12.5]], T: [OPEN.T, [3, 1.2, 0], [7, 1.3, 0]], ease: "i", blur: 0.6 });
  // s2: crane up over the crowd, swoop down along the eleven, settle on Messi alone, whip to the empty goal
  add({ t0: c("s2.eleven") - 0.15, blend: 0.6, k: "path", P: [[20.5, 1.6, 6.5], [1.5, 1.6, 6.5]], T: [[18.5, 1.25, 0], [0, 1.25, 0]], ease: "s", blur: 1.6 });
  add({ t0: c("s2.messi") + 0.3, blend: 0.4, k: "path", P: [[1.5, 1.6, 6.5], [-5.5, 2.6, 10]], T: [[0, 1.25, 0], [-4, 1.1, 0]], blur: 1.4 });
  add({ t0: c("s2.nokeeper") - 0.1, blend: 0.45, whip: true, k: "path", P: [[-34, 2.2, 1.4], [-36, 2.0, 0.9]], T: [[-52.5, 1.3, 0], [-52.5, 1.2, 0]], blur: 1.0 });
  // s3: whip back to the kick-off; high angle for the press, down into the ring, then ride with Messi
  add({ t0: KO + 0.15, blend: 0.45, whip: true, k: "path", P: [[-3, 17, 15], [-1, 12, 12]], T: [[2, 0, 0], [1.5, 0, 0]], blur: 0.4 });
  add({ t0: c("s3.none") - 0.1, blend: 0.8, k: "path", P: [[0.05, 1.45, 2.8], [0.1, 1.5, 3.2]], T: [[0.05, 1.25, 0], [0.1, 1.25, 0]], blur: 1.8 });
  add({ t0: TAP1 - 0.3, blend: 0.3, k: "follow", who: "m", off: [[0.1, 3.4, 7.4], [0.3, 2.6, 6.6]], look: [1.0, 0.9, -1], blur: 2.0 });
  // shot -> keeper view; the punt rides up with the ball; behind #7 looking at the empty goal; chase the long shot
  add({ t0: SHOT1 + 0.08, blend: 0.3, whip: true, k: "path", P: [[44.5, 1.7, 6.5], [45.5, 1.8, 6.8]], T: [[51.5, 1.2, 0], [51, 1.4, 0]], blur: 1.2 });
  add({ t0: PUNT + 0.1, blend: 0.35, k: "follow", who: "ball", off: [[-2, 2, 18], [6, 2, 20]], look: [0, 0.5, 0], blur: 0.8 });
  add({ t0: c("s4.empty") - 0.2, blend: 0.45, k: "path", P: [[7.0, 2.4, 5.6], [6.4, 2.3, 5.2]], T: [[-52, 1.2, -0.5], [-52, 1.2, 0]], blur: 1.0 });
  add({ t0: R_SHOT + 0.05, blend: 0.25, k: "follow", who: "ball", off: [[7, 1.4, 0.8], [7, 1.4, 0.8]], look: [-8, 0.1, -0.8], blur: 1.6, rideY: true });
  add({ t0: G1 - 0.25, blend: 0.25, k: "path", P: [[-44, 1.9, 7.2], [-45.5, 2.3, 8.5]], T: [[-52.5, 1.1, 0], [-50, 1.3, 0]], blur: 1.2 });
  // s5: whip to the centre circle; ride with the solo run; stop at the goal as the stadium goes quiet
  add({ t0: SOLO - 0.2, blend: 0.5, whip: true, k: "follow", who: "m", off: [0.3, 1.5, 7], look: [1.2, 1.4, -1], blur: 2.2 });
  add({ t0: SOLO + 3.3, blend: 0.5, k: "path", P: [[46, 1.8, 8], [47.5, 2.4, 9.5]], T: [[51.5, 1.1, 0], [50.5, 1.4, 0]], blur: 1.4 });
  // s6: wide and high as he runs the whole pitch back; down beside him as he walks; ride the sprint; free kick from behind
  add({ t0: s("s6") + 0.1, blend: 0.6, whip: true, k: "follow", who: "m", off: [[4, 14, 26], [-2, 12, 24]], look: [-6, 0, 0], blur: 0.2, flat: true });
  add({ t0: c("s6.walk") - 0.3, blend: 0.8, k: "follow", who: "m", off: [[0.3, 1.6, 7.5], [0.2, 1.5, 6]], look: [0.4, 1.4, -1], blur: 2.0 });
  add({ t0: SPRINT - 0.15, blend: 0.3, k: "follow", who: "m", off: [0.3, 1.5, 6.8], look: [1.3, 1.3, -1], blur: 2.4 });
  add({ t0: c("s6.fk") + 0.1, blend: 0.35, whip: true, k: "path", P: [[23.0, 2.2, 2.6], [23.4, 2.2, 2.4]], T: [[40, 1.6, -0.8], [40, 1.7, -0.9]], fov: [56, 46], blur: 1.4 });
  add({ t0: FK + 0.2, blend: 0.2, k: "path", P: [[23.4, 2.2, 2.4], [24, 2.3, 2.1]], T: [[44, 1.8, -1.5], [50, 2, -2.4]], fov: [46, 36], blur: 1.2 });
  // s7: touchline (subs, the near stand behind them), pan to the empty dugout, high corner view, push in on the header
  add({ t0: c("s7.corner") - 0.15, blend: 0.7, whip: true, k: "path", P: [[-33, 15, 20], [-35.5, 12, 16.5]], T: [[-47, 0, 1.5], [-47.5, 0, 1]], blur: 0 });
  add({ t0: c("s7.mark") - 0.3, blend: 0.6, k: "path", P: [[-38, 6.5, 13], [-40, 5.5, 11]], T: [[-47, 1, 1], [-48, 1, 0.5]], blur: 0.6 });
  // s8: slow push-in on Messi's face, then ride the last attack, then the goal from behind the far post
  add({ t0: s("s8") - 0.2, blend: 0.6, whip: true, k: "path", P: [[0.5, 1.6, 5.5], [0.45, 1.5, 2.3]], T: [[0.5, 1.4, 0], [0.45, 1.45, 0]], fov: [58, 44], blur: 2.2 });
  add({ t0: LAST - 0.15, blend: 0.45, k: "follow", who: "m", off: [[0.3, 1.5, 6.6], [0.3, 1.45, 5.2]], look: [1.1, 1.35, -1], blur: 2.4 });
  add({ t0: SHOT2 + 0.05, blend: 0.3, k: "path", P: [[46.5, 1.6, 8.5], [47.5, 1.8, 8]], T: [[53, 1.1, 1], [52.5, 1.3, 1]], blur: 1.4 });
  // s9: slow orbit around Messi showing his shirt to the near stand
  add({ t0: s("s9") + 0.05, blend: 0.45, whip: true, k: "path", P: [[40.6, 1.45, 26.4], [37.6, 1.7, 27.0], [35.6, 2.0, 28.6]], T: [[40, 1.9, 32], [40, 1.9, 32], [40.2, 2.0, 32]], blur: 2.0 });
  // s10: crane up over the stadium behind the full-time board, then dive back down to the opening close-up (loop)
  add({ t0: s("s10") + 0.05, blend: 0.5, k: "follow", who: "m", off: [[0.3, 1.5, -5.4], [-0.3, 1.5, -5.0]], look: [-0.3, 1.5, 1], blur: 2.0 });
  add({ t0: c("s10.loop") - 0.35, blend: 0.3, whip: true, k: "path", P: [[2.5, 6, 13], OPEN.P], T: [[0.8, 1, 0], OPEN.T], ease: "o", blur: 0.6 });
  sh.forEach((x, i) => { x.t1 = x.t1 ?? (sh[i + 1] ? sh[i + 1].t0 : END); });
  sh[sh.length - 1].t1 = END;

  // ---------------- props ----------------
  const props = {
    tw: { at: (t) => t < s("s3") ? [-52.6 + 0.4, 0, lerp(-6, 7, clamp((t - c("s2.nokeeper") + 0.2) / 1.6, 0, 1))] :
            [lerp(-6, -18, clamp((t - c("s7.bench")) / 2.4, 0, 1)), 0, 34.3], h: 0.8, unit: 120,
          only: [c("s2.nokeeper") - 0.3, s("s3")] },
    subboard: { p: [1.5, 0, 35.2], h: 2.4, unit: 420, only: [0, 0] },
    dugout: { p: [-12, 0, 36.6], h: 2.3, unit: 330 },
    flag: { p: [-52.4, 0, 33.9], h: 1.5, unit: 300 },
    shirt: { at: (t) => { const p = path(mPath)(t); return [p.x, 1.55 + 0.08 * Math.sin(t * 5), p.z - 0.05]; }, h: 0.9, unit: 260,
             only: [s("s9"), s("s10")] },
    heart: { at: (t) => [41.6, 2.55 + 0.6 * sstep(c("s9.same") + 0.3, c("s9.same") + 0.7, t), 43.3], h: 2.0, unit: 330,
             only: [c("s9.same") + 0.3, s("s10") + 1.2] },
  };
  props.tw.rotSpin = true;

  // ---------------- bubbles over heads ----------------
  const bubbles = [
    { who: "m", t0: c("s3.none") + 0.1, t1: c("s3.self") - 0.1, text: "?", cls: "" },
    { who: "m", t0: c("s3.himself") - 0.05, t1: TAP1 + 0.9, text: "FREE ✓", cls: "dark" },
  ];
  for (let i = 1; i < 11; i++) bubbles.push({ who: "r" + i, t0: c("s3.self") + 0.15 + i * 0.2, t1: c("s3.himself") - 0.1, text: "✕", cls: "red" });
  for (const i of [3, 4, 6, 7]) bubbles.push({ who: "r" + i, t0: c("s6.bored") + 0.1 + (i % 3) * 0.15, t1: SPRINT, text: "zzz", cls: "" });
  bubbles.push({ who: "r2", t0: SOLO + 1.0, t1: SOLO + 2.0, text: "???", cls: "" }, { who: "r5", t0: SOLO + 1.6, t1: SOLO + 2.6, text: "???", cls: "" });
  bubbles.push({ who: "q1", t0: c("s7.mark"), t1: CK, text: "MARKED", cls: "dark" });
  for (const n of ["r1", "r3", "r4", "r5", "r9", "q0", "q2"]) bubbles.push({ who: n, t0: c("s7.mark") + 0.5 + Math.random() * 0 + n.charCodeAt(1) * 0.004, t1: G4 - 0.1, text: "FREE", cls: "red" });
  bubbles.push({ who: "r2", t0: TAP2 + 0.3, t1: G5, text: "???", cls: "" });
  bubbles.push({ who: "m", t0: c("s10.follow") + 0.1, t1: FT + 0.95, text: "FOLLOW +", cls: "red follow" });

  // ---------------- overlays ----------------
  const chip = (id, t0, t1, k, v, x, y, cls = "", from = "right") => ({ id, t0, t1, from, cls: "chip " + cls, style: `left:${x}px;top:${y}px`,
    html: `<div class="ck">${k}</div><div class="cv">${v}</div>` });
  const slam = (id, t0, t1, html, top, size = 128, color = "#ffd23f") => ({ id, t0, t1, slam: true, cls: "slam", style: `top:${top}px;font-size:${size}px;color:${color}`, html });
  const overlays = [
    slam("sl-prime", -1, 1.35, "PRIME<br>MESSI", 360, 150),
    slam("sl-vs", 1.3, s("s2") - 0.05, "<b>vs.</b> REAL<br>MADRID", 360, 130),
    chip("c-eleven", c("s2.eleven"), c("s2.nomates") - 0.1, "REAL MADRID", "11 players", 120, 400),
    chip("c-one", c("s2.messi"), c("s2.nomates") - 0.1, "MESSI", "1 player", 420, 560, "red", "left"),
    chip("c-mates", c("s2.nomates"), c("s2.nokeeper") - 0.05, "TEAM-MATES", "0", 120, 400, "dark"),
    chip("c-keeper", c("s2.nokeeper"), s("s3") - 0.05, "GOALKEEPER", "none", 120, 400, "dark"),
    chip("c-self", c("s3.himself"), c("s3.through") + 0.9, "PASS", "MESSI → MESSI", 120, 400, "gold"),
    chip("c-empty", c("s4.empty"), R_SHOT + 0.4, "MESSI'S GOAL", "empty", 120, 400, "dark"),
    chip("c-report", c("s6.walks") - 0.1, SPRINT - 0.1, "SCOUTING REPORT", "Walks. A lot.", 120, 400, "dark"),
    chip("c-self2", TAP2, SHOT2 + 0.3, "PASS", "MESSI → MESSI", 120, 400, "gold"),
    slam("sl-goal", G5 + 0.05, s("s9") - 0.05, "GOAL!!!", 360, 170),
    chip("c-y17", c("s9.y17"), s("s10") + 0.1, "23 APRIL 2017", "Real 2–3 Barça · 92'", 60, 400, "gold"),
    chip("c-same", c("s9.same"), s("s10") + 0.1, "TODAY", "Same score", 420, 560, "red", "left"),
    { id: "hud", t0: KO - 0.1, t1: c("s10.loop") - 0.3, cls: "hud", style: "opacity:0",
      html: `<span class="t">RMA</span><span class="sc"><b id="hs">0</b>–<b id="as">0</b></span><span class="t">MES</span><span class="mn" id="mn">1'</span>` },
    { id: "stam", t0: c("s6.stam") - 0.1, t1: s("s9") + 0.2, cls: "stam",
      html: `<span>MESSI STAMINA</span><div class="bar"><i id="stb"></i><i id="sts" style="background:repeating-linear-gradient(45deg,#ffd23f 0 8px,#e0a800 8px 16px)"></i></div><span id="stp">100%</span>` },
    { id: "ft", t0: -10, t1: -9, cls: "ft",
      html: `<div class="fth">FULL TIME</div><div class="fts">RMA <b>2–3</b> MESSI</div><table>
        <tr><td class="h">10</td><td>team-mates</td><td class="k">0</td></tr>
        <tr><td class="h">1</td><td>goalkeepers</td><td class="k">0</td></tr>
        <tr><td class="h">0</td><td>passes Messi → Messi</td><td class="k">2</td></tr>
        <tr><td class="h">3</td><td>substitutes</td><td class="k">0</td></tr></table>
        <div class="fts" style="margin-top:18px;font-size:30px;color:#ffd23f">Most liked comment decides the next case</div>` },
    slam("sl-prime2", END - 0.35, END + 1, "PRIME<br>MESSI", 360, 150),
    { id: "conf", t0: G5, t1: s("s9") + 1.0, cls: "conf", style: "inset:0",
      html: Array.from({ length: 70 }, (_, i) => `<i style="left:${(i * 157) % 1080}px;background:${["#ffd23f", "#e0412f", "#4f7cff", "#f4f4f2", "#1f9d55"][i % 5]}"></i>`).join("") },
  ];

  // ---------------- score, minute, stamina ----------------
  const score = (t) => [t >= G1 ? 1 : 0, t >= G4 ? 2 : t >= G1 ? 1 : 0, t >= G5 ? 3 : t >= G3 ? 2 : t >= G2 ? 1 : 0];
  const minute = (t) => t >= FT ? "FT" : t >= s("s8") ? "92'" : t >= s("s7") ? "89'" : t >= s("s6") ? `${Math.round(lerp(55, 71, clamp((t - s("s6")) / 11, 0, 1)))}'`
    : t >= s("s5") ? "38'" : t >= G1 ? "23'" : t >= s("s4") ? "22'" : `${Math.max(1, Math.round((t - KO) * 0.7))}'`;
  const stamina = (t) => {
    if (t < c("s6.stam")) return 100;
    if (t < c("s6.walk")) return lerp(100, 34, sstep(c("s6.stam"), c("s6.walk"), t));
    if (t < SPRINT) return lerp(34, 40, sstep(c("s6.walk"), SPRINT, t));
    if (t < s("s7")) return lerp(40, 14, sstep(SPRINT, FOUL, t));
    if (t < s("s8")) return lerp(14, 6, sstep(s("s7"), c("s7.two"), t));
    return 3;
  };
  const saved = (t) => (t < c("s8.saved") ? 0 : t < LAST ? 1 : 1 - sstep(LAST, SHOT2, t)); // the one saved sprint (gold)

  return {
    actors: A, ball, shots: sh, props, bubbles, overlays,
    nets: { left: [G1, G4], right: [G2, G3, G5] },
    shake: [G1, G2, G3, G4, G5],
    crowd: (t) => {
      let a = 0.05;
      if (t > c("s2.fans") && t < c("s2.eleven") + 1) a = 0.28;
      for (const g of [G1, G4]) if (t > g && t < g + 3.2) a = 0.55 * (1 - sstep(g + 2.4, g + 3.2, t)) + 0.05;
      for (const g of [G2, G3, G5]) if (t > g && t < g + 3) a = 0;
      if (t > G5 && t < FT) a = 0;
      return a;
    },
    flashes: (t) => { for (const g of [G2, G3, G5]) if (t > g && t < g + 2) return 0.3; return t > c("s2.fans") && t < c("s2.eleven") ? 0.15 : 0.04; },
    ballHidden: (t) => false,
    custom: (t, { el }) => {
      const [h, a] = [score(t)[0] + (t >= G4 ? 1 : 0), score(t)[2]];
      el("hs").textContent = String(t >= G4 ? 2 : t >= G1 ? 1 : 0); el("as").textContent = String(a);
      el("mn").textContent = minute(t);
      // the HUD pops when the score changes
      let pop = 0; for (const g of [G1, G2, G3, G4, G5]) if (t >= g && t < g + 0.3) pop = Math.sin(((t - g) / 0.3) * Math.PI);
      el("hud").style.transform = `scale(${1 + pop * 0.15})`;
      // stamina: centred and big while the narrator talks about it in the last minute
      const st = stamina(t), sv = saved(t), blink = st < 20 ? (Math.floor(t * 4) % 2 ? 0.45 : 1) : 1;
      el("stb").style.width = `${st}%`; el("stb").style.background = st < 25 ? "#e0412f" : st < 55 ? "#ffd23f" : "#1f9d55"; el("stb").style.opacity = String(blink);
      el("sts").style.left = `${st}%`; el("sts").style.width = `${sv * 22}%`;
      el("stp").textContent = `${Math.round(st)}%` + (sv > 0.5 ? " + 1 SPRINT" : "");
      const big = sstep(c("s8.three") - 0.3, c("s8.three"), t) * (1 - sstep(c("s8.self") - 0.3, c("s8.self"), t));
      const sNode = el("stam");
      sNode.style.transformOrigin = "0 0";
      sNode.style.transform = `translate(${lerp(0, -440, big)}px, ${lerp(0, 380, big)}px) scale(${lerp(1, 1.75, big)})`;
      // tumbleweed rolls
      const tw = document.getElementById("w3-tw-spin"); if (tw) tw.style.transform = `rotate(${t * 260}deg)`;
      // confetti
      const conf = el("conf").children;
      for (let i = 0; i < conf.length; i++) {
        const k = (t - G5 - (i % 10) * 0.05), y = -40 + k * (380 + (i * 37) % 260);
        conf[i].style.opacity = k > 0 ? "1" : "0";
        conf[i].style.transform = `translate(${Math.sin(k * 3 + i) * 40}px, ${y}px) rotate(${k * 400 + i * 30}deg)`;
      }
    },
  };
}
