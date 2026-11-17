// COULD? POV series: stylised low-poly 3D people (big heads, simple limbs), posable per frame.
// makePerson(THREE, opts) -> { root, pose(p) }. Origin = hip point, the person faces -z.
//   opts: skin, hair, hairStyle ('short'|'bald'|'bun'|'long'|'cap'|'side'), shirt (hex or THREE.Texture), pants, scale, glasses, uniform
//   pose: { seated (0..1), lean (deg fwd), twist (deg), headYaw, headPitch (+ = looks down), headRoll (deg),
//           armL/armR: [raise fwd deg, out deg, elbow deg], legs (0 seated .. 1 standing), mouth 0..1, blink 0..1, brow -1..1 }
const D = Math.PI / 180;

export function makePerson(THREE, o = {}) {
  const lam = (c, extra = {}) => new THREE.MeshLambertMaterial({ color: c, ...extra });
  const skinM = lam(o.skin ?? 0xf1c6a0), hairM = lam(o.hair ?? 0x3b2a1e), pantsM = lam(o.pants ?? 0x2d3a55);
  const shirtM = o.shirt && o.shirt.isTexture ? new THREE.MeshLambertMaterial({ map: o.shirt }) : lam(o.shirt ?? 0x4f7fd1);
  const dark = lam(0x161620), white = lam(0xffffff);
  const mesh = (g, m, parent, x = 0, y = 0, z = 0) => { const k = new THREE.Mesh(g, m); k.position.set(x, y, z); parent.add(k); return k; };
  const S = o.scale ?? 1;
  const root = new THREE.Group(); root.scale.setScalar(S);
  const hips = new THREE.Group(); root.add(hips);

  // legs: thigh + shin per side, pivot at the hip; seated = thighs forward, shins down
  const legs = [];
  for (const sx of [-1, 1]) {
    const hip = new THREE.Group(); hip.position.set(sx * 0.1, 0, 0); hips.add(hip);
    mesh(new THREE.CapsuleGeometry(0.075, 0.32, 4, 10), pantsM, hip, 0, -0.2, 0);
    const knee = new THREE.Group(); knee.position.set(0, -0.42, 0); hip.add(knee);
    mesh(new THREE.CapsuleGeometry(0.065, 0.32, 4, 10), pantsM, knee, 0, -0.2, 0);
    const shoe = mesh(new THREE.BoxGeometry(0.11, 0.08, 0.22), dark, knee, 0, -0.42, -0.05);
    legs.push({ hip, knee, shoe });
  }
  // torso
  const torso = new THREE.Group(); hips.add(torso);
  const body = mesh(new THREE.CapsuleGeometry(0.19, 0.3, 6, 14), shirtM, torso, 0, 0.3, 0); body.scale.set(1.05, 1, 0.72);
  if (o.uniform) { const tie = mesh(new THREE.BoxGeometry(0.09, 0.05, 0.02), lam(0xd8202c), torso, 0, 0.56, -0.14); tie.rotation.z = 0.6; }
  // head
  const neck = new THREE.Group(); neck.position.set(0, 0.62, 0); torso.add(neck);
  mesh(new THREE.CylinderGeometry(0.06, 0.07, 0.1, 10), skinM, neck, 0, 0.02, 0);
  const head = new THREE.Group(); head.position.set(0, 0.2, 0); neck.add(head);
  const skull = mesh(new THREE.SphereGeometry(0.17, 24, 18), skinM, head); skull.scale.set(0.95, 1.05, 0.98);
  for (const sx of [-1, 1]) mesh(new THREE.SphereGeometry(0.035, 10, 8), skinM, head, sx * 0.165, -0.01, 0.01);           // ears
  mesh(new THREE.SphereGeometry(0.03, 10, 8), skinM, head, 0, -0.02, -0.168);                                             // nose
  const eyes = [], pupils = [], brows = [];
  for (const sx of [-1, 1]) {
    const e = mesh(new THREE.SphereGeometry(0.038, 14, 10), white, head, sx * 0.06, 0.035, -0.142); e.scale.set(1, 1.15, 0.5); eyes.push(e);
    const p = mesh(new THREE.SphereGeometry(0.019, 10, 8), dark, head, sx * 0.06, 0.033, -0.162); pupils.push(p);
    const b = mesh(new THREE.BoxGeometry(0.06, 0.013, 0.02), hairM, head, sx * 0.06, 0.092, -0.152); brows.push(b);
  }
  const mouth = mesh(new THREE.SphereGeometry(0.04, 14, 10), lam(0x5a1f24), head, 0, -0.078, -0.15); mouth.scale.set(1, 0.18, 0.4);
  if (o.beard) { const bd = mesh(new THREE.SphereGeometry(0.15, 16, 12, 0, Math.PI * 2, Math.PI * 0.45, Math.PI * 0.55), hairM, head, 0, 0.0, 0.0); bd.scale.set(1.02, 1.0, 1.03); }
  if (o.glasses) {
    for (const sx of [-1, 1]) { const r = mesh(new THREE.TorusGeometry(0.042, 0.007, 6, 18), dark, head, sx * 0.06, 0.035, -0.168); void r; }
    mesh(new THREE.BoxGeometry(0.04, 0.008, 0.008), dark, head, 0, 0.04, -0.17);
  }
  // hair
  const hs = o.hairStyle ?? "short";
  if (hs !== "bald") {
    const cap = mesh(new THREE.SphereGeometry(0.178, 24, 16, 0, Math.PI * 2, 0, Math.PI * (hs === "long" ? 0.62 : 0.5)), hairM, head, 0, 0.012, 0.012);
    cap.rotation.x = -0.25;
    if (hs === "bun") mesh(new THREE.SphereGeometry(0.07, 12, 10), hairM, head, 0, 0.12, 0.13);
    if (hs === "long") { const back = mesh(new THREE.BoxGeometry(0.3, 0.3, 0.08), hairM, head, 0, -0.08, 0.12); void back; }
    if (hs === "cap") { cap.material = lam(o.capColor ?? 0x1d3f9b); mesh(new THREE.BoxGeometry(0.22, 0.02, 0.14), cap.material, head, 0, 0.09, -0.19); }
    if (hs === "side") { const f = mesh(new THREE.BoxGeometry(0.22, 0.06, 0.06), hairM, head, 0.03, 0.14, -0.13); f.rotation.z = -0.2; }
  } else {
    for (const sx of [-1, 1]) mesh(new THREE.SphereGeometry(0.05, 10, 8), hairM, head, sx * 0.15, 0.03, 0.06);              // fringe above the ears
  }
  // arms: shoulder pivot, upper arm, elbow pivot, forearm, hand
  const arms = [];
  for (const sx of [-1, 1]) {
    const sh = new THREE.Group(); sh.position.set(sx * 0.24, 0.53, 0); torso.add(sh);
    mesh(new THREE.CapsuleGeometry(0.06, 0.2, 4, 10), shirtM, sh, 0, -0.14, 0);
    const el = new THREE.Group(); el.position.set(0, -0.29, 0); sh.add(el);
    mesh(new THREE.CapsuleGeometry(0.05, 0.2, 4, 10), o.shortSleeve ? skinM : shirtM, el, 0, -0.13, 0);
    const hand = mesh(new THREE.SphereGeometry(0.055, 12, 10), skinM, el, 0, -0.29, 0); hand.scale.set(0.9, 1.1, 0.7);
    const grip = new THREE.Group(); grip.position.set(0, -0.32, 0); el.add(grip);   // attach props here (phone, suitcase handle)
    arms.push({ sh, el, hand, grip, sx });
  }

  const pose = (p = {}) => {
    const st = p.legs ?? (p.seated === false ? 1 : 0);                 // 0 seated, 1 standing
    for (const L of legs) { L.hip.rotation.x = (1 - st) * 88 * D + (p.legKick || 0) * D; L.knee.rotation.x = (1 - st) * -88 * D; }
    hips.position.y = 0;
    torso.rotation.set(-(p.lean || 0) * D, (p.twist || 0) * D, (p.side || 0) * D);
    head.rotation.set(-(p.headPitch || 0) * D, (p.headYaw || 0) * D, (p.headRoll || 0) * D, "YXZ");
    arms.forEach((A, i) => { const a = (i ? p.armR : p.armL) || [5, 8, 15];
      A.sh.rotation.set(a[0] * D, 0, A.sx * a[1] * D, "ZXY"); A.el.rotation.set(a[2] * D, 0, 0); });
    const m = Math.max(0, Math.min(1, p.mouth || 0));
    mouth.scale.set(1 - m * 0.15, 0.18 + m * 0.95, 0.4);
    const bl = p.blink || 0; eyes.forEach((e) => (e.scale.y = 1.15 * (1 - 0.9 * bl))); pupils.forEach((q) => (q.visible = bl < 0.6));
    const br = p.brow || 0; brows.forEach((b, i) => { b.position.y = 0.092 + br * 0.018; b.rotation.z = (i ? -1 : 1) * br * 0.35; });
    if (p.eyesWide != null) eyes.forEach((e) => e.scale.set(1 + p.eyesWide * 0.25, 1.15 * (1 + p.eyesWide * 0.3) * (1 - 0.9 * bl), 0.5));
  };
  pose({});
  return { root, hips, torso, head, arms, pose, body, mouth };
}

// a deterministic "random" from an integer seed
export const rnd = (seed) => { let a = seed | 0; return () => { a = (a + 0x6d2b79f5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a);
  t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; };
