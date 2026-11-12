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
    for (const [g, ph, r, y] of gulls) { const a = ph + t * 0.25; g.position.set(Math.cos(a) * r, y + Math.sin(t + ph) * 0.6, Math.sin(a) * r); g.rotation.y = -a; }
  };
  return { crowd, flashAt: () => {}, boardsAt: () => {}, nets: {} };
}
