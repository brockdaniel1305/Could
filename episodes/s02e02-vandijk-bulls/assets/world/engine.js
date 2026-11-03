// COULD? world engine: one continuous Three.js stadium, 2D SVG characters as billboards projected into it,
// a camera that moves through shots with blended transitions, and DOM overlays (HUD, slams, chips, boards).
// Everything is a pure function of time t (HyperFrames hf-seek), built from a "plot" object (see the episode's world/director.js).
import * as THREE from "../lib/three.module.min.js";
import { buildStadium } from "./stadium3d.js";

export const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
export const sstep = (a, b, t) => { const x = clamp((t - a) / (b - a), 0, 1); return x * x * (3 - 2 * x); };
export const lerp = (a, b, k) => a + (b - a) * k;
const EASE = { l: (f) => f, s: (f) => f * f * (3 - 2 * f), i: (f) => f * f, o: (f) => 1 - (1 - f) * (1 - f) };
// distance covered along an eased segment at fraction f (for the run cycle): len * ease(f)

// ---------------- paths ----------------
// waypoints [t, x, z, ease?] ; ease applies to the segment that ENDS at this waypoint. Same t twice = teleport.
export function path(wps) {
  // ease "j" = jump cut: hold the previous position until t, then appear at the new one
  const S = wps.map((w, i) => ({ t: w[0], x: w[1], z: w[2], j: w[3] === "j", e: EASE[w[3] === "j" ? "l" : w[3] || "s"], i })).sort((a, b) => a.t - b.t || a.i - b.i);
  const W = [];
  for (const w of S) { if (w.j && W.length) W.push({ ...W[W.length - 1], t: w.t }); W.push(w); }
  const lens = [0];
  for (let i = 1; i < W.length; i++) lens.push(lens[i - 1] + (W[i].t > W[i - 1].t ? Math.hypot(W[i].x - W[i - 1].x, W[i].z - W[i - 1].z) : 0));
  return (t) => {
    if (t <= W[0].t) return { x: W[0].x, z: W[0].z, d: 0 };
    for (let i = 1; i < W.length; i++) {
      if (t < W[i].t) {
        const a = W[i - 1], b = W[i], f = b.e((t - a.t) / (b.t - a.t));
        return { x: lerp(a.x, b.x, f), z: lerp(a.z, b.z, f), d: lens[i - 1] + (lens[i] - lens[i - 1]) * f };
      }
    }
    const L = W[W.length - 1]; return { x: L.x, z: L.z, d: lens[W.length - 1] };
  };
}

export function createWorld(plot) {
  const canvas = document.getElementById("w3-gl");
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
  renderer.setPixelRatio(1); renderer.setSize(1080, 1920, false); renderer.outputColorSpace = THREE.SRGBColorSpace;
  const scene = new THREE.Scene();
  // foreground pass: everything nearer than the closest character is drawn again on a second canvas ABOVE the 2D characters
  // (blurred), so fences, lanterns, flowers etc. frame and occlude them like real foreground objects
  const fgCanvas = document.getElementById("w3-fg");
  const fgR = fgCanvas && plot.foreground !== false ? new THREE.WebGLRenderer({ canvas: fgCanvas, antialias: true, alpha: true, preserveDrawingBuffer: true }) : null;
  if (fgR) { fgR.setPixelRatio(1); fgR.setSize(1080, 1920, false); fgR.outputColorSpace = THREE.SRGBColorSpace; fgR.setClearColor(0x000000, 0); }
  const cam = new THREE.PerspectiveCamera(58, 1080 / 1920, 0.1, 700);
  const st = (plot.buildWorld || buildStadium)(THREE, scene);

  // ---------------- actors ----------------
  const el = (id) => document.getElementById(id);
  const actors = {};
  for (const [name, a] of Object.entries(plot.actors)) {
    const node = el("w3-" + name);
    const rig = (p) => node.querySelector(`[id$="-${p}"]`);
    actors[name] = { ...a, name, node, pos: path(a.path), ev: a.ev || [],
      legL: rig("legL"), legR: rig("legR"), armL: rig("armL"), armR: rig("armR"), pupL: rig("pupL"), pupR: rig("pupR"),
      h: a.h || 1.75, unit: a.unit || 340, y: a.y || 0,
      legsA: node.querySelectorAll(".legA"), legsB: node.querySelectorAll(".legB"),
      vSide: node.querySelector(".v-side"), vFront: node.querySelector(".v-front"), stars: rig("stars"),
      mO: rig("m-o"), mSmile: rig("m-smile") };
  }
  const evOf = (a, k, t) => a.ev.filter((e) => e[0] === k && t >= e[1]);
  const pA = new THREE.Vector3(), pB = new THREE.Vector3(), camDir = new THREE.Vector3(0, 0, -1);
  function project(x, y, z, hM) {
    pA.set(x, y, z).project(cam); pB.set(x, y + hM, z).project(cam);
    const vis = pA.z < 1 && pA.z > -1 && cam.position.distanceTo(new THREE.Vector3(x, y, z)) > 0.6;
    return { vis, X: (pA.x + 1) * 540, Y: (1 - pA.y) * 960, h: (pA.y - pB.y) * -960, dist: cam.position.distanceTo(new THREE.Vector3(x, y, z)) };
  }
  function actorAt(a, t) {
    const p = a.pos(t), p2 = a.pos(t + 0.05);
    const speed = Math.hypot(p2.x - p.x, p2.z - p.z) / 0.05;
    let rot = 0, sx = 1, dy = a.y, arms = null, armR = null, show = true, dizzy = false, yawn = false;
    for (const e of a.ev) {
      const [k, t0, d = 0.6] = e;
      if (t < t0) continue;
      if (k === "spin" && t < t0 + d) sx = Math.cos(((t - t0) / d) * Math.PI * 6);
      if (k === "fall") rot = (e[3] || -1) * 80 * sstep(t0, t0 + 0.35, t);
      if (k === "up") rot *= 1 - sstep(t0, t0 + 0.4, t);
      if (k === "jump" && t < t0 + d) dy += Math.abs(Math.sin((t - t0) * 9)) * 0.35;
      if (k === "arms" && t < t0 + d) arms = 160;
      if (k === "armsUp" && t < t0 + d) arms = 175;
      if (k === "hide" && t < t0 + d) show = false;
      if (k === "armR" && t < t0 + d) armR = 170;            // one arm up (offside!)
      if (k === "dizzy" && t < t0 + d) dizzy = true;          // stars over the head
      if (k === "yawn" && t < t0 + d) yawn = true;            // mouth open
      if (k === "charge" && t < t0 + d) dy += Math.abs(Math.sin((t - t0) * 14)) * 0.12;
      if (k === "dive") { const f = sstep(t0, t0 + 0.3, t); rot = (e[3] || 1) * 85 * f; dy += Math.sin(Math.min(1, (t - t0) / 0.4) * Math.PI) * 0.6; }
    }
    if (a.only && !(t >= a.only[0] && t < a.only[1])) show = false;
    return { x: p.x, z: p.z, d: p.d, vx: (p2.x - p.x) / 0.05, vz: (p2.z - p.z) / 0.05, speed, rot, sx, dy, arms, armR, show, dizzy, yawn };
  }
  function drawActor(a, t) {
    const s = actorAt(a, t);
    if (!s.show) { a.node.style.display = "none"; return; }
    const pr = project(s.x, s.dy, s.z, a.h);
    if (!pr.vis) { a.node.style.display = "none"; return; }
    a.node.style.display = "block";
    const k = Math.abs(pr.h) / a.unit;
    let sx = Math.abs(s.sx) < 0.12 ? 0.12 * Math.sign(s.sx || 1) : s.sx;
    // two-view sprites (bulls): head-on when running towards/away from the camera, else side view facing the way it runs
    if (a.vSide) {
      let front = a.view === "front";
      if (s.speed > 0.4) {
        const fx = camDir.x, fz = camDir.z, dot = (s.vx * fx + s.vz * fz) / (s.speed * Math.hypot(fx, fz) || 1);
        front = Math.abs(dot) > 0.72;
        if (!front) { const q = project(s.x + s.vx * 0.1, s.dy, s.z + s.vz * 0.1, a.h); sx *= q.X < pr.X ? -1 : 1; }
      } else if (a.facing) sx *= a.facing(t);
      a.vSide.style.display = front ? "none" : "inline"; a.vFront.style.display = front ? "inline" : "none";
    }
    if (a.stars) a.stars.setAttribute("opacity", s.dizzy ? "1" : "0");
    if (a.mO) { a.mO.setAttribute("opacity", s.yawn ? "1" : "0"); if (a.mSmile) a.mSmile.setAttribute("opacity", s.yawn ? "0" : "1"); }
    a.node.style.transform = `translate(${pr.X.toFixed(1)}px, ${pr.Y.toFixed(1)}px) scale(${(k * sx).toFixed(4)}, ${k.toFixed(4)}) rotate(${s.rot.toFixed(1)}deg)`;
    a.node.style.zIndex = String(5000 - Math.round(pr.dist * 20));
    // run cycle from distance travelled; idle sway when standing
    const run = clamp(s.speed / 2.5, 0, 1), ph = (s.d / (a.stride || 1.9)) * Math.PI * 2;
    const sw = run * Math.sin(ph) * 32 + (1 - run) * Math.sin(t * 2.2 + a.unit) * 2;
    if (a.legL) { a.legL.style.transform = `rotate(${sw}deg)`; a.legR.style.transform = `rotate(${-sw}deg)`; }
    for (const g of a.legsA) g.style.transform = `rotate(${sw}deg)`;
    for (const g of a.legsB) g.style.transform = `rotate(${-sw}deg)`;
    if (a.armL) {
      const al = s.arms != null ? s.arms : -sw * 0.8, ar = s.armR != null ? -s.armR : s.arms != null ? -s.arms : sw * 0.8;
      a.armL.style.transform = `rotate(${al}deg)`; a.armR.style.transform = `rotate(${ar}deg)`;
    }
    if (a.pupL || a.pupR) { const look = a.look ? a.look(t) : 0; for (const p of [a.pupL, a.pupR]) if (p) p.style.transform = `translateX(${look * 5}px)`; }
    return { ...s, pr };
  }

  // ---------------- ball ----------------
  // segments: { t0, t1, k: "at", who, dx, dz, y } | { t0, t1, k: "fly", a: [x,y,z], b: [x,y,z], h } | { t0, k: "rest", p: [x,y,z] }
  const ballNode = el("w3-ball"), ballSpin = ballNode ? ballNode.querySelector('[id$="-spin"]') : null;
  if (!plot.ball) plot.ball = [{ t0: 0, k: "rest", p: [0, -50, 0] }];
  const ballPos = (t) => {
    let seg = plot.ball[0];
    for (const s of plot.ball) if (t >= s.t0) seg = s;
    if (seg.k === "rest") return seg.p;
    if (seg.k === "juggle") { const a = actors[seg.who].pos(t); return [a.x + 0.32, 0.12 + Math.abs(Math.sin(t * 4.4)) * 0.85, a.z + 0.25]; }
    if (seg.k === "at") {
      const a = actors[seg.who].pos(t), sp = actors[seg.who];
      const bounce = Math.abs(Math.sin((a.d / (sp.stride || 1.9)) * Math.PI * 2)) * 0.12;
      return [a.x + (seg.dx || 0), (seg.y || 0) + (seg.y ? 0 : bounce), a.z + (seg.dz || 0)];
    }
    const f = clamp((t - seg.t0) / (seg.t1 - seg.t0), 0, 1), e = seg.ease ? EASE[seg.ease](f) : f;
    return [lerp(seg.a[0], seg.b[0], e), lerp(seg.a[1], seg.b[1], e) + Math.sin(e * Math.PI) * (seg.h || 0), lerp(seg.a[2], seg.b[2], e) + Math.sin(e * Math.PI) * (seg.curve || 0)];
  };
  const posOf = (who, t) => { const p = actors[who].pos(t); return [p.x, 0, p.z]; };

  // ---------------- props (static 2D billboards: bench, sub board, flag, tumbleweed, fan sign) ----------------
  const props = Object.entries(plot.props || {}).map(([name, p]) => ({ ...p, node: el("w3-" + name) }));

  // ---------------- camera ----------------
  const v3 = (a) => new THREE.Vector3(a[0], a[1], a[2]);
  const rollOf = (s, u) => (Array.isArray(s.roll) ? lerp(s.roll[0], s.roll[1], EASE.s(u)) : s.roll || 0);
  function shotPose(s, t) {
    const u = clamp((t - s.t0) / (s.t1 - s.t0), 0, 1);
    if (s.k === "path") {
      const e = EASE[s.ease || "s"](u);
      const n = s.P.length - 1, i = Math.min(n - 1, Math.floor(e * n)), f = e * n - i;
      const P = n === 0 ? v3(s.P[0]) : v3(s.P[i]).lerp(v3(s.P[i + 1]), EASE.s(f));
      const T = n === 0 ? v3(s.T[0]) : v3(s.T[Math.min(i, s.T.length - 2)]).lerp(v3(s.T[Math.min(i + 1, s.T.length - 1)]), EASE.s(f));
      return { P, T, fov: s.fov ? lerp(s.fov[0], s.fov[1] ?? s.fov[0], e) : 58, blur: s.blur ?? 0, roll: rollOf(s, e) };
    }
    // follow: an actor or the ball, with offsets (offsets may be [from, to] pairs over the shot)
    const tgt = s.who === "ball" ? ballPos(t) : posOf(s.who, t);
    const off = (o) => (Array.isArray(o[0]) ? [0, 1, 2].map((j) => lerp(o[0][j], o[1][j], EASE.s(u))) : o);
    const o = off(s.off), l = off(s.look || [0, 1.2, 0]);
    const lag = s.lockY != null ? s.lockY : null;
    const ry = s.rideY ? tgt[1] : 0; // rideY: the camera rises and falls with the ball (chase cam)
    const P = new THREE.Vector3(tgt[0] + o[0], (lag ?? 0) + ry + o[1], tgt[2] + o[2]);
    const T = new THREE.Vector3(tgt[0] + l[0], (s.who === "ball" && !s.flat && !s.rideY ? tgt[1] * 0.6 : ry) + l[1], tgt[2] + l[2]);
    return { P, T, fov: s.fov ? lerp(s.fov[0], s.fov[1] ?? s.fov[0], u) : 58, blur: s.blur ?? 2.2, roll: rollOf(s, u) };
  }
  function camAt(t) {
    const S = plot.shots;
    let i = 0; while (i < S.length - 1 && t >= S[i + 1].t0) i++;
    let pose = shotPose(S[i], t), whip = 0;
    // blend into the next shot over its "blend" seconds before it starts (fluid moves instead of cuts)
    const nx = S[i + 1];
    if (nx && nx.blend && t > nx.t0 - nx.blend) {
      const f = EASE.s(clamp((t - (nx.t0 - nx.blend)) / nx.blend, 0, 1)), q = shotPose(nx, nx.t0);
      pose = { P: pose.P.clone().lerp(q.P, f), T: pose.T.clone().lerp(q.T, f), fov: lerp(pose.fov, q.fov, f), blur: lerp(pose.blur, q.blur, f),
               roll: lerp(pose.roll || 0, q.roll || 0, f) };
      if (nx.whip) whip = Math.sin(f * Math.PI);
    }
    if (plot.camBounds) plot.camBounds(pose.P);   // keep the camera out of walls
    cam.position.copy(pose.P); cam.fov = pose.fov; cam.updateProjectionMatrix(); cam.lookAt(pose.T);
    if (pose.roll) cam.rotateZ((pose.roll * Math.PI) / 180);   // dutch angle
    // a little handheld drift keeps every shot alive
    cam.rotation.z += Math.sin(t * 0.9) * 0.004; cam.rotation.x += Math.sin(t * 1.3 + 1) * 0.002;
    cam.updateMatrixWorld();
    camDir.copy(pose.T).sub(pose.P);
    return { blur: pose.blur, whip };
  }

  // ---------------- overlays + bubbles are created from the plot ----------------
  const host = el("w3-ov"), chars = el("w3-chars");
  for (const o of plot.overlays || []) {
    const d = document.createElement("div"); d.id = o.id; d.className = "ov " + (o.cls || ""); d.innerHTML = o.html || "";
    if (o.style) d.setAttribute("style", o.style); host.appendChild(d);
  }
  (plot.bubbles || []).forEach((b, i) => { b.id = b.id || "w3-bub" + i; const d = document.createElement("div"); d.id = b.id;
    d.className = "bub " + (b.cls || ""); d.textContent = b.text; (el("w3-bubs") || chars).appendChild(d); });
  const ov = (plot.overlays || []).map((o) => ({ ...o, node: el(o.id) }));
  const shake = plot.shake || [];
  const texts = (plot.texts || []).map((x) => ({ ...x, node: el(x.id) }));

  function renderAt(t) {
    const { blur, whip } = camAt(t);
    const amp = plot.crowd ? plot.crowd(t) : 0.05;
    st.crowd(t, amp); st.boardsAt(t); st.flashAt(t, plot.flashes ? plot.flashes(t) : 0.08);
    for (const [side, times] of Object.entries(plot.nets || {})) {
      const n = st.nets[side]; let b = 0;
      for (const g of times) if (t >= g && t < g + 0.8) b = Math.max(b, Math.sin(((t - g) / 0.8) * Math.PI) * Math.exp(-(t - g) * 2));
      n.scale.x = 1 + b * 0.8; n.position.x = (side === "left" ? -1 : 1) * (52.5 + 1 + b * 0.8);
    }
    renderer.render(scene, cam);
    let dmin = Infinity;
    for (const a of Object.values(actors)) { const r = drawActor(a, t); if (r && r.pr && r.pr.vis && !a.noOcclude && r.pr.X > -150 && r.pr.X < 1230 && r.pr.Y > 0 && r.pr.Y < 2300) dmin = Math.min(dmin, r.pr.dist); }
    if (fgR) {
      const far = Math.min(dmin, plot.fgMax || 60) - 0.7;
      if (far > 0.5) {
        const bg = scene.background, hidden = [];
        scene.background = null;
        scene.traverse((o) => { if (o.userData.noFg && o.visible) { o.visible = false; hidden.push(o); } });
        const near = cam.near, f0 = cam.far; cam.near = 0.1; cam.far = far; cam.updateProjectionMatrix();
        fgR.render(scene, cam);
        cam.near = near; cam.far = f0; cam.updateProjectionMatrix();
        hidden.forEach((o) => (o.visible = true)); scene.background = bg;
        fgCanvas.style.display = "block"; fgCanvas.style.filter = `blur(${plot.fgBlur ?? 5}px)`;
      } else { fgR.clear(); fgCanvas.style.display = "none"; }
    }
    // ball
    const bp = ballPos(t), bpr = project(bp[0], bp[1], bp[2], 0.22);
    const showBall = !!ballNode && !(plot.ballHidden && plot.ballHidden(t));
    if (bpr.vis && showBall) {
      ballNode.style.display = "block";
      ballNode.style.transform = `translate(${bpr.X.toFixed(1)}px, ${bpr.Y.toFixed(1)}px) scale(${(Math.abs(bpr.h) / 76).toFixed(4)})`;
      ballNode.style.zIndex = String(5000 - Math.round(bpr.dist * 20) + 1);
      ballSpin.style.transform = `rotate(${t * 700}deg)`;
      const sh = el("w3-ballshadow"), spr = project(bp[0], 0, bp[2], 0.22);
      sh.style.transform = `translate(${spr.X.toFixed(1)}px, ${spr.Y.toFixed(1)}px) scale(${(Math.abs(spr.h) / 76).toFixed(4)})`;
      sh.style.zIndex = String(5000 - Math.round(spr.dist * 20)); sh.style.display = "block";
      sh.style.opacity = String(clamp(0.35 - bp[1] * 0.05, 0.05, 0.35));
    } else if (ballNode) { ballNode.style.display = "none"; el("w3-ballshadow").style.display = "none"; }
    // props
    for (const p of props) {
      const on = !p.only || (t >= p.only[0] && t < p.only[1]);
      const pos = p.at ? p.at(t) : p.p;
      const pr = project(pos[0], pos[1], pos[2], p.h);
      if (!on || !pr.vis) { p.node.style.display = "none"; continue; }
      p.node.style.display = "block";
      p.node.style.transform = `translate(${pr.X.toFixed(1)}px, ${pr.Y.toFixed(1)}px) scale(${(Math.abs(pr.h) / p.unit).toFixed(4)}) rotate(${p.rot ? p.rot(t) : 0}deg)`;
      p.node.style.zIndex = String(5000 - Math.round(pr.dist * 20));
    }
    // bubbles over actors' heads
    for (const b of plot.bubbles || []) {
      const node = el(b.id), a = actors[b.who];
      const on = t >= b.t0 && t < b.t1;
      if (!on) { node.style.display = "none"; continue; }
      const s = actorAt(a, t), pr = project(s.x, s.dy + a.h + 0.35, s.z, 0.5);
      if (!pr.vis) { node.style.display = "none"; continue; }
      const pop = sstep(b.t0, b.t0 + 0.15, t) * (1 - sstep(b.t1 - 0.12, b.t1, t));
      node.style.display = "block"; node.style.opacity = String(pop); node.style.zIndex = "6000";
      node.style.transform = `translate(${pr.X.toFixed(1)}px, ${pr.Y.toFixed(1)}px) translate(-50%, -100%) scale(${clamp(Math.abs(pr.h) / 60, 0.45, 1.6) * (0.6 + 0.4 * pop)})`;
    }
    // overlays: fade/slide in and out on their times
    for (const o of ov) {
      const on = t >= o.t0 && t < o.t1;
      if (!on) { o.node.style.opacity = "0"; continue; }
      const fin = o.slam ? sstep(o.t0, o.t0 + 0.14, t) : sstep(o.t0, o.t0 + 0.25, t), fout = 1 - sstep(o.t1 - 0.2, o.t1, t);
      const sc = o.slam ? lerp(2.1, 1, fin) : 1, dx = o.slam ? 0 : (1 - fin) * (o.from === "left" ? -700 : 700);
      o.node.style.opacity = String(Math.min(fin, fout));
      o.node.style.transform = `translateX(${dx}px) scale(${sc}) rotate(${o.slam ? -3 : 0}deg)`;
    }
    for (const x of texts) x.node.textContent = x.at(t);
    if (plot.custom) plot.custom(t, { el, sstep, clamp, lerp });
    // depth of field + whip blur
    const b = blur + whip * 9;
    canvas.style.filter = `blur(${b.toFixed(2)}px) saturate(1.08)`;
    el("w3-chars").style.filter = whip > 0.05 ? `blur(${(whip * 6).toFixed(2)}px)` : "none";
    // screen shake on impacts
    let sh = 0; for (const s of shake) if (t >= s && t < s + 0.3) sh = Math.max(sh, (1 - (t - s) / 0.3) * 14);
    el("w3-stage").style.transform = sh ? `translate(${(Math.sin(t * 90) * sh).toFixed(1)}px, ${(Math.cos(t * 77) * sh * 0.6).toFixed(1)}px)` : "none";
  }
  return { renderAt, actors, ballPos, posOf };
}
