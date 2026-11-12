// S2E10 "Could 11 Ronaldinhos beat 11 Zidanes?" - flair vs elegance as a Clásico: prime Ronaldinho (Barça 2005) vs prime Zidane (Real 2002).
// Thread: Ronaldinho always smiles. All eleven Zidanes do the roulette at once and get dizzy, the Ronaldinhos juggle instead of
// defending, Zidane's Glasgow volley (0-1); no-look pass - every Zidane runs the wrong way - and a toe-poke (1-1); minute 90 elastico
// past all eleven (2-1) ... and the Zidanes applaud, like the Bernabéu in 2005 -> comments decide.
// Ronaldinhos attack +x (Zidane goal at x = 52.5), Zidanes attack -x (Ronaldinho goal at x = -52.5).
import { path, sstep, clamp, lerp } from "./engine.js";

export default function plot(T) {
  const c = (k) => { if (!(k in T.cue)) throw new Error("cue " + k); return T.cue[k]; };
  const s = (k) => T.start[k];
  const END = T.duration, CUT = 1.3, LOOPJ = c("s11.loop") - 0.5;

  const VOL = c("s6.nil") - 0.6, G1 = c("s6.nil") - 0.1;                                          // Glasgow volley, 0-1
  const PASS = c("s8.pass") + 0.05, RECV = c("s8.pass") + 0.6, TOE = c("s8.eq") - 0.55, G2 = c("s8.eq") - 0.1;   // no-look + toe-poke, 1-1
  const RUN0 = c("s9.ela") + 0.1, RUN1 = c("s9.win") - 0.5, G3 = c("s9.win") - 0.1;               // elastico past all eleven, 2-1

  const W = {}, names = [];
  for (let i = 0; i < 11; i++) names.push("D" + i, "Z" + i);
  names.push("REF");
  names.forEach((n) => (W[n] = []));
  const at = (n, t, x, z, e) => W[n].push([t, x, z, e]);
  const idx = (n) => (n === "REF" ? -1 : +n.slice(1));
  const jumpAll = (t, f) => names.forEach((n) => { const p = f(n, idx(n), n[0] === "D"); if (p) at(n, t, p[0], p[1], "j"); });
  const LZ = (i) => -9 + i * 1.8;
  const ROWS = (i, side) => [side * (1.9 + (i % 5) * 1.35), -3.2 - (i > 5 ? 1.7 : 0) - (i % 2) * 0.3];
  const ROW = (k) => [-4.4 - 1.5 * k, 5.5 - 0.12 * k];                                            // diagonal row facing the camera

  // hook: Ronaldinho D10 juggling, grinning; Zidane Z5 spinning behind him
  const HOOKPOS = (n, i, dd) => (n === "D10" ? [-3.3, 0.2] : n === "Z5" ? [-7.4, -1.2] : n === "REF" ? [-14, 10] :
    dd ? [-16 - i * 1.4, (i % 2 ? 1 : -1) * (5 + i)] : [-22 - i * 1.3, (i % 2 ? -1 : 1) * (4 + i)]);
  names.forEach((n) => { const [x, z] = HOOKPOS(n, idx(n), n[0] === "D"); at(n, 0, x, z); });
  jumpAll(CUT + 0.01, (n, i, dd) => (n === "REF" ? [0, -9.5] : [dd ? -1.6 : 1.6, LZ(i)]));
  // s2 / s3: line-ups
  jumpAll(s("s2") - 0.05, (n, i, dd) => (n === "D10" ? [-0.95, 0] : n === "Z5" ? [0.95, 0.05] : n === "REF" ? [0, -2.4] :
    dd ? ROWS(i === 10 ? 5 : i, -1) : ROWS(i === 5 ? 10 : i, 1)));
  // s4: all eleven Zidanes in one diagonal row, each spinning on the spot (the roulette)
  const ZORD = ["Z5", "Z1", "Z2", "Z3", "Z4", "Z6", "Z7", "Z8", "Z9", "Z10", "Z0"];
  jumpAll(s("s4") - 0.05, (n, i, dd) => (ZORD.includes(n) ? ROW(ZORD.indexOf(n)) : n === "REF" ? [-8, 2] : dd ? [-30 - i, 10 + i] : null));
  // s5: the Ronaldinhos juggling in their own half, the dizzy Zidanes wander past
  const JUG = (i) => [-12 + (i % 4) * 1.6 - (i > 4 ? 0.8 : 0), -1.8 + Math.floor((i - 1) / 4) * 1.9];
  jumpAll(s("s5") - 0.05, (n, i, dd) => (dd && i >= 1 ? JUG(i) : n === "D0" ? [-51.6, 0] : n === "REF" ? [-4, 9] : !dd ? [-4 - (i % 4) * 2.2, -9 - (i % 3) * 1.6] : null));
  // s6: Zidane's volley - cross from the right, Z5 on the edge of the box
  jumpAll(s("s6") - 0.05, (n, i, dd) => (n === "Z5" ? [-40.6, 2.2] : n === "Z3" ? [-46, 24] : n === "D0" ? [-51.6, 0] : n === "Z0" ? [51.6, 0] : n === "REF" ? [-34, -10] :
    dd ? [-46 + (i % 4) * 2.2, ((i % 3) - 1) * 6] : [-36 + (i % 4) * 2.6, (i % 2 ? 1 : -1) * (7 + i * 0.6)]));
  // s7: face to face
  jumpAll(s("s7") - 0.3, (n, i, dd) => (n === "D10" ? [-0.7, 0] : n === "Z5" ? [0.7, 0] : n === "REF" ? [0, -3] : dd ? [-6 - i, (i % 2 ? 1 : -1) * (5 + i)] : [6 + i, (i % 2 ? 1 : -1) * (5 + i)]));
  // s8: no-look pass - Ronaldinho stares left, the Zidanes all run left, the pass goes right to D7, toe-poke
  jumpAll(s("s8") - 0.05, (n, i, dd) => (n === "D10" ? [12, 0] : n === "D7" ? [24, -7] : n === "Z0" ? [51.6, 0] : n === "D0" ? [-51.6, 0] : n === "REF" ? [6, -10] :
    !dd ? [15 + (i % 4) * 2.4, -2.5 + ((i % 3) - 1) * 2.6] : [2 + (i % 4) * 3, ((i % 3) - 1) * 10]));
  names.filter((n) => n[0] === "Z" && n !== "Z0").forEach((n) => { const i = idx(n); at(n, c("s8.look") + 0.2, 15 + (i % 4) * 2.4, -2.5 + ((i % 3) - 1) * 2.6);
    at(n, PASS + 0.3, 16 + (i % 4) * 2.4, 9 + ((i % 3) - 1) * 2.6, "s"); });
  at("D7", RECV - 0.2, 24, -7); at("D7", TOE - 0.1, 37.4, -3.2, "i"); at("D7", G2 + 0.8, 39, -1, "o");
  // s9: minute 90 - elastico past all eleven Zidanes, lined up across his way
  const LANE = [6, 9.5, 13, 16.5, 20, 23.5, 27, 30.5, 34, 37.5];
  const LANEZ = ["Z1", "Z2", "Z3", "Z4", "Z5", "Z6", "Z7", "Z8", "Z9", "Z10"];
  jumpAll(s("s9") - 0.05, (n, i, dd) => (n === "D10" ? [1.2, 0] : n === "Z0" ? [51.8, 0] : n === "D0" ? [-51.6, 0] : n === "REF" ? [-4, 9] :
    !dd ? [LANE[LANEZ.indexOf(n)], (i % 2 ? 1 : -1) * 0.7] : [-4 - (i % 4) * 3, ((i % 3) - 1) * 8]));
  at("D10", RUN0, 1.2, 0); at("D10", RUN1, 46.2, 0.15, "i"); at("D10", G3 + 0.9, 48, 3, "o");
  const PASSAT = (x) => RUN0 + ((x - 1.2) / 45) * (RUN1 - RUN0);
  // s10: the Zidanes applaud - diagonal row again, Ronaldinho in front grinning
  jumpAll(s("s10") - 0.05, (n, i, dd) => (ZORD.includes(n) ? ROW(ZORD.indexOf(n)) : n === "D10" ? [-1.4, 7.6] : n === "REF" ? [-6.4, 2.6] : dd ? [-30 - i, 12 + i] : null));
  // s11: Ronaldinho winks into the camera
  jumpAll(s("s11") - 0.05, (n, i, dd) => (n === "D10" ? [0, 0] : dd ? [-6 - i, -4 - (i % 3) * 2] : n === "REF" ? [-10, -8] : [6 + i, -4 - (i % 3) * 2]));
  // loop
  names.forEach((n) => { const [x, z] = HOOKPOS(n, idx(n), n[0] === "D"); at(n, LOOPJ, x, z, "j"); at(n, END, x, z, "l"); });
  for (const n of names) W[n].sort((p, q) => p[0] - q[0]);

  const A = {};
  for (const n of names) {
    const dd = n[0] === "D", i = idx(n), ev = [];
    if (n === "Z5") ev.push(["spin", 0.1, 1.0]);
    if (!dd && n !== "Z0") { ev.push(["spin", c("s4.roul") + 0.25 + (i % 3) * 0.05, 1.1], ["spin", c("s4.same") + 0.1, 0.9], ["dizzy", c("s4.same") + 0.9, s("s6") - c("s4.same") - 0.8]); }
    if (n === "Z0") ev.push(["spin", c("s4.roul") + 0.25, 1.1], ["dizzy", c("s4.same") + 0.9, 2.0]);
    if (dd && i >= 1) for (let k = 0; k < 6; k++) ev.push(["jump", c("s5.nodef") + 0.2 + k * 0.4 + (i % 3) * 0.12, 0.28]);   // keepy-ups
    if (n === "Z5") ev.push(["jump", VOL - 0.2, 0.4], ["armsUp", G1 + 0.1, 1.2]);
    if (n === "D0") ev.push(["dive", G1 - 0.2, 1, -1], ["up", G1 + 1.2]);
    if (n === "D7") ev.push(["charge", TOE - 0.6, 0.6], ["armsUp", G2 + 0.15, 1.1]);
    if (n === "Z0") ev.push(["dive", G2 - 0.15, 1, 1], ["up", G2 + 1.2]);
    if (LANEZ.includes(n)) ev.push(["spin", PASSAT(LANE[LANEZ.indexOf(n)]) + 0.05, 0.6], ["fall", PASSAT(LANE[LANEZ.indexOf(n)]) + 0.4, 0, i % 2 ? 1 : -1], ["up", s("s10") - 0.1]);
    if (n === "D10") ev.push(["charge", RUN0, RUN1 - RUN0], ["armsUp", G3 + 0.1, 1.3]);
    if (!dd) for (let k = 0; k < 10; k++) ev.push(["arms", c("s10.clap") + 0.05 + k * 0.34 + (i % 2) * 0.05, 0.17, 70]);         // applause
    A[n] = { path: W[n], ev, h: dd ? 1.82 : 1.85, unit: 360, stride: dd ? 1.9 : 2.0 };
  }
  A.D10.look = (t) => (t >= c("s8.look") && t < PASS + 0.2 ? -1 : t >= PASS + 0.2 && t < RECV ? 1 : 0);

  // ---------------- ball ----------------
  const ball = [
    { t0: 0, k: "juggle", who: "D10" },
    { t0: CUT + 0.01, k: "rest", p: [0, 0, 0.6] },
    { t0: s("s2") - 0.05, k: "rest", p: [0, -50, 0] },
    { t0: s("s4") - 0.05, k: "at", who: "Z5", dx: 0.5, dz: 0.1 },
    { t0: s("s5") - 0.05, k: "juggle", who: "D5" },
    { t0: s("s6") - 0.05, k: "rest", p: [-46, 0, 23.6] },
    { t0: c("s6.vol") - 0.2, t1: VOL, k: "fly", a: [-46, 0, 23.6], b: [-40.9, 1.0, 2.3], h: 6 },
    { t0: VOL, t1: G1, k: "fly", a: [-40.9, 1.0, 2.3], b: [-52.7, 2.2, -3.0], h: 0.3 },
    { t0: G1, k: "rest", p: [-53.2, 0.1, -3.0] },
    { t0: s("s7") - 0.3, k: "rest", p: [0, 0, 0.3] },
    { t0: s("s8") - 0.05, k: "at", who: "D10", dx: 0.5, dz: 0.1 },
    { t0: PASS, t1: RECV, k: "fly", a: [12.5, 0, 0.1], b: [24.4, 0, -6.9], h: 0.05 },
    { t0: RECV, k: "at", who: "D7", dx: 0.5, dz: 0.1 },
    { t0: TOE, t1: G2, k: "fly", a: [37.9, 0, -3.1], b: [52.8, 0.4, 2.4], h: 0.1 },
    { t0: G2, k: "rest", p: [53.2, 0.1, 2.4] },
    { t0: s("s9") - 0.05, k: "at", who: "D10", dx: 0.5, dz: 0.1 },
    { t0: RUN1, t1: G3, k: "fly", a: [46.7, 0, 0.15], b: [52.8, 1.4, -2.6], h: 0.4, curve: -0.4 },
    { t0: G3, k: "rest", p: [53.2, 0.1, -2.6] },
    { t0: s("s10") - 0.05, k: "rest", p: [0, -50, 0] },
    { t0: s("s11") - 0.05, k: "juggle", who: "D10" },
  ];

  // ---------------- camera ----------------
  const sh = [], add = (o) => sh.push(o);
  const HOOKCAM = { k: "path", P: [[0.6, 1.25, 1.2], [0.6, 1.25, 1.0]], T: [[-5, 1.35, -0.2], [-5, 1.35, -0.2]], fov: [48, 46], roll: 4, blur: 2.2 };
  add({ t0: 0, ...HOOKCAM });
  add({ t0: CUT, k: "path", P: [[0, 1.2, 12], [0, 1.25, 11]], T: [[0, 1.7, 0], [0, 1.7, 0]], fov: [50, 46], blur: 1.4 });
  add({ t0: s("s2") + 0.05, whip: true, k: "path", P: [[-1.6, 1.6, 6.4], [-1.4, 1.6, 5.8]], T: [[-1.4, 1.75, 0], [-1.3, 1.75, 0]], fov: [44, 42], blur: 2.2 });
  add({ t0: c("s2.smile") - 0.05, blend: 0.35, k: "path", P: [[-0.95, 1.62, 3.4], [-0.95, 1.62, 2.8]], T: [[-0.95, 1.68, 0], [-0.95, 1.7, 0]], fov: [42, 38], blur: 2.4 });
  add({ t0: s("s3") + 0.05, whip: true, k: "path", P: [[1.6, 1.7, 6.4], [1.4, 1.7, 5.8]], T: [[1.4, 1.85, 0], [1.3, 1.85, 0]], fov: [44, 42], blur: 2.2 });
  add({ t0: s("s4") + 0.05, whip: true, k: "path", P: [[0.4, 1.7, 9.0], [0.0, 1.65, 8.4]], T: [[-5.6, 1.5, 5.2], [-5.6, 1.5, 5.2]], fov: [48, 46], blur: 1.8 });
  add({ t0: s("s5") + 0.05, whip: true, k: "path", P: [[-7.4, 1.6, 5.4], [-7.8, 1.6, 4.8]], T: [[-10.4, 1.2, -0.4], [-10.4, 1.2, -0.4]], fov: [50, 46], blur: 2.0 });
  add({ t0: s("s6") + 0.05, whip: true, k: "path", P: [[-36.4, 0.9, 6.4], [-36.8, 0.9, 6.0]], T: [[-41.5, 1.4, 1.4], [-42, 1.5, 1.2]], fov: [50, 48], blur: 1.8 });
  add({ t0: VOL + 0.05, blend: 0.25, k: "path", P: [[-46.5, 1.6, -9.5], [-47.5, 1.8, -9]], T: [[-53, 1.8, -2], [-52.5, 1.8, -2]], fov: [48, 44], blur: 1.4 });
  add({ t0: s("s7") + 0.05, blend: 0.4, whip: true, k: "path", P: [[0, 1.55, 5.2], [0, 1.6, 4.4]], T: [[0, 1.65, 0], [0, 1.7, 0]], fov: [48, 42], blur: 2.4 });
  add({ t0: s("s8") + 0.05, whip: true, k: "path", P: [[12.4, 1.62, 3.4], [12.3, 1.62, 3.0]], T: [[12.0, 1.62, 0], [12.0, 1.64, 0]], fov: [42, 38], blur: 2.4 });
  add({ t0: c("s8.look") + 1.0, blend: 0.3, k: "path", P: [[8.2, 2.6, 8.4], [8.6, 2.8, 8.8]], T: [[16, 1.0, 1.0], [17, 1.0, 1.5]], fov: [52, 52], blur: 1.4 });
  add({ t0: RECV - 0.1, blend: 0.3, k: "follow", who: "D7", off: [[-4.2, 1.5, 4.6], [-4.4, 1.5, 4.2]], look: [3, 1.0, -0.4], fov: [50, 48], blur: 1.8 });
  add({ t0: TOE + 0.05, blend: 0.2, k: "path", P: [[46.5, 1.6, 8.5], [47.5, 1.8, 8]], T: [[53, 1.1, 1.0], [52.5, 1.3, 1.0]], fov: [48, 44], blur: 1.4 });
  add({ t0: s("s9") + 0.05, whip: true, k: "follow", who: "D10", off: [[0.8, 1.3, 5.6], [0.6, 1.3, 5.2]], look: [0.2, 1.0, 0], fov: [52, 52], blur: 1.8 });
  add({ t0: RUN1 - 0.05, blend: 0.25, k: "path", P: [[46.5, 1.6, -8.5], [47.5, 1.8, -8]], T: [[53, 1.4, -1.5], [52.5, 1.4, -1.5]], fov: [48, 44], blur: 1.4 });
  add({ t0: s("s10") + 0.05, whip: true, k: "path", P: [[1.6, 1.7, 10.6], [1.2, 1.65, 10.0]], T: [[-5.6, 1.55, 5.2], [-5.6, 1.55, 5.2]], fov: [48, 44], blur: 1.8 });
  add({ t0: s("s11") + 0.05, whip: true, k: "path", P: [[0.1, 1.62, 3.2], [0.1, 1.62, 2.8]], T: [[0, 1.66, 0], [0, 1.68, 0]], fov: [42, 38], blur: 2.4 });
  add({ t0: c("s11.loop") - 0.3, blend: 0.3, whip: true, ...HOOKCAM });
  sh.forEach((x, i) => { x.t1 = x.t1 ?? (sh[i + 1] ? sh[i + 1].t0 : END); });
  sh[sh.length - 1].t1 = END;

  // ---------------- overlays ----------------
  const chip = (id, t0, t1, kk, v, x, y, cls = "", from = "right") => ({ id, t0, t1, from, cls: "chip " + cls, style: `left:${x}px;top:${y}px`,
    html: `<div class="ck">${kk}</div><div class="cv">${v}</div>` });
  const slam = (id, t0, t1, html, top, size = 128) => ({ id, t0, t1, slam: true, cls: "slam", style: `top:${top}px;font-size:${size}px`, html });
  const lower = (id, t0, who, min, y = 560) => chip(id, t0, t0 + 1.3, "GOAL · " + min, who, 60, y, "dark", "left");
  const overlays = [
    slam("sl-a", -1, s("s2") - 0.05, "11 RONALDINHOS<br><b>vs.</b> 11 ZIDANES", 340, 88),
    chip("c-bdo", c("s2.bdo"), s("s3") - 0.05, "PRIME RONALDINHO · 2005", "Ballon d'Or", 80, 400, "gold"),
    chip("c-z", c("s3.pz") + 0.3, s("s4") - 0.05, "PRIME ZIDANE · 2002", "Real Madrid", 80, 400, "dark"),
    { id: "c-keep", t0: c("s5.jug"), t1: s("s6") - 0.05, from: "right", cls: "chip gold", style: "left:100px;top:400px",
      html: '<div class="ck">KEEPY-UPS</div><div class="cv" id="keepn">0</div>' },
    chip("c-glas", c("s6.vol") + 0.2, G1 + 0.2, "GLASGOW", "2002", 120, 400, "dark"),
    lower("g1", G1 + 0.3, "Zidane (volley)", "17'"),
    lower("g2", G2 + 0.3, "Ronaldinho (toe-poke)", "44'"),
    lower("g3", G3 + 0.3, "Ronaldinho (elastico)", "90'"),
    chip("c-ov", c("s10.mad"), s("s11") - 0.05, "BERNABÉU · 2005", "Standing ovation", 80, 400, "gold"),
    chip("c-who", c("s11.who"), LOOPJ, "COMMENT", "Who will win?", 120, 460, "red"),
    { id: "hud", t0: c("s4.ko") - 0.1, t1: LOOPJ, cls: "hud", style: "opacity:0",
      html: `<span class="t">DIN</span><span class="sc"><b id="hs">0</b>–<b id="as">0</b></span><span class="t">ZID</span><span class="mn" id="mn">1'</span>` },
    slam("sl-end", END - 0.3, END + 1, "11 RONALDINHOS<br><b>vs.</b> 11 ZIDANES", 340, 88),
  ];
  const bubbles = [
    { who: "D10", t0: c("s2.smile") + 0.1, t1: s("s3") - 0.1, text: "😁", cls: "" },
    { who: "Z5", t0: c("s3.eleg") + 0.1, t1: s("s4") - 0.1, text: "✨", cls: "" },
    { who: "Z5", t0: c("s4.same") + 1.0, t1: s("s5") - 0.1, text: "@#%?!", cls: "dark small" },
    { who: "D5", t0: c("s5.jug") + 0.1, t1: s("s6") - 0.1, text: "😁", cls: "" },
    { who: "REF", t0: c("s7.follow") + 0.05, t1: c("s7.q") - 0.05, text: "♥ LIKE + FOLLOW +", cls: "red follow" },
    { who: "D10", t0: c("s7.q"), t1: s("s8") - 0.1, text: "DINHO?", cls: "red" },
    { who: "Z5", t0: c("s7.q") + 0.3, t1: s("s8") - 0.1, text: "ZIZOU?", cls: "" },
    { who: "D10", t0: c("s8.look") + 0.1, t1: c("s8.look") + 0.5, text: "👀", cls: "" },
    { who: "Z3", t0: PASS + 0.4, t1: RECV + 0.3, text: "WRONG WAY!", cls: "dark small" },
    { who: "D10", t0: c("s10.clap") + 0.1, t1: s("s11") - 0.1, text: "😁", cls: "" },
    { who: "D10", t0: c("s11.who") - 0.4, t1: LOOPJ, text: "😉", cls: "" },
  ];
  const bursts = [{ who: "Z5", t: VOL, text: "BANG!" }, { who: "D7", t: TOE, text: "TOE!" }];
  const minute = (t) => t >= c("s9.min") ? "90'" : t >= s("s8") ? "44'" : t >= s("s6") ? "17'" : t >= s("s4") ? "2'" : "1'";

  return {
    actors: A, ball, shots: sh, overlays, bubbles, bursts,
    grade: "contrast(1.14) saturate(1.2) brightness(0.95)",
    nets: { left: [G1], right: [G2, G3] }, shake: [G1, G2, G3],
    crowd: (t) => [G1, G2, G3].some((g) => t > g && t < g + 2.4) ? 0.5 : t > c("s10.clap") && t < s("s11") ? 0.5 : 0.1,
    flashes: (t) => ([G1, G3].some((g) => t > g && t < g + 2) || (t > c("s10.clap") && t < s("s11")) ? 0.3 : 0.05),
    speedlines: (t) => Math.max(0.55 * (1 - sstep(CUT - 0.1, CUT + 0.1, t)), 0.55 * sstep(END - 0.35, END - 0.2, t),
      0.4 * sstep(RUN0, RUN0 + 0.2, t) * (1 - sstep(RUN1, RUN1 + 0.3, t))),
    custom: (t, { el }) => {
      el("keepn").textContent = String(Math.round(47 * sstep(c("s5.jug"), s("s6") - 0.3, t)));
      el("hs").textContent = String(t >= G3 ? 2 : t >= G2 ? 1 : 0);
      el("as").textContent = String(t >= G1 ? 1 : 0);
      el("mn").textContent = minute(t);
      let pop = 0; for (const gg of [G1, G2, G3]) if (t >= gg && t < gg + 0.3) pop = Math.sin(((t - gg) / 0.3) * Math.PI);
      el("hud").style.transform = `scale(${1 + pop * 0.15})`;
    },
  };
}
