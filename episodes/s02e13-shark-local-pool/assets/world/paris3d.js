// COULD? 3D world: Paris, 14 July 1789 - a stone-and-timber street with slate roofs, barricades of barrels and carts, tricolour
// garlands and banners, smoke over the roofs, Notre-Dame-like towers at one end and the Bastille at the other.
// The street sits far from the origin (x ~ -2000) so a second world (the stadium) can live at the origin in the same scene.
// buildParis(THREE, scene) -> { crowd(t, amp), boardsAt(), flashAt(), nets, door(f), lights }
export const PARIS = { x0: -2110, x1: -1975, half: 3.2, bastille: [-1946, 0] };

export function buildParis(THREE, scene) {
  const mulberry = (a) => () => { a |= 0; a = (a + 0x6d2b79f5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  const rnd = mulberry(1789), R2 = mulberry(14);
  const tmp = new THREE.Object3D(), col = new THREE.Color();
  const tex = (w, h, draw, rep) => { const c = document.createElement("canvas"); c.width = w; c.height = h; draw(c.getContext("2d"), w, h);
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8;
    if (rep) { t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(rep[0], rep[1]); } return t; };
  const lights = [];
  const light = (l) => { scene.add(l); lights.push(l); return l; };
  light(new THREE.AmbientLight(0xffffff, 0.55));
  light(new THREE.HemisphereLight(0xfff0dc, 0x7a5a3c, 0.65));
  const sun = light(new THREE.DirectionalLight(0xffc98a, 1.2)); sun.position.set(-2040, 60, 50); sun.target.position.set(-2040, 0, 0); scene.add(sun.target);
  const sky = tex(8, 512, (g, w, h) => { const gr = g.createLinearGradient(0, 0, 0, h);
    gr.addColorStop(0, "#3d5f96"); gr.addColorStop(0.45, "#c98a74"); gr.addColorStop(0.75, "#f0b36c"); gr.addColorStop(1, "#f7dcb0"); g.fillStyle = gr; g.fillRect(0, 0, w, h); });
  const fog = new THREE.Fog(0xe8c9a3, 90, 520);

  const { x0, x1, half } = PARIS, L = x1 - x0, cx = (x0 + x1) / 2;
  const cobble = tex(256, 256, (g) => { g.fillStyle = "#7c7469"; g.fillRect(0, 0, 256, 256);
    for (let y = 0; y < 8; y++) for (let x = 0; x < 8; x++) { const v = 108 + ((x * 5 + y * 11) % 5) * 9;
      g.fillStyle = `rgb(${v + 14},${v + 8},${v})`; g.fillRect(x * 32 + 2 + (y % 2) * 14, y * 32 + 2, 28, 28); } }, [L / 2, 8]);
  const street = new THREE.Mesh(new THREE.PlaneGeometry(L + 70, 16), new THREE.MeshLambertMaterial({ map: cobble }));
  street.rotation.x = -Math.PI / 2; street.position.set(cx + 30, 0, 0); street.userData.noFg = true; scene.add(street);
  const square = new THREE.Mesh(new THREE.PlaneGeometry(60, 60), new THREE.MeshLambertMaterial({ map: cobble }));
  square.rotation.x = -Math.PI / 2; square.position.set(x1 + 18, 0.005, 0); square.userData.noFg = true; scene.add(square);

  // facades: cream stone with grey-blue shutters, or white plaster with timber beams; shop fronts on the ground floor
  const STONE = ["#e6d9bf", "#d8c9aa", "#efe4cc", "#cfc2a6"];
  const facade = (base, timber) => tex(256, 512, (g, w, h) => {
    g.fillStyle = base; g.fillRect(0, 0, w, h);
    if (timber) { g.strokeStyle = "#5a3b22"; g.lineWidth = 10; for (let y = 0; y < h; y += 128) { g.beginPath(); g.moveTo(0, y); g.lineTo(w, y); g.stroke(); }
      for (let x = 0; x <= w; x += 64) { g.beginPath(); g.moveTo(x, 0); g.lineTo(x, h - 110); g.stroke(); }
      g.beginPath(); for (let y = 0; y < h - 128; y += 128) { g.moveTo(0, y); g.lineTo(64, y + 128); g.moveTo(256, y); g.lineTo(192, y + 128); } g.stroke(); }
    for (let f = 0; f < 3; f++) { const y = 40 + f * 128;
      for (const x of [34, 150]) { g.fillStyle = "#4b6a8a"; g.fillRect(x - 14, y, 14, 76); g.fillRect(x + 72, y, 14, 76);
        g.fillStyle = "#2b2b33"; g.fillRect(x, y, 72, 76); g.fillStyle = "#f3e7c9"; g.fillRect(x + 5, y + 5, 28, 32); g.fillRect(x + 39, y + 5, 28, 32);
        g.fillStyle = "#c9a26a"; g.fillRect(x, y + 34, 72, 4); } }
    g.fillStyle = "#6b3e22"; g.fillRect(0, h - 110, w, 110); g.fillStyle = "#e8c46a"; g.fillRect(20, h - 96, 96, 70); g.fillRect(140, h - 96, 96, 70);
    g.fillStyle = "#3a2414"; g.fillRect(0, h - 120, w, 12); });
  const facades = STONE.map((c, i) => facade(c, i % 2 === 1));
  const slate = new THREE.MeshLambertMaterial({ color: 0x55606f });
  const people = [];
  const SHIRT = [0xf3efe4, 0x2b4f8f, 0xc22f2f, 0xf3efe4, 0x6b4a2a, 0x2b4f8f, 0xd9c08a];
  const floorsY = [3.9, 7.3, 10.7];
  for (const s of [-1, 1]) {
    let x = x0;
    while (x < x1 - 2) {
      const w = 6 + rnd() * 3, hgt = 11 + rnd() * 5, k = (rnd() * facades.length) | 0;
      const mat = new THREE.MeshLambertMaterial({ map: facades[k].clone() }); mat.map.needsUpdate = true; mat.map.wrapS = mat.map.wrapT = THREE.RepeatWrapping; mat.map.repeat.set(w / 6, 1);
      const b = new THREE.Mesh(new THREE.BoxGeometry(w, hgt, 9), [mat, mat, slate, slate, mat, mat]); b.position.set(x + w / 2, hgt / 2, s * (6.2 + 4.5)); scene.add(b);
      const roof = new THREE.Mesh(new THREE.CylinderGeometry(0.01, 6.6, 4, 4, 1), slate); roof.rotation.y = Math.PI / 4; roof.scale.set(w / 9.2, 1, 1.05);
      roof.position.set(x + w / 2, hgt + 2, s * 10.7); scene.add(roof);
      const chim = new THREE.Mesh(new THREE.BoxGeometry(0.8, 2.4, 0.8), new THREE.MeshLambertMaterial({ color: 0x8a5a44 })); chim.position.set(x + 1 + rnd() * (w - 2), hgt + 3, s * 9); scene.add(chim);
      for (const y of floorsY) for (let px = x + 0.6; px < x + w - 0.4; px += 0.8) if (rnd() < 0.5) people.push([px, y - 0.4, s * 5.95, SHIRT[(rnd() * SHIRT.length) | 0], rnd()]);
      x += w + 0.05;
    }
    for (let r = 0; r < 3; r++) for (let px = x0 + 1; px < x1 + 6; px += 0.6) if (rnd() < 0.72) people.push([px + rnd() * 0.2, 0, s * (4.0 + r * 0.6), SHIRT[(rnd() * SHIRT.length) | 0], rnd()]);
  }
  // back rows and distant towers so roof shots stay full
  for (const s of [-1, 1]) for (const row of [0, 1, 2]) {
    let x = x0 - 40 + R2() * 6;
    while (x < x1 + 70) {
      const w = 7 + R2() * 6, hgt = 10 + R2() * 10 + row * 3, zc = s * (21 + row * 14 + R2() * 4);
      if (!(x > x1 - 6 && Math.abs(zc) < 34)) {
        const mat = new THREE.MeshLambertMaterial({ map: facades[(R2() * 4) | 0] });
        const b = new THREE.Mesh(new THREE.BoxGeometry(w, hgt, 12), [mat, mat, slate, slate, mat, mat]); b.position.set(x + w / 2, hgt / 2, zc); scene.add(b);
        const roof = new THREE.Mesh(new THREE.CylinderGeometry(0.01, 6.8, 3.2, 4, 1), slate); roof.rotation.y = Math.PI / 4; roof.scale.set(w / 9.4, 1, 1.25); roof.position.set(x + w / 2, hgt + 1.6, zc); scene.add(roof);
      }
      x += w + 0.4;
    }
  }
  const stoneTex = tex(256, 256, (g, w, h) => { g.fillStyle = "#cdbb98"; g.fillRect(0, 0, w, h); g.strokeStyle = "rgba(70,55,35,0.4)"; g.lineWidth = 3;
    for (let y = 0; y < h; y += 24) { g.beginPath(); g.moveTo(0, y); g.lineTo(w, y); g.stroke(); for (let xx = (y / 24) % 2 ? 0 : 24; xx < w; xx += 48) { g.beginPath(); g.moveTo(xx, y); g.lineTo(xx, y + 24); g.stroke(); } } }, [4, 4]);
  const stone = new THREE.MeshLambertMaterial({ map: stoneTex });
  // cathedral front closing the street (two square towers, rose window)
  const nd = new THREE.Mesh(new THREE.BoxGeometry(12, 26, 34), stone); nd.position.set(x0 - 7, 13, 0); scene.add(nd);
  for (const z of [-11, 11]) { const tw = new THREE.Mesh(new THREE.BoxGeometry(10, 44, 10), stone); tw.position.set(x0 - 7, 22, z); scene.add(tw); }
  const rose = new THREE.Mesh(new THREE.CircleGeometry(4, 28), new THREE.MeshLambertMaterial({ color: 0x40557a, emissive: 0x20283c })); rose.rotation.y = Math.PI / 2; rose.position.set(x0 - 0.9, 18, 0); scene.add(rose);
  for (const [tx, tz, th] of [[-2060, -50, 40], [-1995, 55, 36], [-2150, 45, 30]]) { const tw = new THREE.Mesh(new THREE.BoxGeometry(6, th, 6), stone); tw.position.set(tx, th / 2, tz); scene.add(tw);
    const sp = new THREE.Mesh(new THREE.ConeGeometry(4.6, 12, 4), slate); sp.rotation.y = Math.PI / 4; sp.position.set(tx, th + 6, tz); scene.add(sp); }
  for (let i = 0; i < 22; i++) { const a = (i / 22) * Math.PI * 2, r = 320 + R2() * 80, hh = 30 + R2() * 40;
    const m = new THREE.Mesh(new THREE.ConeGeometry(80 + R2() * 50, hh, 7), new THREE.MeshLambertMaterial({ color: 0x9a8f86 })); m.position.set(cx + Math.cos(a) * r, hh / 2 - 4, Math.sin(a) * r); scene.add(m); }

  // the Bastille: eight round towers, curtain walls, battlements, gate with two door leaves, drawbridge over a moat
  const [bx, bz] = PARIS.bastille;
  const dark = new THREE.MeshLambertMaterial({ map: tex(256, 256, (g, w, h) => { g.fillStyle = "#8f8778"; g.fillRect(0, 0, w, h); g.strokeStyle = "rgba(40,35,30,0.45)"; g.lineWidth = 3;
    for (let y = 0; y < h; y += 20) { g.beginPath(); g.moveTo(0, y); g.lineTo(w, y); g.stroke(); for (let xx = (y / 20) % 2 ? 0 : 20; xx < w; xx += 40) { g.beginPath(); g.moveTo(xx, y); g.lineTo(xx, y + 20); g.stroke(); } } }, [3, 3]) });
  const moat = new THREE.Mesh(new THREE.PlaneGeometry(52, 40), new THREE.MeshLambertMaterial({ color: 0x3f5d66 })); moat.rotation.x = -Math.PI / 2; moat.position.set(bx, 0.02, bz); moat.userData.noFg = true; scene.add(moat);
  const wall = new THREE.Mesh(new THREE.BoxGeometry(36, 22, 24), dark); wall.position.set(bx, 11, bz); scene.add(wall);
  for (const [dx, dz] of [[-18, -12], [-18, 12], [18, -12], [18, 12], [-6, -12], [6, -12], [-6, 12], [6, 12]]) {
    const t = new THREE.Mesh(new THREE.CylinderGeometry(4.2, 4.6, 26, 18), dark); t.position.set(bx + dx, 13, bz + dz); scene.add(t);
    for (let k = 0; k < 10; k++) { const a = (k / 10) * Math.PI * 2, m = new THREE.Mesh(new THREE.BoxGeometry(1, 1.4, 1), dark); m.position.set(bx + dx + Math.cos(a) * 4.1, 26.7, bz + dz + Math.sin(a) * 4.1); scene.add(m); }
  }
  for (let k = 0; k < 18; k++) { const m = new THREE.Mesh(new THREE.BoxGeometry(1, 1.4, 1), dark); m.position.set(bx - 18.4, 22.7, bz - 9 + k * 1.05); scene.add(m); }
  const gx = bx - 18.2;
  const arch = new THREE.Mesh(new THREE.BoxGeometry(0.6, 6.4, 5.4), new THREE.MeshLambertMaterial({ color: 0x1c1612 })); arch.position.set(gx - 0.1, 3.2, bz); scene.add(arch);
  const woodM = new THREE.MeshLambertMaterial({ color: 0x6a4424 });
  const leaves = [-1, 1].map((s) => { const piv = new THREE.Group(); piv.position.set(gx - 0.45, 0, bz + s * 2.6); scene.add(piv);
    const lf = new THREE.Mesh(new THREE.BoxGeometry(0.3, 6.0, 2.6), woodM); lf.position.set(0, 3.0, -s * 1.3); piv.add(lf);
    for (const y of [1.2, 3, 4.8]) { const band = new THREE.Mesh(new THREE.BoxGeometry(0.34, 0.25, 2.6), new THREE.MeshLambertMaterial({ color: 0x2a2a2a })); band.position.set(0, y, -s * 1.3); piv.add(band); }
    return { piv, s }; });
  const bridge = new THREE.Mesh(new THREE.BoxGeometry(9, 0.4, 5), woodM); bridge.position.set(gx - 5, 0.25, bz); scene.add(bridge);
  const door = (f) => { for (const { piv, s } of leaves) piv.rotation.y = s * f * 1.6; };   // f 0 closed .. 1 burst open
  // tricolour banners on the Bastille and on the houses, garlands across the street with lanterns
  const TRI = [0x2b4f8f, 0xf3efe4, 0xc22f2f];
  for (let k = 0; k < 3; k++) { const ban = new THREE.Mesh(new THREE.PlaneGeometry(2.2, 9), new THREE.MeshBasicMaterial({ color: TRI[k], side: THREE.DoubleSide })); ban.position.set(gx - 0.5, 16, bz - 6 + k * 2.2 + (k > 0 ? 3.6 : 0) * 0); scene.add(ban); }
  for (const s of [-1, 1]) for (let x = x0 + 3; x < x1 - 1; x += 6.5) for (let k = 0; k < 3; k++) {
    const b = new THREE.Mesh(new THREE.PlaneGeometry(0.55, 3.2), new THREE.MeshBasicMaterial({ color: TRI[k], side: THREE.DoubleSide })); b.position.set(x + k * 0.55, 9.2, s * 6.08); scene.add(b); }
  const tri = new THREE.BufferGeometry(); tri.setAttribute("position", new THREE.Float32BufferAttribute([-0.24, 0, 0, 0.24, 0, 0, 0, -0.5, 0], 3));
  const flags = [], lanterns = [];
  const lineMat = new THREE.LineBasicMaterial({ color: 0x2d2a26 });
  for (let x = x0 + 2; x < x1 - 1; x += 6.5) {
    const yb = (Math.round(x) % 13 + 13) % 13 < 6.5 ? 8.4 : 10.8, pts = [];
    for (let k = 0; k <= 24; k++) { const f = k / 24; pts.push(new THREE.Vector3(x + 0.8 * f, yb - Math.sin(f * Math.PI) * 1.5, -6 + 12 * f)); }
    scene.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), lineMat));
    for (let k = 1; k < 24; k++) flags.push([pts[k], TRI[k % 3]]);
    lanterns.push(pts[12]);
  }
  const flagMesh = new THREE.InstancedMesh(tri, new THREE.MeshBasicMaterial({ side: THREE.DoubleSide }), flags.length);
  flags.forEach(([p, cc], i) => { tmp.position.copy(p); tmp.rotation.set(0, Math.PI / 2, 0); tmp.updateMatrix(); flagMesh.setMatrixAt(i, tmp.matrix); flagMesh.setColorAt(i, col.setHex(cc)); });
  scene.add(flagMesh);
  for (const p of lanterns) { const l = new THREE.Mesh(new THREE.BoxGeometry(0.4, 0.6, 0.4), new THREE.MeshBasicMaterial({ color: 0xffd27a })); l.position.copy(p).add(new THREE.Vector3(0, -0.5, 0)); scene.add(l); }
  // barricades along the street: barrels, crates, cart wheels
  const barrels = [], crates = [], wheels = [];
  for (const s of [-1, 1]) for (let x = x0 + 4; x < x1; x += 2.2 + rnd() * 2) {
    const r = rnd(); if (r < 0.45) barrels.push([x, s * (3.35 + rnd() * 0.3)]); else if (r < 0.8) crates.push([x, s * (3.4 + rnd() * 0.3), rnd()]); else wheels.push([x, s * 3.45]);
  }
  const barrelMesh = new THREE.InstancedMesh(new THREE.CylinderGeometry(0.42, 0.42, 1.0, 12), new THREE.MeshLambertMaterial({ color: 0x7a4a26 }), barrels.length);
  barrels.forEach((b, i) => { tmp.position.set(b[0], 0.5, b[1]); tmp.rotation.set(0, 0, 0); tmp.updateMatrix(); barrelMesh.setMatrixAt(i, tmp.matrix); }); scene.add(barrelMesh);
  const crateMesh = new THREE.InstancedMesh(new THREE.BoxGeometry(1, 0.9, 0.9), new THREE.MeshLambertMaterial({ color: 0x9a6a3a }), crates.length);
  crates.forEach((b, i) => { tmp.position.set(b[0], 0.45, b[1]); tmp.rotation.set(0, b[2], 0); tmp.updateMatrix(); crateMesh.setMatrixAt(i, tmp.matrix); }); scene.add(crateMesh);
  const wheelMesh = new THREE.InstancedMesh(new THREE.TorusGeometry(0.6, 0.09, 6, 16), new THREE.MeshLambertMaterial({ color: 0x4a3018 }), wheels.length);
  wheels.forEach((b, i) => { tmp.position.set(b[0], 0.62, b[1]); tmp.rotation.set(0, Math.PI / 2, 0.2); tmp.updateMatrix(); wheelMesh.setMatrixAt(i, tmp.matrix); }); scene.add(wheelMesh);
  // smoke over the roofs, dust in the street, warm light shafts
  const puff = tex(64, 64, (g) => { const gr = g.createRadialGradient(32, 32, 0, 32, 32, 32); gr.addColorStop(0, "rgba(90,84,80,0.75)"); gr.addColorStop(1, "rgba(90,84,80,0)"); g.fillStyle = gr; g.fillRect(0, 0, 64, 64); });
  const smoke = [];
  for (let i = 0; i < 6; i++) { const base = [x0 + 15 + i * 21, 14 + R2() * 6, (R2() < 0.5 ? -1 : 1) * (14 + R2() * 20)];
    for (let k = 0; k < 7; k++) { const sp = new THREE.Sprite(new THREE.SpriteMaterial({ map: puff, transparent: true, depthWrite: false })); scene.add(sp); smoke.push({ sp, base, k }); } }
  const shaft = tex(64, 256, (g, w, h) => { const gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, "rgba(255,220,170,0.5)"); gr.addColorStop(1, "rgba(255,220,170,0)"); g.fillStyle = gr; g.fillRect(0, 0, w, h); });
  for (let x = x0 + 8; x < x1; x += 12) { const sf = new THREE.Mesh(new THREE.PlaneGeometry(2.2, 16), new THREE.MeshBasicMaterial({ map: shaft, transparent: true, opacity: 0.2,
      blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide, fog: false })); sf.position.set(x, 7, 0); sf.rotation.set(0, Math.PI / 2, 0.45); sf.userData.noFg = true; scene.add(sf); }
  // crowd in front of the Bastille
  for (let k = 0; k < 260; k++) { const a = Math.PI / 2 + (rnd() - 0.5) * 2.2, r = 9 + rnd() * 9; people.push([gx - 8 + Math.cos(a) * r * 0.6 - 2, 0, Math.sin(a) * r * (rnd() < 0.5 ? 1 : -1), SHIRT[(rnd() * SHIRT.length) | 0], rnd()]); }

  const N = people.length;
  const bodies = new THREE.InstancedMesh(new THREE.BoxGeometry(0.46, 0.6, 0.3), new THREE.MeshLambertMaterial(), N);
  const heads = new THREE.InstancedMesh(new THREE.BoxGeometry(0.3, 0.3, 0.3), new THREE.MeshLambertMaterial(), N);
  const caps = new THREE.InstancedMesh(new THREE.BoxGeometry(0.32, 0.12, 0.32), new THREE.MeshLambertMaterial({ color: 0xc22f2f }), N);
  const SKIN = [0xf1c9a5, 0xe0ac7e, 0xc68863, 0x8d5a3b];
  people.forEach((p, i) => { bodies.setColorAt(i, col.setHex(p[3])); heads.setColorAt(i, col.setHex(SKIN[(p[4] * 4) | 0])); });
  scene.add(bodies, heads, caps);
  const crowd = (t, amp) => {
    for (let i = 0; i < N; i++) { const p = people[i], hop = Math.abs(Math.sin(t * 5 + p[4] * 6.28)) * amp * (0.6 + p[4] * 0.8);
      tmp.position.set(p[0], p[1] + 0.3 + hop, p[2]); tmp.rotation.set(0, 0, 0); tmp.updateMatrix(); bodies.setMatrixAt(i, tmp.matrix);
      tmp.position.y += 0.47; tmp.updateMatrix(); heads.setMatrixAt(i, tmp.matrix);
      tmp.position.y += 0.2; tmp.updateMatrix(); caps.setMatrixAt(i, tmp.matrix); }
    bodies.instanceMatrix.needsUpdate = heads.instanceMatrix.needsUpdate = caps.instanceMatrix.needsUpdate = true;
    for (const s of smoke) { const f = ((t * 0.12 + s.k / 7) % 1); s.sp.position.set(s.base[0] + f * 6, s.base[1] + f * 22, s.base[2]); const sc = 6 + f * 14; s.sp.scale.set(sc, sc, 1); s.sp.material.opacity = (1 - f) * 0.55; }
  };
  return { crowd, door, lights, sky, fog };
}

// inside the street below roof height, the square in front of the Bastille, never inside a wall
export function parisBounds(P) {
  const { x0, x1 } = PARIS;
  if (P.x > x0 - 1 && P.x < x1 && P.y < 22) P.z = Math.max(-5.4, Math.min(5.4, P.z));
  if (P.x >= x1 && P.x < PARIS.bastille[0] - 19 && P.y < 30) P.z = Math.max(-16, Math.min(16, P.z));
  if (P.x >= PARIS.bastille[0] - 19 && P.x < PARIS.bastille[0] + 26 && Math.abs(P.z) < 17 && P.y < 30) P.x = PARIS.bastille[0] - 19;   // not inside the fortress
  P.y = Math.max(0.35, P.y);
  return P;
}
