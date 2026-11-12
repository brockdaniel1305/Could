// S2E11 "Could Kevin De Bruyne find the Fortnite pirate token?" - short satire on our own cartoon pirate island (no game assets).
// Thread: everyone opens chest after chest for nothing; De Bruyne "sees what nobody sees", finds the token in the first chest -
// and passes it to a random teammate. Another assist. -> "Comment: would you pass it?"
import { path, sstep, clamp, lerp } from "./engine.js";
import { buildIsland } from "./island3d.js";

export default function plot(T) {
  const c = (k) => { if (!(k in T.cue)) throw new Error("cue " + k); return T.cue[k]; };
  const s = (k) => T.start[k];
  const END = T.duration, CUT = 1.3, LOOPJ = c("s8.loop") - 0.5;
  const CH = [2.4, -0.4], KPOS = [1.25, 0.45], TPOS = [9, -4.5], OPOS = [-7, -6], OCH = [-7.9, -6.9];
  const OPEN = c("s4.there") - 0.05, KICK = c("s6.then") + 0.8, CATCH = c("s6.rand") + 0.05;

  const W = { K: [], T: [], O: [] };
  const at = (n, t, x, z, e) => W[n].push([t, x, z, e]);
  at("K", 0, 0.6, 0.6); at("K", c("s4.first") - 0.1, 0.6, 0.6); at("K", OPEN - 0.25, KPOS[0], KPOS[1], "s");
  at("K", c("s8.who") + 0.2, KPOS[0], KPOS[1]); at("K", LOOPJ - 0.05, 4.6, 3.8, "s"); at("K", LOOPJ, 0.6, 0.6, "j"); at("K", END, 0.6, 0.6);
  at("T", 0, 30, -30); at("T", s("s5") - 0.05, TPOS[0], TPOS[1], "j"); at("T", LOOPJ, 30, -30, "j"); at("T", END, 30, -30);
  at("O", 0, OPOS[0], OPOS[1]); at("O", END, OPOS[0], OPOS[1]);

  const evK = [["leap", -1.3, 2.6, 3.0], ["leap", END - 1.3, 2.6, 3.0], ["charge", KICK - 0.35, 0.35]];
  const evT = [["armsUp", CATCH - 0.15, 0.6], ["jump", s("s8") + 0.1, 0.4], ["jump", s("s8") + 0.6, 0.4], ["jump", s("s8") + 1.1, 0.4], ["armsUp", s("s8"), LOOPJ - s("s8")]];
  const evO = []; for (let k = 0; k < 8; k++) evO.push(["arms", 1.4 + k * 0.85, 0.35, 120]);                    // opens chest after chest
  const A = {
    K: { path: W.K, ev: evK, h: 1.81, unit: 360, stride: 1.9 },
    T: { path: W.T, ev: evT, h: 1.78, unit: 360, stride: 1.9 },
    O: { path: W.O, ev: evO, h: 1.76, unit: 360, stride: 1.9 },
  };
  A.K.look = (t) => (t >= c("s3.sees") && t < s("s4") ? 0.8 : 0);
  const kdy = (t) => { let d = 0; for (const t0 of [-1.3, END - 1.3]) if (t >= t0 && t < t0 + 2.6) d += Math.sin(clamp((t - t0) / 2.6, 0, 1) * Math.PI) * 3.0; return d; };

  // ---------------- props ----------------
  const PS = {}; const pos = (n, t) => { const p = (PS[n] = PS[n] || path(A[n].path))(t); return [p.x, p.z]; };
  const tokenAt = (t) => {
    if (t < OPEN + 0.1) return [CH[0], -5, CH[1]];
    if (t < c("s6.then") + 0.1) { const f = sstep(OPEN + 0.1, OPEN + 0.7, t); return [CH[0], lerp(0.5, 1.7, f) + Math.sin(t * 3) * 0.06, CH[1] + 0.1]; }
    if (t < KICK) { const f = sstep(c("s6.then") + 0.1, KICK - 0.05, t); return [lerp(CH[0], KPOS[0] + 0.45, f), lerp(1.7, 0.18, f), lerp(CH[1] + 0.1, KPOS[1] + 0.1, f)]; }
    if (t < CATCH) { const f = clamp((t - KICK) / (CATCH - KICK), 0, 1); return [lerp(KPOS[0] + 0.45, TPOS[0] + 0.1, f), lerp(0.18, 1.3, f) + Math.sin(f * Math.PI) * 2.6, lerp(KPOS[1] + 0.1, TPOS[1] + 0.2, f) + Math.sin(f * Math.PI) * -1.2]; }
    if (t < s("s8")) return [TPOS[0] + 0.32, 1.25, TPOS[1] + 0.2];
    const j = Math.abs(Math.sin((t - s("s8")) * 6.3)) * 0.35; return [TPOS[0], 2.15 + j, TPOS[1] + 0.15];
  };
  const props = {
    chute: { h: 1.1, unit: 340, only: [-1, END + 1], at: (t) => { if (t > CUT + 0.15 && t < LOOPJ) return [0, -50, 0]; const k = pos("K", t); return [k[0], kdy(t) + 0.95, k[1]]; } },
    chest: { h: 0.62, unit: 120, p: [CH[0], 0, CH[1]], only: [-1, OPEN] },
    chestopen: { h: 1.0, unit: 155, p: [CH[0], 0, CH[1]], only: [OPEN, LOOPJ] },
    token: { h: 0.42, unit: 120, only: [OPEN + 0.1, LOOPJ], at: tokenAt, rot: (t) => (t > KICK && t < CATCH ? (t - KICK) * 900 : Math.sin(t * 2) * 10) },
    ochest: { h: 0.62, unit: 120, p: [OCH[0], 0, OCH[1]] },
  };
  // the closed chest is also back for the loop
  props.chest2 = undefined; delete props.chest2;
  const chestOnly = props.chest.only; props.chest.only = [-1, OPEN]; void chestOnly;

  // ---------------- camera ----------------
  const sh = [], add = (o) => sh.push(o);
  const HOOKCAM = { k: "path", P: [[3.6, 0.85, 4.2], [3.5, 0.85, 4.1]], T: [[0.8, 3.6, 0.3], [0.8, 1.6, 0.3]], fov: [50, 48], roll: 3, blur: 2.0 };
  add({ t0: 0, ...HOOKCAM });
  add({ t0: CUT, whip: true, k: "path", P: [[15, 10, 21], [12, 8, 17]], T: [[0, 0.6, 0], [0, 0.6, 0]], fov: [52, 50], blur: 0.8 });
  add({ t0: s("s2") + 0.05, whip: true, k: "path", P: [[-4.2, 1.6, -1.0], [-4.6, 1.6, -1.6]], T: [[-7.6, 1.0, -6.4], [-7.6, 1.0, -6.4]], fov: [48, 46], blur: 2.0 });
  add({ t0: s("s3") + 0.05, whip: true, k: "path", P: [[0.75, 1.62, 3.6], [0.75, 1.62, 3.0]], T: [[0.6, 1.68, 0.6], [0.6, 1.7, 0.6]], fov: [42, 38], blur: 2.4 });
  add({ t0: c("s3.sees") + 0.9, blend: 0.4, k: "path", P: [[-1.6, 2.8, 3.6], [-1.4, 2.6, 3.2]], T: [[2.4, 0.5, -0.4], [2.4, 0.5, -0.4]], fov: [50, 48], blur: 1.6 });
  add({ t0: s("s4") + 0.05, whip: true, k: "path", P: [[4.8, 1.4, 3.8], [4.4, 1.35, 3.4]], T: [[1.9, 1.0, -0.2], [1.9, 1.1, -0.2]], fov: [48, 44], blur: 2.0 });
  add({ t0: s("s5") + 0.05, whip: true, k: "path", P: [[-3.6, 2.0, 5.2], [-3.2, 2.0, 4.8]], T: [[5.6, 1.1, -2.6], [5.6, 1.1, -2.6]], fov: [48, 46], blur: 1.6 });
  add({ t0: s("s6") + 0.05, whip: true, k: "path", P: [[-1.2, 1.4, 2.8], [-0.8, 1.5, 2.6]], T: [[8.5, 1.4, -4.2], [8.5, 1.6, -4.2]], fov: [48, 46], blur: 1.6 });
  add({ t0: CATCH - 0.15, blend: 0.25, k: "path", P: [[10.6, 1.6, -1.3], [10.4, 1.6, -1.6]], T: [[9, 1.5, -4.5], [9, 1.55, -4.5]], fov: [46, 42], blur: 2.0 });
  add({ t0: s("s7") + 0.05, whip: true, k: "path", P: [[1.7, 1.62, 3.4], [1.6, 1.62, 3.0]], T: [[1.25, 1.68, 0.45], [1.25, 1.7, 0.45]], fov: [42, 38], blur: 2.4 });
  add({ t0: s("s8") + 0.05, whip: true, k: "path", P: [[10.7, 1.8, -1.0], [10.5, 1.8, -1.4]], T: [[9, 1.9, -4.5], [9, 1.9, -4.5]], fov: [48, 44], blur: 2.0 });
  add({ t0: c("s8.loop") - 0.3, blend: 0.3, whip: true, ...HOOKCAM });
  sh.forEach((x, i) => { x.t1 = x.t1 ?? (sh[i + 1] ? sh[i + 1].t0 : END); });
  sh[sh.length - 1].t1 = END;

  // ---------------- overlays ----------------
  const chip = (id, t0, t1, kk, v, x, y, cls = "", from = "right") => ({ id, t0, t1, from, cls: "chip " + cls, style: `left:${x}px;top:${y}px`,
    html: `<div class="ck">${kk}</div><div class="cv">${v}</div>` });
  const slam = (id, t0, t1, html, top, size = 128) => ({ id, t0, t1, slam: true, cls: "slam", style: `top:${top}px;font-size:${size}px`, html });
  const VISION = '<svg width="1080" height="1920" viewBox="0 0 1080 1920">' +
    ['M140,1700 Q300,900 545,1000', 'M60,1500 Q380,760 545,1000', 'M300,1880 Q700,1400 545,1000', 'M900,1800 Q860,1200 545,1000'].map((d) => `<path d="${d}"/>`).join("") +
    '<circle cx="545" cy="1000" r="46" fill="none" stroke="#ffd23f" stroke-width="10"/></svg>';
  const overlays = [
    slam("sl-a", -1, s("s2") - 0.05, "COULD KDB FIND<br><b>THE PIRATE TOKEN?</b>", 330, 84),
    { id: "c-odds", t0: c("s2.say"), t1: s("s3") - 0.05, from: "right", cls: "chip red", style: "left:80px;top:1180px",
      html: '<div class="ck">CHESTS OPENED · TOKENS: 0</div><div class="cv"><span id="chn">0</span> / 700,000</div>' },
    { id: "vision", t0: c("s3.sees") + 1.0, t1: s("s4") - 0.05, cls: "vision", html: VISION },
    chip("c-found", c("s4.there") + 0.2, s("s5") - 0.05, "CHESTS OPENED: 1", "TOKENS: 1", 80, 400, "gold"),
    chip("c-ast", c("s7.assist"), s("s8") - 0.05, "KEVIN DE BRUYNE", "ASSISTS +1", 120, 1180, "gold"),
    chip("c-who", c("s8.who"), LOOPJ, "COMMENT", "Would you pass it?", 100, 1180, "red"),
    slam("sl-end", END - 0.3, END + 1, "COULD KDB FIND<br><b>THE PIRATE TOKEN?</b>", 330, 84),
  ];
  const bubbles = [
    { who: "O", t0: c("s2.odds") + 0.3, t1: s("s3") - 0.1, text: "WOOD. AGAIN.", cls: "dark" },
    { who: "K", t0: c("s3.sees") + 0.1, t1: c("s3.sees") + 0.9, text: "👀", cls: "" },
    { who: "T", t0: c("s5.follow") + 0.05, t1: s("s6") - 0.1, text: "♥ LIKE + FOLLOW +", cls: "red follow" },
    { who: "T", t0: CATCH + 0.15, t1: s("s7") - 0.05, text: "WHO ARE YOU?", cls: "" },
    { who: "K", t0: c("s7.course") + 0.1, t1: s("s8") - 0.1, text: "👍", cls: "" },
  ];
  const bursts = [{ who: "K", t: KICK, text: "PING!" }];

  return {
    actors: A, shots: sh, overlays, bubbles, bursts, props, buildWorld: buildIsland,
    grade: "contrast(1.08) saturate(1.15) brightness(1.0)",
    custom: (t, { el }) => {
      el("chn").textContent = Math.round(1284 * sstep(c("s2.say"), s("s3") - 0.2, t)).toLocaleString("en-US");
    },
  };
}
