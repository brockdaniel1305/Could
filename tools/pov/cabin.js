// COULD? POV series: a narrow-body airliner cabin (3+3 seats) in three.js, plus the world outside the windows.
// Coordinates: floor y = 0, the aircraft nose is -z, row r sits at z = r * ROW, seat letters A..F across x (A = left window).
// buildCabin(THREE, scene, opts) -> handles the director animates (masks, lights, hatch, door, water, outside world, ...).
import { rnd } from "./people.js";

export const ROW = 0.82;
export const SEAT_X = { A: -1.4, B: -0.92, C: -0.44, D: 0.44, E: 0.92, F: 1.4 };
export const WALL = 1.86;

export function buildCabin(THREE, scene, opts = {}) {
  const R = rnd(11);
  const FRONT = opts.front ?? -13, BACK = opts.back ?? 5, EXIT_ROW = opts.exitRow ?? -4;
  const zf = FRONT * ROW - 0.9, zb = BACK * ROW + 0.5;       // first row front edge, last row back edge
  const ZDOOR0 = zb + 0.35, ZDOOR1 = ZDOOR0 + 0.95, ZREAR = ZDOOR1 + 0.9, ZBULK = zf - 0.15;
  const tex = (w, h, draw, rep) => { const c = document.createElement("canvas"); c.width = w; c.height = h; draw(c.getContext("2d"), w, h);
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8;
    if (rep) { t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(rep[0], rep[1]); } return t; };
  const lam = (c, extra = {}) => new THREE.MeshLambertMaterial({ color: c, ...extra });
  const add = (g, m, x, y, z, parent = scene) => { const k = new THREE.Mesh(g, m); k.position.set(x, y, z); parent.add(k); return k; };
  const box = (w, h, d, m, x, y, z, parent) => add(new THREE.BoxGeometry(w, h, d), m, x, y, z, parent);
  const H = {};

  // ---------------- outside: sky dome, ocean, clouds (one group the director tilts / lifts) ----------------
  const outside = new THREE.Group(); scene.add(outside); H.outside = outside;
  const skyT = tex(8, 512, (g, w, h) => { const gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, "#2f6fc4"); gr.addColorStop(0.45, "#8fc6ef");
    gr.addColorStop(0.5, "#dceefa"); gr.addColorStop(1, "#dceefa"); g.fillStyle = gr; g.fillRect(0, 0, w, h); });
  const sky = add(new THREE.SphereGeometry(900, 32, 16), new THREE.MeshBasicMaterial({ map: skyT, side: THREE.BackSide, fog: false }), 0, 0, 0, outside);
  const seaT = tex(256, 256, (g) => { g.fillStyle = "#1f6fae"; g.fillRect(0, 0, 256, 256); g.strokeStyle = "rgba(255,255,255,0.35)"; g.lineWidth = 3;
    for (let k = 0; k < 16; k++) { g.beginPath(); const y = R() * 256; for (let x = 0; x <= 256; x += 16) g.lineTo(x, y + Math.sin(x / 13 + k) * 4); g.stroke(); } }, [220, 220]);
  const ocean = add(new THREE.PlaneGeometry(3000, 3000), new THREE.MeshLambertMaterial({ map: seaT, fog: true }), 0, -300, 0, outside);
  ocean.rotation.x = -Math.PI / 2; H.ocean = ocean; H.seaT = seaT;
  const cloudM = lam(0xffffff, { flatShading: true }); H.clouds = [];
  for (let k = 0; k < 26; k++) { const g = new THREE.Group(); for (let q = 0; q < 4; q++) add(new THREE.IcosahedronGeometry(12 + R() * 9, 1), cloudM, q * 14 - 20, R() * 6, R() * 8, g);
    g.position.set(-150 - R() * 500, -120 + R() * 260, -900 + R() * 1800); outside.add(g); H.clouds.push(g); }
  scene.fog = new THREE.Fog(0xcfe4f5, 60, 1400);

  // ---------------- floor, aisle, path lights ----------------
  const carpetT = tex(128, 128, (g) => { g.fillStyle = "#3a4a6b"; g.fillRect(0, 0, 128, 128); g.fillStyle = "rgba(255,255,255,0.06)";
    for (let k = 0; k < 40; k++) g.fillRect(R() * 128, R() * 128, 6, 2); }, [8, 30]);
  box(WALL * 2, 0.04, zb - zf + 6, new THREE.MeshLambertMaterial({ map: carpetT }), 0, -0.02, (zf + zb) / 2 + 2);
  box(0.42, 0.045, zb - zf + 3, lam(0x2a3550), 0, -0.015, (zf + zb) / 2);
  H.pathM = new THREE.MeshLambertMaterial({ color: 0x2b3a2b, emissive: 0x6dff9a, emissiveIntensity: 0 });
  for (let z = zf; z < zb + 2.5; z += 0.36) for (const sx of [-1, 1]) box(0.03, 0.02, 0.18, H.pathM, sx * 0.23, 0.012, z);

  // ---------------- walls with rounded windows ----------------
  const wallM = lam(0xe9e6df), wallM2 = lam(0xdcd8cf), frameM = lam(0xf6f4ef);
  const winShape = (w, h, hw, hh, r) => { const s = new THREE.Shape(); s.moveTo(-w / 2, -h / 2); s.lineTo(w / 2, -h / 2); s.lineTo(w / 2, h / 2); s.lineTo(-w / 2, h / 2); s.lineTo(-w / 2, -h / 2);
    const p = new THREE.Path(); const x0 = -hw / 2, y0 = -hh / 2;
    p.moveTo(x0 + r, y0); p.lineTo(x0 + hw - r, y0); p.quadraticCurveTo(x0 + hw, y0, x0 + hw, y0 + r); p.lineTo(x0 + hw, y0 + hh - r);
    p.quadraticCurveTo(x0 + hw, y0 + hh, x0 + hw - r, y0 + hh); p.lineTo(x0 + r, y0 + hh); p.quadraticCurveTo(x0, y0 + hh, x0, y0 + hh - r);
    p.lineTo(x0, y0 + r); p.quadraticCurveTo(x0, y0, x0 + r, y0); s.holes.push(p); return new THREE.ShapeGeometry(s, 10); };
  const winGeo = winShape(ROW, 0.72, 0.27, 0.4, 0.12), exitGeo = winShape(ROW, 0.72, 0.5, 0.66, 0.08);
  for (const side of [-1, 1]) {
    const x = side * WALL;
    box(0.06, 0.76, ZDOOR0 - ZBULK, wallM2, x, 0.38, (ZBULK + ZDOOR0) / 2);                 // lower wall
    box(0.06, 0.24, ZDOOR0 - ZBULK, wallM, x, 1.58, (ZBULK + ZDOOR0) / 2);                  // band above the windows
    for (let r = FRONT - 1; r <= BACK; r++) {
      const z = r * ROW - 0.12, ex = side < 0 && r === EXIT_ROW;
      const m = add(ex ? exitGeo : winGeo, wallM, x - side * 0.01, 1.1, z); m.rotation.y = side < 0 ? Math.PI / 2 : -Math.PI / 2;
      m.material = new THREE.MeshLambertMaterial({ color: 0xe9e6df, side: THREE.DoubleSide });
      if (!ex) { const ring = add(new THREE.TorusGeometry(0.15, 0.012, 6, 24), frameM, x - side * 0.035, 1.1, z); ring.rotation.y = Math.PI / 2; ring.scale.set(1, 1.3, 1);
        // a pulled-up window shade (a sliver at the top)
        box(0.02, 0.05, 0.26, lam(0xd7d2c6), x - side * 0.04, 1.29, z); }
    }
    // rear section: door on the left, plain wall on the right
    if (side < 0) { box(0.06, 2.0, ZREAR - ZDOOR1, wallM2, x, 1.0, (ZDOOR1 + ZREAR) / 2); box(0.06, 0.2, ZDOOR1 - ZDOOR0, wallM2, x, 1.9, (ZDOOR0 + ZDOOR1) / 2); }
    else box(0.06, 2.0, ZREAR - ZDOOR0, wallM2, x, 1.0, (ZDOOR0 + ZREAR) / 2);
  }
  // the over-wing exit hatch (row EXIT_ROW, left): a door panel with a red handle; the director hides it when it opens
  const hz = EXIT_ROW * ROW - 0.12;
  H.hatch = new THREE.Group(); H.hatch.position.set(-WALL + 0.04, 1.1, hz); scene.add(H.hatch);
  box(0.05, 0.66, 0.5, lam(0xe2ded5), 0, 0, 0, H.hatch);
  const hwin = add(new THREE.TorusGeometry(0.13, 0.02, 6, 20), frameM, 0.03, 0.08, 0, H.hatch); hwin.rotation.y = Math.PI / 2; hwin.scale.set(1, 1.3, 1);
  box(0.04, 0.05, 0.2, lam(0xd8202c), 0.04, 0.27, 0, H.hatch);
  const signT = (txt, bg, fg, w = 256, h = 96) => tex(w, h, (g) => { g.fillStyle = bg; g.fillRect(0, 0, w, h); g.fillStyle = fg; g.font = `900 ${h * 0.62}px Inter, Arial`;
    g.textAlign = "center"; g.textBaseline = "middle"; g.fillText(txt, w / 2, h / 2 + 3); });
  H.exitSigns = [];
  const exitSign = (x, y, z, ry = 0) => { const m = new THREE.MeshBasicMaterial({ map: signT("EXIT", "#0d7a3a", "#eafff1") }); const s = box(0.34, 0.12, 0.03, m, x, y, z); s.rotation.y = ry; H.exitSigns.push(s); return s; };
  exitSign(-WALL + 0.05, 1.56, hz, Math.PI / 2); exitSign(0, 1.98, ZBULK + 0.3); exitSign(0, 1.98, hz - 0.3); exitSign(0, 1.98, ZDOOR0 + 0.2, Math.PI);

  // ---------------- ceiling, bins, passenger service units ----------------
  const ceil = add(new THREE.CylinderGeometry(WALL, WALL, ZREAR - ZBULK, 40, 1, true, -Math.PI / 2, Math.PI), lam(0xf1efe9, { side: THREE.BackSide }), 0, 1.66, (ZBULK + ZREAR) / 2);
  ceil.rotation.x = Math.PI / 2; ceil.rotation.y = Math.PI / 2; ceil.scale.set(1, 1, 0.42);
  ceil.rotation.set(Math.PI / 2, 0, 0); ceil.scale.set(1, 1, 1);
  ceil.geometry = new THREE.CylinderGeometry(WALL, WALL, ZREAR - ZBULK, 40, 1, true, Math.PI / 2, Math.PI); ceil.scale.set(1, 1, 0.42); ceil.rotation.set(Math.PI / 2, 0, 0);
  ceil.position.set(0, 1.66, (ZBULK + ZREAR) / 2);
  const binT = tex(256, 128, (g) => { g.fillStyle = "#f3f1ec"; g.fillRect(0, 0, 256, 128); g.strokeStyle = "#cfcac0"; g.lineWidth = 4; g.strokeRect(4, 6, 248, 116);
    g.fillStyle = "#b9b3a6"; g.fillRect(110, 92, 36, 10); });
  H.bins = {};
  for (const side of [-1, 1]) {
    const x = side * (WALL - 0.42);
    for (let r = FRONT - 1; r <= BACK; r++) {
      const z = r * ROW - 0.12, g = new THREE.Group(); g.position.set(x, 1.9, z); scene.add(g);
      box(0.78, 0.42, ROW - 0.02, lam(0xe7e4dc), side * 0.02, 0, 0, g);
      // the door: pivots at its top edge (open = swing up)
      const door = new THREE.Group(); door.position.set(-side * 0.39, 0.21, 0); g.add(door);
      const dm = add(new THREE.BoxGeometry(0.03, 0.42, ROW - 0.04), new THREE.MeshLambertMaterial({ map: binT }), 0, -0.21, 0, door); void dm;
      H.bins[`${side < 0 ? "L" : "R"}${r}`] = { g, door };
    }
    // service-unit strip under the bins (reading lights + the mask doors)
    box(0.5, 0.05, ZDOOR0 - ZBULK, lam(0xd9d5cc), side * (WALL - 0.58), 1.665, (ZBULK + ZDOOR0) / 2);
  }
  // ceiling light strips
  H.stripM = new THREE.MeshLambertMaterial({ color: 0xffffff, emissive: 0xfff4e0, emissiveIntensity: 1 });
  for (const side of [-1, 1]) box(0.06, 0.02, ZDOOR0 - ZBULK, H.stripM, side * 0.62, 2.28, (ZBULK + ZDOOR0) / 2);

  // ---------------- seats ----------------
  const seatM = lam(0x24427a), seatM2 = lam(0x1d355f), headM = lam(0xf2f0ea), armM = lam(0x8b93a1), trayM = lam(0x6f7785);
  H.seats = {};
  for (let r = FRONT; r <= BACK; r++) for (const [L, x] of Object.entries(SEAT_X)) {
    const z = r * ROW, g = new THREE.Group(); g.position.set(x, 0, z); scene.add(g);
    box(0.46, 0.14, 0.5, seatM, 0, 0.44, 0.02, g);                                   // cushion
    const back = new THREE.Group(); back.position.set(0, 0.48, 0.27); g.add(back); back.rotation.x = 0.12;
    box(0.46, 0.66, 0.13, seatM2, 0, 0.33, 0, back);
    box(0.42, 0.16, 0.02, headM, 0, 0.56, -0.07, back);                                 // headrest cover
    box(0.36, 0.26, 0.02, trayM, 0, 0.36, 0.075, back);                                   // tray table on the back
    box(0.38, 0.14, 0.03, lam(0x2c3550), 0, 0.12, 0.08, back);                           // seat pocket
    box(0.05, 0.36, 0.5, armM, -0.25, 0.2, 0.02, g);
    if (L === "C" || L === "F") box(0.05, 0.36, 0.5, armM, 0.25, 0.2, 0.02, g);
    box(0.4, 0.04, 0.06, lam(0x333a48), 0, 0.06, -0.2, g);                               // seat legs bar
    H.seats[`${r}${L}`] = { g, back, x, z };
  }
  // the safety card in the pocket of seat (row -1, A) - the director pulls it out
  const cardT = tex(256, 384, (g, w, h) => { g.fillStyle = "#f7f3e8"; g.fillRect(0, 0, w, h); g.fillStyle = "#14141f"; g.font = "900 26px Inter, Arial"; g.textAlign = "center";
    g.fillText("SAFETY", w / 2, 36); g.fillStyle = "#c9d6e2"; g.beginPath(); g.ellipse(w / 2, 210, 46, 150, 0, 0, Math.PI * 2); g.fill();
    g.fillStyle = "#9fb0c2"; g.fillRect(28, 180, 200, 34);
    for (let k = 0; k < 14; k++) { g.fillStyle = k === 4 ? "#d8202c" : "#6b7a8c"; g.fillRect(w / 2 - 30, 100 + k * 16, 24, 10); g.fillRect(w / 2 + 6, 100 + k * 16, 24, 10); }
    g.fillStyle = "#1f9d55"; for (const [x, y] of [[44, 165], [212, 165], [44, 310], [212, 310]]) { g.beginPath(); g.moveTo(x, y); g.lineTo(x + (x < 128 ? -22 : 22), y + 12); g.lineTo(x, y + 24); g.fill(); }
    g.fillStyle = "#14141f"; g.font = "700 20px Inter, Arial"; g.fillText("BRACE · EXITS · VEST", w / 2, 368); });
  H.card = box(0.17, 0.25, 0.006, new THREE.MeshLambertMaterial({ map: cardT }), SEAT_X.A, 0.62, -ROW + 0.36); H.card.rotation.x = 0.12;

  // ---------------- oxygen masks: one per seat, hanging from the service unit ----------------
  H.masks = [];
  const maskM = lam(0xffd23f), tubeM = lam(0xf4f4f2);
  for (let r = FRONT; r <= BACK; r++) for (const [L, x] of Object.entries(SEAT_X)) {
    const pivot = new THREE.Group(); pivot.position.set(x * 0.95, 1.66, r * ROW - 0.36); scene.add(pivot);
    const len = 0.42 + R() * 0.1;
    add(new THREE.CylinderGeometry(0.006, 0.006, len, 5), tubeM, 0, -len / 2, 0, pivot);
    const cup = add(new THREE.CylinderGeometry(0.05, 0.065, 0.07, 14), maskM, 0, -len - 0.03, 0, pivot);
    const bag = add(new THREE.SphereGeometry(0.04, 10, 8), lam(0xf0f0f0, { transparent: true, opacity: 0.7 }), 0, -len + 0.08, 0.03, pivot); void bag;
    H.masks.push({ pivot, cup, len, r, L, ph: R() * 6.28, fr: 2.2 + R() * 1.4 });
  }

  // ---------------- front bulkhead, galley, rear galley + door ----------------
  box(WALL * 2, 2.4, 0.08, lam(0xd9d4c9), 0, 1.2, ZBULK);
  box(0.9, 1.2, 0.3, lam(0xbfc5cc), -0.9, 0.6, ZBULK + 0.15); box(0.9, 1.2, 0.3, lam(0xbfc5cc), 0.9, 0.6, ZBULK + 0.15);
  H.jumpSeat = box(0.45, 0.06, 0.3, lam(0x2c3550), 0, 0.55, ZBULK + 0.2);
  box(WALL * 2, 2.4, 0.08, lam(0xd9d4c9), 0, 1.2, ZREAR);
  for (let k = 0; k < 3; k++) box(0.42, 1.0, 0.5, lam(0xbfc5cc), 0.9 - k * 0.0, 0.5, ZREAR - 0.3 - k * 0.0).position.x = 1.35 - k * 0.45;
  H.rearDoor = new THREE.Group(); H.rearDoor.position.set(-WALL + 0.03, 0, ZDOOR0); scene.add(H.rearDoor);
  box(0.08, 1.9, ZDOOR1 - ZDOOR0, lam(0xd3cec4), 0, 0.95, (ZDOOR1 - ZDOOR0) / 2, H.rearDoor);
  box(0.05, 0.08, 0.3, lam(0x8b93a1), 0.06, 1.1, 0.5, H.rearDoor);
  H.Z = { front: ZBULK, back: ZREAR, door0: ZDOOR0, door1: ZDOOR1, exit: hz };

  // ---------------- the wing, seen through the windows near the exit rows ----------------
  const wing = new THREE.Group(); wing.position.set(-WALL - 0.1, 0.45, (EXIT_ROW - 2) * ROW); scene.add(wing); H.wing = wing;
  const wshape = new THREE.Shape(); wshape.moveTo(0, -2.4); wshape.lineTo(-16, 1.2); wshape.lineTo(-16, 2.6); wshape.lineTo(0, 2.6); wshape.lineTo(0, -2.4);
  const wg = new THREE.ExtrudeGeometry(wshape, { depth: 0.18, bevelEnabled: false }); const wm = add(wg, lam(0xc9ced6), 0, 0, 0, wing); wm.rotation.x = Math.PI / 2;
  const eng = add(new THREE.CylinderGeometry(0.55, 0.62, 2.4, 20), lam(0x9aa3ae), -5.5, -0.6, -0.6, wing); eng.rotation.x = Math.PI / 2;

  // ---------------- water on the cabin floor (raised by the director), water pouring in at the rear door ----------------
  const wT = tex(256, 256, (g) => { g.fillStyle = "#4fb6cf"; g.fillRect(0, 0, 256, 256); g.strokeStyle = "rgba(255,255,255,0.7)"; g.lineWidth = 3;
    for (let k = 0; k < 18; k++) { g.beginPath(); const y = R() * 256; for (let x = 0; x <= 256; x += 16) g.lineTo(x, y + Math.sin(x / 11 + k) * 5); g.stroke(); } }, [3, 12]);
  H.waterT = wT;
  H.water = add(new THREE.PlaneGeometry(WALL * 2 - 0.08, ZREAR - ZBULK), new THREE.MeshLambertMaterial({ map: wT, transparent: true, opacity: 0.5, depthWrite: false, emissive: 0x0d3a48, emissiveIntensity: 0.6 }), 0, -0.2, (ZBULK + ZREAR) / 2);
  H.water.rotation.x = -Math.PI / 2;
  const pourT = tex(64, 256, (g, w, h) => { g.fillStyle = "#3aa4c4"; g.fillRect(0, 0, w, h); g.fillStyle = "rgba(255,255,255,0.55)";
    for (let k = 0; k < 40; k++) g.fillRect(R() * w, R() * h, 3, 18 + R() * 30); }, [1, 2]);
  H.pourT = pourT;
  H.pour = add(new THREE.PlaneGeometry(1.6, 1.4), new THREE.MeshLambertMaterial({ map: pourT, transparent: true, opacity: 0.85, side: THREE.DoubleSide, depthWrite: false }),
    -WALL + 0.5, 0.25, (ZDOOR0 + ZDOOR1) / 2);
  H.pour.rotation.set(-Math.PI / 2 + 0.5, 0, Math.PI / 2); H.pour.visible = false;

  // ---------------- lights ----------------
  H.amb = new THREE.AmbientLight(0xffffff, 0.55); scene.add(H.amb);
  H.hemi = new THREE.HemisphereLight(0xfff6e8, 0x5b6478, 0.75); scene.add(H.hemi);
  H.sun = new THREE.DirectionalLight(0xfff1d8, 0.7); H.sun.position.set(-20, 12, 5); scene.add(H.sun);
  H.reds = [];
  for (let k = 0; k < 5; k++) { const p = new THREE.PointLight(0xff2a1a, 0, 6, 1.6); p.position.set(0, 2.1, -9 + k * 3.4); scene.add(p); H.reds.push(p); }
  H.exitLight = new THREE.PointLight(0xfff6dc, 0, 6, 1.5); H.exitLight.position.set(-WALL + 0.4, 1.2, hz); scene.add(H.exitLight);
  H.doorLight = new THREE.PointLight(0xe8f6ff, 0, 9, 1.2); H.doorLight.position.set(-WALL + 0.5, 1.2, (ZDOOR0 + ZDOOR1) / 2); scene.add(H.doorLight);
  return H;
}
