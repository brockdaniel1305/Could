// S2E15 "Could Bayern's injured players beat Manchester United?" - Bayern's injury list (9, with crutches, casts, a wheelchair)
// vs Man United (eleven fit players, nine games without a win, a brand-new manager). Bayern attack +x (United goal x = +52.5),
// United attack -x (Bayern goal x = -52.5). Thread: Neuer's crutch (hook = the penalty save; s8).
import { path, sstep, clamp, lerp } from "./engine.js";

export default function plot(T) {
  const c = (k) => { if (!(k in T.cue)) throw new Error("cue " + k); return T.cue[k]; };
  const s = (k) => T.start[k];
  const END = T.duration, LOOPJ = c("s11.loop") - 0.12;

  const BAY = ["NEU", "KIM", "DAV", "PAV", "MUS", "GNA", "DIA", "BUC"];
  const UTD = ["U1", "U2", "U3", "U4", "U5", "U6", "U7", "U8", "U9", "U10", "U11"];
  const names = [...BAY, ...UTD, "MGR", "PHY", "REF"];
  const W = {}; names.forEach((n) => (W[n] = []));
  const at = (n, t, x, z, e) => W[n].push([t, x, z, e]);
  const jumpAll = (t, f) => names.forEach((n) => { const p = f(n); if (p) at(n, t, p[0], p[1], "j"); });
  const OFF = (n) => [80 + names.indexOf(n), 60];

  // key times
  const PK = c("s8.crutch") + 0.25, SAVE = c("s8.saved") - 0.15;       // penalty, saved with the crutch
  const HK = 1.0;                                                     // hook: the save happens at 1.0 s
  const G1 = c("s6.one") - 0.1, G2 = c("s10.two") - 0.1;
  const SHOT = c("s11.who") - 0.1;

  // ---------- s1 hook: the crutch save (cold open), then both teams at the centre circle ----------
  const HOOKPOS = (n) => (n === "NEU" ? [-51.6, 0.2] : n === "U9" ? [-42.5, 1.2] : n === "REF" ? [-40, 9] : OFF(n));
  names.forEach((n) => { const p = HOOKPOS(n); at(n, 0, p[0], p[1]); });
  const LINE = (n) => { const b = BAY.indexOf(n), u = UTD.indexOf(n);
    if (b >= 0) return [-1.8 - (b % 4) * 1.3, -3 + Math.floor(b / 4) * 2.2];
    if (u >= 0) return [1.8 + (u % 4) * 1.3, -4 + Math.floor(u / 4) * 2.2];
    return n === "REF" ? [0, -5.5] : OFF(n); };
  jumpAll(1.7, LINE);

  // ---------- s2 the injury list: Bayern hobble in one after another; the wheelchair is pushed past ----------
  const ROW = (k) => [-7 + k * 1.75, 0];
  jumpAll(s("s2") - 0.05, (n) => { const b = BAY.indexOf(n); return b >= 0 ? [ROW(b)[0], -9] : n === "PHY" ? [-14, -3.2] : OFF(n); });
  BAY.forEach((n, b) => { const [x, z] = ROW(b); at(n, s("s2") + 0.2 + b * 0.25, x, -9); at(n, s("s2") + 2.6 + b * 0.25, x, z, "s"); });
  at("PHY", c("s2.nine") - 0.2, -14, -3.2); at("PHY", s("s3") - 0.1, 10, -3.2, "l");

  // ---------- s3 United march in proudly; the new manager reads the line-up upside down ----------
  jumpAll(s("s3") - 0.05, (n) => { const u = UTD.indexOf(n); return u >= 0 ? [-8 + u * 1.6, -6] : n === "MGR" ? [3.0, 5.2] : OFF(n); });
  UTD.forEach((n, u) => { at(n, s("s3") + 0.1, -8 + u * 1.6, -6); at(n, c("s3.mgr") - 0.2, -8 + u * 1.6, 0, "s"); });

  // ---------- s4 kick-off: eleven against nine (+ wheelchair) ----------
  jumpAll(s("s4") - 0.05, (n) => { const b = BAY.indexOf(n), u = UTD.indexOf(n);
    if (b >= 0) return n === "NEU" ? [-12, 0] : [-2.5 - (b % 3) * 3, -6 + Math.floor(b / 3) * 5];
    if (u >= 0) return n === "U1" ? [13, 0] : [2.5 + (u % 3) * 2.8, -8 + Math.floor(u / 3) * 4.5];
    return n === "REF" ? [0, 7] : OFF(n); });

  // ---------- s5 United's first pass goes straight to Musiala ----------
  jumpAll(s("s5") - 0.05, (n) => (n === "U8" ? [2.5, 0.3] : n === "U6" ? [9, -3] : n === "MUS" ? [-2.5, 4.6] : n === "U4" ? [6, 4] :
    n === "DIA" ? [-6, -3] : n === "REF" ? [0, -7] : OFF(n)));

  // ---------- s6 Musiala dribbles in slow motion through the whole United defence ----------
  const DEF = ["U2", "U3", "U4", "U5", "U6"], DX = [40.5, 42.5, 44.5, 46.5, 48.5];
  const D0 = c("s6.slow"), D1 = G1 - 0.6;
  const PASSAT = (k) => lerp(D0, D1, (DX[k] - 38) / (49.5 - 38));
  jumpAll(s("s6") - 0.05, (n) => (n === "MUS" ? [36.5, 0.4] : DEF.includes(n) ? [DX[DEF.indexOf(n)], (DEF.indexOf(n) % 2 ? 1 : -1) * 1.1] :
    n === "U1" ? [52, 0] : n === "GNA" ? [33, -5] : n === "REF" ? [36, 9] : OFF(n)));
  at("MUS", D0, 38, 0.4); at("MUS", D1, 49.5, 0.2, "l"); at("MUS", G1 + 1.0, 50.5, -1.5, "o");

  // ---------- s7 face to face ----------
  jumpAll(s("s7") - 0.05, (n) => (n === "MUS" ? [-0.6, 0] : n === "U7" ? [0.6, 0] : n === "REF" ? [0, -3] : OFF(n)));

  // ---------- s8 penalty: Neuer can't dive, sticks out his crutch ----------
  const PKPOS = (n) => (n === "NEU" ? [-51.6, 0.2] : n === "U9" ? [-40.6, 0.3] : n === "REF" ? [-38, 8] : n === "KIM" ? [-36, -6] :
    n === "U7" ? [-35, 5] : n === "DAV" ? [-35.5, 6] : OFF(n));
  jumpAll(s("s8") - 0.05, PKPOS);
  at("U9", PK - 0.6, -40.6, 0.3); at("U9", PK, -41.3, 0.3, "i");

  // ---------- s9 half-time: one physio, nine patients ----------
  const PAT = (k) => [-6 + (k % 4) * 3, -3 + Math.floor(k / 4) * 5];
  jumpAll(s("s9") - 0.05, (n) => { const b = BAY.indexOf(n); return b >= 0 ? PAT(b) : n === "PHY" ? [-7, -5] : OFF(n); });
  [0, 5, 1, 4, 2, 7, 3, 6].forEach((b, k) => { const [x, z] = PAT(b); at("PHY", c("s9.physio") - 0.3 + k * 0.28, x + 0.9, z + 0.5, "s"); });

  // ---------- s10 Davies sprints on one leg down the wing, still faster ----------
  const R0 = c("s10.davies") - 0.1, R1 = G2 - 0.7;
  jumpAll(s("s10") - 0.05, (n) => (n === "DAV" ? [18, 22] : n === "U2" ? [14, 22.5] : n === "U3" ? [12, 21] : n === "U5" ? [44, 4] :
    n === "U1" ? [52, 0] : n === "REF" ? [30, 12] : OFF(n)));
  at("DAV", R0, 18, 22); at("DAV", R1, 43, 12, "l"); at("DAV", G2 + 0.9, 45, 9, "o");
  at("U2", R0 + 0.3, 14, 22.5); at("U2", R1 + 0.5, 34, 18, "l");
  at("U3", R0 + 0.3, 12, 21); at("U3", R1 + 0.5, 31, 17, "l");

  // ---------- s11 last chance: an empty goal ----------
  jumpAll(s("s11") - 0.05, (n) => (n === "U9" ? [-44.5, 2.2] : n === "NEU" ? [-46, -14] : n === "PHY" ? [-45, -13] : n === "REF" ? [-38, 8] :
    n === "U7" ? [-36, 6] : OFF(n)));
  at("U9", SHOT - 0.5, -44.5, 2.2); at("U9", SHOT, -45.3, 1.9, "i");

  // loop back into the hook
  names.forEach((n) => { const p = HOOKPOS(n); at(n, LOOPJ, p[0], p[1], "j"); at(n, END, p[0], p[1]); });
  for (const n of names) W[n].sort((p, q) => p[0] - q[0]);

  // ---------------- actors ----------------
  const A = {};
  for (const n of names) {
    const ev = [];
    if (n === "NEU") ev.push(["armR", HK - 0.35, 1.2, 75], ["armR", c("s8.crutch") - 0.05, s("s9") - c("s8.crutch"), 80],       ["fall", s("s11") - 0.05, 0, -1], ["up", LOOPJ - 0.45]);
    if (n === "U9") ev.push(["armsUp", SAVE + 0.6, 0]);
    if (DEF.includes(n)) ev.push(["fall", PASSAT(DEF.indexOf(n)) + 0.15, 0, DEF.indexOf(n) % 2 ? 1 : -1], ["up", s("s7") - 0.1]);
    if (n === "U1") ev.push(["fall", G1 - 0.15, 0, 1], ["up", s("s7") - 0.1], ["fall", G2 - 0.15, 0, -1], ["up", s("s11") - 0.1]);
    if (n === "MUS") ev.push(["armsUp", G1 + 0.2, 1.2]);
    if (n === "DAV") ev.push(["jump", R0, R1 - R0 + 0.6], ["armsUp", G2 + 0.25, 1.2]);
    if (n === "MGR") ev.push(["armR", c("s3.mgr"), s("s4") - c("s3.mgr"), 60]);
    if (n === "PHY") ev.push(["armsUp", c("s9.nine"), 0.8]);
    if (["KIM", "PAV", "GNA", "BUC", "DIA"].includes(n)) ev.push(["fall", c("s9.ht") + 0.1 + BAY.indexOf(n) * 0.06, s("s10") - c("s9.ht") - 0.3, BAY.indexOf(n) % 2 ? 1 : -1],
      ["up", s("s10") - 0.05]);
    if (UTD.includes(n) && n !== "U1") ev.push(["jump", c("s4.count") + 0.05 * UTD.indexOf(n), 0.5]);
    A[n] = { path: W[n], ev, h: 1.82, unit: 360, stride: n === "MUS" ? 1.0 : n === "DAV" ? 2.6 : BAY.includes(n) ? 1.1 : 1.9, autoFlip: true };
  }

  // ---------------- ball ----------------
  const ball = [
    { t0: 0, t1: HK, k: "fly", a: [-42.0, 0, 1.0], b: [-49.9, 0.9, 0.55], h: 0.4 },
    { t0: HK, t1: HK + 0.7, k: "fly", a: [-49.9, 0.9, 0.55], b: [-46, 0, 6.5], h: 2.2, ease: "o" },          // off the crutch
    { t0: HK + 0.7, k: "rest", p: [-46, 0, 6.5] },
    { t0: 1.7, k: "rest", p: [0, 0, 0] },
    { t0: s("s2") - 0.05, k: "rest", p: [0, -50, 0] },
    { t0: s("s4") - 0.05, k: "rest", p: [0, 0, 0] },
    { t0: s("s5") - 0.05, k: "at", who: "U8", dx: -0.5, dz: 0 },
    { t0: c("s5.pass") + 0.2, t1: c("s5.bay") + 0.2, k: "fly", a: [2.0, 0, 0.3], b: [-2.1, 0, 4.4], h: 0.3 },
    { t0: c("s5.bay") + 0.2, k: "rest", p: [-2.1, 0, 4.4] },
    { t0: s("s6") - 0.05, k: "at", who: "MUS", dx: 0.5, dz: 0 },
    { t0: D1, t1: G1, k: "fly", a: [50.0, 0, 0.2], b: [52.9, 0.15, 0.3], h: 0.05 },
    { t0: G1, t1: G1 + 0.3, k: "fly", a: [52.9, 0.15, 0.3], b: [54.2, 0.1, 0.3], h: 0.1 },
    { t0: G1 + 0.3, k: "rest", p: [54.2, 0.1, 0.3] },
    { t0: s("s7") - 0.05, k: "rest", p: [0, 0, 0.5] },
    { t0: s("s8") - 0.05, k: "rest", p: [-41.5, 0, 0.2] },
    { t0: PK, t1: SAVE, k: "fly", a: [-41.5, 0, 0.2], b: [-49.9, 0.9, 0.55], h: 0.4 },
    { t0: SAVE, t1: SAVE + 0.7, k: "fly", a: [-49.9, 0.9, 0.55], b: [-46, 0, 6.5], h: 2.2, ease: "o" },
    { t0: SAVE + 0.7, k: "rest", p: [-46, 0, 6.5] },
    { t0: s("s9") - 0.05, k: "rest", p: [0, -50, 0] },
    { t0: s("s10") - 0.05, k: "at", who: "DAV", dx: 0.55, dz: -0.2 },
    { t0: R1, t1: G2, k: "fly", a: [43.6, 0, 11.6], b: [52.9, 0.9, 2.0], h: 0.6, curve: 0.4 },
    { t0: G2, t1: G2 + 0.3, k: "fly", a: [52.9, 0.9, 2.0], b: [54.2, 0.1, 2.2], h: 0.1 },
    { t0: G2 + 0.3, k: "rest", p: [54.2, 0.1, 2.2] },
    { t0: s("s11") - 0.05, k: "rest", p: [-46.0, 0, 1.8] },
    { t0: SHOT, t1: SHOT + 0.4, k: "fly", a: [-46.0, 0, 1.8], b: [-50.5, 1.4, 4.8], h: 0.4 },
    { t0: SHOT + 0.4, k: "rest", p: [-50.5, 1.4, 4.8] },                                                // freeze
    { t0: LOOPJ, k: "rest", p: [-42.0, 0, 1.0] },
  ];

  // ---------------- props: wheelchair (pushed by the physio in s2, parked in s4/s9), the manager's sheet ----------------
  const PS = {}; const pos = (n, t) => { const p = (PS[n] = PS[n] || path(A[n].path))(t); return [p.x, p.z]; };
  const props = {
    wheelchair: { h: 1.15, unit: 230, at: (t) => { if (t < s("s3")) { const p = pos("PHY", t); return [p[0] + 1.1, 0, p[1] + 0.1]; }
      if (t < s("s9")) return [-9, 0, 4]; return [-6 + 3 * 1.2, 0, 4.2]; },
      only: [s("s2") - 0.05, s("s5") - 0.05], sc: () => [1, 1] },
    sheet: { h: 0.42, unit: 130, at: (t) => { const p = pos("MGR", t); return [p[0] + 0.35, 1.25, p[1] + 0.12]; }, only: [s("s3") - 0.05, s("s4") - 0.05] },
  };

  // ---------------- camera ----------------
  const sh = [], add = (o) => sh.push(o);
  const HOOKCAM = { k: "path", P: [[-47.2, 1.0, 4.6], [-47.6, 1.0, 4.3]], T: [[-50.8, 0.95, 0.4], [-50.8, 0.95, 0.4]], fov: [50, 46], blur: 1.6 };
  add({ t0: 0, ...HOOKCAM });
  add({ t0: 1.7, k: "path", P: [[0, 2.2, 11], [0, 2.0, 9.5]], T: [[0, 0.9, -1.5], [0, 0.9, -1.5]], fov: [52, 50], blur: 1.2 });
  add({ t0: s("s2") + 0.05, whip: true, k: "path", P: [[-6.5, 1.5, 6.5], [1.5, 1.5, 6.5]], T: [[-6, 1.1, -2], [1.5, 1.1, -2]], fov: [50, 50], blur: 1.2, ease: "l" });
  add({ t0: c("s2.neuer") - 0.1, blend: 0.3, k: "path", P: [[-6.6, 1.3, 3.2], [-6.8, 1.2, 2.8]], T: [[-7, 0.9, 0], [-7, 0.9, 0]], fov: [46, 42], blur: 1.6 });
  add({ t0: c("s2.mus") - 0.1, blend: 0.3, k: "path", P: [[-0.5, 1.4, 4.6], [0.4, 1.4, 4.4]], T: [[0, 0.9, 0], [0.6, 0.9, 0]], fov: [50, 48], blur: 1.4 });
  add({ t0: s("s3") + 0.05, whip: true, k: "path", P: [[-6, 1.6, 6], [2, 1.6, 6.5]], T: [[-4, 1.2, -1], [3, 1.2, -1]], fov: [52, 52], blur: 1.2, ease: "l" });
  add({ t0: c("s3.mgr") - 0.05, blend: 0.3, k: "path", P: [[4.6, 1.6, 8.2], [4.4, 1.6, 7.8]], T: [[3.0, 1.4, 5.2], [3.0, 1.4, 5.2]], fov: [44, 40], blur: 1.8 });
  add({ t0: s("s4") + 0.05, whip: true, k: "path", P: [[0, 5.5, 17], [0, 4.6, 15]], T: [[0, 0, -1], [0, 0.2, -1]], fov: [54, 52], blur: 0.8 });
  add({ t0: s("s5") + 0.05, whip: true, k: "path", P: [[1.0, 1.4, 9.5], [-0.5, 1.4, 9.0]], T: [[0.5, 0.8, 2.5], [-1.5, 0.8, 3.5]], fov: [50, 48], blur: 1.2 });
  add({ t0: s("s6") + 0.05, whip: true, k: "follow", who: "MUS", off: [[-0.5, 1.4, 5.6], [-0.8, 1.4, 5.2]], look: [1.5, 0.9, -0.5], fov: [50, 50], blur: 1.4 });
  add({ t0: G1 - 0.3, blend: 0.25, k: "path", P: [[48.5, 1.2, 6.0], [49.0, 1.3, 5.6]], T: [[53, 0.8, -0.5], [53, 0.9, -0.5]], fov: [50, 46], blur: 1.2 });
  add({ t0: s("s7") + 0.05, whip: true, k: "path", P: [[0, 1.6, 4.6], [0, 1.6, 4.0]], T: [[0, 1.6, 0], [0, 1.65, 0]], fov: [48, 44], blur: 2.0 });
  add({ t0: s("s8") + 0.05, whip: true, k: "path", P: [[-36.6, 1.6, 1.0], [-37.0, 1.6, 0.95]], T: [[-50, 1.0, -0.2], [-50, 1.0, -0.2]], fov: [46, 42], blur: 1.4 });
  add({ t0: c("s8.dive") - 0.05, blend: 0.3, ...HOOKCAM });
  add({ t0: s("s9") + 0.05, whip: true, k: "path", P: [[-1.5, 4.2, 10.5], [-1.5, 3.8, 9.5]], T: [[-1.5, 0.3, 0], [-1.5, 0.3, 0]], fov: [52, 50], blur: 0.8 });
  add({ t0: s("s10") + 0.05, whip: true, k: "follow", who: "DAV", off: [[-3.0, 1.6, 6.0], [-3.0, 1.6, 5.6]], look: [1.0, 0.9, -1.0], fov: [52, 52], blur: 1.2 });
  add({ t0: G2 - 0.35, blend: 0.25, k: "path", P: [[47.5, 1.3, 7.5], [48, 1.4, 7]], T: [[53, 0.9, 0.5], [53, 1.0, 0.5]], fov: [50, 46], blur: 1.2 });
  add({ t0: s("s11") + 0.05, whip: true, k: "path", P: [[-40.6, 1.3, 3.6], [-41.0, 1.3, 3.4]], T: [[-50, 1.0, 1.0], [-50, 1.0, 1.0]], fov: [50, 46], blur: 1.4 });
  add({ t0: c("s11.loop") - 0.12, blend: 0.12, whip: true, ...HOOKCAM });
  sh.forEach((x, i) => { x.t1 = x.t1 ?? (sh[i + 1] ? sh[i + 1].t0 : END); });
  sh[sh.length - 1].t1 = END;

  // ---------------- overlays ----------------
  const chip = (id, t0, t1, kk, v, x, y, cls = "", from = "right") => ({ id, t0, t1, from, cls: "chip " + cls, style: `left:${x}px;top:${y}px`,
    html: `<div class="ck">${kk}</div><div class="cv">${v}</div>` });
  const slam = (id, t0, t1, html, top, size = 96) => ({ id, t0, t1, slam: true, cls: "slam", style: `top:${top}px;font-size:${size}px`, html });
  const lower = (id, t0, who, min, y = 560, t1 = t0 + 1.4) => chip(id, t0, t1, "GOAL · " + min, who, 60, y, "dark", "left");
  const overlays = [
    slam("sl-a", -1, s("s2") - 0.05, "BAYERN'S INJURY LIST<br><b>vs.</b> MAN UNITED", 330, 86),
    chip("c-inj", c("s2.nine"), c("s2.neuer") - 0.05, "BAYERN", "INJURED: 9", 100, 420, "red"),
    chip("c-neu", c("s2.neuer"), c("s2.mus") - 0.05, "NEUER", "TORN TENDON", 100, 420, "dark"),
    chip("c-mus", c("s2.mus"), s("s3") - 0.05, "MUSIALA · GNABRY · DAVIES", "MUSCLE PROBLEMS", 60, 420, "dark"),
    chip("c-utd", c("s3.nine"), c("s3.mgr") - 0.05, "MAN UNITED · LAST 9 GAMES", "WINS: 0", 80, 420, "red"),
    chip("c-mgr", c("s3.mgr") + 0.2, s("s4") - 0.05, "NEW MANAGER", "FIRST DAY", 100, 420, "gold"),
    chip("c-1192", c("s4.count"), s("s5") - 0.05, "PLAYERS", "11 vs 9", 140, 420, "gold"),
    chip("c-slow", c("s6.slow"), G1 - 0.1, "MUSIALA", "SLOW-MO 0.5×", 100, 420, "dark"),
    lower("g1", G1 + 0.3, "Musiala (on one crutch)", "23'", 560, s("s7") - 0.05),
    chip("c-save", SAVE + 0.15, s("s9") - 0.05, "PENALTY", "SAVED (CRUTCH)", 80, 420, "gold"),
    chip("c-phy", c("s9.physio"), s("s10") - 0.05, "PHYSIOS: 1", "PATIENTS: 9", 100, 420, "red"),
    chip("c-dav", c("s10.faster"), G2 - 0.2, "DAVIES · ON ONE LEG", "STILL FASTER", 60, 420, "gold"),
    lower("g2", G2 + 0.3, "Davies (one leg)", "90'"),
    chip("c-who", c("s11.who"), LOOPJ, "COMMENT", "Who wins the rematch?", 60, 460, "red"),
    { id: "hud", t0: c("s4.ko") - 0.1, t1: LOOPJ, cls: "hud", style: "opacity:0",
      html: `<span class="t">FCB</span><span class="sc"><b id="hs">0</b>–<b id="as">0</b></span><span class="t">MUN</span><span class="mn" id="mn">1'</span>` },
    slam("sl-end", END - 0.3, END + 1, "BAYERN'S INJURY LIST<br><b>vs.</b> MAN UNITED", 330, 86),
  ];
  const bubbles = [
    { who: "NEU", t0: c("s2.neuer") + 0.3, t1: c("s2.mus") - 0.1, text: "I'M FINE.", cls: "small" },
    { who: "MGR", t0: c("s3.mgr") + 0.4, t1: s("s4") - 0.1, text: "WHO IS NO. 9?", cls: "small" },
    { who: "U10", t0: c("s4.count") + 0.1, t1: s("s5") - 0.1, text: "...8, 9?", cls: "mun small" },
    { who: "MUS", t0: c("s5.bay") + 0.3, t1: s("s6") - 0.1, text: "THANKS!", cls: "fcb small" },
    { who: "REF", t0: c("s7.follow") + 0.05, t1: c("s7.q") - 0.05, text: "♥ LIKE + FOLLOW +", cls: "red follow" },
    { who: "MUS", t0: c("s7.q"), t1: s("s8") - 0.1, text: "BAYERN?", cls: "fcb" },
    { who: "U7", t0: c("s7.q") + 0.3, t1: s("s8") - 0.1, text: "UNITED?", cls: "mun" },
    { who: "NEU", t0: c("s8.dive") + 0.2, t1: c("s8.crutch") - 0.1, text: "CAN'T DIVE.", cls: "small" },
    { who: "PHY", t0: c("s9.physio") + 0.2, t1: s("s10") - 0.1, text: "ICE! ICE! ICE!", cls: "small" },
    { who: "DAV", t0: c("s10.davies") + 0.3, t1: c("s10.faster") - 0.1, text: "BOING BOING", cls: "fcb small" },
  ];
  const bursts = [{ who: "NEU", t: HK, text: "CLANG!" }, { who: "NEU", t: SAVE, text: "CLANG!" }];
  const minute = (t) => (t >= c("s10.min") ? "90'" : t >= s("s9") ? "45'" : t >= s("s8") ? "38'" : t >= s("s6") ? "23'" : "1'");

  return {
    actors: A, ball, shots: sh, overlays, bubbles, bursts, props,
    grade: "contrast(1.12) saturate(1.2) brightness(0.96)",
    nets: { right: [G1, G2], left: [] }, shake: [HK, G1, SAVE, G2],
    crowd: (t) => ([G1, G2, SAVE].some((g) => t > g && t < g + 2.2) ? 0.5 : 0.12),
    flashes: (t) => ([G1, G2].some((g) => t > g && t < g + 2) ? 0.3 : 0.06),
    speedlines: (t) => Math.max(0.5 * (1 - sstep(1.5, 1.8, t)) * sstep(HK - 0.2, HK, t), 0.5 * sstep(END - 0.35, END - 0.2, t),
      0.35 * sstep(R0, R0 + 0.2, t) * (1 - sstep(R1, R1 + 0.3, t))),
    custom: (t, { el }) => {
      el("hs").textContent = String(t >= G2 ? 2 : t >= G1 ? 1 : 0);
      el("as").textContent = "0";
      el("mn").textContent = minute(t);
      let pop = 0; for (const gg of [G1, G2]) if (t >= gg && t < gg + 0.3) pop = Math.sin(((t - gg) / 0.3) * Math.PI);
      el("hud").style.transform = `scale(${1 + pop * 0.15})`;
    },
  };
}
