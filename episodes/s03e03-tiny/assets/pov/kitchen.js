// COULD? POV series: a giant kitchen counter seen by someone 3 cm tall. World units: 1 unit = 1 "you-metre" = 1.75 cm real,
// so everything is ~57x bigger than you (a 10 cm mug is 5.7 units tall, a sugar grain ~0.06 real m = an ice cube to you).
// The counter top is y = 0; the back wall (tiles) is at z = -16, the front edge of the counter (where Ben stands) at z = +18.
// buildKitchen(THREE, scene) -> handles (Ben's arm + spoon, the toaster toast, the phone, the cat Mochi, lights, ...).
import { rnd } from "./people.js";

export function buildKitchen(THREE, scene) {
  const R = rnd(33), H = {};
  const tex = (w, h, draw, rep) => { const c = document.createElement("canvas"); c.width = w; c.height = h; draw(c.getContext("2d"), w, h);
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8;
    if (rep) { t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(rep[0], rep[1]); } return t; };
  const lam = (c, e = {}) => new THREE.MeshLambertMaterial({ color: c, ...e });
  const std = (c, r = 0.5, m = 0, e = {}) => new THREE.MeshStandardMaterial({ color: c, roughness: r, metalness: m, ...e });
  const add = (geo, m, x, y, z, p = scene) => { const k = new THREE.Mesh(geo, m); k.position.set(x, y, z); p.add(k); return k; };
  const box = (w, h, d, m, x, y, z, p) => add(new THREE.BoxGeometry(w, h, d), m, x, y, z, p);
  scene.background = new THREE.Color(0xf3ede2);
  scene.fog = new THREE.Fog(0xf3ede2, 60, 220);

  // ---------------- the counter (wood top), back wall tiles, cabinets, window ----------------
  const woodT = tex(512, 512, (g) => { g.fillStyle = "#c99b64"; g.fillRect(0, 0, 512, 512);
    for (let k = 0; k < 90; k++) { g.strokeStyle = `rgba(${120 + R() * 40},${80 + R() * 30},${40},${0.15 + R() * 0.2})`; g.lineWidth = 1 + R() * 3; g.beginPath();
      const y = R() * 512; g.moveTo(0, y); for (let x = 0; x <= 512; x += 32) g.lineTo(x, y + Math.sin(x / 60 + k) * 4); g.stroke(); }
    g.strokeStyle = "rgba(90,60,30,0.35)"; g.lineWidth = 3; for (let x = 0; x <= 512; x += 128) { g.beginPath(); g.moveTo(x, 0); g.lineTo(x, 512); g.stroke(); } }, [3, 2]);
  H.counter = box(300, 2, 34, new THREE.MeshLambertMaterial({ map: woodT }), 0, -1, 1);
  box(300, 40, 2, lam(0xe9e4da), 0, -21, 18);                                           // cabinet fronts below the edge
  const tileT = tex(512, 512, (g) => { g.fillStyle = "#cfd8d3"; g.fillRect(0, 0, 512, 512);
    for (let y = 0; y < 512; y += 64) for (let x = 0; x < 512; x += 64) { const v = R() * 18 - 9; g.fillStyle = `rgb(${207 + v},${216 + v},${211 + v})`; g.fillRect(x + 3, y + 3, 58, 58);
      g.fillStyle = "rgba(255,255,255,0.35)"; g.fillRect(x + 8, y + 8, 22, 5); if (R() < 0.06) { g.fillStyle = "#b9c2bd"; g.beginPath(); g.moveTo(x + 50, y + 3); g.lineTo(x + 61, y + 3); g.lineTo(x + 61, y + 16); g.fill(); } }
    g.strokeStyle = "#e9e6dd"; g.lineWidth = 6; for (let k = 0; k <= 512; k += 64) { g.beginPath(); g.moveTo(k, 0); g.lineTo(k, 512); g.moveTo(0, k); g.lineTo(512, k); g.stroke(); }
    for (let k = 0; k < 160; k++) { g.fillStyle = `rgba(120,110,90,${R() * 0.18})`; const x = Math.round(R() * 8) * 64, y = R() * 512; g.fillRect(x - 3, y, 6, 4 + R() * 20); } }, [13, 4]);
  box(300, 90, 1, new THREE.MeshLambertMaterial({ map: tileT }), 0, 45, -16.5);
  box(300, 40, 20, lam(0xe9e4da), 0, 105, -7);                                          // upper cabinets
  const winT = tex(256, 256, (g) => { const gr = g.createLinearGradient(0, 0, 0, 256); gr.addColorStop(0, "#9fd0f5"); gr.addColorStop(1, "#eaf6ff"); g.fillStyle = gr;
    g.fillRect(0, 0, 256, 256); g.fillStyle = "#7fbf6a"; g.fillRect(0, 190, 256, 66); g.strokeStyle = "#fff"; g.lineWidth = 14; g.strokeRect(0, 0, 256, 256); g.beginPath(); g.moveTo(128, 0); g.lineTo(128, 256); g.stroke(); });
  add(new THREE.PlaneGeometry(60, 50), new THREE.MeshBasicMaterial({ map: winT }), 70, 50, -15.9);
  // far kitchen beyond the counter edge (blurred by fog): fridge, table, floor
  box(40, 200, 30, lam(0xdcdcdc), -110, 40, 60); box(80, 4, 50, lam(0xb07a48), 40, -20, 90); box(500, 1, 500, lam(0xd8c8a8), 0, -60, 100);

  // ---------------- objects on the counter ----------------
  // coffee mug (Ben's), a sugar bowl with lid, the toaster, the phone, crumbs, sugar grains, a puddle, a tea towel
  H.mug = new THREE.Group(); H.mug.position.set(-9, 0, 4); scene.add(H.mug);
  add(new THREE.CylinderGeometry(4.6, 4.2, 5.8, 40, 1, true), std(0x2b6cb0, 0.35, 0, { side: THREE.DoubleSide }), 0, 2.9, 0, H.mug);
  add(new THREE.CylinderGeometry(4.2, 4.2, 0.3, 40), std(0x2b6cb0, 0.35), 0, 0.15, 0, H.mug);
  H.coffee = add(new THREE.CylinderGeometry(4.35, 4.35, 0.2, 40), std(0x5a3418, 0.15), 0, 5.0, 0, H.mug);
  const hdl = add(new THREE.TorusGeometry(1.6, 0.45, 12, 24, Math.PI), std(0x2b6cb0, 0.35), 4.4, 3, 0, H.mug); hdl.rotation.z = -Math.PI / 2;
  H.bowl = new THREE.Group(); H.bowl.position.set(8, 0, -2); scene.add(H.bowl);
  add(new THREE.CylinderGeometry(4, 3.2, 4.5, 40, 1, true), std(0xf4f1ea, 0.25, 0, { side: THREE.DoubleSide }), 0, 2.25, 0, H.bowl);
  add(new THREE.CylinderGeometry(3.2, 3.2, 0.3, 40), std(0xf4f1ea, 0.25), 0, 0.15, 0, H.bowl);
  const sug = tex(128, 128, (g) => { g.fillStyle = "#fbfaf6"; g.fillRect(0, 0, 128, 128); for (let k = 0; k < 400; k++) { g.fillStyle = `rgba(200,200,200,${R() * 0.5})`; g.fillRect(R() * 128, R() * 128, 3, 3); } });
  add(new THREE.CylinderGeometry(3.9, 3.9, 0.2, 40), new THREE.MeshLambertMaterial({ map: sug }), 0, 3.6, 0, H.bowl);
  H.lid = add(new THREE.SphereGeometry(4.2, 32, 12, 0, Math.PI * 2, 0, Math.PI / 2), std(0xf4f1ea, 0.25), 0, 4.5, 0, H.bowl); H.lid.scale.y = 0.35;
  add(new THREE.SphereGeometry(0.7, 16, 12), std(0xf4f1ea, 0.25), 0, 6.0, 0, H.bowl);
  H.lidHolder = H.lid;
  // toaster with two slots, toast inside
  H.toaster = new THREE.Group(); H.toaster.position.set(-24, 0, -8); scene.add(H.toaster);
  const chrome = std(0xd9dde3, 0.18, 0.9);
  add(new THREE.CapsuleGeometry(5.5, 6, 8, 20), chrome, 0, 6.5, 0, H.toaster).rotation.z = Math.PI / 2;
  box(17, 9, 10, chrome, 0, 5.2, 0, H.toaster); box(1.2, 3, 2.4, lam(0x14141f), 8.8, 6, 2, H.toaster);
  H.toast = [];
  for (const dz of [-2, 2]) { const t = box(10, 8, 0.9, lam(0xd9a05a), 0, 7, dz, H.toaster); H.toast.push(t); }
  // the phone (Ben's), screen up, far end of the counter
  H.phoneT = tex(256, 512, (g, w, h) => { g.fillStyle = "#101522"; g.fillRect(0, 0, w, h); g.fillStyle = "#fff"; g.font = "800 64px Inter, Arial"; g.textAlign = "center";
    g.fillText("7:42", w / 2, 150); g.font = "600 24px Inter, Arial"; g.fillText("Tuesday", w / 2, 190); g.fillStyle = "#2bb3ff"; g.fillRect(30, 300, w - 60, 70);
    g.fillStyle = "#fff"; g.font = "700 22px Inter, Arial"; g.fillText("Mom: Did you eat breakfast?", w / 2, 343); });
  H.phone = new THREE.Group(); H.phone.position.set(24, 0, 2); H.phone.rotation.y = 0.3; scene.add(H.phone);
  box(4.4, 0.5, 8.6, std(0x1a1a22, 0.3, 0.3), 0, 0.25, 0, H.phone);
  const ps = add(new THREE.PlaneGeometry(4, 8.2), new THREE.MeshBasicMaterial({ map: H.phoneT }), 0, 0.52, 0, H.phone); ps.rotation.x = -Math.PI / 2;
  // crumbs (boulders to you), sugar grains (ice cubes), a coffee puddle, a pea
  const crumbM = lam(0xc8904a, { flatShading: true });
  for (let k = 0; k < 40; k++) { const c = add(new THREE.DodecahedronGeometry(0.15 + R() * 0.4, 0), crumbM, -14 + R() * 40, 0.15, -6 + R() * 14); c.rotation.set(R() * 3, R() * 3, R() * 3); }
  H.bigCrumb = add(new THREE.DodecahedronGeometry(1.3, 1), crumbM, 2, 0.9, 1.5); H.bigCrumb.scale.set(1.3, 0.8, 1);
  const grainM = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.05, metalness: 0, transparent: true, opacity: 0.85 });
  H.grains = [];
  for (let k = 0; k < 14; k++) { const g = add(new THREE.BoxGeometry(0.5, 0.5, 0.5), grainM, 10 + R() * 8, 0.25, -0.5 + R() * 6); g.rotation.set(R(), R(), R()); H.grains.push(g); }
  H.bigGrain = add(new THREE.BoxGeometry(0.9, 0.9, 0.9), grainM, 12.5, 0.45, 2.2); H.bigGrain.rotation.set(0.3, 0.6, 0.2);
  const pud = add(new THREE.CircleGeometry(2.4, 40), std(0x6a3d1c, 0.05, 0, { transparent: true, opacity: 0.85 }), 17, 0.03, 3.4); pud.rotation.x = -Math.PI / 2; pud.scale.set(1.4, 1, 1);
  H.puddle = pud;

  // ---------------- detail pass: everyday clutter, labels, wear (everything at 57x scale) ----------------
  const label = (w, h, draw) => new THREE.MeshLambertMaterial({ map: tex(w, h, draw) });
  const txt = (g, s, x, y, font, col, align = "center") => { g.fillStyle = col; g.font = font; g.textAlign = align; g.fillText(s, x, y); };
  // a coffee ring stain and scratches on the worktop
  const stain = add(new THREE.RingGeometry(3.6, 4.4, 48), new THREE.MeshBasicMaterial({ color: 0x6b4423, transparent: true, opacity: 0.35, depthWrite: false }), -2, 0.02, -6); stain.rotation.x = -Math.PI / 2;
  for (let k = 0; k < 30; k++) { const sc = box(2 + R() * 7, 0.01, 0.06, new THREE.MeshBasicMaterial({ color: 0x8a5f33, transparent: true, opacity: 0.4 }), -40 + R() * 90, 0.005, -12 + R() * 26); sc.rotation.y = R() * 3; }
  // mug print
  const mugPrint = add(new THREE.CylinderGeometry(4.64, 4.24, 4.0, 40, 1, true, -0.2, 1.9), label(512, 128, (g, w, h) => { g.clearRect(0, 0, w, h); g.fillStyle = "#2b6cb0"; g.fillRect(0, 0, w, h);
    txt(g, "WORLD'S OKAYEST", w / 2, 52, "900 44px Inter, Arial", "#ffffff"); txt(g, "ROOMMATE", w / 2, 104, "900 50px Inter, Arial", "#ffd23f"); }), 0, 3.2, 0, H.mug);
  mugPrint.material.transparent = false;
  // cereal box
  const cereal = new THREE.Group(); cereal.position.set(-40, 0, -9); cereal.rotation.y = 0.35; scene.add(cereal);
  const cerT = label(256, 384, (g, w, h) => { g.fillStyle = "#e8442e"; g.fillRect(0, 0, w, h); g.fillStyle = "#ffd23f"; g.beginPath(); g.arc(w / 2, 220, 90, 0, 6.3); g.fill();
    for (let k = 0; k < 18; k++) { g.fillStyle = ["#f29b38", "#8a4b1e", "#f6d36b"][k % 3]; g.beginPath(); g.arc(w / 2 - 70 + R() * 140, 190 + R() * 70, 10 + R() * 8, 0, 6.3); g.fill(); }
    txt(g, "CRUNCHY", w / 2, 70, "900 50px Inter, Arial", "#fff"); txt(g, "O's", w / 2, 128, "900 60px Inter, Arial", "#ffd23f"); txt(g, "NEW! MORE CRUNCH", w / 2, 350, "800 24px Inter, Arial", "#fff"); });
  const side = lam(0xc9382a);
  add(new THREE.BoxGeometry(17, 26, 6), [side, side, lam(0xd8d8d8), side, cerT, side], 0, 13, 0, cereal);
  // knife block with handles
  const kb = new THREE.Group(); kb.position.set(-52, 0, -11); kb.rotation.y = 0.2; scene.add(kb);
  const kbW = box(9, 14, 8, lam(0x8a5a32), 0, 7, 0, kb); kbW.rotation.x = -0.25;
  for (let k = 0; k < 5; k++) { const hd = box(1.4, 6 - (k % 2), 1.8, lam(0x1b1b1f), -3 + k * 1.5, 16, -1.5 + (k % 2), kb); hd.rotation.x = -0.25; for (const y of [14.5, 17]) box(0.3, 0.3, 0.3, chrome, -3 + k * 1.5, y, -2.5 + (k % 2), kb); }
  // kettle
  const kettle = new THREE.Group(); kettle.position.set(-66, 0, -8); scene.add(kettle);
  add(new THREE.CylinderGeometry(6.5, 8, 14, 32), std(0xe8e4dc, 0.3), 0, 7, 0, kettle);
  add(new THREE.SphereGeometry(6.5, 24, 12, 0, Math.PI * 2, 0, Math.PI / 2), std(0xe8e4dc, 0.3), 0, 14, 0, kettle).scale.y = 0.45;
  const kh = add(new THREE.TorusGeometry(5, 0.9, 10, 24, Math.PI), lam(0x2a2a2f), 0, 15, 0, kettle);
  const sp = add(new THREE.CylinderGeometry(0.9, 1.6, 7, 12), std(0xe8e4dc, 0.3), -8, 9, 0, kettle); sp.rotation.z = 1.0;
  box(4, 1.5, 0.4, lam(0x2bb34a), 0, 3, 7.9, kettle);
  // paper towel roll on a stand
  const pt = new THREE.Group(); pt.position.set(36, 0, -11); scene.add(pt);
  add(new THREE.CylinderGeometry(4.4, 4.4, 15, 28), lam(0xf8f6f0), 0, 8.5, 0, pt); add(new THREE.CylinderGeometry(5.5, 5.5, 0.6, 28), chrome, 0, 0.3, 0, pt);
  add(new THREE.CylinderGeometry(0.4, 0.4, 18, 8), chrome, 0, 9, 0, pt);
  const flap = box(8.6, 6, 0.15, lam(0xf8f6f0), 0, 3, 4.5, pt); flap.rotation.x = 0.25;
  // fruit bowl: apples, bananas, a lemon
  const fb = new THREE.Group(); fb.position.set(52, 0, -5); scene.add(fb);
  add(new THREE.CylinderGeometry(8, 5, 4, 32, 1, true), std(0x3d8f8a, 0.4, 0, { side: THREE.DoubleSide }), 0, 2, 0, fb);
  for (const [x, z, c] of [[-3, 0, 0xd8202c], [2.5, 1.5, 0xc0392b], [0, -3, 0x6fbf3a], [3.5, -2.2, 0xf2d33b]]) {
    add(new THREE.SphereGeometry(2.5, 18, 14), lam(c), x, 4.5, z, fb); box(0.2, 1, 0.2, lam(0x5a3a1a), x, 7, z, fb); }
  for (let k = 0; k < 3; k++) { const b = add(new THREE.TorusGeometry(5, 1.1, 10, 20, 1.6), lam(0xf4d03f), -1 + k * 0.6, 6.5 + k * 0.8, 1, fb); b.rotation.set(1.3, 0.3 * k, 0.5); }
  // salt & pepper, spice rack on the wall, a basil plant under the window
  for (const [x, c] of [[26, 0xf4f4f2], [30, 0x2a2a2f]]) { add(new THREE.CylinderGeometry(1.8, 2.2, 6, 16), std(c, 0.3), x, 3, -10); add(new THREE.SphereGeometry(1.8, 12, 8, 0, Math.PI * 2, 0, Math.PI / 2), chrome, x, 6, -10); }
  box(30, 1, 6, lam(0x8a5a32), 18, 22, -13.5);
  const spiceCols = ["#c0392b", "#e67e22", "#27ae60", "#8e5a2b", "#f1c40f", "#7f8c8d"];
  ["PAPRIKA", "CURRY", "BASIL", "CUMIN", "TURMERIC", "PEPPER"].forEach((n, k) => { const j = new THREE.Group(); j.position.set(6 + k * 4.8, 22.5, -13.5); scene.add(j);
    add(new THREE.CylinderGeometry(1.8, 1.8, 6, 16), std(0xdfe8ee, 0.1, 0, { transparent: true, opacity: 0.6 }), 0, 3, 0, j);
    add(new THREE.CylinderGeometry(1.6, 1.6, 4.5, 16), lam(spiceCols[k]), 0, 2.4, 0, j); add(new THREE.CylinderGeometry(1.9, 1.9, 1.2, 16), lam(0x1b1b1f), 0, 6.4, 0, j);
    const l = add(new THREE.PlaneGeometry(3, 2.2), label(128, 96, (g, w, h) => { g.fillStyle = "#fffaf0"; g.fillRect(0, 0, w, h); txt(g, n, w / 2, 58, "800 20px Inter, Arial", "#222"); }), 0, 3, 1.85, j); void l; });
  const plant = new THREE.Group(); plant.position.set(64, 0, -11); scene.add(plant);
  add(new THREE.CylinderGeometry(4.5, 3.5, 7, 20), lam(0xc0603a), 0, 3.5, 0, plant);
  for (let k = 0; k < 16; k++) { const lf = add(new THREE.SphereGeometry(2 + R(), 10, 8), lam(k % 2 ? 0x3f9b3a : 0x2f7d32), Math.cos(k) * (2 + R() * 3), 8 + R() * 8, Math.sin(k * 1.7) * 3, plant); lf.scale.set(1, 0.4, 0.7); lf.rotation.set(R(), R() * 3, R()); }
  // wall: a double socket with a cable, a light switch, a calendar, a utensil rail with a ladle and a whisk
  const plateM = std(0xf6f4ee, 0.4);
  box(9, 5, 0.6, plateM, -30, 14, -15.9);
  for (const dx of [-2.2, 2.2]) { add(new THREE.CircleGeometry(1.6, 20), lam(0xe0ddd5), -30 + dx, 14, -15.55); for (const hx of [-0.5, 0.5]) add(new THREE.CircleGeometry(0.25, 8), lam(0x222222), -30 + dx + hx, 14, -15.5); }
  const cable = add(new THREE.TubeGeometry(new THREE.CatmullRomCurve3([new THREE.Vector3(-27.8, 14, -15.3), new THREE.Vector3(-27, 8, -15), new THREE.Vector3(-25, 1, -13), new THREE.Vector3(-24, 0.4, -9)]), 20, 0.35, 8), lam(0x2a2a2f));
  void cable; box(4, 6, 0.6, plateM, -12, 34, -15.9); box(1.4, 2.4, 0.5, lam(0xffffff), -12, 34, -15.5);
  const cal = add(new THREE.PlaneGeometry(17, 23), label(256, 340, (g, w, h) => { g.fillStyle = "#fffdf6"; g.fillRect(0, 0, w, h); g.fillStyle = "#3a7bd5"; g.fillRect(0, 0, w, 150);
    g.fillStyle = "#cfe8ff"; g.beginPath(); g.moveTo(0, 150); g.lineTo(90, 70); g.lineTo(160, 120); g.lineTo(256, 40); g.lineTo(256, 150); g.fill();
    txt(g, "NOVEMBER", w / 2, 185, "900 26px Inter, Arial", "#222"); g.strokeStyle = "#bbb"; g.lineWidth = 1;
    for (let r = 0; r < 5; r++) for (let c = 0; c < 7; c++) { g.strokeRect(14 + c * 33, 200 + r * 27, 33, 27); g.fillStyle = "#555"; g.font = "600 11px Inter"; g.fillText(String(r * 7 + c + 1), 22 + c * 33, 212 + r * 27); }
    g.strokeStyle = "#d8202c"; g.lineWidth = 3; g.beginPath(); g.arc(14 + 4 * 33 + 16, 200 + 2 * 27 + 13, 15, 0, 6.3); g.stroke(); }), -50, 52, -15.9);
  void cal; box(60, 0.8, 0.8, chrome, 40, 44, -15.4);
  const ladle = new THREE.Group(); ladle.position.set(30, 43, -14.9); scene.add(ladle);
  box(0.8, 16, 0.4, chrome, 0, -8, 0, ladle); add(new THREE.SphereGeometry(2.6, 16, 10, 0, Math.PI * 2, Math.PI / 2, Math.PI / 2), chrome, 0, -16, 1, ladle);
  const whisk = new THREE.Group(); whisk.position.set(38, 43, -14.9); scene.add(whisk); box(1, 9, 1, lam(0x1b1b1f), 0, -4.5, 0, whisk);
  for (let k = 0; k < 6; k++) { const w = add(new THREE.TorusGeometry(2.4, 0.12, 6, 20), chrome, 0, -12, 0, whisk); w.rotation.y = k * 0.52; w.scale.y = 2.2; }
  H.swing = [ladle, whisk];
  // upper cabinet handles, a sink with a tap and a sponge further right
  for (let k = -5; k <= 5; k++) box(0.8, 8, 0.8, chrome, k * 26 + 11, 92, 3.4);
  box(50, 2, 26, std(0xc9ced6, 0.25, 0.7), 110, 0.2, 0); const tap = new THREE.Group(); tap.position.set(110, 0, -12); scene.add(tap);
  add(new THREE.CylinderGeometry(1.4, 1.8, 20, 16), chrome, 0, 10, 0, tap); const tb = add(new THREE.TorusGeometry(5, 1.2, 10, 20, Math.PI), chrome, 0, 20, 5, tap); tb.rotation.y = Math.PI / 2;
  box(9, 3, 6, lam(0xf2d33b), 88, 1.5, -10); box(9, 1, 6, lam(0x2bb34a), 88, 3.2, -10);
  // toaster detail: a lever, a dial, a brand plate, crumbs around it
  box(3, 1.2, 1.6, lam(0x14141f), 8.9, 9, -2, H.toaster); add(new THREE.CylinderGeometry(1.2, 1.2, 0.8, 20), lam(0x14141f), 9.1, 4, 1.5, H.toaster).rotation.z = Math.PI / 2;
  box(0.2, 1.5, 5, lam(0x9aa0aa), 8.7, 1.2, 0, H.toaster);
  // tile grime: re-draw the tile texture with grout dirt and a few chipped tiles
  // ---------------- Ben: a giant arm + hand + spoon, his torso beyond the counter edge ----------------
  H.ben = new THREE.Group(); scene.add(H.ben);
  const skin = lam(0xe3b08a), shirt = lam(0x3f6fb5);
  const hoodT = tex(512, 512, (g, w, h) => { g.fillStyle = "#3f6fb5"; g.fillRect(0, 0, w, h);
    for (let k = 0; k < 3000; k++) { g.fillStyle = R() > 0.5 ? "rgba(255,255,255,0.05)" : "rgba(0,0,0,0.06)"; g.fillRect(R() * w, R() * h, 2, 2); }
    g.fillStyle = "#f4f4f2"; g.font = "900 64px Inter, Arial"; g.textAlign = "center"; g.fillText("COLLEGE", w / 2, 210); g.font = "800 34px Inter, Arial"; g.fillText("ATHLETICS · EST. 2019", w / 2, 255);
    g.strokeStyle = "#2c5490"; g.lineWidth = 8; g.strokeRect(120, 330, 272, 140); g.beginPath(); g.moveTo(256, 330); g.lineTo(256, 470); g.stroke();
    g.fillStyle = "#2c5490"; g.fillRect(0, 490, w, 22); });
  H.benTorso = add(new THREE.CapsuleGeometry(26, 40, 8, 24), [new THREE.MeshLambertMaterial({ map: hoodT })][0], -10, 30, 54, H.ben); H.benTorso.scale.set(1.1, 1, 0.55);
  for (const sx of [-1, 1]) { const str = add(new THREE.CylinderGeometry(0.6, 0.6, 22, 8), lam(0xf4f4f2), -10 + sx * 7, 52, 39.5, H.ben); str.rotation.x = 0.15;
    add(new THREE.SphereGeometry(1.2, 8, 6), lam(0xf4f4f2), -10 + sx * 7, 41, 38, H.ben); }
  H.benHead = new THREE.Group(); H.benHead.position.set(-10, 92, 44); H.benHead.scale.setScalar(1.45); H.ben.add(H.benHead);
  add(new THREE.SphereGeometry(15, 32, 24), skin, 0, 0, 0, H.benHead);
  add(new THREE.SphereGeometry(15.4, 32, 16, 0, Math.PI * 2, 0, Math.PI * 0.42), lam(0x3b2a1e), 0, 1, 1, H.benHead);
  for (const sx of [-1, 1]) { add(new THREE.SphereGeometry(2.2, 14, 10), lam(0xffffff), sx * 5, 2, -13.4, H.benHead).scale.z = 0.5;
    add(new THREE.SphereGeometry(1.1, 10, 8), lam(0x14141f), sx * 5, 1.6, -14.3, H.benHead); }
  H.benMouth = add(new THREE.SphereGeometry(2.4, 14, 10), lam(0x5a1f24), 0, -6, -13.6, H.benHead); H.benMouth.scale.set(1.4, 0.2, 0.5);
  add(new THREE.SphereGeometry(2.2, 12, 10), skin, 0, -1.5, -14.6, H.benHead).scale.set(0.8, 1, 0.8);
  for (const sx of [-1, 1]) { add(new THREE.SphereGeometry(3, 12, 10), skin, sx * 14.6, 0, 0, H.benHead).scale.set(0.5, 1, 0.8);
    const br = box(5, 0.9, 1, lam(0x3b2a1e), sx * 5, 5.2, -13.6, H.benHead); br.rotation.z = -sx * 0.15; }
  const stub = add(new THREE.SphereGeometry(15.2, 32, 16, 0, Math.PI * 2, Math.PI * 0.6, Math.PI * 0.28), new THREE.MeshLambertMaterial({ color: 0x6b5a4a, transparent: true, opacity: 0.35 }), 0, 0, 0, H.benHead); void stub;
  H.arm = new THREE.Group(); H.ben.add(H.arm);
  const sleeve = add(new THREE.CylinderGeometry(5.5, 6.5, 40, 20), shirt, 0, 20, 0, H.arm);
  const fore = add(new THREE.CylinderGeometry(4, 4.8, 26, 20), skin, 0, -6, 0, H.arm); void sleeve; void fore;
  H.hand = new THREE.Group(); H.hand.position.set(0, -20, 0); H.arm.add(H.hand);
  box(9, 4, 11, skin, 0, -2, 0, H.hand);
  for (let k = 0; k < 4; k++) { const f = add(new THREE.CapsuleGeometry(1.1, 5, 4, 10), skin, -3.2 + k * 2.1, -3.5, -6.5, H.hand); f.rotation.x = 1.2; }
  const th = add(new THREE.CapsuleGeometry(1.3, 5, 4, 10), skin, 5, -1.5, -2, H.hand); th.rotation.set(0.8, 0, -0.8);
  H.spoon = new THREE.Group(); H.hand.add(H.spoon); H.spoon.position.set(0, -4, -7);
  add(new THREE.CylinderGeometry(0.5, 0.5, 26, 10), chrome, 0, -10, 0, H.spoon);
  const bowlS = add(new THREE.SphereGeometry(2.2, 20, 12), chrome, 0, -23.5, 0, H.spoon); bowlS.scale.set(1, 0.4, 1.5);

  // ---------------- Mochi, the cat (giant): body, head, ears, big eyes with slit pupils, whiskers, tail ----------------
  const furT = tex(256, 256, (g, w, h) => { g.fillStyle = "#e8964a"; g.fillRect(0, 0, w, h); g.strokeStyle = "#b8662a"; g.lineWidth = 10;
    for (let k = 0; k < 9; k++) { g.beginPath(); const x = k * 30 + 8; g.moveTo(x, 0); g.bezierCurveTo(x + 18, 70, x - 14, 150, x + 10, 256); g.stroke(); }
    for (let k = 0; k < 1500; k++) { g.fillStyle = R() > 0.5 ? "rgba(255,220,170,0.25)" : "rgba(140,70,20,0.2)"; g.fillRect(R() * w, R() * h, 1, 4); } });
  const fur = new THREE.MeshLambertMaterial({ map: furT }), fur2 = lam(0xf6e7d3), dark = lam(0x2a1a10);
  const cat = new THREE.Group(); scene.add(cat); H.cat = cat;
  H.catBody = add(new THREE.SphereGeometry(10, 32, 24), fur, 0, 10, 14, cat); H.catBody.scale.set(1.1, 0.95, 1.9);
  add(new THREE.SphereGeometry(7.5, 24, 18), fur2, 0, 8, 0, cat).scale.set(1, 0.9, 0.8);       // chest
  H.catHead = new THREE.Group(); H.catHead.position.set(0, 20, -4); cat.add(H.catHead);
  const hd = add(new THREE.SphereGeometry(9, 32, 24), fur, 0, 0, 0, H.catHead); hd.scale.set(1.15, 0.95, 1);
  add(new THREE.SphereGeometry(4.2, 20, 14), fur2, 0, -3.2, -6.5, H.catHead).scale.set(1.3, 0.8, 0.8);   // muzzle
  for (const sx of [-1, 1]) {
    const ear = add(new THREE.ConeGeometry(3.6, 7, 4), fur, sx * 5.6, 8.5, 0, H.catHead); ear.rotation.z = -sx * 0.3;
    add(new THREE.ConeGeometry(2.2, 4.5, 4), lam(0xf2a9a0), sx * 5.4, 8.2, -0.9, H.catHead).rotation.z = -sx * 0.3;
  }
  H.catEyes = []; H.catPupils = [];
  for (const sx of [-1, 1]) {
    const e = add(new THREE.SphereGeometry(2.3, 24, 16), std(0x9ad94a, 0.15), sx * 3.8, 1.6, -7.2, H.catHead); e.scale.set(1, 1, 0.55); H.catEyes.push(e);
    const p = add(new THREE.SphereGeometry(1, 16, 12), std(0x050505, 0.1), sx * 3.8, 1.6, -8.4, H.catHead); p.scale.set(0.35, 1.9, 0.4); H.catPupils.push(p);
    add(new THREE.SphereGeometry(0.35, 8, 6), new THREE.MeshBasicMaterial({ color: 0xffffff }), sx * 3.8 + 0.6, 2.4, -8.6, H.catHead);
    for (let k = 0; k < 3; k++) { const w = add(new THREE.CylinderGeometry(0.06, 0.06, 9, 4), lam(0xffffff), sx * 6.5, -3 + k * 0.7, -7.5, H.catHead);
      w.rotation.z = Math.PI / 2 + sx * (k - 1) * 0.12; }
  }
  add(new THREE.SphereGeometry(0.8, 12, 10), lam(0xe0707a), 0, -1.6, -9.4, H.catHead);         // nose
  H.catMouth = add(new THREE.SphereGeometry(1.2, 12, 10), dark, 0, -4.4, -9, H.catHead); H.catMouth.scale.set(1.2, 0.1, 0.5);
  H.paws = [];
  for (const [x, z] of [[-4.5, -4], [4.5, -4], [-6, 26], [6, 26]]) { const p = add(new THREE.SphereGeometry(2.6, 14, 10), fur2, x, 1.5, z, cat); p.scale.set(1, 0.6, 1.3); H.paws.push(p); }
  H.tail = [];
  let parent = cat, tp = [0, 14, 33];
  for (let k = 0; k < 9; k++) { const g = new THREE.Group(); g.position.set(...(k ? [0, 0, 3.4] : tp)); parent.add(g);
    add(new THREE.SphereGeometry(2.2 - k * 0.1, 12, 10), k > 6 ? fur2 : fur, 0, 0, 1.7, g).scale.set(1, 1, 1.4); H.tail.push(g); parent = g; }
  cat.visible = false;

  // ---------------- lights: warm morning light from the window ----------------
  H.amb = new THREE.AmbientLight(0xfff4e6, 0.55); scene.add(H.amb);
  H.hemi = new THREE.HemisphereLight(0xfff8ee, 0xb08a60, 0.55); scene.add(H.hemi);
  H.sun = new THREE.DirectionalLight(0xfff0d8, 1.3); H.sun.position.set(60, 90, 40); scene.add(H.sun);
  H.shadowM = new THREE.MeshBasicMaterial({ color: 0x000000, transparent: true, opacity: 0, depthWrite: false });
  H.benShadow = add(new THREE.CircleGeometry(14, 32), H.shadowM, 0, 0.05, 6); H.benShadow.rotation.x = -Math.PI / 2;
  H.catShadow = add(new THREE.CircleGeometry(16, 32), H.shadowM.clone(), 0, 0.06, 0); H.catShadow.rotation.x = -Math.PI / 2;
  return H;
}
