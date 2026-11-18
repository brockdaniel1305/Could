// COULD? POV series: a car interior (left-hand drive, you in the passenger seat) stuck in an open desert, plus a sandstorm wall.
// Coordinates: floor of the car y = 0.3 (seat cushion 0.5), car forward = -z, driver x = -0.37, passenger x = +0.37.
// buildCar(THREE, scene) -> handles for the director (screens to redraw, doors, sunroof, steam, storm, lights, ...).
import { rnd } from "./people.js";

export function buildCar(THREE, scene, opts = {}) {
  const R = rnd(21), H = {};
  const tex = (w, h, draw, rep) => { const c = document.createElement("canvas"); c.width = w; c.height = h; const g = c.getContext("2d"); draw(g, w, h);
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; t.userData = { c, g };
    if (rep) { t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(rep[0], rep[1]); } return t; };
  const lam = (c, e = {}) => new THREE.MeshLambertMaterial({ color: c, ...e });
  const add = (geo, m, x, y, z, p = scene) => { const k = new THREE.Mesh(geo, m); k.position.set(x, y, z); p.add(k); return k; };
  const box = (w, h, d, m, x, y, z, p) => add(new THREE.BoxGeometry(w, h, d), m, x, y, z, p);

  // ---------------- sky, sun, desert ----------------
  const skyT = tex(8, 512, (g, w, h) => { const gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, "#3d86c9"); gr.addColorStop(0.4, "#9cc9ea");
    gr.addColorStop(0.5, "#f3e6c8"); gr.addColorStop(1, "#f3e6c8"); g.fillStyle = gr; g.fillRect(0, 0, w, h); });
  H.sky = add(new THREE.SphereGeometry(2400, 32, 16), new THREE.MeshBasicMaterial({ map: skyT, side: THREE.BackSide, fog: false }), 0, 0, 0);
  H.sun = add(new THREE.SphereGeometry(60, 20, 12), new THREE.MeshBasicMaterial({ color: 0xfff6d0, fog: false }), 700, 1500, -1400);
  const sandT = tex(256, 256, (g) => { g.fillStyle = "#e3b874"; g.fillRect(0, 0, 256, 256);
    for (let k = 0; k < 2500; k++) { g.fillStyle = k % 2 ? "rgba(160,110,50,0.18)" : "rgba(255,235,190,0.25)"; g.fillRect(R() * 256, R() * 256, 2, 2); }
    g.strokeStyle = "rgba(170,120,60,0.25)"; g.lineWidth = 3; for (let k = 0; k < 12; k++) { g.beginPath(); const y = R() * 256; for (let x = 0; x <= 256; x += 16) g.lineTo(x, y + Math.sin(x / 20 + k) * 6); g.stroke(); } }, [300, 300]);
  const geo = new THREE.PlaneGeometry(5000, 5000, 220, 220); const pos = geo.attributes.position;
  for (let i = 0; i < pos.count; i++) { const x = pos.getX(i), y = pos.getY(i), d = Math.hypot(x, y);
    const dune = Math.sin(x * 0.012 + Math.sin(y * 0.004) * 2) * 9 + Math.sin(y * 0.009 + x * 0.003) * 7 + Math.sin(x * 0.031 + y * 0.02) * 2.5;
    pos.setZ(i, dune * Math.min(1, Math.max(0, (d - 30) / 120))); }
  geo.computeVertexNormals();
  H.ground = add(geo, new THREE.MeshLambertMaterial({ map: sandT, flatShading: true }), 0, -0.02, 0); H.ground.rotation.x = -Math.PI / 2;
  // tyre tracks behind the car, scrub, rocks (the cover in option B), far mountains
  for (let k = 0; k < 40; k++) for (const sx of [-0.8, 0.8]) { const t = box(0.25, 0.02, 0.9, lam(0xc99a5b), sx + Math.sin(k * 0.3) * 0.4, 0.0, 3 + k * 1.1); t.rotation.y = Math.sin(k * 0.3) * 0.2; }
  const scrubM = lam(0x8a8a4a, { flatShading: true });
  for (let k = 0; k < 70; k++) { const a = R() * Math.PI * 2, d = 15 + R() * 260; add(new THREE.IcosahedronGeometry(0.5 + R() * 0.8, 0), scrubM, Math.cos(a) * d, 0.2, Math.sin(a) * d); }
  const rockM = lam(0xa4563a, { flatShading: true }), rockM2 = lam(0x8a4530, { flatShading: true });
  H.rocks = new THREE.Group(); H.rocks.position.set(190, 0, -230); scene.add(H.rocks);
  for (let k = 0; k < 9; k++) { const r = add(new THREE.DodecahedronGeometry(8 + R() * 14, 0), k % 2 ? rockM : rockM2, (R() - 0.5) * 50, 4 + R() * 10, (R() - 0.5) * 30, H.rocks); r.scale.y = 0.8 + R() * 0.9; }
  const mtM = lam(0xc58a5c, { flatShading: true });
  for (let k = 0; k < 14; k++) { const a = -2.4 + k * 0.35, m = add(new THREE.ConeGeometry(120 + R() * 140, 90 + R() * 120, 5), mtM, Math.sin(a) * 1700, 30, -Math.cos(a) * 1700); m.rotation.y = R() * 3; }
  scene.fog = new THREE.Fog(0xf0dcb4, 120, 2300); H.fogNear = 120; H.fogFar = 2300;

  // ---------------- the sandstorm: a curved, billowing wall on the horizon ----------------
  const stormT = tex(512, 256, (g, w, h) => { const gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, "rgba(150,90,42,0)"); gr.addColorStop(0.18, "rgba(150,88,40,0.95)");
    gr.addColorStop(1, "rgba(95,52,24,1)"); g.fillStyle = gr; g.fillRect(0, 0, w, h);
    for (let k = 0; k < 90; k++) { const x = R() * w, y = 30 + R() * 90, r = 20 + R() * 46; const gg = g.createRadialGradient(x, y, 0, x, y, r);
      gg.addColorStop(0, "rgba(196,132,70,0.9)"); gg.addColorStop(1, "rgba(196,132,70,0)"); g.fillStyle = gg; g.beginPath(); g.arc(x, y, r, 0, 6.3); g.fill(); } }, [3, 1]);
  H.stormT = stormT;
  H.storm = add(new THREE.CylinderGeometry(1, 1, 1, 64, 1, true, Math.PI * 0.62, Math.PI * 0.76), new THREE.MeshBasicMaterial({ map: stormT, transparent: true, side: THREE.DoubleSide, depthWrite: false, fog: false }), 0, 0, 0);
  H.storm.visible = false;
  H.dust = [];
  const dustM = new THREE.MeshBasicMaterial({ color: 0xe9c68f, transparent: true, opacity: 0.35, depthWrite: false });
  for (let k = 0; k < 60; k++) { const d = add(new THREE.PlaneGeometry(1.5 + R() * 3, 0.08 + R() * 0.12), dustM.clone(), 0, 0.3 + R() * 1.2, -4 - R() * 40); d.userData = { s: R(), sp: 4 + R() * 6 }; H.dust.push(d); }

  // ---------------- the car ----------------
  const car = new THREE.Group(); scene.add(car); H.car = car;
  const paint = lam(0xc0392b), trim = lam(0x34373e), plastic = lam(0x6a6458), plastic2 = lam(0x4f4a42), fabric = lam(0x9a8f7e), glassM = new THREE.MeshLambertMaterial({ color: 0xbfe0f0, transparent: true, opacity: 0.12, depthWrite: false });
  // floor, seats
  box(1.5, 0.05, 2.6, lam(0x2a2c31), 0, 0.3, 0.2, car);
  for (const sx of [-0.37, 0.37]) {
    box(0.52, 0.14, 0.5, fabric, sx, 0.5, 0.05, car);
    const b = box(0.52, 0.72, 0.12, fabric, sx, 0.88, 0.34, car); b.rotation.x = 0.15;
    box(0.3, 0.22, 0.1, fabric, sx, 1.35, 0.4, car);
  }
  box(1.4, 0.16, 0.55, fabric, 0, 0.52, 1.05, car); const rb = box(1.4, 0.65, 0.12, fabric, 0, 0.88, 1.32, car); rb.rotation.x = 0.12;
  box(0.18, 0.28, 0.6, plastic2, 0, 0.48, -0.15, car);                                         // centre console
  // dashboard
  const dash = box(1.5, 0.3, 0.45, plastic, 0, 0.8, -0.82, car); dash.rotation.x = -0.12;
  box(1.5, 0.06, 0.12, plastic2, 0, 0.97, -0.66, car);
  box(0.3, 0.06, 0.12, lam(0x111317), -0.37, 0.95, -0.63, car);                                // cluster hood
  // the centre screen (GPS + outside temperature), the cluster (temp warning), the radio
  const screen = (w, h) => tex(w, h, () => {});
  H.gpsT = screen(512, 320); H.gps = box(0.34, 0.21, 0.012, new THREE.MeshBasicMaterial({ map: H.gpsT }), 0, 1.11, -0.6, car); H.gps.rotation.x = -0.18;
  box(0.37, 0.24, 0.02, lam(0x15171b), 0, 1.11, -0.612, car).rotation.x = -0.18;
  H.radioT = screen(512, 128); H.radio = box(0.26, 0.065, 0.012, new THREE.MeshBasicMaterial({ map: H.radioT }), 0, 0.74, -0.6, car); H.radio.rotation.x = -0.5;
  H.clusterT = screen(256, 128); H.cluster = box(0.26, 0.12, 0.01, new THREE.MeshBasicMaterial({ map: H.clusterT }), -0.37, 0.9, -0.62, car); H.cluster.rotation.x = -0.25;
  // steering wheel
  const wheel = new THREE.Group(); wheel.position.set(-0.37, 0.92, -0.48); wheel.rotation.x = -0.45; car.add(wheel); H.wheel = wheel;
  add(new THREE.TorusGeometry(0.18, 0.025, 10, 32), lam(0x1b1d22), 0, 0, 0, wheel);
  box(0.3, 0.04, 0.02, lam(0x1b1d22), 0, 0, 0, wheel); add(new THREE.CylinderGeometry(0.05, 0.05, 0.04, 16), lam(0x2c2f36), 0, 0, 0, wheel).rotation.x = Math.PI / 2;
  // glovebox, air vents
  box(0.4, 0.12, 0.02, plastic2, 0.37, 0.72, -0.6, car);
  for (const x of [-0.12, 0.12, 0.58]) box(0.1, 0.04, 0.02, lam(0x15171b), x, 0.88, -0.6, car);
  // windshield frame: A-pillars, roof, header, sunroof hole
  for (const sx of [-1, 1]) { const p = box(0.06, 0.64, 0.06, trim, sx * 0.69, 1.205, -0.6, car); p.rotation.x = 0.77; }
  box(1.46, 0.06, 0.1, trim, 0, 1.43, -0.33, car);
  const roofM = lam(0xd8d2c4);
  box(1.46, 0.04, 0.35, roofM, 0, 1.47, -0.15, car); box(1.46, 0.04, 0.95, roofM, 0, 1.47, 1.0, car);
  for (const sx of [-1, 1]) box(0.45, 0.04, 0.6, roofM, sx * 0.5, 1.47, 0.3, car);                 // around the sunroof (0.56 wide)
  H.sunroof = box(0.56, 0.02, 0.6, new THREE.MeshLambertMaterial({ color: 0x223040, transparent: true, opacity: 0.55 }), 0, 1.46, 0.3, car);
  const wsGeo = new THREE.PlaneGeometry(1.4, 0.72); const ws = add(wsGeo, glassM, 0, 1.2, -0.6, car); ws.rotation.x = 0.77;
  // doors: lower panel + window frame, the driver's door hinges at its front edge
  const door = (sx) => { const g = new THREE.Group(); g.position.set(sx * 0.74, 0, -0.45); car.add(g);
    box(0.05, 0.62, 0.95, lam(0x4a4e57), 0, 0.66, 0.47, g); box(0.06, 0.04, 0.95, trim, 0, 0.98, 0.47, g);
    box(0.04, 0.05, 0.16, lam(0x9aa0aa), -sx * 0.03, 0.85, 0.65, g);                             // handle
    box(0.05, 0.42, 0.05, trim, 0, 1.2, 0.95, g);                                                   // B-pillar
    const gl = add(new THREE.PlaneGeometry(0.92, 0.42), glassM, 0, 1.2, 0.47, g); gl.rotation.y = Math.PI / 2; return g; };
  H.doorL = door(-1); H.doorR = door(1);
  for (const sx of [-1, 1]) { box(0.05, 1.0, 0.9, lam(0x4a4e57), sx * 0.74, 0.8, 0.95, car); }     // rear doors (solid-ish)
  box(0.05, 0.42, 0.9, glassM, -0.74, 1.2, 0.95, car).visible = false;
  box(1.46, 0.6, 0.05, lam(0x3a3d44), 0, 0.85, 1.42, car);                                         // back of the rear seat row / trunk wall
  const rearWin = add(new THREE.PlaneGeometry(1.3, 0.38), glassM, 0, 1.25, 1.45, car); void rearWin;
  // rear-view mirror with a cactus air freshener (because of course)
  box(0.22, 0.06, 0.02, lam(0x1b1d22), 0, 1.33, -0.4, car); box(0.02, 0.08, 0.02, lam(0x1b1d22), 0, 1.38, -0.4, car);
  H.freshener = new THREE.Group(); H.freshener.position.set(0, 1.3, -0.4); car.add(H.freshener);
  box(0.004, 0.08, 0.004, lam(0xffffff), 0, -0.04, 0, H.freshener);
  const cact = box(0.05, 0.09, 0.008, lam(0x2bb34a), 0, -0.13, 0, H.freshener); box(0.03, 0.012, 0.008, lam(0x2bb34a), 0.03, -0.12, 0, H.freshener); void cact;
  // hood with steam, side mirrors
  const hood = box(1.5, 0.08, 1.4, paint, 0, 0.85, -1.55, car); hood.rotation.x = 0.06;
  box(1.5, 0.3, 0.06, paint, 0, 0.72, -2.25, car);
  for (const sx of [-1, 1]) box(0.16, 0.1, 0.05, paint, sx * 0.86, 1.02, -0.62, car);
  H.steam = [];
  const steamM = new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.3, depthWrite: false });
  for (let k = 0; k < 40; k++) { const s = add(new THREE.SphereGeometry(0.08, 10, 8), steamM.clone(), 0, 1, -1.8, car); s.userData = { ph: R(), x: (R() - 0.5) * 0.7 }; H.steam.push(s); }
  // back seat: the bag, half a bottle of water, three bags of salty chips
  H.bottle = new THREE.Group(); H.bottle.position.set(0.25, 0.68, 1.0); car.add(H.bottle);
  add(new THREE.CylinderGeometry(0.035, 0.035, 0.22, 14), new THREE.MeshLambertMaterial({ color: 0xd8f0ff, transparent: true, opacity: 0.45 }), 0, 0.11, 0, H.bottle);
  H.water = add(new THREE.CylinderGeometry(0.031, 0.031, 0.09, 14), lam(0x5fb8e8), 0, 0.05, 0, H.bottle);
  add(new THREE.CylinderGeometry(0.018, 0.018, 0.03, 10), lam(0x1d6fd1), 0, 0.235, 0, H.bottle);
  const chipT = (c, label) => tex(128, 160, (g, w, h) => { g.fillStyle = c; g.fillRect(0, 0, w, h); g.fillStyle = "#fff"; g.font = "900 26px Inter, Arial"; g.textAlign = "center";
    g.fillText(label, w / 2, 70); g.font = "700 18px Inter, Arial"; g.fillText("EXTRA SALT", w / 2, 100); });
  H.chips = [];
  [["#d8202c", "SALTY"], ["#1d6fd1", "SALTY"], ["#f2a51a", "SALTY"]].forEach(([c, l], k) => {
    const m = box(0.16, 0.22, 0.05, new THREE.MeshLambertMaterial({ map: chipT(c, l) }), -0.1 - k * 0.17, 0.7, 1.05 + k * 0.02, car); m.rotation.set(-0.5, 0.2 * (k - 1), 0.1 * k); H.chips.push(m); });
  box(0.4, 0.25, 0.25, lam(0x3b5b7a), -0.45, 0.72, 1.0, car);                                      // backpack

  // ---------------- lights ----------------
  H.amb = new THREE.AmbientLight(0xfff1dc, 0.75); scene.add(H.amb);
  H.hemi = new THREE.HemisphereLight(0xcfe6ff, 0xe3b874, 0.65); scene.add(H.hemi);
  H.sunL = new THREE.DirectionalLight(0xfff0d0, 1.25); H.sunL.position.set(30, 60, -40); scene.add(H.sunL);
  return H;
}

// redraw helpers for the screens (canvas textures)
export function drawScreen(T, fn) { const { c, g } = T.userData; g.clearRect(0, 0, c.width, c.height); fn(g, c.width, c.height); T.needsUpdate = true; }
