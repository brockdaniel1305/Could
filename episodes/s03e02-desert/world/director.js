// S3E02 "Could you survive being stranded in the desert? (Part 1)" - one continuous POV shot from the passenger seat.
// The engine dies (49 °C, no signal), the GPS "shortcut", half a bottle of water, Maya on the roof for one bar, Maya wants to walk -
// you stop her - the radio warns of a sandstorm - a brown wall rises on the horizon. "What would you do in this situation?" -> A/B.
import { keyed, sstep, lerp, clamp, noise } from "./engine.js";
import { makePerson, rnd } from "./people.js";
import { buildCar, drawScreen } from "./car.js";

const END_CARD = 34.9, STORM0 = 29.6;
const EYE = [0.37, 1.16, 0.12];

export default {
  head: [
    [0.0, 30, 2, -4, ...EYE], [1.2, 34, 3, 2, ...EYE], [2.0, 40, 2, 0, ...EYE],                                     // Maya slams the wheel, steam over the hood
    [2.6, 18, -14, 0, ...EYE], [3.9, 16, -16, 0, ...EYE],                                     // the screen: 49 °C
    [4.4, 0, -30, 0, ...EYE], [6.2, 2, -32, 0, ...EYE],                                       // your phone: no signal
    [6.7, 30, -6, 0, ...EYE], [8.8, 34, -4, 0, ...EYE],                                       // Maya, the GPS
    [9.3, 22, -16, 0, 0.33, 1.14, 0.06], [12.6, 20, -18, 0, 0.33, 1.14, 0.04],                // the GPS screen: "You have arrived"
    [13.4, 172, -46, 0, 0.04, 1.25, 0.3], [16.5, 176, -42, 0, 0.04, 1.26, 0.32],                // back seat: water, chips
    [17.2, 100, 22, 0, ...EYE], [19.9, 104, 26, 0, ...EYE],                                     // Maya up through the sunroof
    [20.6, 62, 2, 0, ...EYE], [23.2, 66, 0, 0, ...EYE],                                       // she opens her door
    [23.9, 58, -4, 0, 0.3, 1.16, 0.1], [27.2, 54, -2, 0, 0.3, 1.16, 0.1],                     // you hold her back
    [27.8, 12, -22, 0, ...EYE], [30.4, 10, -20, 0, ...EYE],                                   // the radio
    [31.3, 2, 3, 0, 0.36, 1.2, 0.05], [34.9, 0, 5, 0, 0.36, 1.22, 0.0], [41, -1, 5, 0, 0.36, 1.22, -0.02],   // the storm
  ],
  fov: (t) => 72 - 18 * sstep(31.0, 35.5, t) - 8 * sstep(9.2, 10.4, t) * (1 - sstep(12.4, 12.9, t)),
  shake: (t) => (t < 1.6 ? 1.6 * (1 - sstep(0.3, 1.6, t)) + 0.2 : t > 20.4 && t < 20.9 ? 0.4 : 0.06 + 0.25 * sstep(STORM0, 40, t)),
  fx: (t) => ({ dim: 0.6 * sstep(END_CARD, END_CARD + 0.5, t), bright: 1 + 0.12 * sstep(20.5, 21.2, t) * (1 - sstep(23.6, 24.4, t)) - 0.15 * sstep(STORM0 + 2, 40, t),
                sat: 1 - 0.15 * sstep(STORM0, 40, t) }),

  build(THREE, scene, cam) {
    const S = { V3: THREE.Vector3 }, R = rnd(8);
    const H = buildCar(THREE, scene); S.H = H;
    const lam = (c, e = {}) => new THREE.MeshLambertMaterial({ color: c, ...e });
    // Maya: driver, yellow top, sunglasses on her head
    const M = makePerson(THREE, { skin: 0xc68863, hair: 0x2b1d14, hairStyle: "long", shirt: 0xffc21a, pants: 0x3a6ea5, scale: 0.98, shortSleeve: true });
    M.root.position.set(-0.37, 0.52, 0.08); scene.add(M.root); S.M = M;
    const shades = new THREE.Mesh(new THREE.BoxGeometry(0.2, 0.04, 0.03), lam(0x111111)); shades.position.set(0, 0.15, -0.12); M.head.add(shades);
    const phone = new THREE.Group(); M.arms[1].grip.add(phone); phone.position.set(0, -0.02, -0.02); phone.rotation.set(-1.3, 0, 0);
    phone.add(new THREE.Mesh(new THREE.BoxGeometry(0.075, 0.15, 0.012), lam(0x1a1a22))); S.mphone = phone;

    // your hands (camera space), sleeve spanned shoulder -> wrist every frame
    const skin = lam(0xe8b996), sleeve = lam(0x4a6fa5);
    const mkHand = (sx) => { const g = new THREE.Group(); cam.add(g);
      const arm = new THREE.Mesh(new THREE.CylinderGeometry(0.044, 0.056, 1, 12), sleeve); cam.add(arm);
      g.add(new THREE.Mesh(new THREE.BoxGeometry(0.08, 0.03, 0.09), skin));
      const f = new THREE.Mesh(new THREE.BoxGeometry(0.075, 0.025, 0.06), skin); f.position.set(0, -0.012, -0.075); f.rotation.x = 0.5; g.add(f);
      const th = new THREE.Mesh(new THREE.CapsuleGeometry(0.013, 0.04, 4, 8), skin); th.position.set(-sx * 0.048, 0, -0.03); th.rotation.set(Math.PI / 2, 0, sx * 0.6); g.add(th);
      g.userData = { arm, sx }; g.visible = false; return g; };
    S.hL = mkHand(-1); S.hR = mkHand(1);
    // your phone (right hand): NO SERVICE
    const pT = (() => { const c = document.createElement("canvas"); c.width = 160; c.height = 300; const g = c.getContext("2d");
      g.fillStyle = "#0f1420"; g.fillRect(0, 0, 160, 300); g.fillStyle = "#fff"; g.font = "700 20px Inter, Arial"; g.fillText("12:47", 12, 28);
      g.fillStyle = "#ff5a4f"; g.font = "900 22px Inter, Arial"; g.fillText("No Service", 20, 140); g.fillStyle = "#8a94a1"; g.font = "600 16px Inter, Arial"; g.fillText("SOS only? —", 30, 170);
      for (let k = 0; k < 4; k++) { g.fillStyle = "#3a4250"; g.fillRect(110 + k * 10, 24 - k * 4, 6, 6 + k * 4); }
      const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t; })();
    S.yphone = new THREE.Mesh(new THREE.BoxGeometry(0.075, 0.15, 0.01), [lam(0x222), lam(0x222), lam(0x222), lam(0x222), new THREE.MeshBasicMaterial({ map: pT }), lam(0x222)]);
    S.yphone.position.set(0, 0.03, -0.09); S.yphone.rotation.set(-1.25, 0, 0); S.hR.add(S.yphone); S.yphone.visible = false;
    // the bottle in your hand
    S.handBottle = H.bottle.clone(); S.handBottle.position.set(0, 0.0, -0.08); S.handBottle.rotation.set(0.2, 0, 0); S.hR.add(S.handBottle); S.handBottle.visible = false;

    S.handR = keyed([
      [0, 0.25, -0.6, -0.4, 0, 0, 0], [4.2, 0.2, -0.6, -0.4, 0, 0, 0], [4.6, 0.02, -0.16, -0.34, 0.9, 0, 0], [6.2, 0.03, -0.17, -0.34, 0.9, 0, 0], [6.6, 0.2, -0.6, -0.4, 0, 0, 0],
      [13.4, 0.2, -0.6, -0.4, 0, 0, 0], [13.9, 0.05, -0.2, -0.42, 0, 0, 0], [14.4, 0.03, -0.1, -0.36, 0.3, 0, 0], [16.4, 0.04, -0.11, -0.36, 0.3, 0, 0], [16.9, 0.2, -0.6, -0.4, 0, 0, 0],
    ]);
    S.handL = keyed([
      [0, -0.25, -0.6, -0.4, 0, 0, 0], [23.5, -0.25, -0.6, -0.4, 0, 0, 0], [23.95, -0.12, -0.14, -0.48, -0.3, 0.4, -0.5], [26.9, -0.13, -0.15, -0.47, -0.3, 0.4, -0.5], [27.4, -0.25, -0.6, -0.4, 0, 0, 0],
    ]);
    // Maya's pose path: [t, lean, twist, headYaw, headPitch, armL(3), armR(3), legs, rise, eyesWide, brow]
    S.maya = keyed([
      [0, 6, -10, -25, -4, 50, 8, 40, 45, 8, 40, 0, 0, 0.8, 1], [2.2, 4, -10, -30, -6, 50, 8, 40, 45, 8, 40, 0, 0, 0.6, 1],
      [6.4, 4, -10, -30, 0, 55, 8, 45, 70, 18, 70, 0, 0, 0.4, -0.6], [8.9, 4, -10, -34, 4, 55, 8, 45, 40, 18, 60, 0, 0, 0.2, -0.4],
      [12.8, 4, -6, -20, 0, 50, 8, 45, 40, 18, 60, 0, 0, 0.2, -0.2],
      [16.8, 0, 0, 0, -20, 170, 10, 10, 175, 5, 10, 1, 0.75, 0.6, 0.8], [20.0, 0, 0, 0, -20, 170, 10, 10, 175, 5, 10, 1, 0.75, 0.6, 0.8],
      [20.5, 4, 30, 40, 0, 40, 30, 40, 20, 10, 40, 0, 0, 0.3, 0.4], [23.3, 4, 40, 50, 0, 40, 30, 40, 20, 10, 40, 0, 0, 0.2, 0.6],
      [24.0, 2, -10, -40, 0, 60, 30, 50, 20, 10, 40, 0, 0, 0.5, -0.5], [27.4, 2, -10, -38, 0, 60, 30, 50, 20, 10, 40, 0, 0, 0.4, -0.3],
      [28.0, 6, 0, -12, 14, 50, 8, 45, 50, 8, 45, 0, 0, 0.6, 0.6], [30.8, 6, 0, -10, 12, 50, 8, 45, 50, 8, 45, 0, 0, 0.8, 0.8],
      [31.6, 12, 0, 6, -4, 50, 8, 45, 95, 6, 20, 0, 0, 1.2, 1], [41, 12, 0, 4, -4, 50, 8, 45, 95, 6, 20, 0, 0, 1.2, 1],
    ]);
    S.screenKey = "";
    return S;
  },

  update(t, S) {
    const H = S.H;
    // ---------------- the world: steam, dust, the sandstorm ----------------
    H.steam.forEach((s) => { const u = ((t * 0.55 + s.userData.ph) % 1), on = 1 - sstep(14, 22, t) * 0.7;
      s.position.set(s.userData.x + Math.sin(t * 2 + s.userData.ph * 6) * 0.08 + u * 0.3, 0.95 + u * 1.2, -1.75 - u * 0.25);
      s.scale.setScalar(0.6 + u * 2.2); s.material.opacity = (1 - u) * 0.45 * on; });
    const wind = 1 + 3 * sstep(STORM0, 40, t);
    H.dust.forEach((d) => { const u = (t * d.userData.sp * wind * 0.06 + d.userData.s) % 1; d.position.x = -30 + u * 60; d.lookAt(0, d.position.y, 0);
      d.material.opacity = (0.15 + 0.4 * sstep(STORM0, 38, t)) * Math.sin(u * Math.PI); });
    const sg = sstep(STORM0, 41, t);
    H.storm.visible = t > STORM0 - 0.2;
    const r = lerp(1500, 380, sg), h = lerp(20, 700, sstep(STORM0, 35.5, t));
    H.storm.scale.set(r, h, r); H.storm.position.set(0, h / 2 - 4, 0);
    H.stormT.offset.x = (t * 0.004) % 1; H.stormT.offset.y = Math.sin(t * 0.5) * 0.01;
    H.sun.material.color.setScalar(1 - 0.3 * sg);
    scene_fog(H, t, sg);
    // lights: hot and bright, turning orange-brown as the storm comes
    H.amb.intensity = lerp(0.75, 0.5, sg); H.sunL.intensity = lerp(1.25, 0.6, sg);
    H.amb.color.setRGB(1, lerp(0.95, 0.75, sg), lerp(0.86, 0.6, sg));
    H.freshener.rotation.z = Math.sin(t * 2.2) * 0.25 + (t < 1.5 ? Math.sin(t * 14) * 0.5 * (1 - t / 1.5) : 0);
    H.wheel.rotation.z = t < 2 ? Math.sin(t * 9) * 0.06 : 0;
    // doors / sunroof
    H.doorL.rotation.y = -1.0 * sstep(20.45, 20.9, t) * (1 - sstep(23.9, 24.4, t));
    H.sunroof.visible = t < 16.6;
    // ---------------- screens ----------------
    const key = [t < 9.9 ? "route" : "arrived", t >= 27.4 && t < 34.9 ? (Math.floor(t * 3) % 2) : "fm", Math.floor(t * 2) % 2].join("|");
    if (key !== S.screenKey) { S.screenKey = key; const [g1, rd, blink] = key.split("|");
      drawScreen(H.gpsT, (g, w, hh) => { g.fillStyle = "#e9e2cf"; g.fillRect(0, 0, w, hh); g.strokeStyle = "#c9b98f"; g.lineWidth = 3;
        for (let k = 0; k < 8; k++) { g.beginPath(); g.moveTo(0, 40 * k); g.lineTo(w, 40 * k + 30); g.stroke(); }
        g.strokeStyle = "#1d6fd1"; g.lineWidth = 12; g.beginPath(); g.moveTo(60, 300); g.quadraticCurveTo(200, 200, 260, 160); g.lineTo(420, 60); g.stroke();
        g.fillStyle = "#d8202c"; g.beginPath(); g.arc(260, 160, 14, 0, 6.3); g.fill();
        g.fillStyle = "#14141f"; g.fillRect(0, 0, w, 48); g.fillStyle = "#fff"; g.font = "800 28px Inter, Arial"; g.fillText("☀ 49°C", 16, 34); g.fillText("12:47", w - 100, 34);
        if (g1 === "route") { g.fillStyle = "#1d6fd1"; g.fillRect(0, hh - 64, w, 64); g.fillStyle = "#fff"; g.font = "900 30px Inter, Arial"; g.fillText("SHORTCUT  ·  FASTEST ROUTE", 18, hh - 22); }
        else { g.fillStyle = "#2bb34a"; g.fillRect(0, hh - 84, w, 84); g.fillStyle = "#fff"; g.font = "900 40px Inter, Arial"; g.fillText("🏁 YOU HAVE ARRIVED", 18, hh - 28); } });
      drawScreen(H.radioT, (g, w, hh) => { g.fillStyle = "#081018"; g.fillRect(0, 0, w, hh); g.font = "900 56px Inter, Arial";
        if (rd === "fm") { g.fillStyle = "#6ff0ff"; g.fillText("FM  98.1", 40, 84); }
        else { g.fillStyle = rd === "1" ? "#ff3b2f" : "#ffd23f"; g.fillText("⚠ SANDSTORM", 20, 84); } });
      drawScreen(H.clusterT, (g, w, hh) => { g.fillStyle = "#0b0d12"; g.fillRect(0, 0, w, hh); g.fillStyle = blink === "1" ? "#ff3b2f" : "#5a1410"; g.font = "900 34px Inter, Arial";
        g.fillText("ENGINE", 20, 50); g.fillStyle = "#ffd23f"; g.font = "800 30px Inter, Arial"; g.fillText("TEMP ▲ HOT", 20, 98); }); }
    // ---------------- Maya ----------------
    const m = S.maya(t), M = S.M, talk = S.mouthOf("MAYA", t);
    M.root.position.set(-0.37 + m[12] * 0.3 - (t > 20.5 && t < 23.6 ? 0.1 : 0), 0.52 + m[11] * 0.45 + m[12] * 0.3, 0.08 + m[12] * 0.2);
    M.pose({ lean: m[0] + (t < 2.2 ? Math.abs(Math.sin(t * 8)) * 10 : 0), twist: m[1], headYaw: m[2] + noise(t, 3) * 4, headPitch: m[3],
             armL: [m[4] + (t < 2.2 ? Math.abs(Math.sin(t * 8)) * 18 : 0), m[5], m[6]], armR: [m[7] + (t < 2.2 ? Math.abs(Math.sin(t * 8 + 0.4)) * 18 : 0), m[8], m[9]],
             legs: m[10], mouth: talk, blink: (t % 3.3) < 0.12 ? 1 : 0, eyesWide: m[13], brow: m[14] });
    S.mphone.visible = t > 16.6 && t < 20.4;
    // ---------------- your hands ----------------
    for (const [h, fn] of [[S.hR, S.handR], [S.hL, S.handL]]) {
      const v = fn(t); h.position.set(v[0], v[1], v[2]); h.rotation.set(v[3], v[4], v[5]); h.visible = v[1] > -0.42;
      const arm = h.userData.arm; arm.visible = h.visible;
      if (h.visible) { h.updateMatrix(); const wr = new S.V3(0, 0, 0.07).applyMatrix4(h.matrix), sh = new S.V3(h.userData.sx * 0.24, -0.5, 0.05);
        const d = wr.clone().sub(sh), L = d.length(); arm.position.copy(sh).add(wr).multiplyScalar(0.5); arm.scale.set(1, L, 1);
        arm.quaternion.setFromUnitVectors(new S.V3(0, 1, 0), d.normalize()); }
    }
    S.yphone.visible = t > 4.5 && t < 6.4;
    S.handBottle.visible = t > 14.2 && t < 16.6; H.bottle.visible = !S.handBottle.visible;
    S.handBottle.children[1] && (S.handBottle.children[1].position.y = 0.05 + Math.sin(t * 6) * 0.004);
  },

  endCard(doc) {
    const hook = doc.getElementById("pov-hook"), end = doc.getElementById("pov-end");
    const items = [...end.querySelectorAll("[data-at]")];
    return (t) => {
      hook.style.opacity = String(sstep(0.0, 0.15, t) * (1 - sstep(2.1, 2.4, t)));
      end.style.display = t >= END_CARD - 0.05 ? "block" : "none";
      for (const el of items) { const at = END_CARD + +el.dataset.at, f = sstep(at, at + 0.28, t);
        el.style.opacity = String(f); el.style.transform = `translateY(${((1 - f) * 40).toFixed(1)}px) scale(${(0.92 + 0.08 * f + (el.dataset.pulse ? Math.sin(t * 3.2) * 0.012 * f : 0)).toFixed(4)})`; }
    };
  },
};

function scene_fog(H, t, sg) {
  // the air turns brown and thick as the storm closes in
  const f = H.ground.parent.fog; if (!f) return;
  f.color.setRGB(lerp(0.94, 0.62, sg), lerp(0.86, 0.45, sg), lerp(0.7, 0.27, sg));
  f.near = lerp(H.fogNear, 40, sg); f.far = lerp(H.fogFar, 900, sg);
}
