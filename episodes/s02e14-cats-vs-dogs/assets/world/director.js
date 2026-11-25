// S2E14 "Could 11 cats beat 11 dogs?" - eleven cats (purple, keeper green) vs eleven dogs of different breeds (orange, keeper: golden retriever).
// Thread: the retriever keeper happily brings the ball back - to the other team (hook, and after the equaliser).
// Cats defend the left goal (x = -52.5), dogs the right goal (x = +52.5).
import { path, sstep, clamp, lerp } from "./engine.js";
import META from "./meta.js";

export default function plot(T) {
  const c = (k) => { if (!(k in T.cue)) throw new Error("cue " + k); return T.cue[k]; };
  const s = (k) => T.start[k];
  const END = T.duration, CUT = 1.3, LOOPJ = c("s11.loop") - 0.12;

  const DROP = 1.75;                                                  // hook: the retriever drops the ball at the cat's paws
  const ROLL0 = c("s5.slow") + 0.05, G1 = c("s5.one") - 0.1;          // the slow push, 1-0
  const LASER0 = c("s7.laser") - 0.1;                                 // laser dot appears
  const G2 = c("s8.eq") - 0.12;                                       // greyhound, 1-1
  const FETCH0 = c("s8.back") - 0.35, GIVE = c("s8.cats") - 0.1;      // the keeper fetches the ball ... and gives it to the cats
  const CHASE = c("s9.bad") + 0.1;                                    // dogs chase the "mailman"
  const BOXT = c("s10.box") + 0.55, INBOX = c("s10.gone") - 0.35;      // box lands, cats jump in
  const KICK = c("s11.who") - 0.1;                                    // dachshund penalty, freeze

  const W = {}, names = [];
  for (let i = 0; i < 11; i++) names.push("C" + i, "D" + i);
  names.push("REF");
  names.forEach((n) => (W[n] = []));
  const at = (n, t, x, z, e) => W[n].push([t, x, z, e]);
  const idx = (n) => (n === "REF" ? -1 : +n.slice(1));
  const jumpAll = (t, f) => names.forEach((n) => { const p = f(n, idx(n), n[0] === "C"); if (p) at(n, t, p[0], p[1], "j"); });
  const OFF = (n, i, cc) => [cc ? -70 - i : 70 + i, 40 + i];          // parked out of shot

  // ---------- s1 hook: the retriever trots out of his goal and drops the ball at a bored cat's paws ----------
  const HOOK = { D0a: [51.5, 2.6], D0b: [48.95, 2.2], C10: [48.25, 2.45] };
  const HV = [(HOOK.D0b[0] - HOOK.D0a[0]) / 1.5, (HOOK.D0b[1] - HOOK.D0a[1]) / 1.5];
  const HOOKPOS = (n, i, cc) => (n === "D0" ? HOOK.D0a : n === "C10" ? HOOK.C10 : n === "REF" ? [30, -12] : OFF(n, i, cc));
  names.forEach((n) => { const [x, z] = HOOKPOS(n, idx(n), n[0] === "C"); at(n, 0, x, z); });
  at("D0", 1.5, HOOK.D0b[0], HOOK.D0b[1], "l");

  // ---------- s2 the dogs: line-up facing the camera; the greyhound zooms past; the pug chases its tail ----------
  const GX = (k) => -1.45 + (k % 3) * 1.45 + (Math.floor(k / 3) % 2) * 0.55, GZ = (k) => -Math.floor(k / 3) * 1.25;
  const DOGROW = ["D0", "D9", "D2", "D4", "D3", "D5", "D6", "D7", "D8", "D10"];   // D1 (greyhound) runs past instead
  jumpAll(s("s2") - 0.05, (n, i, cc) => (DOGROW.includes(n) ? [GX(DOGROW.indexOf(n)), GZ(DOGROW.indexOf(n))] : n === "D1" ? [-16, 1.6] : n === "REF" ? [0, -20] : OFF(n, i, cc)));
  const GREY = c("s2.grey") + 0.1;
  at("D1", GREY, -16, 1.6); at("D1", GREY + 0.75, 18, 1.6, "l");
  const PUGX = GX(DOGROW.indexOf("D4")), PUGZ = GZ(DOGROW.indexOf("D4"));
  const FOC = c("s2.focus") - 0.1;
  for (let k = 0; k <= 12; k++) { const a = (k / 12) * Math.PI * 4; at("D4", FOC + k * 0.12, PUGX + Math.sin(a) * 0.32, PUGZ + 0.32 - Math.cos(a) * 0.32, "l"); }

  // ---------- s3 the cats: line-up, half of them asleep ----------
  const SLEEP = ["C2", "C3", "C5", "C7", "C9"];
  jumpAll(s("s3") - 0.05, (n, i, cc) => (cc ? [GX(i), GZ(i)] : OFF(n, i, cc)));

  // ---------- s4 kick-off: all ten dogs pile onto the ball ----------
  const KO = c("s4.ko"), PILE = c("s4.chase") + 0.85;
  const RING = (k) => [Math.cos((k / 10) * Math.PI * 2) * 4.0, Math.sin((k / 10) * Math.PI * 2) * 3.0];
  jumpAll(s("s4") - 0.05, (n, i, cc) => (!cc && i > 0 ? RING(i - 1) : n === "D0" ? [51.6, 0] : n === "C10" ? [3.6, -3.2] : n === "C4" ? [-3.4, -3.6] :
    n === "C1" ? [5.2, -4.4] : n === "REF" ? [-2.5, -6] : OFF(n, i, cc)));
  for (let i = 1; i < 11; i++) { const [x, z] = RING(i - 1); at("D" + i, c("s4.chase"), x, z); at("D" + i, PILE, x * 0.07, z * 0.07, "i"); }

  // ---------- s5 the push: a cat 4 m in front of the empty dog goal, the retriever wags at the post ----------
  const CATP = [48.2, 0.15], BALLP = [48.62, 0.32];
  jumpAll(s("s5") - 0.05, (n, i, cc) => (n === "C10" ? CATP : n === "D0" ? [52.2, -2.9] : n === "D3" ? [41, -6] : n === "D6" ? [40, 5] :
    n === "REF" ? [38, 9] : OFF(n, i, cc)));

  // ---------- s6 nose to nose ----------
  jumpAll(s("s6") - 0.05, (n, i, cc) => (n === "C10" ? [-0.46, 0] : n === "D3" ? [0.55, 0] : n === "REF" ? [-2.5, -4] : n === "C4" ? [-3, -2.5] : n === "D6" ? [3.4, -2.2] : OFF(n, i, cc)));

  // ---------- s7 laser pointer: every cat (keeper included) chases the red dot ----------
  const CATS0 = (i) => (i === 0 ? [-51.7, 0] : [-43 + (i % 5) * 1.9, -5 + Math.floor(i / 2) * 1.6 - (i % 2) * 0.8]);
  jumpAll(s("s7") - 0.05, (n, i, cc) => (cc ? CATS0(i) : n === "D1" ? [-31, -6] : n === "D7" ? [-28, 3] : n === "REF" ? [-30, -12] : OFF(n, i, cc)));
  const LP = [[LASER0, -40, 2], [LASER0 + 0.7, -35, 7], [LASER0 + 1.4, -41, 11], [LASER0 + 2.1, -36, 14], [LASER0 + 2.8, -44.5, 17.5], [LASER0 + 3.4, -43.6, 18.4]];
  const lp = path(LP.map((p) => [p[0], p[1], p[2], "s"]));
  const LASEROFF = c("s8.grey") + 0.6;
  for (let i = 0; i < 11; i++) {
    const n = "C" + i, lag = 0.35 + (i % 4) * 0.12, ox = Math.cos(i * 2.4) * 1.2, oz = Math.sin(i * 2.4) * 0.9;
    for (let k = 1; k < LP.length; k++) { const q = lp(LP[k][0] - 0.15); at(n, LP[k][0] + lag, q.x + ox * (k / LP.length), q.z + oz * (k / LP.length), "s"); }
  }
  at("C10", LASER0 + 4.3, -41.3, 14.6, "s");
  // ---------- s8 the greyhound scores into the empty goal; the retriever fetches the ball - and brings it to the cats ----------
  at("D1", s("s8") - 0.05, -33, -5, "j"); at("D1", G2 - 0.45, -46.2, -1.0, "i");
  const SITC = { C10: [-41.3, 14.6] };
  at("D0", FETCH0 - 0.05, -52.3, 0.35, "j"); at("D0", FETCH0 + 0.35, -52.0, 0.6);
  at("D0", GIVE, -41.95, 14.15, "s");

  // ---------- s9 the referee's kit looks like a mailman's ----------
  const ARC = (k) => [-3.2 + k * 0.72, -3.4 - Math.abs(k - 4.5) * 0.25];
  jumpAll(s("s9") - 0.05, (n, i, cc) => (n === "REF" ? [0, 0] : !cc && i > 0 ? ARC(i - 1) : n === "D0" ? [51.6, 0] : cc && i > 5 ? [-9 - i, -6 + i * 0.4] : OFF(n, i, cc)));
  at("REF", CHASE, 0, 0); at("REF", CHASE + 2.6, 30, 3, "i");
  for (let i = 1; i < 11; i++) { const [x, z] = ARC(i - 1); at("D" + i, CHASE + 0.15 + (i % 3) * 0.08, x, z); at("D" + i, CHASE + 2.9, 28 - (i % 4) * 0.9, 2 + ((i % 3) - 1) * 0.9, "i"); }

  // ---------- s10 the box ----------
  const BOXP = [-6.6, 0.4];
  const INC = ["C2", "C3", "C5", "C7", "C9"], STAY = ["C1", "C4", "C6", "C8", "C10"];
  const CIRC = (k, r) => [BOXP[0] + Math.cos(k * 1.26 + 0.6) * r, BOXP[1] + Math.sin(k * 1.26 + 0.6) * r * 0.75];
  jumpAll(s("s10") - 0.05, (n, i, cc) => (INC.includes(n) ? CIRC(INC.indexOf(n), 2.0) : STAY.includes(n) ? CIRC(STAY.indexOf(n) + 0.5, 3.1) :
    n === "C0" ? [-51.7, 0] : OFF(n, i, cc)));
  INC.forEach((n, k) => { const p = CIRC(k, 2.0); at(n, BOXT + 0.15 + k * 0.08, p[0], p[1]); at(n, INBOX - 0.15 + k * 0.05, BOXP[0], BOXP[1] + 0.05, "i"); });

  // ---------- s11 last chance: dachshund penalty, the keeper cat is busy grooming ----------
  jumpAll(s("s11") - 0.05, (n, i, cc) => (n === "D2" ? [-40.4, 0.05] : n === "C0" ? [-52.0, 0] : n === "REF" ? [-38, 6] : n === "C10" ? [-36, -6] :
    n === "C6" ? [-35, -8] : n === "D3" ? [-34, 8] : n === "D9" ? [-33, 6.5] : OFF(n, i, cc)));
  at("D2", KICK - 0.65, -40.4, 0.05); at("D2", KICK, -41.25, 0.03, "i");

  // ---------- loop back into the hook ----------
  names.forEach((n) => { const [x, z] = HOOKPOS(n, idx(n), n[0] === "C"); const back = n === "D0" ? END - LOOPJ : 0;
    at(n, LOOPJ, x - HV[0] * back, z - HV[1] * back, "j"); at(n, END, x, z, "l"); });
  for (const n of names) W[n].sort((p, q) => p[0] - q[0]);

  // ---------------- actors ----------------
  const span = (t, a, b) => t >= a && t < b;
  const A = {};
  for (const n of names) {
    const cc = n[0] === "C", i = idx(n), ev = [];
    let viewAt = (t) => (cc ? "front" : "side"), facing = () => 1;
    if (n === "D0") { viewAt = (t) => (span(t, s("s2"), s("s3")) ? "front" : "side"); facing = (t) => (t < s("s2") || t > LOOPJ ? -1 : t < s("s8") ? -1 : 1); }
    if (!cc && n !== "D0") viewAt = (t) => (span(t, s("s2"), s("s3")) || span(t, s("s9"), CHASE) ? "front" : "side");
    if (n === "D3") facing = (t) => (span(t, s("s6"), s("s7")) ? -1 : 1);
    if (n === "D2") facing = () => -1;
    if (n === "C10") viewAt = (t) => (span(t, s("s6"), s("s7")) ? "side" : "front");
    if (n === "C10") facing = () => 1;
    if (n === "REF") viewAt = () => "front";
    // events
    if (n === "D0") ev.push(["jump", G1 + 0.05, 1.2], ["jump", GIVE + 0.05, 0.6]);
    if (n === "D4") ev.push(["spin", FOC, 1.5]);
    if (n === "C1") ev.push(["yawn", c("s3.start") + 0.1, 1.1]);
    if (SLEEP.includes(n)) ev.push(["hide", s("s3") - 0.05, s("s4") - s("s3")]);
    if (!cc && i > 0) ev.push(["jump", PILE - 0.1, 2.0]);
    if (n === "C10") ev.push(["paw", c("s5.push") + 0.2, ROLL0 + 0.25 - c("s5.push"), 48, 1.6]);
    if (!cc && i > 0) ev.push(["yawn", c("s9.bad") - 0.05, 2.6]);   // barking
    if (n === "REF") ev.push(["armsUp", CHASE, 3]);
    if (INC.includes(n)) ev.push(["hide", INBOX + 0.05, s("s11") - INBOX]);
    if (n === "C0") ev.push(["armR", s("s11") + 0.2, LOOPJ - s("s11") - 0.2, 160]);   // grooming
    const m = META[n];
    A[n] = { path: W[n], ev, h: m.h, unit: m.unit, stride: cc ? 0.55 : n === "D1" ? 1.4 : n === "D2" || n === "D4" || n === "D5" ? 0.4 : 0.8,
      viewAt, facing, dust: !cc && i > 0, look: n === "C10" ? () => 0 : undefined };
  }

  // ---------------- ball ----------------
  const ball = [
    { t0: 0, k: "at", who: "D0", dx: -0.36, dz: -0.02, y: 0.4 },                                             // in the retriever's mouth
    { t0: DROP, t1: DROP + 0.35, k: "fly", a: [HOOK.D0b[0] - 0.36, 0.4, HOOK.D0b[1] - 0.02], b: [48.55, 0.0, 2.55], h: 0.12 },
    { t0: DROP + 0.35, k: "rest", p: [48.55, 0.0, 2.55] },
    { t0: s("s2") - 0.05, k: "rest", p: [0, -50, 0] },
    { t0: s("s4") - 0.05, k: "rest", p: [0, 0, 0] },
    { t0: c("s4.same") + 0.2, t1: s("s5") - 0.1, k: "fly", a: [0, 0.1, 0], b: [4.5, 0, 1.2], h: 0.6, ease: "o" },   // squirts out of the pile
    { t0: s("s5") - 0.05, k: "rest", p: [BALLP[0], 0, BALLP[1]] },
    { t0: ROLL0, t1: G1, k: "fly", a: [BALLP[0], 0, BALLP[1]], b: [52.7, 0.05, 0.45], h: 0, ease: "o" },          // ... slowly
    { t0: G1, k: "rest", p: [53.1, 0.05, 0.45] },
    { t0: s("s6") - 0.05, k: "rest", p: [0.05, 0, 0.35] },
    { t0: s("s7") - 0.05, k: "rest", p: [-36, 0, -6.2] },
    { t0: s("s8") - 0.05, k: "at", who: "D1", dx: -0.5, dz: 0.05 },
    { t0: G2 - 0.45, t1: G2, k: "fly", a: [-46.7, 0, -1.0], b: [-52.9, 0.3, -0.4], h: 0.3 },
    { t0: G2, k: "rest", p: [-53.2, 0.05, -0.4] },
    { t0: FETCH0 + 0.3, k: "at", who: "D0", dx: 0.3, dz: 0.24, y: 0.43 },                                      // the keeper fetches it
    { t0: GIVE, t1: GIVE + 0.3, k: "fly", a: [-41.65, 0.43, 14.39], b: [-41.1, 0, 14.85], h: 0.1 },
    { t0: GIVE + 0.3, k: "rest", p: [-41.1, 0, 14.85] },
    { t0: s("s9") - 0.05, k: "rest", p: [0, -50, 0] },
    { t0: s("s11") - 0.05, k: "rest", p: [-41.5, 0, 0] },
    { t0: KICK, t1: KICK + 0.45, k: "fly", a: [-41.5, 0, 0], b: [-50.3, 0.5, 0.45], h: 0.35 },
    { t0: KICK + 0.45, k: "rest", p: [-50.3, 0.5, 0.45] },                                                        // freeze
    { t0: LOOPJ, k: "at", who: "D0", dx: -0.36, dz: -0.02, y: 0.4 },
  ];

  // ---------------- props ----------------
  const props = {};
  SLEEP.forEach((n) => { props["sleep" + n.slice(1)] = { p: [GX(+n.slice(1)), 0, GZ(+n.slice(1)) + 0.02], h: 0.25, unit: 125, only: [s("s3") - 0.05, s("s4") - 0.05] }; });
  props.laser = { at: (t) => { const q = lp(t); return [q.x, 0.02, q.z]; }, h: 0.1, unit: 50, only: [LASER0, LASEROFF] };
  props.box = { at: (t) => [BOXP[0], 7 * (1 - sstep(c("s10.box"), BOXT, t)) ** 1.5, BOXP[1]], h: 0.392, unit: 196, only: [c("s10.box"), INBOX + 0.1] };
  props.boxfull = { p: [BOXP[0], 0, BOXP[1]], h: 0.5, unit: 250, only: [INBOX + 0.1, s("s11") - 0.05] };

  // ---------------- camera ----------------
  const sh = [], add = (o) => sh.push(o);
  const HOOKCAM = { k: "path", P: [[49.5, 0.62, 8.0], [49.3, 0.6, 7.6]], T: [[49.5, 0.36, 2.45], [49.3, 0.36, 2.45]], fov: [54, 52], blur: 1.6 };
  add({ t0: 0, ...HOOKCAM });
  add({ t0: CUT, k: "path", P: [[47.55, 0.42, 4.6], [47.65, 0.4, 4.3]], T: [[48.55, 0.3, 2.3], [48.55, 0.3, 2.3]], fov: [44, 40], blur: 1.4 });
  add({ t0: s("s2") + 0.05, whip: true, k: "path", P: [[-0.7, 1.3, 5.8], [0.6, 1.2, 5.3]], T: [[-0.2, 0.3, -1.4], [0.3, 0.3, -1.4]], fov: [54, 52], blur: 1.2, ease: "l" });
  add({ t0: c("s2.focus") - 0.2, blend: 0.35, k: "path", P: [[PUGX + 0.2, 0.55, PUGZ + 2.7], [PUGX + 0.1, 0.5, PUGZ + 2.4]], T: [[PUGX, 0.25, PUGZ + 0.3], [PUGX, 0.25, PUGZ + 0.3]], fov: [46, 42], blur: 1.6 });
  add({ t0: s("s3") + 0.05, whip: true, k: "path", P: [[-0.7, 1.2, 5.4], [0.6, 1.1, 5.0]], T: [[-0.2, 0.25, -1.4], [0.3, 0.25, -1.4]], fov: [54, 52], blur: 1.2, ease: "l" });
  add({ t0: s("s4") + 0.05, whip: true, k: "path", P: [[0.3, 2.2, 7.4], [0.2, 1.9, 6.4]], T: [[0, 0.2, 0], [0, 0.3, 0]], fov: [54, 52], blur: 1.2 });
  add({ t0: c("s4.same") - 0.15, blend: 0.3, k: "path", P: [[2.4, 0.9, 4.2], [2.9, 0.8, 3.8]], T: [[0.6, 0.4, 0.2], [1.4, 0.35, 0.4]], fov: [48, 46], blur: 1.6 });
  add({ t0: s("s5") + 0.05, whip: true, k: "path", P: [[46.6, 0.5, 2.9], [46.9, 0.48, 2.6]], T: [[48.6, 0.3, 0.3], [48.6, 0.3, 0.3]], fov: [46, 44], blur: 1.2 });
  add({ t0: ROLL0 - 0.05, blend: 0.25, k: "path", P: [[47.6, 0.32, 0.55], [48.4, 0.3, 0.5]], T: [[52.6, 0.45, 0.2], [52.6, 0.45, 0.2]], fov: [48, 46], blur: 1.0 });
  add({ t0: c("s5.look") - 0.05, k: "path", P: [[48.2, 0.43, 1.3], [48.2, 0.43, 1.12]], T: [[48.2, 0.42, 0.15], [48.2, 0.42, 0.15]], fov: [34, 30], blur: 1.8 });
  add({ t0: G1 - 0.25, k: "path", P: [[49.2, 0.8, 3.4], [49.5, 0.8, 3.1]], T: [[52.6, 0.5, -1.4], [52.6, 0.5, -1.4]], fov: [52, 50], blur: 1.2 });
  add({ t0: s("s6") + 0.05, whip: true, k: "path", P: [[0.05, 0.6, 3.5], [0.05, 0.6, 3.1]], T: [[0.05, 0.5, 0], [0.05, 0.5, 0]], fov: [50, 48], blur: 1.8 });
  add({ t0: s("s7") + 0.05, whip: true, k: "follow", who: "C10", off: [[4.2, 2.5, 7.2], [4.4, 2.6, 7.4]], look: [-1.6, 0.2, -1.2], fov: [54, 54], blur: 1.0 });
  add({ t0: s("s8") + 0.05, whip: true, k: "follow", who: "D1", off: [[2.4, 0.9, 4.4], [2.0, 0.9, 4.6]], look: [-2.6, 0.35, -1.4], fov: [52, 50], blur: 1.2 });
  add({ t0: FETCH0 + 0.05, k: "follow", who: "D0", off: [[3.4, 1.2, -2.6], [3.2, 1.0, -2.3]], look: [0, 0.35, 0], fov: [48, 46], blur: 1.4 });
  add({ t0: GIVE - 0.45, blend: 0.4, k: "path", P: [[-38.6, 0.6, 12.2], [-38.9, 0.55, 12.5]], T: [[-41.5, 0.32, 14.8], [-41.5, 0.32, 14.8]], fov: [46, 42], blur: 1.4 });
  add({ t0: s("s9") + 0.05, whip: true, k: "path", P: [[0.4, 1.7, 3.6], [0.3, 1.65, 3.0]], T: [[0, 1.45, 0], [0, 1.5, 0]], fov: [46, 42], blur: 1.6 });
  add({ t0: c("s9.kit") + 0.9, k: "path", P: [[1.8, 0.7, 0.9], [1.6, 0.65, 0.6]], T: [[0, 0.4, -3.6], [0, 0.4, -3.6]], fov: [56, 52], blur: 1.2 });
  add({ t0: CHASE + 0.2, blend: 0.3, k: "path", P: [[-1.8, 1.5, 7.2], [-0.6, 1.5, 7.2]], T: [[0.6, 0.5, -1.2], [2.6, 0.5, -0.6]], fov: [58, 58], blur: 1.0 });
  add({ t0: s("s10") + 0.05, whip: true, k: "path", P: [[-6.4, 1.1, 5.2], [-6.5, 0.95, 4.6]], T: [[-6.6, 0.45, 0.2], [-6.6, 0.35, 0.3]], fov: [50, 48], blur: 1.2 });
  add({ t0: s("s11") + 0.05, whip: true, k: "path", P: [[-40.95, 0.42, 2.7], [-41.0, 0.4, 2.45]], T: [[-41.0, 0.25, 0], [-41.0, 0.25, 0]], fov: [48, 44], blur: 1.4 });
  add({ t0: c("s11.pen") + 0.05, k: "path", P: [[-49.2, 0.45, 2.6], [-49.4, 0.42, 2.3]], T: [[-52, 0.3, -0.1], [-52, 0.3, -0.1]], fov: [44, 40], blur: 1.6 });
  add({ t0: c("s11.who") - 0.8, k: "path", P: [[-41.0, 0.42, 2.7], [-41.1, 0.42, 2.6]], T: [[-41.0, 0.25, 0], [-41.1, 0.25, 0]], fov: [48, 46], blur: 1.2 });
  add({ t0: KICK + 0.12, k: "path", P: [[-48.3, 0.55, 2.9], [-48.4, 0.55, 2.8]], T: [[-51.2, 0.4, 0.1], [-51.2, 0.4, 0.1]], fov: [46, 44], blur: 1.4 });
  add({ t0: c("s11.loop") - 0.12, blend: 0.12, whip: true, ...HOOKCAM });
  sh.forEach((x, i) => { x.t1 = x.t1 ?? (sh[i + 1] ? sh[i + 1].t0 : END); });
  sh[sh.length - 1].t1 = END;

  // ---------------- overlays ----------------
  const chip = (id, t0, t1, kk, v, x, y, cls = "", from = "right") => ({ id, t0, t1, from, cls: "chip " + cls, style: `left:${x}px;top:${y}px`,
    html: `<div class="ck">${kk}</div><div class="cv">${v}</div>` });
  const slam = (id, t0, t1, html, top, size = 128) => ({ id, t0, t1, slam: true, cls: "slam", style: `top:${top}px;font-size:${size}px`, html });
  const lower = (id, t0, who, min, y = 560) => chip(id, t0, t0 + 1.3, "GOAL · " + min, who, 60, y, "dark", "left");
  const overlays = [
    slam("sl-a", -1, s("s2") - 0.05, "11 CATS<br><b>vs.</b> 11 DOGS", 340, 110),
    chip("c-grey", GREY, c("s2.focus") - 0.1, "GREYHOUND", "70 KM/H", 100, 400, "red"),
    chip("c-foc", c("s2.focus"), s("s3") - 0.05, "FOCUS", "0", 120, 400, "dark"),
    chip("c-sleep", c("s3.ct") + 0.2, c("s3.start") - 0.05, "CATS SLEEP", "16 H / DAY", 100, 400, "dark"),
    chip("c-start", c("s3.start"), s("s4") - 0.05, "TODAY", "STARTING XI", 100, 400, "gold"),
    chip("c-slow", ROLL0 + 0.1, c("s5.look") - 0.05, "BALL SPEED", "0.4 KM/H", 100, 400, "gold"),
    lower("g1", G1 + 0.3, "Cat No. 11 (one paw)", "20'"),
    chip("c-laser", LASER0, s("s8") - 0.05, "IN THE CROWD", "LASER POINTER", 80, 400, "red"),
    lower("g2", G2 + 0.3, "Greyhound (empty net)", "55'"),
    chip("c-ref", c("s9.kit") + 0.1, CHASE - 0.05, "REFEREE KIT", "= MAILMAN KIT", 80, 400, "dark"),
    chip("c-pause", CHASE + 0.4, s("s10") - 0.05, "GAME", "PAUSED", 120, 400, "red"),
    chip("c-avail", c("s10.gone"), s("s11") - 0.05, "CATS AVAILABLE", "6", 120, 400, "gold"),
    chip("c-who", c("s11.who"), LOOPJ, "COMMENT", "Who will win?", 120, 460, "red"),
    { id: "hud", t0: c("s4.ko") - 0.1, t1: LOOPJ, cls: "hud", style: "opacity:0",
      html: `<span class="t">CATS</span><span class="sc"><b id="hs">0</b>–<b id="as">0</b></span><span class="t">DOGS</span><span class="mn" id="mn">1'</span>` },
    slam("sl-end", END - 0.3, END + 1, "11 CATS<br><b>vs.</b> 11 DOGS", 340, 110),
  ];
  const bubbles = [
    { who: "C10", t0: DROP + 0.45, t1: s("s2") - 0.1, text: "...", cls: "small" },
    { who: "D4", t0: FOC + 0.2, t1: s("s3") - 0.1, text: "TAIL?!", cls: "orange small" },
    { who: "C1", t0: c("s3.start") + 0.1, t1: s("s4") - 0.1, text: "*yawn*", cls: "small" },
    { who: "C10", t0: c("s4.same") + 0.3, t1: s("s5") - 0.1, text: "...", cls: "small" },
    { who: "D0", t0: G1 + 0.2, t1: s("s6") - 0.1, text: "♥", cls: "red" },
    { who: "C10", t0: c("s6.follow") + 0.05, t1: c("s6.q") - 0.05, text: "♥ LIKE + FOLLOW +", cls: "red follow" },
    { who: "C10", t0: c("s6.q"), t1: s("s7") - 0.1, text: "TEAM CAT?", cls: "purple" },
    { who: "D3", t0: c("s6.q") + 0.3, t1: s("s7") - 0.1, text: "TEAM DOG?", cls: "orange" },
    { who: "D0", t0: GIVE - 0.6, t1: s("s9") - 0.1, text: "HERE YOU GO!", cls: "small" },
    { who: "D5", t0: c("s9.kit") + 1.0, t1: CHASE - 0.05, text: "MAILMAN?!", cls: "orange small" },
    { who: "D2", t0: c("s11.pen") + 0.3, t1: KICK - 0.2, text: "MY TIME.", cls: "orange small" },
    { who: "C0", t0: c("s11.pen") + 0.4, t1: c("s11.who") - 0.85, text: "*lick*", cls: "small" },
  ];
  const bursts = [{ who: "D3", t: PILE + 0.05, text: "WOOF!" }, { who: "D6", t: CHASE + 0.05, text: "WOOF!" }];
  const minute = (t) => (t >= c("s9.min") ? "90'" : t >= s("s7") ? "55'" : t >= s("s5") ? "20'" : "1'");

  return {
    actors: A, ball, shots: sh, overlays, bubbles, bursts, props,
    grade: "contrast(1.12) saturate(1.22) brightness(0.98)",
    nets: { right: [G1], left: [G2] }, shake: [G1, G2, PILE, BOXT],
    crowd: (t) => ([G1, G2].some((g) => t > g && t < g + 2.4) ? 0.5 : t > PILE && t < PILE + 1.5 ? 0.35 : 0.1),
    flashes: (t) => ([G1, G2].some((g) => t > g && t < g + 2) ? 0.3 : 0.05),
    speedlines: (t) => Math.max(0.55 * (1 - sstep(CUT - 0.1, CUT + 0.1, t)), 0.55 * sstep(END - 0.35, END - 0.2, t),
      0.5 * sstep(GREY - 0.05, GREY + 0.05, t) * (1 - sstep(GREY + 0.6, GREY + 0.8, t)), 0.4 * sstep(s("s8"), s("s8") + 0.1, t) * (1 - sstep(G2 - 0.1, G2 + 0.1, t))),
    custom: (t, { el }) => {
      el("hs").textContent = String(t >= G1 ? 1 : 0);
      el("as").textContent = String(t >= G2 ? 1 : 0);
      el("mn").textContent = minute(t);
      let pop = 0; for (const gg of [G1, G2]) if (t >= gg && t < gg + 0.3) pop = Math.sin(((t - gg) / 0.3) * Math.PI);
      el("hud").style.transform = `scale(${1 + pop * 0.15})`;
    },
  };
}
