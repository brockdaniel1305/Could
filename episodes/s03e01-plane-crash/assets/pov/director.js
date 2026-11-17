// S3E01 "Could you survive a plane crash? (Part 1)" - one continuous first-person shot from seat 23A.
// Dive (masks, red light, Frank films) -> brace -> ditching on the sea -> dark cabin, water rising -> the choice: wing exit or rear door.
// Times are seconds in the final cut (voice lines placed by pov.json, see pov_timing.json).
import { keyed, sstep, lerp, clamp, noise } from "./engine.js";
import { makePerson, rnd } from "./people.js";
import { buildCabin, ROW, SEAT_X, WALL } from "./cabin.js";

const IMPACT = 26.3, END_CARD = 47.4;
const EYE = [-1.38, 1.18, 0.14];

export default {
  // ---------------- head (camera) path: [t, yaw, pitch, roll, x, y, z]; yaw + = left (window), pitch + = up ----------------
  head: [
    [0.0, -80, 2, 3, ...EYE], [1.25, -76, 1, -2, ...EYE],                                   // Frank screaming
    [1.75, 84, -14, 8, ...EYE], [2.45, 86, -12, 5, ...EYE],                                     // the window: the sea, tilted
    [2.75, 6, 26, 0, ...EYE], [3.35, 4, 18, 0, ...EYE], [3.9, -6, 2, 0, ...EYE],             // the mask
    [5.0, -12, 3, 0, ...EYE], [8.8, -22, 6, 1, -1.38, 1.24, 0.12], [10.6, -24, 6, 0, -1.38, 1.24, 0.12],              // down the aisle: the flight attendant
    [11.1, -80, 3, 0, ...EYE], [13.2, -78, 1, 0, ...EYE], [14.0, -80, -2, 0, ...EYE], [16.2, -77, 2, 0, ...EYE],   // Frank films
    [16.75, -8, -50, 0, -1.38, 1.1, 0.16], [18.6, -6, -52, 0, -1.38, 1.1, 0.16],              // belt
    [19.1, 0, -36, 0, -1.38, 1.1, 0.12], [19.9, 1, -26, 0, -1.38, 1.12, 0.1],                // safety card
    [20.4, -5, 3, 0, ...EYE], [23.6, -4, 0, 0, -1.38, 1.15, 0.1],                            // count the rows
    [24.35, -2, -58, 0, -1.38, 0.86, -0.12], [26.25, -2, -62, 0, -1.38, 0.8, -0.16],         // BRACE
    [26.45, -1, -70, 2, -1.38, 0.74, -0.24], [27.6, -2, -60, -1, -1.38, 0.8, -0.16],          // impact jolt, stay down
    [28.6, 50, -6, 0, ...EYE], [29.3, 80, -10, 2, ...EYE], [30.3, 78, -9, 1, ...EYE],          // up, the window: water
    [30.95, -6, 7, 0, -1.38, 1.26, 0.1], [32.5, -8, 6, 0, -1.38, 1.26, 0.1],                                       // the flight attendant at the exit
    [33.0, -58, 14, 0, ...EYE], [35.2, -56, 12, 0, ...EYE],                                    // across the aisle: the suitcase guy
    [35.75, -82, 0, 0, ...EYE], [41.2, -80, -2, 0, ...EYE], [41.55, -70, 6, -4, -1.44, 1.18, 0.22],   // Frank, the vest
    [42.0, -40, -10, 6, -1.1, 1.45, -0.2], [42.5, -30, -8, 4, -0.62, 1.58, -0.32], [42.9, -6, -8, -3, 0.06, 1.62, 0.3],              // climb into the aisle
    [44.1, -2, -10, 0, 0.06, 1.62, 0.32],                                                     // front: jammed, water
    [45.0, 160, -8, 0, 0.06, 1.62, 0.34], [45.35, 158, -10, 0, 0.06, 1.62, 0.34],           // rear: open door, water pouring in
    [46.0, 121, -22, 0, 0.15, 1.62, -0.3], [47.6, 120, -20, 0, 0.15, 1.62, -0.3], [54.0, 116, -14, 0, 0.14, 1.64, -0.32],   // Frank: "Which way?"
  ],
  fov: (t) => 72 - 22 * sstep(44.6, 45.0, t) * (1 - sstep(45.3, 45.6, t)) - 10 * sstep(9.0, 10.4, t) * (1 - sstep(10.7, 11.1, t)) - 12 * sstep(20.8, 23.4, t) * (1 - sstep(23.6, 24.2, t)),
  shake: (t) => {
    if (t < IMPACT) return 0.45 + 0.25 * Math.max(0, Math.sin(t * 0.9)) + 0.6 * sstep(22, IMPACT, t);
    if (t < IMPACT + 1.2) return 3.2 * (1 - sstep(IMPACT, IMPACT + 1.2, t)) + 0.2;
    return 0.12 + 0.08 * Math.sin(t * 0.7) + (t > 41.2 && t < 41.8 ? 0.8 : 0);
  },
  fx: (t) => {
    const dive = t < IMPACT, pulse = Math.pow(0.5 + 0.5 * Math.sin(t * 6.2), 2);
    const black = (t >= IMPACT && t < IMPACT + 0.45) ? (Math.floor(t * 30) % 4 === 1 ? 0.6 : 1) : t >= IMPACT + 0.45 && t < IMPACT + 0.9 ? 1 - sstep(IMPACT + 0.45, IMPACT + 0.9, t) : 0;
    return { red: dive ? 0.12 + 0.2 * pulse : 0, black, blur: t > IMPACT && t < 30 ? 3.5 * (1 - sstep(IMPACT + 0.5, 29.6, t)) : 0,
             sat: t > IMPACT && t < 30 ? lerp(0.45, 1, sstep(IMPACT + 0.5, 29.8, t)) : 1, dim: 0.62 * sstep(END_CARD, END_CARD + 0.5, t) };
  },

  build(THREE, scene, cam) {
    const S = { V3: THREE.Vector3 }, R = rnd(5);
    const H = buildCabin(THREE, scene, { front: -13, back: 5, exitRow: -4 });
    S.H = H;
    const tex = (w, h, draw) => { const c = document.createElement("canvas"); c.width = w; c.height = h; draw(c.getContext("2d"), w, h);
      const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t; };
    const lam = (c, e = {}) => new THREE.MeshLambertMaterial({ color: c, ...e });

    // ---------------- Frank (23B): Hawaiian shirt, bald, glasses ----------------
    const hawaii = tex(256, 256, (g) => { g.fillStyle = "#13a3a3"; g.fillRect(0, 0, 256, 256);
      for (let k = 0; k < 22; k++) { const x = R() * 256, y = R() * 256; g.fillStyle = k % 3 ? "#ff6b4a" : "#ffd23f";
        for (let p = 0; p < 5; p++) { g.beginPath(); g.ellipse(x + Math.cos(p * 1.26) * 9, y + Math.sin(p * 1.26) * 9, 8, 5, p * 1.26, 0, 6.3); g.fill(); }
        g.fillStyle = "#fff3c4"; g.beginPath(); g.arc(x, y, 4, 0, 6.3); g.fill(); }
      g.strokeStyle = "#0b6e5a"; g.lineWidth = 5; for (let k = 0; k < 10; k++) { g.beginPath(); g.moveTo(R() * 256, R() * 256); g.quadraticCurveTo(R() * 256, R() * 256, R() * 256, R() * 256); g.stroke(); } });
    hawaii.wrapS = hawaii.wrapT = THREE.RepeatWrapping; hawaii.repeat.set(2, 2);
    const F = makePerson(THREE, { skin: 0xf0b896, hair: 0x6b5a4a, hairStyle: "bald", shirt: hawaii, pants: 0xc9b48a, glasses: true, scale: 1.08, shortSleeve: true, beard: false });
    F.root.position.set(SEAT_X.C, 0.5, 0.06); scene.add(F.root); S.F = F;
    const phone = new THREE.Group(); F.arms[1].grip.add(phone); phone.position.set(0, -0.02, -0.03); phone.rotation.set(-1.2, 0, 0);
    phone.add(new THREE.Mesh(new THREE.BoxGeometry(0.075, 0.15, 0.012), lam(0x1a1a22)));
    const scr = new THREE.Mesh(new THREE.PlaneGeometry(0.066, 0.135), new THREE.MeshBasicMaterial({ color: 0x9fd8ff })); scr.position.z = -0.007; scr.rotation.y = Math.PI; phone.add(scr);
    const rec = new THREE.Mesh(new THREE.SphereGeometry(0.008, 8, 6), new THREE.MeshBasicMaterial({ color: 0xff2a2a })); rec.position.set(0.024, 0.06, 0.008); phone.add(rec);
    S.phone = phone; S.rec = rec;
    // his life vest (yellow), inflated later
    const vest = new THREE.Group(); F.torso.add(vest); vest.position.set(0, 0.33, -0.02);
    const vm = lam(0xffc21a);
    const vb = new THREE.Mesh(new THREE.CapsuleGeometry(0.2, 0.2, 6, 16), vm); vb.scale.set(1.05, 0.9, 0.78); vest.add(vb);
    for (const sx of [-1, 1]) { const tab = new THREE.Mesh(new THREE.BoxGeometry(0.03, 0.08, 0.02), lam(0xd8202c)); tab.position.set(sx * 0.07, -0.26, -0.2); vest.add(tab); }
    S.vest = vest; vest.visible = false;
    // Frank's own (ignored) mask hangs in front of him: handled with the other masks

    // ---------------- the flight attendant ----------------
    const FA = makePerson(THREE, { skin: 0xd9a27c, hair: 0xe3c27a, hairStyle: "bun", shirt: 0x1c2a4a, pants: 0x1c2a4a, uniform: true, scale: 1.0 });
    FA.root.rotation.y = Math.PI; scene.add(FA.root); S.FA = FA;

    // ---------------- the suitcase guy (22D) ----------------
    const SG = makePerson(THREE, { skin: 0xf2c9a8, hair: 0x9a9a9a, hairStyle: "side", shirt: 0x7a3b8f, pants: 0x3a3a3a, scale: 1.0, beard: true });
    scene.add(SG.root); S.SG = SG;
    const sticker = tex(256, 128, (g, w, h) => { g.fillStyle = "#ff4fa3"; g.fillRect(0, 0, w, h); g.fillStyle = "#ffd23f"; g.fillRect(16, 30, w - 32, 68);
      g.fillStyle = "#14141f"; g.font = "900 44px Inter, Arial"; g.textAlign = "center"; g.textBaseline = "middle"; g.fillText("DUTY FREE", w / 2, 66); });
    const suit = new THREE.Group(); scene.add(suit); S.suit = suit;
    const sm = [lam(0xff4fa3), lam(0xff4fa3), lam(0xff4fa3), lam(0xff4fa3), new THREE.MeshLambertMaterial({ map: sticker }), new THREE.MeshLambertMaterial({ map: sticker })];
    suit.add(new THREE.Mesh(new THREE.BoxGeometry(0.42, 0.55, 0.24), sm));
    const handle = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.04, 0.03), lam(0x222222)); handle.position.y = 0.3; suit.add(handle);

    // ---------------- other passengers ----------------
    const skins = [0xf1c6a0, 0xd9a27c, 0x8d5a3b, 0xf6d3b8, 0xb98563, 0x5e3a26], hairs = [0x2b1d14, 0x6b4a2a, 0xe3c27a, 0x111111, 0x9a9a9a, 0xa0522d];
    const shirts = [0x4f7fd1, 0xd8202c, 0x2bb34a, 0xffd23f, 0x8a8f98, 0xff7a59, 0x2a2a33, 0x13a3a3, 0xf4f4f2];
    const styles = ["short", "long", "bun", "cap", "side", "bald", "short", "long"];
    S.pax = [];
    for (let r = -12; r <= -1; r++) for (const L of ["A", "B", "C", "D", "E", "F"]) {
      if (r === -1 && (L === "D" || L === "A" || L === "B")) continue;   // the suitcase guy's seat; nobody right in front of you
      if (R() < 0.18) continue;
      const p = makePerson(THREE, { skin: skins[(R() * 6) | 0], hair: hairs[(R() * 6) | 0], hairStyle: styles[(R() * 8) | 0], shirt: shirts[(R() * 9) | 0],
                                    pants: 0x2d3a55, scale: 0.95 + R() * 0.12, glasses: R() < 0.2 });
      p.root.position.set(SEAT_X[L], 0.5, r * ROW + 0.06); scene.add(p.root);
      const crowd = (L === "C" || L === "D") && r >= -6 && S.pax.filter((q) => q.crowd).length < 6;
      S.pax.push({ p, r, L, seed: R() * 100, crowd, ci: S.pax.filter((q) => q.crowd).length });
    }

    // ---------------- you: legs, seat belt, the peanut bag ----------------
    const you = new THREE.Group(); scene.add(you); S.you = you;
    const jeans = lam(0x30476e), shoe = lam(0xf4f4f2);
    for (const sx of [-1, 1]) {
      const th = new THREE.Mesh(new THREE.CapsuleGeometry(0.075, 0.36, 4, 10), jeans); th.rotation.x = Math.PI / 2; th.position.set(EYE[0] + sx * 0.1, 0.58, -0.04); you.add(th);
      const sn = new THREE.Mesh(new THREE.CapsuleGeometry(0.065, 0.36, 4, 10), jeans); sn.position.set(EYE[0] + sx * 0.1, 0.3, -0.28); you.add(sn);
      const sh = new THREE.Mesh(new THREE.BoxGeometry(0.11, 0.08, 0.24), shoe); sh.position.set(EYE[0] + sx * 0.1, 0.05, -0.36); you.add(sh);
    }
    const hoodie = lam(0x2e7d6b);
    const belly = new THREE.Mesh(new THREE.BoxGeometry(0.36, 0.3, 0.24), hoodie); belly.position.set(EYE[0], 0.66, 0.24); you.add(belly);
    const strapM = lam(0x6e7480);
    S.strapL = new THREE.Mesh(new THREE.BoxGeometry(0.2, 0.012, 0.05), strapM); S.strapR = S.strapL.clone(); you.add(S.strapL, S.strapR);
    S.buckle = new THREE.Mesh(new THREE.BoxGeometry(0.07, 0.016, 0.06), lam(0xc9ced6)); you.add(S.buckle);
    const pT = tex(128, 96, (g, w, h) => { g.fillStyle = "#d8202c"; g.fillRect(0, 0, w, h); g.fillStyle = "#fff"; g.font = "900 26px Inter, Arial"; g.textAlign = "center"; g.fillText("PEANUTS", w / 2, 58); });
    S.peanuts = new THREE.Mesh(new THREE.BoxGeometry(0.12, 0.012, 0.09), [lam(0xd8202c), lam(0xd8202c), new THREE.MeshLambertMaterial({ map: pT }), lam(0xd8202c), lam(0xd8202c), lam(0xd8202c)]);
    scene.add(S.peanuts);

    // ---------------- your hands (attached to the camera) ----------------
    const skinY = lam(0xe8b996), sleeve = hoodie;
    const mkHand = (sx) => { const g = new THREE.Group(); cam.add(g);
      const arm = new THREE.Mesh(new THREE.CylinderGeometry(0.046, 0.06, 1, 12), sleeve); cam.add(arm);      // placed every frame: shoulder -> wrist
      const cuff = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 0.03, 12), lam(0x25665a)); cuff.rotation.x = Math.PI / 2; cuff.position.set(0, 0, 0.06); g.add(cuff);
      const palm = new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.03, 0.09), skinY); palm.position.set(0, 0, -0.01); g.add(palm);
      const fingers = new THREE.Mesh(new THREE.BoxGeometry(0.075, 0.025, 0.06), skinY); fingers.position.set(0, -0.012, -0.075); fingers.rotation.x = 0.5; g.add(fingers);
      const thumb = new THREE.Mesh(new THREE.CapsuleGeometry(0.013, 0.04, 4, 8), skinY); thumb.position.set(-sx * 0.048, 0.0, -0.03); thumb.rotation.set(Math.PI / 2, 0, sx * 0.6); g.add(thumb);
      const index = new THREE.Mesh(new THREE.CapsuleGeometry(0.012, 0.07, 4, 8), skinY); index.position.set(-sx * 0.026, 0.004, -0.1); index.rotation.x = Math.PI / 2; g.add(index);
      g.userData = { fingers, index, arm, sx }; g.visible = false; return g; };
    S.hL = mkHand(-1); S.hR = mkHand(1);
    // mask: the cup in your hand, then the rim of the mask on your face
    S.handMask = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.05, 0.06, 16, 1, true), lam(0xffd23f, { side: THREE.DoubleSide })); S.handMask.rotation.x = -Math.PI / 2; S.handMask.position.set(0, 0.03, -0.09);
    S.hR.add(S.handMask); S.handMask.visible = false;
    S.faceMask = new THREE.Mesh(new THREE.TorusGeometry(0.09, 0.022, 10, 32), lam(0xffd23f, { transparent: true, opacity: 0.95 }));
    S.faceMask.position.set(0, -0.085, -0.06); S.faceMask.rotation.x = 0.35; cam.add(S.faceMask);
    S.faceTube = new THREE.Mesh(new THREE.CylinderGeometry(0.0025, 0.0025, 0.3, 6), lam(0xf4f4f2)); S.faceTube.position.set(0.07, 0.06, -0.2); S.faceTube.rotation.z = -0.5; cam.add(S.faceTube);
    // the safety card in your hand
    S.handCard = S.H.card.clone(); S.handCard.position.set(0.0, 0.03, -0.1); S.handCard.rotation.set(-1.45, 0, 0); S.hR.add(S.handCard); S.handCard.visible = false;

    // hand paths in camera space: [t, x, y, z, rx, ry, rz]  (hidden when y < -0.4)
    S.handR = keyed([
      [0, 0.25, -0.6, -0.4, 0, 0, 0], [2.6, 0.2, -0.6, -0.4, 0, 0, 0], [2.95, 0.03, 0.06, -0.36, 0.6, 0, 0.2], [3.25, 0.02, 0.0, -0.3, 0.6, 0, 0.2],
      [3.62, 0.03, -0.14, -0.16, 1.0, 0, 0.1], [3.9, 0.2, -0.6, -0.3, 0, 0, 0],
      [16.85, 0.2, -0.6, -0.4, 0, 0, 0], [17.15, 0.07, -0.2, -0.34, -0.3, 0, 0.3], [17.4, 0.03, -0.2, -0.34, -0.3, 0, 0.3], [17.9, 0.2, -0.22, -0.3, -0.3, 0, 0.6],
      [18.5, 0.22, -0.24, -0.3, -0.3, 0, 0.6], [18.9, 0.2, -0.6, -0.4, 0, 0, 0],
      [19.15, 0.12, -0.32, -0.36, 0, 0, 0], [19.6, 0.03, -0.1, -0.3, 0.3, 0, 0.1], [20.15, 0.03, -0.12, -0.3, 0.3, 0, 0.1], [20.55, 0.15, -0.6, -0.4, 0, 0, 0],
      [20.7, 0.15, -0.6, -0.45, 0, 0, 0], [21.0, 0.07, -0.13, -0.42, 0.15, 0, 0.1], [21.7, 0.06, -0.12, -0.46, 0.15, 0, 0.05], [22.4, 0.06, -0.11, -0.5, 0.15, 0, 0],
      [23.1, 0.05, -0.1, -0.54, 0.15, 0, 0], [23.75, 0.12, -0.6, -0.5, 0, 0, 0],
      [24.2, 0.15, -0.6, -0.4, 0, 0, 0], [24.6, 0.09, 0.2, -0.32, -0.9, 0, 0.2], [27.7, 0.09, 0.2, -0.32, -0.9, 0, 0.2], [28.1, 0.06, -0.12, -0.18, 1.0, 0, 0.1],
      [28.55, 0.12, -0.6, -0.25, 0, 0, 0],
      [37.35, 0.2, -0.6, -0.4, 0, 0, 0], [37.65, 0.05, -0.06, -0.36, -1.3, 0, 0], [39.0, 0.06, -0.07, -0.38, -1.3, 0, -0.1], [39.9, 0.2, -0.6, -0.4, 0, 0, 0],
    ]);
    S.handL = keyed([
      [0, -0.25, -0.6, -0.4, 0, 0, 0], [13.15, -0.25, -0.6, -0.4, 0, 0, 0], [13.45, -0.06, -0.04, -0.42, 0, 0, -0.2], [13.85, -0.04, -0.2, -0.42, -0.2, 0, -0.2],
      [14.2, -0.25, -0.6, -0.4, 0, 0, 0],
      [16.85, -0.2, -0.6, -0.4, 0, 0, 0], [17.15, -0.07, -0.2, -0.34, -0.3, 0, -0.3], [17.4, -0.03, -0.2, -0.34, -0.3, 0, -0.3], [17.9, -0.2, -0.22, -0.3, -0.3, 0, -0.6],
      [18.5, -0.22, -0.24, -0.3, -0.3, 0, -0.6], [18.9, -0.2, -0.6, -0.4, 0, 0, 0],
      [24.2, -0.15, -0.6, -0.4, 0, 0, 0], [24.6, -0.09, 0.2, -0.32, -0.9, 0, -0.2], [27.7, -0.09, 0.2, -0.32, -0.9, 0, -0.2], [28.1, -0.2, -0.6, -0.3, 0, 0, 0],
      [41.7, -0.2, -0.6, -0.4, 0, 0, 0], [42.1, -0.12, -0.16, -0.4, -0.4, 0, -0.3], [42.7, -0.14, -0.2, -0.38, -0.4, 0, -0.3], [43.1, -0.2, -0.6, -0.4, 0, 0, 0],
    ]);
    // Frank's pose path: [t, lean, twist, headYaw, headPitch, headRoll, armL(3), armR(3), eyesWide, brow]
    S.frank = keyed([
      [0, 10, 22, 55, -12, 0, 150, 30, 40, 150, 30, 40, 1, 1], [2.3, 8, 20, 50, -8, 0, 150, 30, 50, 150, 30, 50, 1, 1],
      [3.0, 4, 0, 0, 0, 0, 20, 12, 60, 20, 12, 60, 0.8, 0.8], [10.6, 6, 0, -10, -4, 0, 20, 12, 60, 20, 12, 60, 0.8, 0.8],
      [11.1, 2, 6, -20, -6, 0, 20, 12, 60, 70, 18, 95, 0.4, 0.4], [13.4, 2, 6, -10, -6, 0, 20, 12, 60, 70, 18, 95, 0.4, 0.4],
      [13.85, 2, 22, 60, 0, 0, 20, 12, 60, 25, 14, 50, 0.6, -0.6], [14.85, 2, 22, 62, 0, -6, 20, 12, 60, 25, 14, 50, 0.6, -0.8],
      [15.3, 2, 6, 20, -4, 0, 20, 12, 60, 75, 18, 95, 0.3, -0.6], [23.9, 4, 6, -12, -6, 0, 20, 12, 60, 75, 18, 95, 0.4, 0.4],
      [24.5, 52, 0, 0, 30, 0, 95, 6, 70, 95, 6, 70, 1, 1], [27.6, 52, 0, 0, 30, 0, 95, 6, 70, 95, 6, 70, 1, 1],
      [29.0, 6, 0, -14, 4, 8, 15, 10, 30, 15, 10, 30, 0.9, 0.6], [35.4, 6, 0, 20, 0, 0, 15, 10, 30, 15, 10, 30, 0.6, 0.6],
      [35.9, 8, 18, 50, 10, 0, 40, 10, 100, 40, 10, 100, 0.6, 0.8], [36.9, 8, 18, 52, 10, 0, 30, 10, 60, 30, 10, 60, 0.8, 1],
      [37.6, 4, 22, 62, 0, 0, 30, 10, 60, 30, 10, 60, 0.4, 0.2], [40.0, 4, 22, 64, -2, -6, 30, 10, 60, 30, 10, 60, 0.3, -0.4],
      [41.3, 0, 18, 60, -6, 0, 40, 60, 10, 40, 60, 10, 1, 1], [41.8, -6, 18, 58, -10, 0, 30, 75, 5, 30, 75, 5, 1.2, 1],
      [45.4, -6, -15, -55, -22, 0, 30, 75, 5, 30, 75, 5, 1, 1], [54, -6, -15, -50, -20, 4, 30, 75, 5, 30, 75, 5, 0.8, 0.9],
    ]);
    // the flight attendant: [t, x, z, facing(deg), lean, legs, armL(3), armR(3), headPitch]
    const ZF = -2.75, ZE = H.Z.exit + 0.2, XE = -1.05;
    S.fa = keyed([
      [0, 0, ZF, 180, 4, 1, 40, 30, 30, 120, 20, 30, -4], [8.9, 0, ZF, 180, 4, 1, 40, 30, 30, 110, 20, 30, -4],
      [9.3, 0, ZF, 180, 22, 1, 70, 20, 10, 70, 20, 10, 6], [10.4, 0, ZF, 180, 30, 1, 40, 25, 10, 40, 25, 10, 10], [23.8, 0, ZF, 180, 10, 1, 60, 20, 30, 60, 20, 30, 0],
      [24.2, 0, ZF, 180, 24, 0.6, 150, 15, 60, 150, 15, 60, -4], [27.8, 0, ZF, 180, 24, 0.6, 150, 15, 60, 150, 15, 60, -4],
      [29.6, XE, ZE, 180, 4, 1, 30, 20, 40, 30, 20, 40, -2], [30.7, XE, ZE, 160, 4, 1, 120, 40, 70, 140, 20, 80, -4], [33.0, XE, ZE, 165, 6, 1, 150, 30, 60, 120, 20, 90, -4],
      [43.0, XE, ZE, 170, 6, 1, 150, 30, 60, 150, 20, 90, -4], [54, XE, ZE, 170, 6, 1, 150, 30, 60, 150, 20, 90, -4],
    ]);
    // the suitcase guy: [t, x, z, facing, legs, armL(3), armR(3), suitcase 0 bin .. 1 hand]
    const ZS = -ROW + 0.06;
    S.sg = keyed([
      [0, SEAT_X.D, ZS, 0, 0, 20, 10, 50, 20, 10, 50, 0], [32.3, SEAT_X.D, ZS, 0, 0, 20, 10, 50, 20, 10, 50, 0],
      [32.75, 0.12, ZS - 0.05, -90, 1, 150, 10, 30, 160, 5, 20, 0], [33.4, 0.12, ZS - 0.05, -90, 1, 150, 10, 30, 160, 5, 20, 0.15],
      [34.0, 0.1, ZS - 0.1, -90, 1, 60, 10, 40, 70, 10, 40, 1], [35.0, 0.06, ZS - 0.4, 0, 1, 30, 10, 30, 40, 10, 30, 1],
      [43.0, 0.04, -2.4, 0, 1, 30, 10, 30, 40, 10, 30, 1], [54, 0.04, -2.5, 0, 1, 30, 10, 30, 40, 10, 30, 1],
    ]);
    return S;
  },

  update(t, S) {
    const H = S.H, dive = t < IMPACT, after = t >= IMPACT;
    // ---------------- the world outside ----------------
    const alt = dive ? 3 + 380 * Math.pow(1 - t / IMPACT, 1.35) : 0;
    const oy = dive ? -alt : lerp(-0.4, 0.95, sstep(IMPACT, IMPACT + 1.6, t)) + Math.sin(t * 1.1) * 0.05;
    H.outside.position.y = 0;
    H.ocean.position.y = oy;
    H.outside.rotation.x = dive ? 0.32 - 0.26 * sstep(23.5, IMPACT, t) : -0.03 * sstep(30, 44, t);
    H.outside.rotation.z = dive ? Math.sin(t * 0.55) * 0.14 + Math.sin(t * 1.7) * 0.03 : Math.sin(t * 0.8) * 0.025;
    H.seaT.offset.y = dive ? (t * 0.9) % 1 : (IMPACT * 0.9 + (t - IMPACT) * 0.004) % 1;
    H.clouds.forEach((c, k) => { c.position.z = ((k * 137 + (dive ? t * 160 : IMPACT * 160)) % 1800) - 900; c.visible = dive; });
    // ---------------- lights ----------------
    const flick = dive ? 0.75 + 0.25 * Math.sin(t * 13) * Math.sin(t * 7.1) : 0;
    H.stripM.emissiveIntensity = dive ? flick : 0;
    H.amb.intensity = dive ? 0.5 + 0.05 * flick : 0.22;
    H.hemi.intensity = dive ? 0.7 : 0.38;
    H.hemi.color.setHex(dive ? 0xfff6e8 : 0xcfe2ff);
    H.sun.intensity = dive ? 0.6 : 1.05;
    H.reds.forEach((p, k) => (p.intensity = dive ? 1.4 * Math.pow(0.5 + 0.5 * Math.sin(t * 6.2 + k * 0.5), 2) : 0));
    H.pathM.emissiveIntensity = after ? 1.3 : 0;
    H.exitSigns.forEach((s) => (s.material.color.setScalar(after ? 1.25 : 1)));
    // over-wing exit opens, rear door opens (water pours in)
    H.hatch.visible = t < 29.7; H.exitLight.intensity = t >= 29.7 ? 1.6 : 0;
    H.rearDoor.visible = t < 30; H.doorLight.intensity = t >= 30 ? 3.0 : 0;
    H.pour.visible = t >= 30; H.pourT.offset.y = (-t * 1.4) % 1;
    // water on the floor: rises, deeper towards the sinking tail
    const lvl = t < 31 ? -0.3 : 0.01 + 0.09 * sstep(31, 46, t), k = 0.032 * sstep(31, 44, t);
    H.water.position.y = lvl + k * ((H.Z.front + H.Z.back) / 2);
    H.water.rotation.x = -Math.PI / 2 - Math.atan(k);
    H.waterT.offset.set((t * 0.02) % 1, (t * 0.05) % 1);
    // ---------------- masks ----------------
    const sw = dive ? 0.35 + 0.25 * sstep(22, IMPACT, t) : after && t < IMPACT + 1 ? 0.9 : 0.12;
    for (const m of H.masks) {
      m.pivot.rotation.x = Math.sin(t * m.fr + m.ph) * sw * 0.6 + (dive ? 0.25 : 0);
      m.pivot.rotation.z = Math.sin(t * m.fr * 0.8 + m.ph * 1.3) * sw * 0.5;
      m.pivot.visible = !(m.r === 0 && m.L === "A" && t > 2.95);                 // yours: in your hand, then on your face
    }
    S.handMask.visible = t > 2.95 && t < 3.62;
    const onFace = t >= 3.62 && t < 28.3;
    S.faceMask.visible = onFace || (t >= 28.3 && t < 28.6); S.faceTube.visible = false;
    if (t >= 28.3) S.faceMask.position.y = -0.085 - (t - 28.3) * 0.4;
    else S.faceMask.position.y = -0.085 + Math.sin(t * 4.4) * 0.003;
    // ---------------- Frank ----------------
    const f = S.frank(t), F = S.F;
    const jit = dive ? 1 : 0.3;
    F.pose({ lean: f[0] + noise(t * 4, 1) * 2 * jit, twist: f[1], headYaw: f[2] + noise(t * 3, 2) * 6 * jit, headPitch: f[3], headRoll: f[4],
             armL: [f[5] + noise(t * 6, 3) * 6 * jit, f[6], f[7]], armR: [f[8] + noise(t * 6, 4) * 6 * jit, f[9], f[10]],
             mouth: Math.max(S.mouthOf("FRANK", t), t < 2.4 ? 0.3 : 0), blink: (t % 3.7) < 0.12 ? 1 : 0, eyesWide: f[11], brow: f[12] });
    S.phone.visible = t > 10.9 && t < 24.2; S.rec.visible = Math.floor(t * 2) % 2 === 0;
    S.vest.visible = t > 30;
    const inf = t < 41.25 ? 1 : 1 + 0.75 * sstep(41.25, 41.7, t) + Math.sin(clamp((t - 41.7) / 0.4, 0, 1) * Math.PI) * 0.1;
    S.vest.scale.set(inf, 1 + (inf - 1) * 0.45, inf * 1.05);
    F.root.position.y = 0.5 + (inf - 1) * 0.05;
    // ---------------- the flight attendant ----------------
    const a = S.fa(t), FA = S.FA;
    FA.root.position.set(a[0], 0, a[1]); FA.root.rotation.y = a[2] * Math.PI / 180;
    const wave = t > 30.6 && t < 54 ? Math.sin(t * 7) * 25 : 0, yell = t > 8.9 && t < 11 ? Math.sin(t * 5) * 10 : 0;
    FA.pose({ lean: a[3], legs: a[4], armL: [a[5] + wave, a[6], a[7]], armR: [a[8] - wave, a[9], a[10] + yell], headPitch: a[11],
              mouth: S.mouthOf("FA", t), blink: (t % 4.3) < 0.12 ? 1 : 0, eyesWide: 0.4, brow: 0.6 });
    FA.root.position.y = 0.9 * a[4] + 0.5 * (1 - a[4]);
    // ---------------- the suitcase guy ----------------
    const g = S.sg(t), SG = S.SG;
    SG.root.position.set(g[0], g[3] < 0.5 ? 0.5 : 0.9 * g[3] + 0.0, g[1] + (g[3] > 0.5 && t > 35 ? Math.sin(t * 9) * 0.02 : 0));
    SG.root.position.y = lerp(0.5, 0.92, g[3]);
    SG.root.rotation.y = g[2] * Math.PI / 180;
    const tug = t > 33.4 && t < 34.4 ? Math.sin(t * 22) * 12 : 0;
    SG.pose({ legs: g[3], lean: t > 35 ? 18 : 4, armL: [g[4] + tug, g[5], g[6]], armR: [g[7] + tug, g[8], g[9]], mouth: S.mouthOf("SG", t),
              headPitch: t > 32.6 && t < 33.8 ? -25 : 0, blink: (t % 3.1) < 0.1 ? 1 : 0, brow: -0.6 });
    const binDoor = H.bins["R-1"]?.door; if (binDoor) binDoor.rotation.z = -1.4 * sstep(32.7, 33.0, t);
    // the suitcase: in the bin -> pulled out -> dragged up the aisle behind him
    const u = g[10];
    if (t < 33.4) S.suit.position.set(1.42, 1.86, -ROW - 0.12);
    else if (t < 34.0) S.suit.position.set(lerp(1.42, 0.35, u), lerp(1.86, 1.2, u), -ROW - 0.12);
    else S.suit.position.set(g[0] + 0.02, 0.3 + (t < 34.4 ? (1 - sstep(34.0, 34.4, t)) * 0.9 : 0), g[1] - 0.45);
    S.suit.rotation.set(0, t > 34 ? 0.2 : 0, t > 33.4 && t < 34.2 ? Math.sin(t * 20) * 0.3 : 0);
    S.suit.visible = t > 32.6;
    // ---------------- other passengers ----------------
    for (const q of S.pax) {
      const br = sstep(24.2, 24.9, t) * (1 - sstep(27.8, 29.0, t));
      const stand = q.crowd ? sstep(29.9, 30.3, t) : 0;
      const p = q.p, s = q.seed;
      p.root.visible = !(t > 29.9 && (q.L === "A" || q.L === "B") && q.r >= -5 && q.r <= -2);

      if (stand > 0) {
        // crowd in the aisle, pushing towards the over-wing exit
        const zt = -2.2 - q.ci * 0.55 + Math.sin(t * 0.9 + s) * 0.06;
        p.root.position.set(Math.sin(s) * 0.12, 0.92, zt); p.root.rotation.y = Math.sin(t * 0.7 + s) * 0.2;
        p.pose({ legs: 1, lean: 10, armL: [60 + Math.sin(t * 3 + s) * 25, 20, 40], armR: [40 + Math.cos(t * 2.6 + s) * 25, 20, 40], headYaw: Math.sin(t * 1.3 + s) * 25 });
      } else {
        p.root.position.set(SEAT_X[q.L], 0.5, q.r * ROW + 0.06); p.root.rotation.y = 0;
        const j = dive ? 1 : 0.25;
        p.pose({ lean: 6 + br * 50 + noise(t * 3, s) * 4 * j, headPitch: br * 30 + noise(t * 2, s + 1) * 8 * j, headYaw: noise(t * 1.5, s + 2) * 25 * j,
                 headRoll: noise(t * 2.5, s + 3) * 8 * j, armL: [20 + br * 70 + (dive ? noise(t * 5, s + 4) * 20 : 0), 15, 50], armR: [20 + br * 70, 15, 50],
                 mouth: dive && (Math.floor(t * 2 + s) % 3 === 0) ? 0.6 : 0.05, blink: ((t + s) % 3.9) < 0.12 ? 1 : 0, eyesWide: 0.6 });
      }
    }
    // ---------------- you: legs, belt, peanuts ----------------
    S.you.visible = t < 41.9;
    const clicked = t >= 17.32, pull = sstep(17.6, 18.4, t);
    const by = 0.67, bz = 0.02;
    if (!clicked) { S.strapL.position.set(EYE[0] - 0.2, 0.6, bz); S.strapL.rotation.set(0, 0, -1.2); S.strapR.position.set(EYE[0] + 0.2, 0.6, bz); S.strapR.rotation.set(0, 0, 1.2);
      S.buckle.position.set(EYE[0] - 0.24, 0.52, bz); }
    else { S.strapL.position.set(EYE[0] - 0.1, by, bz); S.strapL.rotation.set(0, 0, 0); S.strapR.position.set(EYE[0] + 0.1, by, bz); S.strapR.rotation.set(0, 0, 0);
      S.buckle.position.set(EYE[0], by + 0.005, bz); S.strapL.scale.x = S.strapR.scale.x = 1 - pull * 0.15; }
    S.peanuts.visible = t > 24.2 && t < 28.5;
    S.peanuts.position.set(EYE[0] + 0.08 - sstep(24.4, 26.2, t) * 0.18, 0.02, -0.15 - sstep(24.4, 26.6, t) * 0.55 + (t > IMPACT ? Math.sin((t - IMPACT) * 9) * 0.05 * (1 - sstep(IMPACT, 27.3, t)) : 0));
    S.peanuts.rotation.y = t * 2.5;
    // ---------------- hands ----------------
    for (const [h, fn] of [[S.hR, S.handR], [S.hL, S.handL]]) {
      const v = fn(t); h.position.set(v[0], v[1], v[2]); h.rotation.set(v[3], v[4], v[5]); h.visible = v[1] > -0.42;
      if (dive && h.visible) h.position.y += noise(t * 12, v[0] * 10) * 0.004;
      // the sleeve: from a shoulder below the frame to the wrist
      const arm = h.userData.arm; arm.visible = h.visible;
      if (h.visible) { h.updateMatrix(); const wr = new S.V3(0, 0, 0.07).applyMatrix4(h.matrix), sh = new S.V3(h.userData.sx * 0.24, -0.5, 0.05);
        const d = wr.clone().sub(sh), L = d.length(); arm.position.copy(sh).add(wr).multiplyScalar(0.5); arm.scale.set(1, L, 1);
        arm.quaternion.setFromUnitVectors(new S.V3(0, 1, 0), d.normalize()); }
    }
    S.hR.userData.index.visible = t > 20.7 && t < 23.8;                            // pointing while counting rows
    S.handCard.visible = t > 19.45 && t < 20.4; H.card.visible = !(t > 19.45 && t < 20.4);
  },

  // ---------------- DOM: the hook line and the end card ----------------
  endCard(doc) {
    const hook = doc.getElementById("pov-hook"), end = doc.getElementById("pov-end");
    const items = [...end.querySelectorAll("[data-at]")];
    return (t) => {
      const h = sstep(0.0, 0.15, t) * (1 - sstep(2.1, 2.4, t)); hook.style.opacity = String(h);
      end.style.display = t >= END_CARD - 0.05 ? "block" : "none";
      for (const el of items) { const at = END_CARD + +el.dataset.at, f = sstep(at, at + 0.28, t);
        el.style.opacity = String(f); el.style.transform = `translateY(${((1 - f) * 40).toFixed(1)}px) scale(${(0.92 + 0.08 * f + (el.dataset.pulse ? Math.sin(t * 3.2) * 0.012 * f : 0)).toFixed(4)})`; }
    };
  },
};
