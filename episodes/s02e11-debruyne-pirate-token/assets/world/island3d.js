// COULD? 3D world: a sunny cartoon pirate island (our own design - no game assets). Sand disc in a turquoise sea, palm trees,
// wooden huts, treasure chests, a pirate ship at anchor, gulls. buildIsland(THREE, scene) -> { crowd(t), flashAt, boardsAt, nets }
// (same interface as buildStadium). ISLAND.r = sand radius; the action happens around the centre.
export const ISLAND = { r: 34 };

export function buildIsland(THREE, scene) {
  const mulberry = (a) => () => { a |= 0; a = (a + 0x6d2b79f5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  const rnd = mulberry(23);
  const canvasTex = (w, h, draw, rep) => { const c = document.createElement("canvas"); c.width = w; c.height = h; draw(c.getContext("2d"), w, h);
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8;
    if (rep) { t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(rep[0], rep[1]); } return t; };

  // afternoon sky + sun
  scene.background = canvasTex(8, 512, (g, w, h) => { const gr = g.createLinearGradient(0, 0, 0, h);
    gr.addColorStop(0, "#3f8fe0"); gr.addColorStop(0.55, "#8cc8f2"); gr.addColorStop(1, "#ffe9c2"); g.fillStyle = gr; g.fillRect(0, 0, w, h); });
  scene.fog = new THREE.Fog(0xbfe3f2, 120, 600);
  scene.add(new THREE.AmbientLight(0xffffff, 0.62));
  scene.add(new THREE.HemisphereLight(0xffffff, 0xe0c58f, 0.6));
  const sun = new THREE.DirectionalLight(0xfff2d6, 1.2); sun.position.set(60, 90, 40); scene.add(sun);

  // sea with a moving wave pattern
  const waveTex = canvasTex(256, 256, (g) => { g.fillStyle = "#1fa3c6"; g.fillRect(0, 0, 256, 256);
    g.strokeStyle = "rgba(255,255,255,0.35)"; g.lineWidth = 4;
    for (let k = 0; k < 9; k++) { const y = 14 + k * 28; g.beginPath(); for (let x = 0; x <= 256; x += 16) g.lineTo(x, y + Math.sin(x / 20 + k) * 5); g.stroke(); } }, [60, 60]);
  const sea = new THREE.Mesh(new THREE.PlaneGeometry(1400, 1400), new THREE.MeshLambertMaterial({ map: waveTex }));
  sea.rotation.x = -Math.PI / 2; sea.position.y = -0.35; sea.userData.noFg = true; scene.add(sea);
  // shallow water ring + wet sand + dry sand
  const ring = (r, col, y) => { const m = new THREE.Mesh(new THREE.CircleGeometry(r, 72), new THREE.MeshLambertMaterial({ color: col }));
    m.rotation.x = -Math.PI / 2; m.position.y = y; m.userData.noFg = true; scene.add(m); return m; };
  ring(ISLAND.r + 9, 0x5fd3df, -0.3); ring(ISLAND.r + 2.5, 0xd8b77a, -0.05);
  const sandTex = canvasTex(256, 256, (g) => { g.fillStyle = "#f0d59a"; g.fillRect(0, 0, 256, 256);
    for (let k = 0; k < 900; k++) { g.fillStyle = k % 2 ? "rgba(190,150,90,0.25)" : "rgba(255,245,215,0.35)"; g.fillRect(rnd() * 256, rnd() * 256, 2, 2); } }, [14, 14]);
  const sand = new THREE.Mesh(new THREE.CircleGeometry(ISLAND.r, 72), new THREE.MeshLambertMaterial({ map: sandTex }));
  sand.rotation.x = -Math.PI / 2; sand.position.y = 0; sand.userData.noFg = true; scene.add(sand);

  // the island interior is grass (sand only at the beach), with rocks, bushes and a few wooden "builds"
  const grassTex = canvasTex(256, 256, (g) => { g.fillStyle = "#5cbf3a"; g.fillRect(0, 0, 256, 256);
    for (let k = 0; k < 700; k++) { g.fillStyle = k % 3 ? "rgba(40,120,30,0.35)" : "rgba(170,230,110,0.4)"; g.fillRect(rnd() * 256, rnd() * 256, 3, 6); } }, [10, 10]);
  const grass = new THREE.Mesh(new THREE.CircleGeometry(ISLAND.r - 9, 64), new THREE.MeshLambertMaterial({ map: grassTex }));
  grass.rotation.x = -Math.PI / 2; grass.position.y = 0.02; grass.userData.noFg = true; scene.add(grass);
  const rockM = new THREE.MeshLambertMaterial({ color: 0x9aa1a8, flatShading: true }), rockD = new THREE.MeshLambertMaterial({ color: 0x7c838b, flatShading: true });
  [[-26, -20, 4], [28, -14, 3.2], [-31, 10, 2.6], [24, 24, 3.6], [-8, -31, 2.4], [31, 4, 2.2], [-20, 26, 2.8]].forEach(([x, z, r], k) => {
    const m = new THREE.Mesh(new THREE.DodecahedronGeometry(r, 0), k % 2 ? rockM : rockD); m.position.set(x, r * 0.45, z); m.rotation.set(rnd(), rnd(), rnd()); scene.add(m); });
  const bushM = new THREE.MeshLambertMaterial({ color: 0x3e9b2f, flatShading: true }), bushL = new THREE.MeshLambertMaterial({ color: 0x55b83c, flatShading: true });
  for (let k = 0; k < 26; k++) { const a = rnd() * 6.28, r = 6 + rnd() * 19, b = new THREE.Group();
    for (let q = 0; q < 3; q++) { const m = new THREE.Mesh(new THREE.IcosahedronGeometry(0.55 + rnd() * 0.4, 0), q % 2 ? bushM : bushL); m.position.set((q - 1) * 0.55, 0.45, (rnd() - 0.5) * 0.5); b.add(m); }
    b.position.set(Math.cos(a) * r, 0, Math.sin(a) * r); if (Math.hypot(b.position.x - 2, b.position.z) > 5 && Math.hypot(b.position.x - 9, b.position.z + 4.5) > 3) scene.add(b); }
  // wooden build pieces (a little 2-storey "build" and a ramp), grid-textured planks
  const plankTex = canvasTex(128, 128, (g) => { g.fillStyle = "#c98b4a"; g.fillRect(0, 0, 128, 128); g.strokeStyle = "#8a5226"; g.lineWidth = 6;
    g.strokeRect(3, 3, 122, 122); for (let k = 1; k < 4; k++) { g.beginPath(); g.moveTo(0, k * 32); g.lineTo(128, k * 32); g.stroke(); }
    g.lineWidth = 3; g.beginPath(); g.moveTo(64, 0); g.lineTo(64, 32); g.moveTo(32, 32); g.lineTo(32, 64); g.moveTo(96, 64); g.lineTo(96, 96); g.stroke(); });
  const plank = new THREE.MeshLambertMaterial({ map: plankTex, side: THREE.DoubleSide });
  const wall = (x, y, z, ry) => { const m = new THREE.Mesh(new THREE.PlaneGeometry(4, 3.2), plank); m.position.set(x, y + 1.6, z); m.rotation.y = ry; scene.add(m); };
  const floor = (x, y, z) => { const m = new THREE.Mesh(new THREE.PlaneGeometry(4, 4), plank); m.rotation.x = -Math.PI / 2; m.position.set(x, y, z); scene.add(m); };
  for (const [bx, bz] of [[-12, -9], [16, 6]]) for (const lvl of [0, 3.2]) {
    wall(bx, lvl, bz - 2, 0); wall(bx + 2, lvl, bz, Math.PI / 2); wall(bx - 2, lvl, bz, Math.PI / 2); if (lvl) floor(bx, lvl, bz); }
  const ramp = new THREE.Mesh(new THREE.PlaneGeometry(4, 5.2), plank); ramp.position.set(-12, 1.6, -4.9); ramp.rotation.x = -Math.PI / 2 + 0.66; scene.add(ramp);

  // loot beams in rarity colours over the scattered chests (gold, purple, blue) - the genre's "loot here" signal
  const beamM = (col) => new THREE.MeshBasicMaterial({ color: col, transparent: true, opacity: 0.45, depthWrite: false, side: THREE.DoubleSide });
  const beams = [];
  [[-9, -6, 0xffc93c], [11, 4, 0xb36bff], [-5, 11, 0x3fa9ff], [15, -8, 0xffc93c], [-16, 3, 0xb36bff], [3, -14, 0x3fa9ff], [24, 0, 0xffc93c]].forEach(([x, z, col]) => {
    const b = new THREE.Mesh(new THREE.CylinderGeometry(0.35, 0.6, 14, 12, 1, true), beamM(col)); b.position.set(x, 7, z); b.userData.noFg = true; scene.add(b); beams.push(b); });

  // the storm: a huge purple wall closing around the island, with moving streaks
  const stormTex = canvasTex(512, 256, (g, w, h) => { const gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, "rgba(120,40,200,0.0)");
    gr.addColorStop(0.5, "rgba(150,60,230,0.55)"); gr.addColorStop(1, "rgba(110,30,190,0.75)"); g.fillStyle = gr; g.fillRect(0, 0, w, h);
    g.strokeStyle = "rgba(230,200,255,0.55)"; g.lineWidth = 3; for (let k = 0; k < 40; k++) { const x = rnd() * w; g.beginPath(); g.moveTo(x, 0); g.lineTo(x + 30, h); g.stroke(); } }, [6, 1]);
  const storm = new THREE.Mesh(new THREE.CylinderGeometry(125, 125, 64, 96, 1, true), new THREE.MeshBasicMaterial({ map: stormTex, transparent: true, side: THREE.DoubleSide, depthWrite: false }));
  storm.position.y = 26; storm.userData.noFg = true; scene.add(storm);
  // puffy cartoon clouds
  const cloudM = new THREE.MeshLambertMaterial({ color: 0xffffff, flatShading: true });
  for (let k = 0; k < 9; k++) { const g = new THREE.Group(), a = rnd() * 6.28, r = 60 + rnd() * 50;
    for (let q = 0; q < 4; q++) { const m = new THREE.Mesh(new THREE.IcosahedronGeometry(4 + rnd() * 3, 1), cloudM); m.position.set(q * 4.5 - 7, rnd() * 2, rnd() * 3); g.add(m); }
    g.position.set(Math.cos(a) * r, 34 + rnd() * 16, Math.sin(a) * r); g.lookAt(0, g.position.y, 0); g.userData.noFg = true; scene.add(g); }

  // palm trees: curved trunk of stacked segments, a crown of leaves, coconuts
  const trunkM = new THREE.MeshLambertMaterial({ color: 0x9a6b3e }), leafM = new THREE.MeshLambertMaterial({ color: 0x2f9e44, side: THREE.DoubleSide }),
    leafD = new THREE.MeshLambertMaterial({ color: 0x23803a, side: THREE.DoubleSide }), nutM = new THREE.MeshLambertMaterial({ color: 0x5a3a1e });
  const palm = (x, z, h, lean) => {
    const g = new THREE.Group(); g.position.set(x, 0, z); g.rotation.y = rnd() * 6.28;
    let px = 0, py = 0; const n = 8;
    for (let k = 0; k < n; k++) { const s = new THREE.Mesh(new THREE.CylinderGeometry(0.22 - k * 0.012, 0.26 - k * 0.012, h / n + 0.05, 8), trunkM);
      const bend = (k / n) * (k / n) * lean; s.position.set(px + bend, py + h / n / 2, 0); s.rotation.z = -lean * 0.12 * (k / n); g.add(s); py += h / n; px = bend; }
    for (let k = 0; k < 7; k++) { const leaf = new THREE.Mesh(new THREE.PlaneGeometry(3.6, 0.9), k % 2 ? leafM : leafD);
      leaf.position.set(px + Math.cos(k * 0.9) * 1.5, py - 0.3, Math.sin(k * 0.9) * 1.5); leaf.rotation.y = -k * 0.9; leaf.rotation.z = -0.45; g.add(leaf); }
    for (let k = 0; k < 3; k++) { const c = new THREE.Mesh(new THREE.SphereGeometry(0.2, 8, 8), nutM); c.position.set(px + Math.cos(k * 2.1) * 0.3, py - 0.35, Math.sin(k * 2.1) * 0.3); g.add(c); }
    scene.add(g);
  };
  const PALMS = [[-14, -12], [-20, -4], [-24, 8], [-12, 14], [6, 18], [16, 12], [22, -2], [18, -14], [4, -20], [-6, -24], [-28, -14], [28, 8], [-2, 24], [26, -20], [-30, 2], [10, 26]];
  PALMS.forEach(([x, z]) => palm(x, z, 6 + rnd() * 3, 1.2 + rnd() * 1.4));

  // wooden huts on stilts with thatched roofs
  const woodM = new THREE.MeshLambertMaterial({ color: 0x8a5a33 }), woodD = new THREE.MeshLambertMaterial({ color: 0x6b4426 }), thatch = new THREE.MeshLambertMaterial({ color: 0xc9a25a });
  const hut = (x, z, ry) => { const g = new THREE.Group(); g.position.set(x, 0, z); g.rotation.y = ry;
    for (const [sx, sz] of [[-1.6, -1.4], [1.6, -1.4], [-1.6, 1.4], [1.6, 1.4]]) { const p = new THREE.Mesh(new THREE.BoxGeometry(0.22, 1, 0.22), woodD); p.position.set(sx, 0.5, sz); g.add(p); }
    const body = new THREE.Mesh(new THREE.BoxGeometry(3.6, 2.4, 3.2), woodM); body.position.y = 2.2; g.add(body);
    const door = new THREE.Mesh(new THREE.BoxGeometry(0.9, 1.5, 0.05), woodD); door.position.set(0, 1.85, 1.63); g.add(door);
    const roof = new THREE.Mesh(new THREE.ConeGeometry(3.3, 2.0, 4), thatch); roof.position.y = 4.4; roof.rotation.y = Math.PI / 4; g.add(roof);
    scene.add(g); };
  [[-17, -17, 0.4], [14, -18, -0.5], [-22, 14, 2.6], [20, 18, -2.4], [-4, -28, 0.1]].forEach(([x, z, r]) => hut(x, z, r));

  // decorative closed treasure chests scattered around
  const chestM = new THREE.MeshLambertMaterial({ color: 0x8b4f22 }), goldM = new THREE.MeshLambertMaterial({ color: 0xf3c55b });
  const chest = (x, z, ry) => { const g = new THREE.Group(); g.position.set(x, 0, z); g.rotation.y = ry;
    const b = new THREE.Mesh(new THREE.BoxGeometry(1.0, 0.55, 0.65), chestM); b.position.y = 0.28; g.add(b);
    const lid = new THREE.Mesh(new THREE.CylinderGeometry(0.33, 0.33, 1.0, 12, 1, false, 0, Math.PI), chestM); lid.rotation.z = Math.PI / 2; lid.position.y = 0.56; g.add(lid);
    for (const sx of [-0.35, 0.35]) { const band = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.6, 0.68), goldM); band.position.set(sx, 0.3, 0); g.add(band); }
    scene.add(g); };
  [[-9, -6, 0.3], [11, 4, -0.6], [-5, 11, 1.2], [15, -8, 0.9], [-16, 3, -0.2], [3, -14, 2.0], [-12, 22, 0.4], [24, 0, 1.4]].forEach(([x, z, r]) => chest(x, z, r));

  // pirate ship at anchor
  const ship = new THREE.Group(); ship.position.set(-70, -0.2, -55); ship.rotation.y = 0.6;
  const hull = new THREE.Mesh(new THREE.BoxGeometry(22, 4, 7), new THREE.MeshLambertMaterial({ color: 0x5a3519 })); hull.position.y = 1.6; ship.add(hull);
  const bow = new THREE.Mesh(new THREE.ConeGeometry(3.6, 6, 4), new THREE.MeshLambertMaterial({ color: 0x5a3519 })); bow.rotation.z = -Math.PI / 2; bow.position.set(14, 1.8, 0); ship.add(bow);
  for (const mx of [-5, 3]) { const mast = new THREE.Mesh(new THREE.CylinderGeometry(0.3, 0.35, 16, 8), woodD); mast.position.set(mx, 10, 0); ship.add(mast);
    const sail = new THREE.Mesh(new THREE.PlaneGeometry(7, 8), new THREE.MeshLambertMaterial({ color: 0xf2ead8, side: THREE.DoubleSide })); sail.position.set(mx, 10, 0.4); sail.rotation.y = Math.PI / 2; ship.add(sail); }
  const flag = new THREE.Mesh(new THREE.PlaneGeometry(2.4, 1.5), new THREE.MeshLambertMaterial({ color: 0x14141f, side: THREE.DoubleSide })); flag.position.set(-5, 18.6, 0); flag.rotation.y = Math.PI / 2; ship.add(flag);
  scene.add(ship);

  // a few gulls circling (little white chevrons)
  const gullM = new THREE.MeshBasicMaterial({ color: 0xffffff, side: THREE.DoubleSide }), gulls = [];
  for (let k = 0; k < 6; k++) { const g = new THREE.Mesh(new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(-0.6, 0.15, 0), new THREE.Vector3(0, 0, 0), new THREE.Vector3(0.6, 0.15, 0),
      new THREE.Vector3(0, 0.05, 0)]).setIndex([0, 1, 3, 1, 2, 3]), gullM); g.userData.noFg = true; scene.add(g); gulls.push([g, rnd() * 6.28, 18 + rnd() * 30, 14 + rnd() * 8]); }

  const crowd = (t) => {
    waveTex.offset.set((t * 0.004) % 1, (t * 0.002) % 1);
    stormTex.offset.x = (t * 0.02) % 1; storm.rotation.y = t * 0.01;
    beams.forEach((b, k) => { b.material.opacity = 0.4 + Math.sin(t * 3 + k) * 0.1; });
    for (const [g, ph, r, y] of gulls) { const a = ph + t * 0.25; g.position.set(Math.cos(a) * r, y + Math.sin(t + ph) * 0.6, Math.sin(a) * r); g.rotation.y = -a; }
  };
  return { crowd, flashAt: () => {}, boardsAt: () => {}, nets: {} };
}
