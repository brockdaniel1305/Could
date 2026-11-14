// COULD? 3D world: the night stadium with a red 100 m straight across the pitch (8 lanes, start at x = -50, finish at x = +50).
// buildTrack(THREE, scene) -> same interface as buildStadium.
import { buildStadium } from "./stadium3d.js";
export const TRACK = { x0: -50, x1: 50, lane: 1.22, lanes: 8 };
export const laneZ = (n) => (n - 4.5) * TRACK.lane;           // lane 4 = -0.61, lane 5 = +0.61

export function buildTrack(THREE, scene) {
  const st = buildStadium(THREE, scene);
  const { x0, x1, lane, lanes } = TRACK, W = lane * lanes, L = x1 - x0 + 16;
  const c = document.createElement("canvas"); c.width = 2048; c.height = 256; const g = c.getContext("2d");
  g.fillStyle = "#c2412d"; g.fillRect(0, 0, 2048, 256);
  for (let k = 0; k < 3000; k++) { g.fillStyle = k % 2 ? "rgba(90,20,10,0.18)" : "rgba(255,170,140,0.12)"; g.fillRect(Math.random() * 2048, Math.random() * 256, 2, 2); }
  g.fillStyle = "#f4f4f2"; for (let i = 0; i <= lanes; i++) g.fillRect(0, Math.round(i * 256 / lanes) - (i === lanes ? 3 : 0), 2048, 3);
  const px = (x) => ((x - (x0 - 8)) / L) * 2048;
  g.fillRect(px(x0) - 3, 0, 6, 256); g.fillRect(px(x1) - 4, 0, 8, 256);
  for (let k = 0; k < 8; k++) { g.fillStyle = (k % 2) ? "#14141f" : "#f4f4f2"; g.fillRect(px(x1) + 4, k * 32, 10, 32); }
  for (let m = 10; m < 100; m += 10) { g.fillStyle = "rgba(244,244,242,0.5)"; g.fillRect(px(x0 + m) - 1, 0, 2, 256); }
  g.font = "bold 22px Inter, Arial"; g.fillStyle = "#f4f4f2"; for (let i = 0; i < lanes; i++) g.fillText(String(i + 1), px(x0) - 26, i * 32 + 23);
  const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace; tx.anisotropy = 8;
  // a thin slab (not a single plane): its top face always faces up and sits clearly above the pitch, no culling or z-fighting
  const top = new THREE.MeshLambertMaterial({ map: tx }), edge = new THREE.MeshLambertMaterial({ color: 0xa83524 });
  const m = new THREE.Mesh(new THREE.BoxGeometry(L, 0.08, W), [edge, edge, top, edge, edge, edge]);
  m.position.set((x0 - 8 + x1 + 8) / 2, 0.04, 0); scene.add(m);   // (no noFg: the foreground pass must draw it too, or the blurred pitch covers it)
  // starting blocks for lanes 4 and 5, a finish gantry with a timing board
  const blockM = new THREE.MeshLambertMaterial({ color: 0x2a2a33 });
  for (const n of [4, 5]) { const b = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.18, 0.35), blockM); b.position.set(x0 - 0.6, 0.09, laneZ(n)); scene.add(b); }
  const postM = new THREE.MeshLambertMaterial({ color: 0xd9d9d9 });
  for (const z of [-W / 2 - 0.4, W / 2 + 0.4]) { const p = new THREE.Mesh(new THREE.BoxGeometry(0.25, 6.5, 0.25), postM); p.position.set(x1, 3.25, z); scene.add(p); }
  const beam = new THREE.Mesh(new THREE.BoxGeometry(0.3, 0.9, W + 1.2), new THREE.MeshLambertMaterial({ color: 0x14141f })); beam.position.set(x1, 6.2, 0); scene.add(beam);
  return st;
}
