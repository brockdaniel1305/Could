// COULD? 3D world: Pamplona's old town on a bull-run morning. A cobbled street along x (bulls run towards +x),
// double wooden fences at z = +-3 with spectators behind them, painted houses with crowded balconies, and the bullring at the end.
// buildPamplona(THREE, scene) -> { crowd(t, amp), flashAt(), boardsAt(), nets: {} }  (same interface as buildStadium)
export const STREET = { x0: -90, x1: 47, half: 3.0, ring: [74, 0], ringR: 24 };

export function buildPamplona(THREE, scene) {
  const mulberry = (a) => () => { a |= 0; a = (a + 0x6d2b79f5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  const rnd = mulberry(11);
  const canvasTex = (w, h, draw, rep) => { const c = document.createElement("canvas"); c.width = w; c.height = h; draw(c.getContext("2d"), w, h);
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8;
    if (rep) { t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(rep[0], rep[1]); } return t; };

  // morning sky + light
  scene.background = canvasTex(8, 512, (g, w, h) => { const gr = g.createLinearGradient(0, 0, 0, h);
    gr.addColorStop(0, "#5aa7e6"); gr.addColorStop(0.6, "#a9d3f2"); gr.addColorStop(1, "#f3e7cf"); g.fillStyle = gr; g.fillRect(0, 0, w, h); });
  scene.fog = new THREE.Fog(0xe9e2d2, 70, 260);
  scene.add(new THREE.AmbientLight(0xffffff, 0.6));
  scene.add(new THREE.HemisphereLight(0xffffff, 0xc9a77a, 0.65));
  const sun = new THREE.DirectionalLight(0xfff0d0, 1.15); sun.position.set(40, 70, 30); scene.add(sun);

  const { x0, x1, half } = STREET, L = x1 - x0, cx = (x0 + x1) / 2;
  // cobbles
  const cobble = canvasTex(256, 256, (g) => { g.fillStyle = "#8d8378"; g.fillRect(0, 0, 256, 256);
    for (let y = 0; y < 8; y++) for (let x = 0; x < 8; x++) { const v = 120 + ((x * 7 + y * 13) % 5) * 9;
      g.fillStyle = `rgb(${v + 22},${v + 12},${v})`; g.beginPath(); g.ellipse(x * 32 + 16 + (y % 2) * 8, y * 32 + 16, 14, 13, 0, 0, 6.3); g.fill(); } }, [L / 2.2, 6]);
  const street = new THREE.Mesh(new THREE.PlaneGeometry(L, 13), new THREE.MeshLambertMaterial({ map: cobble }));
  street.rotation.x = -Math.PI / 2; street.position.set(cx, 0, 0); scene.add(street);

  // double wooden fences (the bull run barrier)
  const wood = new THREE.MeshLambertMaterial({ color: 0x8a5a33 }), woodD = new THREE.MeshLambertMaterial({ color: 0x6e4526 });
  for (const s of [-1, 1]) for (const off of [0, 0.6]) {
    const z = s * (half + off);
    for (const y of [0.3, 0.7, 1.1, 1.5]) { const p = new THREE.Mesh(new THREE.BoxGeometry(L, 0.16, 0.07), y > 1 ? woodD : wood); p.position.set(cx, y, z); scene.add(p); }
    const n = Math.floor(L / 1.6), posts = new THREE.InstancedMesh(new THREE.BoxGeometry(0.16, 1.75, 0.16), woodD, n), m = new THREE.Object3D();
    for (let i = 0; i < n; i++) { m.position.set(x0 + i * 1.6, 0.87, z); m.updateMatrix(); posts.setMatrixAt(i, m.matrix); } scene.add(posts);
  }

  // houses: facades with windows, green shutters, iron balconies; terracotta roofs
  const PAL = ["#e8c78f", "#f1e2c4", "#d98e62", "#c9d6d8", "#e6b9a0", "#f3d68a"];
  const facade = PAL.map((col) => canvasTex(256, 512, (g, w, h) => {
    g.fillStyle = col; g.fillRect(0, 0, w, h);
    for (let f = 0; f < 4; f++) { const y = 40 + f * 118;
      for (const x of [40, 150]) { g.fillStyle = "#2f5d3a"; g.fillRect(x - 14, y, 14, 70); g.fillRect(x + 56, y, 14, 70);
        g.fillStyle = "#2a2a33"; g.fillRect(x, y, 56, 70); g.fillStyle = "#f6efe2"; g.fillRect(x + 4, y + 4, 22, 30); g.fillRect(x + 30, y + 4, 22, 30);
        g.strokeStyle = "#1a1a1e"; g.lineWidth = 4; g.strokeRect(x - 10, y + 52, 76, 30); g.beginPath();
        for (let k = 0; k < 8; k++) { g.moveTo(x - 10 + k * 10, y + 52); g.lineTo(x - 10 + k * 10, y + 82); } g.stroke(); } }
    g.fillStyle = "rgba(0,0,0,0.08)"; g.fillRect(0, h - 40, w, 40); }));
  const roof = new THREE.MeshLambertMaterial({ color: 0xb4532f });
  const balconyY = [4.2, 7.6, 11.0];
  const people = []; // [x, y, z, colour, phase]
  const SHIRT = [0xf6f4ef, 0xf6f4ef, 0xf6f4ef, 0xd8202c, 0xf6f4ef, 0x2a5aa8, 0xf6f4ef];
  for (const s of [-1, 1]) {
    let x = x0;
    while (x < x1 - 2) {
      const w = 6 + rnd() * 3, hgt = 12 + rnd() * 6, k = (rnd() * PAL.length) | 0;
      const mat = new THREE.MeshLambertMaterial({ map: facade[k].clone() }); mat.map.needsUpdate = true; mat.map.wrapS = mat.map.wrapT = THREE.RepeatWrapping;
      mat.map.repeat.set(w / 6, hgt / 13);
      const b = new THREE.Mesh(new THREE.BoxGeometry(w, hgt, 9), [mat, mat, roof, roof, mat, mat]);
      b.position.set(x + w / 2, hgt / 2, s * (6.2 + 4.5)); scene.add(b);
      // red banners on some balconies
      if (rnd() < 0.45) { const ban = new THREE.Mesh(new THREE.PlaneGeometry(1.4, 2.2), new THREE.MeshLambertMaterial({ color: rnd() < 0.5 ? 0xd8202c : 0xf6f4ef, side: THREE.DoubleSide }));
        ban.position.set(x + 1 + rnd() * (w - 2), balconyY[(rnd() * 3) | 0] - 1.2, s * 6.05); scene.add(ban); }
      for (const y of balconyY) for (let px = x + 0.5; px < x + w - 0.4; px += 0.75) if (rnd() < 0.62) people.push([px, y, s * 5.95, SHIRT[(rnd() * SHIRT.length) | 0], rnd()]);
      x += w + 0.05;
    }
    // spectators standing behind the fences
    for (let r = 0; r < 3; r++) for (let px = x0 + 1; px < x1 - 1; px += 0.62) if (rnd() < 0.8) people.push([px + rnd() * 0.2, 0.45 * r, s * (4.1 + r * 0.6), SHIRT[(rnd() * SHIRT.length) | 0], rnd()]);
  }

  // bullring: sand, red barrier, stepped stands with spectators; open towards the street
  const [rx, rz] = STREET.ring, R = STREET.ringR;
  const sand = new THREE.Mesh(new THREE.CircleGeometry(R + 2, 64), new THREE.MeshLambertMaterial({ color: 0xd9b37a }));
  sand.rotation.x = -Math.PI / 2; sand.position.set(rx, 0.01, rz); scene.add(sand);
  const gap = 0.16; // half-angle of the entrance (towards -x)
  const barrier = new THREE.Mesh(new THREE.CylinderGeometry(R, R, 1.5, 64, 1, true, Math.PI / 2 + gap - Math.PI, 2 * Math.PI - 2 * gap),
    new THREE.MeshLambertMaterial({ color: 0xa3262a, side: THREE.DoubleSide })); barrier.position.set(rx, 0.75, rz); barrier.rotation.y = 0; scene.add(barrier);
  const prof = [new THREE.Vector2(R + 0.3, 0), new THREE.Vector2(R + 0.3, 2.2)];
  for (let r = 0; r < 22; r++) { prof.push(new THREE.Vector2(R + 1 + r * 0.85, 2.2 + r * 0.6)); prof.push(new THREE.Vector2(R + 1 + (r + 1) * 0.85, 2.2 + r * 0.6)); }
  prof.push(new THREE.Vector2(R + 21, 16), new THREE.Vector2(R + 21, 0));
  const stands = new THREE.Mesh(new THREE.LatheGeometry(prof, 72, Math.PI / 2 + gap * 1.6 - Math.PI, 2 * Math.PI - 2 * gap * 1.6),
    new THREE.MeshLambertMaterial({ color: 0xe9dcc4, side: THREE.DoubleSide })); stands.position.set(rx, 0, rz); scene.add(stands);
  const arches = new THREE.Mesh(new THREE.CylinderGeometry(R + 21, R + 21, 4, 72, 1, true), new THREE.MeshLambertMaterial({ color: 0xc98b52, side: THREE.DoubleSide }));
  arches.position.set(rx, 17.5, rz); scene.add(arches);
  for (let r = 0; r < 22; r++) { const rr = R + 1.4 + r * 0.85, n = Math.floor((2 * Math.PI * rr) / 0.62);
    for (let i = 0; i < n; i++) { const a = (i / n) * Math.PI * 2; if (Math.abs(Math.atan2(Math.sin(a - Math.PI), Math.cos(a - Math.PI))) < gap * 2) continue;
      if (rnd() < 0.85) people.push([rx + Math.cos(a) * rr, 2.2 + r * 0.6, rz + Math.sin(a) * rr, SHIRT[(rnd() * SHIRT.length) | 0], rnd()]); } }

  // instanced people: body + head (+ red neckerchief on the white shirts)
  const N = people.length;
  const bodies = new THREE.InstancedMesh(new THREE.BoxGeometry(0.46, 0.6, 0.3), new THREE.MeshLambertMaterial(), N);
  const heads = new THREE.InstancedMesh(new THREE.BoxGeometry(0.3, 0.3, 0.3), new THREE.MeshLambertMaterial(), N);
  const scarves = new THREE.InstancedMesh(new THREE.BoxGeometry(0.34, 0.1, 0.34), new THREE.MeshLambertMaterial({ color: 0xd8202c }), N);
  const SKIN = [0xf1c9a5, 0xe0ac7e, 0xc68863, 0x8d5a3b];
  const col = new THREE.Color(), tmp = new THREE.Object3D();
  people.forEach((p, i) => { bodies.setColorAt(i, col.setHex(p[3])); heads.setColorAt(i, col.setHex(SKIN[(p[4] * 4) | 0])); });
  scene.add(bodies, heads, scarves);
  const crowd = (t, amp) => {
    for (let i = 0; i < N; i++) { const p = people[i], hop = Math.abs(Math.sin(t * 5 + p[4] * 6.28)) * amp * (0.6 + p[4] * 0.8);
      tmp.position.set(p[0], p[1] + 0.3 + hop, p[2]); tmp.updateMatrix(); bodies.setMatrixAt(i, tmp.matrix);
      tmp.position.y += 0.33; tmp.updateMatrix(); scarves.setMatrixAt(i, tmp.matrix);
      tmp.position.y += 0.14; tmp.updateMatrix(); heads.setMatrixAt(i, tmp.matrix); }
    bodies.instanceMatrix.needsUpdate = heads.instanceMatrix.needsUpdate = scarves.instanceMatrix.needsUpdate = true;
  };
  return { crowd, flashAt: () => {}, boardsAt: () => {}, nets: {} };
}
