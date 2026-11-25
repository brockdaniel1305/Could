// COULD? 3D world: Pamplona's old town on a bull-run morning. A cobbled street along x (bulls run towards +x),
// double wooden fences at z = +-3 with spectators behind them, painted houses with crowded balconies, and the bullring at the end.
// buildPamplona(THREE, scene) -> { crowd(t, amp), flashAt(), boardsAt(), nets: {} }  (same interface as buildStadium)
export const STREET = { x0: -90, x1: 47, half: 3.0, ring: [74, 0], ringR: 24 };

export function buildPamplona(THREE, scene) {
  const mulberry = (a) => () => { a |= 0; a = (a + 0x6d2b79f5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  const rnd = mulberry(11);
  const tmpF = new THREE.Object3D(), colF = new THREE.Color();
  const canvasTex = (w, h, draw, rep) => { const c = document.createElement("canvas"); c.width = w; c.height = h; draw(c.getContext("2d"), w, h);
    const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8;
    if (rep) { t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(rep[0], rep[1]); } return t; };

  // morning sky + light
  scene.background = canvasTex(8, 512, (g, w, h) => { const gr = g.createLinearGradient(0, 0, 0, h);
    gr.addColorStop(0, "#5aa7e6"); gr.addColorStop(0.6, "#a9d3f2"); gr.addColorStop(1, "#f3e7cf"); g.fillStyle = gr; g.fillRect(0, 0, w, h); });
  scene.fog = new THREE.Fog(0xe9e2d2, 90, 520);
  scene.add(new THREE.AmbientLight(0xffffff, 0.6));
  scene.add(new THREE.HemisphereLight(0xffffff, 0xc9a77a, 0.65));
  const sun = new THREE.DirectionalLight(0xfff0d0, 1.15); sun.position.set(40, 70, 30); scene.add(sun);

  const { x0, x1, half } = STREET, L = x1 - x0, cx = (x0 + x1) / 2;
  // cobbles
  const cobble = canvasTex(256, 256, (g) => { g.fillStyle = "#8d8378"; g.fillRect(0, 0, 256, 256);
    for (let y = 0; y < 8; y++) for (let x = 0; x < 8; x++) { const v = 120 + ((x * 7 + y * 13) % 5) * 9;
      g.fillStyle = `rgb(${v + 22},${v + 12},${v})`; g.beginPath(); g.ellipse(x * 32 + 16 + (y % 2) * 8, y * 32 + 16, 14, 13, 0, 0, 6.3); g.fill(); } }, [L / 2.2, 6]);
  const street = new THREE.Mesh(new THREE.PlaneGeometry(L, 13), new THREE.MeshLambertMaterial({ map: cobble }));
  street.userData.noFg = true; street.rotation.x = -Math.PI / 2; street.position.set(cx, 0, 0); scene.add(street);
  const outer = new THREE.Mesh(new THREE.PlaneGeometry(900, 900), new THREE.MeshLambertMaterial({ color: 0x9c8f7c }));
  outer.rotation.x = -Math.PI / 2; outer.position.y = -0.05; scene.add(outer);

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
  const archTex = canvasTex(256, 64, (g, w, h) => { g.fillStyle = "#c98b52"; g.fillRect(0, 0, w, h); g.fillStyle = "#7a4a26";
    for (let k = 0; k < 4; k++) { g.beginPath(); g.moveTo(k * 64 + 10, h); g.lineTo(k * 64 + 10, 26); g.arc(k * 64 + 32, 26, 22, Math.PI, 0); g.lineTo(k * 64 + 54, h); g.fill(); } }, [40, 1]);
  const arches = new THREE.Mesh(new THREE.CylinderGeometry(R + 21, R + 21, 4, 72, 1, true), new THREE.MeshLambertMaterial({ map: archTex, side: THREE.DoubleSide }));
  for (let k = 0; k < 36; k++) { const a = (k / 36) * Math.PI * 2, fx = rx + Math.cos(a) * (R + 21), fz = rz + Math.sin(a) * (R + 21);
    const pole = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 4, 5), new THREE.MeshLambertMaterial({ color: 0x333333 })); pole.position.set(fx, 21.5, fz); scene.add(pole);
    const fl = new THREE.Mesh(new THREE.PlaneGeometry(2.2, 1.3), new THREE.MeshBasicMaterial({ color: k % 2 ? 0xd8202c : 0xf6f4ef, side: THREE.DoubleSide }));
    fl.position.set(fx, 22.8, fz); fl.rotation.y = -a; scene.add(fl); }
  arches.position.set(rx, 17.5, rz); scene.add(arches);
  for (let r = 0; r < 22; r++) { const rr = R + 1.4 + r * 0.85, n = Math.floor((2 * Math.PI * rr) / 0.62);
    for (let i = 0; i < n; i++) { const a = (i / n) * Math.PI * 2; if (Math.abs(Math.atan2(Math.sin(a - Math.PI), Math.cos(a - Math.PI))) < gap * 2) continue;
      if (rnd() < 0.85) people.push([rx + Math.cos(a) * rr, 2.2 + r * 0.6, rz + Math.sin(a) * rr, SHIRT[(rnd() * SHIRT.length) | 0], rnd()]); } }

  // ---------- density pass: every frame should be full ----------
  const R2 = mulberry(77);
  // back rows of houses so rooftop shots and gaps between houses never show empty ground
  for (const sgn of [-1, 1]) for (const row of [0, 1, 2]) {
    let x = x0 - 40 + R2() * 6;
    while (x < 140) {
      const w = 7 + R2() * 6, hgt = 10 + R2() * 12 + row * 3, zc = sgn * (21 + row * 14 + R2() * 4);
      const inRing = Math.hypot(x + w / 2 - STREET.ring[0], zc - STREET.ring[1]) < STREET.ringR + 26;
      if (!inRing) {
        const k = (R2() * PAL.length) | 0, mat = new THREE.MeshLambertMaterial({ map: facade[k] });
        const b = new THREE.Mesh(new THREE.BoxGeometry(w, hgt, 12), [mat, mat, roof, roof, mat, mat]);
        b.position.set(x + w / 2, hgt / 2, zc); scene.add(b);
        const ridge = new THREE.Mesh(new THREE.CylinderGeometry(0.01, 6.4, 2.4, 4, 1), roof);
        ridge.rotation.y = Math.PI / 4; ridge.scale.set(w / 9, 1, 1.0); ridge.position.set(x + w / 2, hgt + 1.2, zc); scene.add(ridge);
      }
      x += w + 0.4;
    }
  }
  // the church closing the street behind the corral, with a bell tower
  const stone = new THREE.MeshLambertMaterial({ map: canvasTex(256, 256, (g, w, h) => { g.fillStyle = "#d9c7a3"; g.fillRect(0, 0, w, h);
    g.strokeStyle = "rgba(90,70,40,0.35)"; g.lineWidth = 3; for (let y = 0; y < h; y += 24) { g.beginPath(); g.moveTo(0, y); g.lineTo(w, y); g.stroke();
      for (let xx = (y / 24) % 2 ? 0 : 24; xx < w; xx += 48) { g.beginPath(); g.moveTo(xx, y); g.lineTo(xx, y + 24); g.stroke(); } } }, [4, 4]) });
  const church = new THREE.Mesh(new THREE.BoxGeometry(14, 24, 30), stone); church.position.set(x0 - 8, 12, 0); scene.add(church);
  const tower = new THREE.Mesh(new THREE.BoxGeometry(8, 44, 8), stone); tower.position.set(x0 - 8, 22, -9); scene.add(tower);
  const spire = new THREE.Mesh(new THREE.ConeGeometry(6.2, 12, 4), new THREE.MeshLambertMaterial({ color: 0x5b6a72 })); spire.rotation.y = Math.PI / 4; spire.position.set(x0 - 8, 50, -9); scene.add(spire);
  const rose = new THREE.Mesh(new THREE.CircleGeometry(3.2, 24), new THREE.MeshLambertMaterial({ color: 0x3a5f8a, emissive: 0x1a2a44 })); rose.rotation.y = Math.PI / 2; rose.position.set(x0 - 0.9, 16, 0); scene.add(rose);
  // distant cathedral towers and the hills around the old town
  for (const [tx, tz, th] of [[-30, -48, 46], [25, 52, 40], [-70, 60, 34], [110, -60, 38]]) {
    const tw = new THREE.Mesh(new THREE.BoxGeometry(7, th, 7), stone); tw.position.set(tx, th / 2, tz); scene.add(tw);
    const sp = new THREE.Mesh(new THREE.ConeGeometry(5.2, 10, 4), new THREE.MeshLambertMaterial({ color: 0x55636b })); sp.rotation.y = Math.PI / 4; sp.position.set(tx, th + 5, tz); scene.add(sp);
  }
  for (let i = 0; i < 26; i++) { const a = (i / 26) * Math.PI * 2 + R2() * 0.2, r = 300 + R2() * 90, hh = 45 + R2() * 70;
    const m = new THREE.Mesh(new THREE.ConeGeometry(70 + R2() * 60, hh, 7), new THREE.MeshLambertMaterial({ color: R2() < 0.5 ? 0x7f9a84 : 0x8aa0a8 }));
    m.position.set(Math.cos(a) * r, hh / 2 - 4, Math.sin(a) * r); scene.add(m); }
  // clouds
  const cloudTex = canvasTex(256, 128, (g, w, h) => { for (let k = 0; k < 9; k++) { const gx = 40 + k * 22, gy = 70 - Math.sin(k / 8 * Math.PI) * 30, r = 34 + (k % 3) * 8;
    const gr = g.createRadialGradient(gx, gy, 0, gx, gy, r); gr.addColorStop(0, "rgba(255,255,255,0.95)"); gr.addColorStop(1, "rgba(255,255,255,0)"); g.fillStyle = gr; g.fillRect(0, 0, w, h); } });
  for (let i = 0; i < 18; i++) { const c = new THREE.Sprite(new THREE.SpriteMaterial({ map: cloudTex, transparent: true, depthWrite: false, fog: false }));
    const a = R2() * Math.PI * 2, r = 120 + R2() * 220; c.position.set(Math.cos(a) * r - 20, 70 + R2() * 60, Math.sin(a) * r); c.scale.set(80 + R2() * 60, 36 + R2() * 20, 1); scene.add(c); }
  // bunting garlands across the street (fills the strip of sky between the houses)
  const tri = new THREE.BufferGeometry(); tri.setAttribute("position", new THREE.Float32BufferAttribute([-0.24, 0, 0, 0.24, 0, 0, 0, -0.5, 0], 3)); tri.computeVertexNormals();
  const flags = [], FLAGC = [0xd8202c, 0xf6f4ef, 0xd8202c, 0x2e8b57, 0xf6f4ef, 0xf2c230];
  const lineMat = new THREE.LineBasicMaterial({ color: 0x3a3a3a });
  for (let x = x0 + 2; x < x1 - 1; x += 6.5) for (const yb of [x % 13 < 6.5 ? 8.6 : 11.2]) {
    const pts = [], n = 24;
    for (let k = 0; k <= n; k++) { const f = k / n, z = -6.0 + 12 * f; pts.push(new THREE.Vector3(x + 0.8 * f, yb - Math.sin(f * Math.PI) * 1.5, z)); }
    scene.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), lineMat));
    for (let k = 1; k < n; k++) flags.push([pts[k], FLAGC[(((k + Math.round(x)) % FLAGC.length) + FLAGC.length) % FLAGC.length]]);
  }
  const flagMesh = new THREE.InstancedMesh(tri, new THREE.MeshBasicMaterial({ side: THREE.DoubleSide }), flags.length);
  flags.forEach(([p, cc], i) => { tmpF.position.copy(p); tmpF.rotation.set(0, Math.PI / 2, 0); tmpF.updateMatrix(); flagMesh.setMatrixAt(i, tmpF.matrix); flagMesh.setColorAt(i, colF.setHex(cc)); });
  scene.add(flagMesh);
  // flower boxes and hanging banners on the balconies, wall lanterns
  const boxes = [], blooms = [];
  for (const sgn of [-1, 1]) for (let x = x0 + 0.9; x < x1 - 1; x += 2.6) for (const y of balconyY) if (R2() < 0.55) { boxes.push([x, y - 0.55, sgn * 6.05]); blooms.push([x, y - 0.32, sgn * 6.05]); }
  const boxMesh = new THREE.InstancedMesh(new THREE.BoxGeometry(1.1, 0.3, 0.35), new THREE.MeshLambertMaterial({ color: 0x5b3a22 }), boxes.length);
  const bloomMesh = new THREE.InstancedMesh(new THREE.SphereGeometry(0.22, 6, 4), new THREE.MeshLambertMaterial(), blooms.length * 3);
  boxes.forEach((b, i) => { tmpF.position.set(...b); tmpF.rotation.set(0, 0, 0); tmpF.updateMatrix(); boxMesh.setMatrixAt(i, tmpF.matrix); });
  blooms.forEach((b, i) => { for (let k = 0; k < 3; k++) { tmpF.position.set(b[0] - 0.35 + k * 0.35, b[1], b[2]); tmpF.updateMatrix(); bloomMesh.setMatrixAt(i * 3 + k, tmpF.matrix);
    bloomMesh.setColorAt(i * 3 + k, colF.setHex([0xe8343c, 0xf2a0b8, 0x3f9b4a][(k + i) % 3])); } });
  scene.add(boxMesh, bloomMesh);
  for (const sgn of [-1, 1]) for (let x = x0 + 4; x < x1 - 1; x += 7) {
    const ban = new THREE.Mesh(new THREE.PlaneGeometry(0.9, 3.4), new THREE.MeshLambertMaterial({ color: R2() < 0.6 ? 0xd8202c : 0xf6f4ef, side: THREE.DoubleSide }));
    ban.position.set(x + R2(), 9.0 + R2() * 2, sgn * 6.08); scene.add(ban);
    const lamp = new THREE.Mesh(new THREE.BoxGeometry(0.35, 0.6, 0.35), new THREE.MeshLambertMaterial({ color: 0x222222, emissive: 0x332200 }));
    lamp.position.set(x + 2.5, 3.3, sgn * 5.85); scene.add(lamp);
  }
  // street clutter: rolled newspapers and lost red scarves
  const clutter = new THREE.InstancedMesh(new THREE.BoxGeometry(0.26, 0.03, 0.07), new THREE.MeshLambertMaterial(), 140);
  for (let i = 0; i < 140; i++) { tmpF.position.set(x0 + R2() * L, 0.03, (R2() - 0.5) * 5.6); tmpF.rotation.set(0, R2() * 6.3, 0); tmpF.updateMatrix();
    clutter.setMatrixAt(i, tmpF.matrix); clutter.setColorAt(i, colF.setHex(R2() < 0.75 ? 0xf3efe4 : 0xd8202c)); }
  clutter.userData.noFg = true; scene.add(clutter);
  // light shafts across the street and floating dust
  const shaftTex = canvasTex(64, 256, (g, w, h) => { const gr = g.createLinearGradient(0, 0, 0, h); gr.addColorStop(0, "rgba(255,240,200,0.5)"); gr.addColorStop(1, "rgba(255,240,200,0)");
    g.fillStyle = gr; g.fillRect(0, 0, w, h); });
  for (let x = x0 + 8; x < x1; x += 11) { const sft = new THREE.Mesh(new THREE.PlaneGeometry(2.2, 16), new THREE.MeshBasicMaterial({ map: shaftTex, transparent: true, opacity: 0.22,
      blending: THREE.AdditiveBlending, depthWrite: false, side: THREE.DoubleSide, fog: false }));
    sft.position.set(x, 7, 0); sft.rotation.set(0, Math.PI / 2, 0.45); sft.userData.noFg = true; scene.add(sft); }
  const DN = 420, dustPos = new Float32Array(DN * 3), dustBase = [];
  for (let i = 0; i < DN; i++) dustBase.push([x0 + 10 + R2() * (L - 10), 0.3 + R2() * 7, (R2() - 0.5) * 5.6, R2() * 6.3]);
  const dustGeo = new THREE.BufferGeometry(); dustGeo.setAttribute("position", new THREE.BufferAttribute(dustPos, 3));
  const dust = new THREE.Points(dustGeo, new THREE.PointsMaterial({ color: 0xfff1cf, size: 0.06, transparent: true, opacity: 0.7, depthWrite: false }));
  dust.userData.noFg = true; scene.add(dust);
  const dustAt = (t) => { dustBase.forEach((d, i) => { dustPos[i * 3] = d[0] + Math.sin(t * 0.3 + d[3]) * 0.6; dustPos[i * 3 + 1] = d[1] + Math.sin(t * 0.5 + d[3] * 2) * 0.3;
    dustPos[i * 3 + 2] = d[2] + Math.cos(t * 0.4 + d[3]) * 0.3; }); dustGeo.attributes.position.needsUpdate = true; };

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
    dustAt(t);
  };
  return { crowd, flashAt: () => {}, boardsAt: () => {}, nets: {} };
}

// keep the camera out of the houses: inside the street (incl. the spectator strip) unless it is above the rooftops
export function pamplonaBounds(P) {
  const { x0, x1, ring, ringR } = STREET;
  if (P.y < 24 && P.x > x0 - 1 && P.x < x1 + 2) P.z = Math.max(-5.6, Math.min(5.6, P.z));
  if (P.y < 20 && Math.hypot(P.x - ring[0], P.z - ring[1]) > ringR - 0.5 && P.x > x1 + 2) {   // in the ring: stay on the sand
    const a = Math.atan2(P.z - ring[1], P.x - ring[0]), r = ringR - 0.5; P.x = ring[0] + Math.cos(a) * r; P.z = ring[1] + Math.sin(a) * r; }
  P.y = Math.max(0.35, P.y);
  return P;
}
