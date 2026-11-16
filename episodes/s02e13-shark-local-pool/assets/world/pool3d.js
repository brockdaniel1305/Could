// COULD? 3D world for "Could a shark end up in your local pool?": three places in one scene, the camera jumps between them.
//   POOL   (x ~ 0)   : a sunny outdoor public pool (25 m basin, lane ropes, deck tiles, loungers, umbrellas, lifeguard chair, fence)
//                      right next to a river behind the fence. A flood level function globalThis.__flood(t) (metres above the deck,
//                      set by the director) raises a murky flood plane over everything.
//   STREET (x ~ 200) : a flooded town street (houses, traffic light, lamp posts, parked car roofs) under brown water.
//   GOLF   (x ~ -200): a golf course with a lake, a green with a flag, a bunker and trees.
// buildPool(THREE, scene) -> { crowd(t), flashAt, boardsAt, nets, envAt(cam) }.
export const POOL = { L: 25, W: 12.5, deck: 0, water: -0.25, river: -26 };
export const STREET_X = 200, GOLF_X = -200;

export function buildPool(THREE, scene) {
  const mulberry = (a) => () => { a |= 0; a = (a + 0x6d2b79f5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  const rnd = mulberry(7);
  const tex = (w, h, draw, rep) => { const c = document.createElement("canvas"); c.width = w; c.height = h; draw(c.getContext("2d"), w, h);
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8;
    if (rep) { t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(rep[0], rep[1]); } return t; };
  const lam = (o) => new THREE.MeshLambertMaterial(o);
  const box = (w, h, d, mat, x, y, z, ry = 0) => { const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), mat); m.position.set(x, y, z); m.rotation.y = ry; scene.add(m); return m; };
  const flat = (w, d, mat, x, y, z, noFg = true) => { const m = new THREE.Mesh(new THREE.BoxGeometry(w, 0.04, d), mat); m.position.set(x, y - 0.02, z); m.userData.noFg = noFg; scene.add(m); return m; };

  // ---- sky / light (sunny; the street gets a grey storm sky via envAt) ----
  const skySun = tex(8, 512, (g, w, h) => { const gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, "#3f8fe0"); gr.addColorStop(0.6, "#9fd2f5"); gr.addColorStop(1, "#eaf6ff"); g.fillStyle = gr; g.fillRect(0, 0, w, h); });
  const skyStorm = tex(8, 512, (g, w, h) => { const gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, "#4b5563"); gr.addColorStop(0.6, "#8a94a1"); gr.addColorStop(1, "#c9cfd6"); g.fillStyle = gr; g.fillRect(0, 0, w, h); });
  scene.background = skySun; scene.fog = new THREE.Fog(0xdceefa, 90, 420);
  scene.add(new THREE.AmbientLight(0xffffff, 0.62)); scene.add(new THREE.HemisphereLight(0xffffff, 0xbfae8f, 0.6));
  const sun = new THREE.DirectionalLight(0xfff3dc, 1.15); sun.position.set(40, 80, 50); scene.add(sun);
  const clouds = [];
  const cloudM = lam({ color: 0xffffff, flatShading: true });
  for (let k = 0; k < 14; k++) { const g = new THREE.Group(), x = -300 + rnd() * 600, z = -160 - rnd() * 80;
    for (let q = 0; q < 4; q++) { const m = new THREE.Mesh(new THREE.IcosahedronGeometry(5 + rnd() * 4, 1), cloudM); m.position.set(q * 6 - 9, rnd() * 3, rnd() * 4); g.add(m); }
    g.position.set(x, 45 + rnd() * 25, z); g.userData.noFg = true; scene.add(g); clouds.push(g); }

  // ---- ground everywhere: grass, with holes cut out for the pool basin and the river (otherwise it covers both) ----
  const grassT = tex(256, 256, (g) => { g.fillStyle = "#5fb548"; g.fillRect(0, 0, 256, 256);
    for (let k = 0; k < 900; k++) { g.fillStyle = k % 3 ? "rgba(40,120,30,0.3)" : "rgba(170,230,110,0.35)"; g.fillRect(rnd() * 256, rnd() * 256, 2, 5); } }, [0.1, 0.1]);
  { const sh = new THREE.Shape(); sh.moveTo(-600, -600); sh.lineTo(600, -600); sh.lineTo(600, 600); sh.lineTo(-600, 600); sh.lineTo(-600, -600);
    const hole = (x0, z0, x1, z1) => { const h = new THREE.Path(); h.moveTo(x0, -z0); h.lineTo(x0, -z1); h.lineTo(x1, -z1); h.lineTo(x1, -z0); h.lineTo(x0, -z0); sh.holes.push(h); };
    hole(-12.5, -6.25, 12.5, 6.25); hole(-300, -34, 300, -18);
    const gm = new THREE.Mesh(new THREE.ShapeGeometry(sh), lam({ map: grassT })); gm.rotation.x = -Math.PI / 2; gm.position.y = -0.03; gm.userData.noFg = true; scene.add(gm); }

  // ======================= POOL =======================
  const { L, W } = POOL;
  const deckT = tex(256, 256, (g) => { g.fillStyle = "#e9e3d6"; g.fillRect(0, 0, 256, 256); g.strokeStyle = "#cfc6b4"; g.lineWidth = 3;
    for (let k = 0; k <= 256; k += 64) { g.beginPath(); g.moveTo(k, 0); g.lineTo(k, 256); g.moveTo(0, k); g.lineTo(256, k); g.stroke(); } }, [16, 10]);
  // deck with a hole for the basin: four slabs around it
  const deckM = lam({ map: deckT });
  flat(L + 30, 10, deckM, 0, 0.0, -W / 2 - 5); flat(L + 30, 14, deckM, 0, 0.0, W / 2 + 7); flat(15, W, deckM, -L / 2 - 7.5, 0.0, 0); flat(15, W, deckM, L / 2 + 7.5, 0.0, 0);
  // basin: tiled walls and floor
  const tileT = tex(128, 128, (g) => { g.fillStyle = "#7fd3ef"; g.fillRect(0, 0, 128, 128); g.strokeStyle = "#5bb7d8"; g.lineWidth = 2;
    for (let k = 0; k <= 128; k += 16) { g.beginPath(); g.moveTo(k, 0); g.lineTo(k, 128); g.moveTo(0, k); g.lineTo(128, k); g.stroke(); } }, [6, 1]);
  const wallM = lam({ map: tileT, side: THREE.DoubleSide });
  box(L, 2, 0.2, wallM, 0, -1, -W / 2); box(L, 2, 0.2, wallM, 0, -1, W / 2); box(0.2, 2, W, wallM, -L / 2, -1, 0); box(0.2, 2, W, wallM, L / 2, -1, 0);
  const floorT = tex(256, 128, (g) => { g.fillStyle = "#6cc6e6"; g.fillRect(0, 0, 256, 128); g.fillStyle = "#1d3f9b";
    for (let k = 0; k < 6; k++) g.fillRect(8, 10 + k * 20, 240, 4); });
  flat(L, W, lam({ map: floorT }), 0, -1.95, 0);
  // the water surface (sparkly, slightly transparent) + lane ropes
  const waterT = tex(256, 256, (g) => { g.fillStyle = "#2fb4e0"; g.fillRect(0, 0, 256, 256);
    g.strokeStyle = "rgba(255,255,255,0.45)"; g.lineWidth = 3; for (let k = 0; k < 14; k++) { g.beginPath(); const y = rnd() * 256; for (let x = 0; x <= 256; x += 16) g.lineTo(x, y + Math.sin(x / 18 + k) * 4); g.stroke(); } }, [4, 2]);
  const water = new THREE.Mesh(new THREE.PlaneGeometry(L, W), new THREE.MeshLambertMaterial({ map: waterT, transparent: true, opacity: 0.86 }));
  water.rotation.x = -Math.PI / 2; water.position.y = POOL.water; water.userData.noFg = true; scene.add(water);
  const ropeM = [lam({ color: 0xd8202c }), lam({ color: 0xf4f4f2 }), lam({ color: 0x1d3f9b })];
  for (let r = 1; r < 6; r++) { const z = -W / 2 + r * (W / 6);
    for (let k = 0; k < 50; k++) { const s = new THREE.Mesh(new THREE.SphereGeometry(0.11, 8, 6), ropeM[(k >> 2) % 3]); s.position.set(-L / 2 + 0.25 + k * 0.5, POOL.water + 0.05, z); scene.add(s); } }
  // starting blocks, ladders, lifeguard chair, loungers, umbrellas, fence, changing huts, trees
  const blockM = lam({ color: 0xf4f4f2 }), redM = lam({ color: 0xd8202c }), metalM = lam({ color: 0xbfc5cc }), woodM = lam({ color: 0xc28b55 });
  for (let r = 0; r < 6; r++) { const z = -W / 2 + (r + 0.5) * (W / 6); box(0.7, 0.7, 0.6, blockM, -L / 2 - 0.5, 0.35, z); }
  for (const z of [-W / 2 + 0.6, W / 2 - 0.6]) for (const dz of [-0.25, 0.25]) box(0.06, 1.2, 0.06, metalM, L / 2 + 0.15, 0.2, z + dz);
  // lifeguard chair (white frame, red seat)
  for (const [dx, dz] of [[-0.6, -0.5], [0.6, -0.5], [-0.6, 0.5], [0.6, 0.5]]) box(0.12, 2.4, 0.12, blockM, 4 + dx, 1.2, W / 2 + 2.2 + dz);
  box(1.5, 0.15, 1.2, redM, 4, 2.4, W / 2 + 2.2); box(1.5, 0.9, 0.12, redM, 4, 2.9, W / 2 + 2.75);
  const uCols = [0xff7a59, 0x4f9dff, 0xffd23f, 0x2bb3a3];
  for (let k = 0; k < 6; k++) { const x = -14 + k * 5.6, z = W / 2 + 6.5;
    box(0.8, 0.25, 1.9, lam({ color: 0xf4f4f2 }), x, 0.35, z + 1.5); box(0.06, 2.4, 0.06, metalM, x, 1.2, z);
    const u = new THREE.Mesh(new THREE.ConeGeometry(1.6, 0.6, 8), lam({ color: uCols[k % 4] })); u.position.set(x, 2.5, z); scene.add(u); }
  for (let k = -24; k <= 24; k += 1.2) box(0.06, 1.6, 0.06, metalM, k, 0.8, -W / 2 - 8.5);
  for (const y of [0.4, 1.5]) box(48, 0.05, 0.05, metalM, 0, y, -W / 2 - 8.5);
  for (let k = 0; k < 3; k++) box(4, 2.6, 3, lam({ color: [0x4f9dff, 0xffd23f, 0x2bb3a3][k] }), -16 + k * 4.6, 1.3, W / 2 + 12);
  const trunkM = lam({ color: 0x7a5230 }), leafM = lam({ color: 0x3f9b3a, flatShading: true });
  const tree = (x, z, s = 1) => { box(0.35 * s, 3 * s, 0.35 * s, trunkM, x, 1.5 * s, z); const c = new THREE.Mesh(new THREE.IcosahedronGeometry(2.0 * s, 0), leafM); c.position.set(x, 3.6 * s, z); scene.add(c); };
  for (let k = 0; k < 9; k++) tree(-26 + k * 6.5, -W / 2 - 11 - (k % 2) * 2, 1 + (k % 3) * 0.2);
  for (let k = 0; k < 4; k++) tree(-24 + k * 16, W / 2 + 16, 1.1);
  // the river right behind the fence + far bank
  const riverT = tex(256, 256, (g) => { g.fillStyle = "#3d7f8f"; g.fillRect(0, 0, 256, 256); g.strokeStyle = "rgba(255,255,255,0.25)"; g.lineWidth = 3;
    for (let k = 0; k < 10; k++) { g.beginPath(); const y = rnd() * 256; for (let x = 0; x <= 256; x += 16) g.lineTo(x, y + Math.sin(x / 16 + k) * 3); g.stroke(); } }, [40, 3]);
  const river = flat(600, 16, lam({ map: riverT }), 0, -0.5, POOL.river); flat(600, 1.2, lam({ color: 0x9b8a6a }), 0, -0.2, POOL.river + 8.4); flat(600, 16, lam({ color: 0x5b4a33 }), 0, -1.6, POOL.river);
  for (let k = 0; k < 18; k++) tree(-90 + k * 10 + rnd() * 3, POOL.river - 12 - rnd() * 6, 1.3);
  // flood water: one big murky plane, raised by __flood(t)
  const floodT = tex(256, 256, (g) => { g.fillStyle = "#6d6a4f"; g.fillRect(0, 0, 256, 256); g.strokeStyle = "rgba(230,220,190,0.3)"; g.lineWidth = 3;
    for (let k = 0; k < 12; k++) { g.beginPath(); const y = rnd() * 256; for (let x = 0; x <= 256; x += 16) g.lineTo(x, y + Math.sin(x / 14 + k) * 4); g.stroke(); } }, [30, 30]);
  const flood = new THREE.Mesh(new THREE.PlaneGeometry(220, 160), new THREE.MeshLambertMaterial({ map: floodT, transparent: true, opacity: 0.88 }));
  flood.rotation.x = -Math.PI / 2; flood.position.set(0, -5, -10); flood.userData.noFg = true; scene.add(flood);

  // ======================= STREET (flooded) =======================
  const SX = STREET_X;
  flat(20, 200, lam({ color: 0x4a4d55 }), SX, 0.0, 0, false);
  const houseCols = [0xe8c78f, 0xd98e62, 0xc9d6d8, 0xf1e2c4, 0xa9c48f, 0xe6b9a0];
  const winT = tex(128, 256, (g, w, h) => { g.fillStyle = "#ffffff00"; g.clearRect(0, 0, w, h);
    for (let f = 0; f < 3; f++) for (const x of [16, 72]) { g.fillStyle = "#2a2a33"; g.fillRect(x, 30 + f * 74, 40, 46); g.fillStyle = "#cfe3f2"; g.fillRect(x + 4, 34 + f * 74, 32, 38); } });
  for (const s of [-1, 1]) for (let k = 0; k < 9; k++) { const z = -80 + k * 20, hh = 8 + (k % 3) * 2.5;
    const hm = [lam({ color: houseCols[(k + (s > 0 ? 3 : 0)) % 6] })];
    const h = box(10, hh, 14, hm[0], SX + s * 16, hh / 2, z);
    const f = new THREE.Mesh(new THREE.PlaneGeometry(13, hh - 1), new THREE.MeshLambertMaterial({ map: winT, transparent: true }));
    f.position.set(SX + s * 10.95, hh / 2, z); f.rotation.y = s > 0 ? -Math.PI / 2 : Math.PI / 2; scene.add(f);
    const roof = new THREE.Mesh(new THREE.ConeGeometry(9.5, 3, 4), lam({ color: 0xb4532f })); roof.position.set(SX + s * 16, hh + 1.5, z); roof.rotation.y = Math.PI / 4; scene.add(roof); void h; }
  // traffic light, lamp posts, a mailbox, car roofs poking out of the water
  box(0.18, 5, 0.18, lam({ color: 0x2a2a33 }), SX + 6.5, 2.5, 4); box(0.6, 1.6, 0.5, lam({ color: 0x2a2a33 }), SX + 6.5, 5, 4);
  const lamps = [];
  for (const [c, y] of [[0xd8202c, 5.5], [0xffd23f, 5.0], [0x2bb34a, 4.5]]) { const m = new THREE.Mesh(new THREE.SphereGeometry(0.17, 12, 8), new THREE.MeshBasicMaterial({ color: c })); m.position.set(SX + 6.5, y, 4.27); scene.add(m); lamps.push(m); }
  for (let k = 0; k < 6; k++) box(0.14, 6, 0.14, lam({ color: 0x5a5f69 }), SX + (k % 2 ? 7.5 : -7.5), 3, -60 + k * 22);
  box(0.6, 1.3, 0.5, lam({ color: 0x1d3f9b }), SX - 7.2, 0.65, 12);
  for (const [x, z, c] of [[SX - 3, -14, 0xd8202c], [SX + 3.2, 20, 0xf4f4f2], [SX - 3.4, 38, 0x2bb3a3]]) { box(1.9, 0.6, 4, lam({ color: c }), x, 0.85, z); box(1.6, 0.5, 2.2, lam({ color: 0x9fc3d6 }), x, 1.4, z); }
  const sflood = new THREE.Mesh(new THREE.PlaneGeometry(60, 220), new THREE.MeshLambertMaterial({ map: floodT, transparent: true, opacity: 0.9 }));
  sflood.rotation.x = -Math.PI / 2; sflood.position.set(SX, 1.0, 0); sflood.userData.noFg = true; scene.add(sflood);

  // ======================= GOLF =======================
  const GX = GOLF_X;
  const fairT = tex(256, 256, (g) => { for (let k = 0; k < 8; k++) { g.fillStyle = k % 2 ? "#6cc650" : "#5cb544"; g.fillRect(0, k * 32, 256, 32); } }, [6, 6]);
  flat(160, 160, lam({ map: fairT }), GX, 0.0, 0);
  const lakeT = tex(256, 256, (g) => { g.fillStyle = "#2f8fb0"; g.fillRect(0, 0, 256, 256); g.strokeStyle = "rgba(255,255,255,0.3)"; g.lineWidth = 3;
    for (let k = 0; k < 12; k++) { g.beginPath(); const y = rnd() * 256; for (let x = 0; x <= 256; x += 16) g.lineTo(x, y + Math.sin(x / 15 + k) * 3); g.stroke(); } }, [6, 6]);
  const lake = new THREE.Mesh(new THREE.CircleGeometry(18, 48), lam({ map: lakeT })); lake.rotation.x = -Math.PI / 2; lake.scale.set(1.6, 1, 1); lake.position.set(GX, 0.03, -6); lake.userData.noFg = true; scene.add(lake);
  const green = new THREE.Mesh(new THREE.CircleGeometry(7, 32), lam({ color: 0x7ad35c })); green.rotation.x = -Math.PI / 2; green.position.set(GX + 34, 0.04, 16); green.userData.noFg = true; scene.add(green);
  box(0.08, 3, 0.08, lam({ color: 0xf4f4f2 }), GX + 34, 1.5, 16); const flag = box(1.1, 0.7, 0.03, redM, GX + 34.55, 2.6, 16);
  const bunker = new THREE.Mesh(new THREE.CircleGeometry(4, 24), lam({ color: 0xead9a8 })); bunker.rotation.x = -Math.PI / 2; bunker.scale.set(1.5, 1, 1); bunker.position.set(GX + 24, 0.04, 22); bunker.userData.noFg = true; scene.add(bunker);
  for (let k = 0; k < 14; k++) tree(GX - 60 + k * 9 + rnd() * 3, -40 - rnd() * 10, 1.4);
  for (let k = 0; k < 6; k++) tree(GX + 45 + rnd() * 10, -20 + k * 9, 1.2);

  const lvl = () => (typeof globalThis.__flood === "function" ? globalThis.__flood : () => 0);
  const crowd = (t) => {
    waterT.offset.set((t * 0.01) % 1, (t * 0.006) % 1); riverT.offset.x = (t * 0.03) % 1; floodT.offset.set((t * 0.012) % 1, (t * 0.008) % 1); lakeT.offset.x = (t * 0.005) % 1;
    const h = lvl()(t); flood.position.y = h <= 0 ? -5 : -0.5 + h;              // h = metres above the river surface
    river.position.y = -0.52;
    lamps.forEach((m, k) => (m.visible = Math.floor(t * 1.2) % 3 === k));
    flag.rotation.y = Math.sin(t * 2) * 0.3;
    clouds.forEach((g, k) => (g.position.x += 0.002 * (k % 2 ? 1 : -1)));
  };
  const envAt = (cam) => { const storm = cam.position.x > STREET_X - 60;
    scene.background = storm ? skyStorm : skySun; scene.fog.color.setHex(storm ? 0xaeb6c0 : 0xdceefa); };
  return { crowd, flashAt: () => {}, boardsAt: () => {}, nets: {}, envAt };
}
