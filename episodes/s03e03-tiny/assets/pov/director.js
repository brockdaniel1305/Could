// S3E03 "Could you survive being 3 cm tall? (Part 1)" - one continuous POV shot on a giant kitchen counter.
// Ben stirs his coffee (a coffee wave), can't hear you ("Did the toaster just squeak?"), you run for his phone past a sugar grain
// the size of your head, the toaster goes off - and Mochi the cat lands on the counter. She crouches. "What would you do?"
import { keyed, sstep, lerp, clamp, noise } from "./engine.js";
import { rnd } from "./people.js";
import { buildKitchen } from "./kitchen.js";

const C = {          // cue times (s) - match pov.json
  slam: 3.6, ben1: 4.3, yell: 7.1, ben2: 8.7, plan: 11.2, run0: 14.9, sugar: 16.4, run1: 19.0, pop: 19.25, cat: 20.25, mochi: 21.8,
  crouch: 25.0, what: 26.6, end: 28.6,
};
const Y = 1.6;
const RUN = [[-2, 9], [3, 6.6], [8, 4.9], [11.3, 4.0], [11.6, 3.9], [14.5, 5.2], [16.0, 5.8]];

export default {
  C,
  head: [
    [0.0, 34, 16, 3, -1, Y, 15], [2.8, 38, 18, -2, -1, Y, 15],                                     // the mug, a tower
    [3.5, 36, 26, 0, -1, Y, 15], [4.2, 42, 12, 0, -1.2, Y, 14.6],                                  // the spoon slams down, coffee wave
    [5.0, 172, 58, 0, -1.2, Y, 14.6], [6.9, 176, 62, 0, -1.2, Y, 14.6],                            // turn around, up: Ben
    [7.3, 174, 56, 6, -1.2, Y + 0.2, 14.6], [8.5, 178, 60, -6, -1.2, Y + 0.2, 14.6],               // "BEN! DOWN HERE!"
    [10.6, 172, 58, 0, -1.2, Y, 14.6],                                                             // "the toaster?"
    [11.6, -60, 4, 0, -1, Y, 13], [14.6, -64, 2, 0, -1, Y, 12],                                     // the phone, far away
    // the run (head path follows RUN, yaw towards the phone, with stride bob added in afterCam)
    [15.6, -64, 0, 0, 3, Y, 8.6], [16.3, -66, -6, 0, 8, Y, 4.9], [16.9, -40, -14, 0, 11.3, Y, 4.0], [18.2, -36, -16, 0, 11.6, Y, 3.9],   // the sugar grain
    [18.9, -70, 0, 0, 14.5, Y, 5.2], [19.3, -74, 0, 0, 15.2, Y, 5.6],
    [19.75, 70, 14, 0, 15.6, Y, 5.8], [20.15, 66, 16, 0, 15.8, Y, 5.8],                           // the toaster pops behind you
    [20.6, 60, 34, 0, 16.0, Y, 5.9], [24.9, 62, 37, 0, 16.0, Y, 5.9],                            // Mochi lands. Look up.
    [26.4, 61, 24, 0, 16.2, Y - 0.2, 6.0], [35, 61, 20, 0, 16.4, Y - 0.3, 6.1],                   // she crouches, eye to eye
  ],
  fov: (t) => 74 - 14 * sstep(C.crouch, C.end + 1, t) + 6 * sstep(C.run0, C.run0 + 0.6, t) * (1 - sstep(C.run1, C.run1 + 0.4, t)),
  shake: (t) => {
    const stomp = (a) => Math.max(0, 1 - Math.abs(t - a) * 4);
    return 0.08 + 1.2 * stomp(0.2) + 0.9 * stomp(1.3) + 1.6 * stomp(C.slam + 0.1) + 1.0 * stomp(C.pop) + 2.2 * stomp(C.cat) + (t > C.run0 && t < C.run1 ? 0.25 : 0);
  },
  fx: (t) => ({ dim: 0.6 * sstep(C.end, C.end + 0.5, t), sat: 1 - 0.1 * sstep(C.cat, C.end, t) }),
  afterCam: (t, S, cam) => {          // running bob
    if (t > C.run0 && t < C.run1 + 0.2 && !(t > 16.9 && t < 18.2)) { const ph = t * 11; cam.position.y += Math.abs(Math.sin(ph)) * 0.18; cam.rotation.z += Math.sin(ph) * 0.03; }
  },

  build(THREE, scene, cam) {
    const S = { V3: THREE.Vector3 }, R = rnd(4);
    const H = buildKitchen(THREE, scene); S.H = H;
    const lam = (c) => new THREE.MeshLambertMaterial({ color: c });
    // coffee drops (the wave from the spoon)
    S.drops = [];
    for (let k = 0; k < 26; k++) { const d = new THREE.Mesh(new THREE.SphereGeometry(0.25 + R() * 0.5, 12, 8), new THREE.MeshStandardMaterial({ color: 0x5a3418, roughness: 0.1 }));
      scene.add(d); d.userData = { vx: (R() - 0.2) * 8, vz: 2 + R() * 6, vy: 6 + R() * 7 }; S.drops.push(d); }
    // your hands
    const skin = lam(0xe8b996), sleeve = lam(0x2e7d6b);
    const mkHand = (sx) => { const g = new THREE.Group(); cam.add(g);
      const arm = new THREE.Mesh(new THREE.CylinderGeometry(0.044, 0.056, 1, 12), sleeve); cam.add(arm);
      g.add(new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.03, 0.09), skin));
      const f = new THREE.Mesh(new THREE.BoxGeometry(0.075, 0.025, 0.06), skin); f.position.set(0, -0.012, -0.075); f.rotation.x = 0.5; g.add(f);
      g.userData = { arm, sx }; g.visible = false; return g; };
    S.hL = mkHand(-1); S.hR = mkHand(1);
    const wave = (side) => [[C.yell - 0.15, side * 0.2, -0.6, -0.4, 0, 0, 0], [C.yell + 0.15, side * 0.14, 0.08, -0.36, -1.2, 0, side * -0.3],
      [C.yell + 0.5, side * 0.2, 0.14, -0.38, -1.2, 0, side * -0.6], [C.yell + 0.85, side * 0.13, 0.06, -0.36, -1.2, 0, side * -0.2],
      [C.yell + 1.2, side * 0.2, 0.14, -0.38, -1.2, 0, side * -0.6], [C.yell + 1.6, side * 0.2, -0.6, -0.4, 0, 0, 0]];
    S.handR = keyed([[0, 0.2, -0.6, -0.4, 0, 0, 0], ...wave(1), [C.cat + 1.2, 0.2, -0.6, -0.4, 0, 0, 0], [C.mochi + 0.3, 0.08, -0.1, -0.4, -1.3, 0, 0],
      [C.crouch, 0.09, -0.12, -0.4, -1.3, 0, 0], [C.crouch + 0.6, 0.2, -0.6, -0.4, 0, 0, 0]]);
    S.handL = keyed([[0, -0.2, -0.6, -0.4, 0, 0, 0], ...wave(-1)]);
    return S;
  },

  update(t, S) {
    const H = S.H;
    // ---------------- Ben: the spoon comes down into the mug, stirs, leaves; he looks around for his phone ----------------
    const inA = sstep(C.slam - 0.7, C.slam, t), outA = sstep(C.ben1 + 1.6, C.ben1 + 2.6, t);
    const stir = t > C.slam && t < C.ben1 + 1.6 ? 1 : 0;
    H.arm.position.set(-9 + Math.sin(t * 9) * 1.4 * stir + 30 * outA, lerp(70, 33, inA) + 30 * outA, lerp(30, 5, inA) + Math.cos(t * 9) * 1.4 * stir + 20 * outA);
    H.arm.rotation.set(0.35 - 0.2 * inA, 0, 0.1);
    H.benHead.rotation.set(0.5, t < C.ben2 ? Math.sin(t * 1.3) * 0.3 : lerp(0, 0.7, sstep(C.ben2, C.ben2 + 0.6, t)), 0);
    H.benMouth.scale.y = 0.2 + S.mouthOf("BEN", t) * 1.2;
    H.ben.position.x = -10 * sstep(C.plan, C.plan + 3, t);
    H.ben.visible = t < C.run1;
    H.benShadow.material.opacity = 0.18 * (1 - outA) * sstep(C.slam - 1, C.slam, t);
    H.coffee.position.y = 5.0 + Math.sin(t * 9) * 0.15 * stir;
    // coffee wave: drops fly out of the mug when the spoon hits
    const dt = t - C.slam;
    S.drops.forEach((d) => { const u = d.userData; d.visible = dt > 0 && dt < 2.5;
      if (!d.visible) return; const tt = Math.min(dt, 1.4);
      d.position.set(-9 + u.vx * tt * 0.6, Math.max(0.2, 6 + u.vy * tt - 9.8 * tt * tt), 4 + u.vz * tt * 0.9);
      d.scale.set(1, d.position.y <= 0.21 ? 0.25 : 1, 1); });
    // ---------------- the toaster pops ----------------
    const pop = t - C.pop;
    H.toast.forEach((tst, k) => { const y = pop < 0 ? 7 : Math.max(9, 7 + 26 * pop - 30 * pop * pop); tst.position.y = y; tst.rotation.z = pop > 0 ? Math.min(1, pop) * (k ? 1.2 : -0.9) : 0; });
    // ---------------- Mochi ----------------
    const cat = H.cat; cat.visible = t > C.cat - 0.35;
    const land = sstep(C.cat - 0.35, C.cat, t);
    const cx = -6, cz = -6;                                         // where she lands, facing you
    cat.position.set(cx, 30 * (1 - land) * (1 - land), cz);
    cat.rotation.y = Math.atan2(-(16 - cx), -(5.9 - cz)) + Math.PI;  // her head (-z) points at you
    cat.rotation.y = Math.atan2(cx - 16, cz - 5.9);
    const cr = sstep(C.crouch, C.crouch + 1.0, t);
    H.catBody.position.y = 10 - 4 * cr; H.catBody.rotation.x = -0.12 * cr;
    H.catHead.position.y = 20 - 9 * cr; H.catHead.position.z = -4 - 3 * cr;
    H.catHead.rotation.set(-0.15 + 0.2 * cr, Math.sin(t * 0.8) * 0.08, Math.sin(t * 1.3) * 0.12 * (1 - cr));
    const wiggle = cr * Math.sin(t * 16) * 0.12; H.catBody.rotation.z = wiggle;
    H.tail.forEach((g, k) => { g.rotation.x = -0.25 + 0.05 * k - 0.4 * cr; g.rotation.y = Math.sin(t * (1.6 + cr * 4) - k * 0.5) * (0.25 + cr * 0.15); });
    const wide = sstep(C.mochi + 0.4, C.mochi + 1.4, t);
    H.catPupils.forEach((p) => p.scale.set(0.35 + 0.95 * wide, 1.9 - 0.2 * wide, 0.4));
    H.catMouth.scale.y = 0.1 + (t > C.cat + 0.5 && t < C.cat + 1.6 ? 0.6 * Math.abs(Math.sin((t - C.cat) * 6)) : 0);
    H.catShadow.position.set(cx, 0.06, cz + 6); H.catShadow.material.opacity = 0.22 * land; H.catShadow.scale.set(1.2, 2, 1);
    // ---------------- sugar grains glint, the phone screen glows ----------------
    H.bigGrain.rotation.y = 0.6 + Math.sin(t * 0.5) * 0.02;
    // ---------------- your hands (sleeve spanned shoulder -> wrist) ----------------
    for (const [h, fn] of [[S.hR, S.handR], [S.hL, S.handL]]) {
      const v = fn(t); h.position.set(v[0], v[1], v[2]); h.rotation.set(v[3], v[4], v[5]); h.visible = v[1] > -0.42;
      const arm = h.userData.arm; arm.visible = h.visible;
      if (h.visible) { h.updateMatrix(); const wr = new S.V3(0, 0, 0.07).applyMatrix4(h.matrix), sh = new S.V3(h.userData.sx * 0.24, -0.5, 0.05);
        const d = wr.clone().sub(sh), L = d.length(); arm.position.copy(sh).add(wr).multiplyScalar(0.5); arm.scale.set(1, L, 1);
        arm.quaternion.setFromUnitVectors(new S.V3(0, 1, 0), d.normalize()); }
    }
  },

  endCard(doc) {
    const hook = doc.getElementById("pov-hook"), end = doc.getElementById("pov-end");
    const items = [...end.querySelectorAll("[data-at]")];
    return (t) => {
      hook.style.opacity = String(sstep(0.0, 0.15, t) * (1 - sstep(2.3, 2.6, t)));
      end.style.display = t >= C.end - 0.05 ? "block" : "none";
      for (const el of items) { const at = C.end + +el.dataset.at, f = sstep(at, at + 0.28, t);
        el.style.opacity = String(f); el.style.transform = `translateY(${((1 - f) * 40).toFixed(1)}px) scale(${(0.92 + 0.08 * f + (el.dataset.pulse ? Math.sin(t * 3.2) * 0.012 * f : 0)).toFixed(4)})`; }
    };
  },
};
