// COULD? POV series engine: one continuous first-person shot rendered with three.js, a pure function of time t (HyperFrames hf-seek).
// The episode director (assets/pov/director.js) builds the set and returns:
//   { build(THREE, scene, cam) -> state, update(t, state), head: [[t, yaw, pitch, roll, x, y, z], ...] (degrees / metres, world),
//     shake(t) -> amplitude, hands(t) -> {L:{...}, R:{...}}, fx(t) -> {red, black, blur, dim, tint}, fov(t) }
// Captions (speaker tag + karaoke words) and the end card are DOM overlays driven by window.__POV (pov_timing.json + pov.json).
import * as THREE from "./three.module.min.js";

const clamp = (x, a, b) => Math.max(a, Math.min(b, x));
const sstep = (a, b, x) => { const f = clamp((x - a) / (b - a), 0, 1); return f * f * (3 - 2 * f); };
const lerp = (a, b, f) => a + (b - a) * f;
const D = Math.PI / 180;
// smooth 1D noise (sum of sines) for handheld sway and shake
const noise = (t, s) => Math.sin(t * 1.7 + s) * 0.5 + Math.sin(t * 3.1 + s * 2.3) * 0.3 + Math.sin(t * 7.3 + s * 0.7) * 0.2;

export function keyed(keys) {
  // keys: [[t, ...values]] -> f(t) = smooth (ease in-out) interpolation between keys, holding at the ends
  return (t) => {
    if (t <= keys[0][0]) return keys[0].slice(1);
    for (let i = 0; i < keys.length - 1; i++) {
      const a = keys[i], b = keys[i + 1];
      if (t <= b[0]) { const f = sstep(a[0], b[0], t); return a.slice(1).map((v, j) => lerp(v, b[j + 1], f)); }
    }
    return keys[keys.length - 1].slice(1);
  };
}

export function createPOV(plot, T) {
  const W = 1080, Hh = 1920;
  const canvas = document.getElementById("pov-gl");
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(1); renderer.setSize(W, Hh, false);
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  const scene = new THREE.Scene();
  const cam = new THREE.PerspectiveCamera(72, W / Hh, 0.03, 2500);
  cam.rotation.order = "YXZ"; scene.add(cam);
  const st = plot.build(THREE, scene, cam);
  const head = keyed(plot.head);

  // ---------------- captions ----------------
  const capBox = document.getElementById("pov-cap"), capTag = document.getElementById("pov-tag"), capTxt = document.getElementById("pov-txt");
  const lines = T.lines, spk = T.speakers || {};
  let lastLine = null;
  function captions(t) {
    // the line on screen: the one being spoken (held 0.35 s after it ends)
    let L = null;
    for (const l of lines) if (t >= l.t0 - 0.05 && t <= l.t0 + l.dur + 0.35) L = l;
    if (!L) { capBox.style.opacity = "0"; return; }
    if (L !== lastLine) {
      lastLine = L; const s = spk[L.who] || {};
      capTag.textContent = s.tag || ""; capTag.style.display = s.tag ? "inline-block" : "none";
      capTxt.innerHTML = L.words.map((w, i) => `<span id="pw${i}">${w[0].replace(/&/g, "&amp;").replace(/</g, "&lt;")}</span>`).join(" ");
      capTxt.style.color = s.color || "#fff"; capBox.className = L.who === "YOU" ? "inner" : "";
    }
    const k = sstep(L.t0 - 0.05, L.t0 + 0.1, t) * (1 - sstep(L.t0 + L.dur + 0.15, L.t0 + L.dur + 0.35, t));
    capBox.style.opacity = String(k);
    capBox.style.transform = `translateY(${((1 - sstep(L.t0 - 0.05, L.t0 + 0.12, t)) * 14).toFixed(1)}px)`;
    L.words.forEach((w, i) => { const e = document.getElementById("pw" + i); if (e) e.className = t >= w[1] - 0.04 ? "on" : ""; });
  }
  // lip sync helper for the director: mouth opening of a speaker at t (0..1)
  const mouthOf = (who, t) => { for (const l of lines) if (l.who === who && t >= l.t0 && t < l.t0 + l.dur) {
    const i = Math.floor((t - l.t0) * 30), e = l.env[i] || 0, e2 = l.env[i + 1] ?? e; return lerp(e, e2, (t - l.t0) * 30 - i); } return 0; };
  const speaking = (who, t) => lines.some((l) => l.who === who && t >= l.t0 && t < l.t0 + l.dur);
  st.mouthOf = mouthOf; st.speaking = speaking;

  // ---------------- full-screen effects ----------------
  const red = document.getElementById("pov-red"), black = document.getElementById("pov-black"), dim = document.getElementById("pov-dim");
  const endCard = plot.endCard ? plot.endCard(document) : null;

  function renderAt(t) {
    plot.update(t, st);
    // head: keyed pose + breathing sway + shake
    const [yaw, pitch, roll, x, y, z] = head(t);
    const sh = plot.shake ? plot.shake(t) : 0;
    const sway = 0.35;   // degrees of handheld/breathing motion, always on: the shot never freezes
    cam.position.set(x + noise(t * 9, 1) * 0.012 * sh, y + Math.sin(t * 1.6) * 0.004 + noise(t * 11, 2) * 0.016 * sh, z + noise(t * 8, 3) * 0.01 * sh);
    cam.rotation.set((pitch + noise(t, 4) * sway + noise(t * 10, 5) * 2.2 * sh) * D, (yaw + noise(t * 0.8, 6) * sway + noise(t * 9, 7) * 2.0 * sh) * D,
                     (roll + noise(t * 0.6, 8) * sway * 0.6 + noise(t * 7, 9) * 1.8 * sh) * D);
    cam.fov = plot.fov ? plot.fov(t) : 72; cam.updateProjectionMatrix();
    if (plot.afterCam) plot.afterCam(t, st, cam);
    renderer.render(scene, cam);
    const f = plot.fx ? plot.fx(t) : {};
    red.style.opacity = String(f.red || 0); black.style.opacity = String(f.black || 0); dim.style.opacity = String(f.dim || 0);
    canvas.style.filter = `blur(${(f.blur || 0).toFixed(2)}px) saturate(${(f.sat ?? 1).toFixed(2)}) brightness(${(f.bright ?? 1).toFixed(2)})`;
    captions(t);
    if (endCard) endCard(t);
  }
  return { renderAt };
}
export { sstep, lerp, clamp, noise };
