<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>Style test 3D stadium</title>
    <style>
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { width: 1080px; height: 1920px; overflow: hidden; background: #0b1426; }
      #root { position: relative; width: 100%; height: 100%; overflow: hidden; }
      #gl { position: absolute; inset: 0; width: 1080px; height: 1920px; }
      #chars { position: absolute; inset: 0; }
      .bb { position: absolute; left: 0; top: 0; width: 0; height: 0; transform-origin: 0 0; will-change: transform; }
      .bb g[id$="-legL"], .bb g[id$="-legR"], .bb g[id$="-armL"], .bb g[id$="-armR"], .bb g[id$="-head"] { transform-box: fill-box; transform-origin: 50% 0; }
      .bb g[id$="-spin"] { transform-box: fill-box; transform-origin: 50% 50%; }
      #vig { position: absolute; inset: 0; pointer-events: none;
             background: radial-gradient(ellipse 80% 60% at 50% 55%, transparent 55%, rgba(5, 8, 20, 0.55) 100%); }
      #tag { position: absolute; left: 50%; top: 230px; transform: translateX(-50%); padding: 14px 30px; border-radius: 18px;
             background: #1a1a2e; color: #ffd23f; font: 900 54px/1 Inter, Arial, sans-serif; letter-spacing: 0.02em; opacity: 0; }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-no-timeline data-start="0" data-duration="8" data-width="1080" data-height="1920">
      <canvas id="gl" width="1080" height="1920"></canvas>
      <div id="chars">
<!--CHARS-->
      </div>
      <div id="vig"></div>
      <div id="tag">STYLE TEST · 2D FRONT / 3D BACK</div>
    </div>
    <script>
      window.__hf = window.__hf || {};
      window.__hf.buildReady = window.__hf.buildReady || {};
      window.__hf.buildReady.stadium = new Promise((r) => { window.__stadiumReady = r; });
    </script>
    <script type="module">
      import * as THREE from "./lib/three.module.min.js";

      // ---------- helpers ----------
      const mulberry = (a) => () => { a |= 0; a = (a + 0x6d2b79f5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a);
        t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
      const hash = (i, j) => mulberry(i * 7919 + j * 104729 + 13)();
      const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
      const sstep = (a, b, t) => { const x = clamp((t - a) / (b - a), 0, 1); return x * x * (3 - 2 * x); };
      const lerp = (a, b, k) => a + (b - a) * k;

      const canvas = document.getElementById("gl");
      const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
      renderer.setPixelRatio(1);
      renderer.setSize(1080, 1920, false);
      renderer.outputColorSpace = THREE.SRGBColorSpace;

      const scene = new THREE.Scene();
      const cam = new THREE.PerspectiveCamera(58, 1080 / 1920, 0.1, 600);

      // sky: night gradient with a few stars
      {
        const c = document.createElement("canvas"); c.width = 64; c.height = 512; const g = c.getContext("2d");
        const gr = g.createLinearGradient(0, 0, 0, 512);
        gr.addColorStop(0, "#050a1c"); gr.addColorStop(0.55, "#12224a"); gr.addColorStop(1, "#2b3f74");
        g.fillStyle = gr; g.fillRect(0, 0, 64, 512);
        const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace; scene.background = tx;
      }
      scene.fog = new THREE.Fog(0x1a2a52, 90, 320);

      scene.add(new THREE.AmbientLight(0xffffff, 0.5));
      scene.add(new THREE.HemisphereLight(0xcfe0ff, 0x1d3a1a, 0.7));
      const key = new THREE.DirectionalLight(0xfff1d6, 1.1); key.position.set(30, 80, 40); scene.add(key);
      const rim = new THREE.DirectionalLight(0x8fb0ff, 0.5); rim.position.set(-40, 50, -60); scene.add(rim);

      const L = 105, W = 68, HL = L / 2, HW = W / 2;

      // ---------- pitch ----------
      {
        const c = document.createElement("canvas"); c.width = 2100; c.height = 1360; const g = c.getContext("2d");
        const s = 20; // px per metre
        for (let i = 0; i < 14; i++) { g.fillStyle = i % 2 ? "#3f9a3e" : "#4aab47"; g.fillRect(i * c.width / 14, 0, c.width / 14 + 1, c.height); }
        g.strokeStyle = "#f4f4f2"; g.lineWidth = 0.14 * s * 1.6;
        g.strokeRect(0.1 * s, 0.1 * s, c.width - 0.2 * s, c.height - 0.2 * s);
        g.beginPath(); g.moveTo(c.width / 2, 0); g.lineTo(c.width / 2, c.height); g.stroke();
        g.beginPath(); g.arc(c.width / 2, c.height / 2, 9.15 * s, 0, Math.PI * 2); g.stroke();
        for (const side of [0, 1]) {
          const x0 = side ? c.width - 16.5 * s : 0, x1 = side ? c.width - 5.5 * s : 0;
          g.strokeRect(x0, c.height / 2 - 20.16 * s, 16.5 * s, 40.32 * s);
          g.strokeRect(x1, c.height / 2 - 9.16 * s, 5.5 * s, 18.32 * s);
        }
        const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace; tx.anisotropy = 8;
        const m = new THREE.Mesh(new THREE.PlaneGeometry(L, W), new THREE.MeshLambertMaterial({ map: tx }));
        m.rotation.x = -Math.PI / 2; scene.add(m);
        const apron = new THREE.Mesh(new THREE.PlaneGeometry(L + 20, W + 20), new THREE.MeshLambertMaterial({ color: 0x3b8a39 }));
        apron.rotation.x = -Math.PI / 2; apron.position.y = -0.02; scene.add(apron);
      }

      // ---------- goals ----------
      const white = new THREE.MeshLambertMaterial({ color: 0xffffff });
      for (const sx of [-1, 1]) {
        const gx = sx * HL;
        const post = (x, y, z, h, rx) => { const m = new THREE.Mesh(new THREE.CylinderGeometry(0.07, 0.07, h, 10), white);
          m.position.set(x, y, z); if (rx) m.rotation.x = Math.PI / 2; scene.add(m); };
        post(gx, 1.22, -3.66, 2.44); post(gx, 1.22, 3.66, 2.44); post(gx, 2.44, 0, 7.32, true);
        const net = new THREE.Mesh(new THREE.BoxGeometry(2, 2.44, 7.32),
          new THREE.MeshLambertMaterial({ color: 0xffffff, transparent: true, opacity: 0.22, wireframe: true }));
        net.position.set(gx + sx * 1, 1.22, 0); scene.add(net);
      }

      // ---------- ad boards ----------
      {
        const c = document.createElement("canvas"); c.width = 1024; c.height = 64; const g = c.getContext("2d");
        g.fillStyle = "#1a1a2e"; g.fillRect(0, 0, 1024, 64);
        g.font = "900 40px Inter, Arial, sans-serif"; g.textBaseline = "middle";
        g.fillStyle = "#ffd23f"; g.fillText("COULD?", 20, 34); g.fillStyle = "#f4efe6"; g.fillText("LIVE RECONSTRUCTION", 210, 34);
        g.fillStyle = "#e0412f"; g.fillRect(700, 12, 8, 40); g.fillStyle = "#4fd1ff"; g.fillText("COULD?", 760, 34);
        const tx = new THREE.CanvasTexture(c); tx.colorSpace = THREE.SRGBColorSpace; tx.wrapS = THREE.RepeatWrapping;
        window.__boardTex = tx;
        const mk = (len, x, z, ry) => { const t = tx.clone(); t.needsUpdate = true; t.repeat.set(len / 14, 1);
          const m = new THREE.Mesh(new THREE.PlaneGeometry(len, 0.9), new THREE.MeshBasicMaterial({ map: t }));
          m.position.set(x, 0.45, z); m.rotation.y = ry; scene.add(m); return t; };
        window.__boards = [mk(L + 8, 0, -HW - 3, 0), mk(L + 8, 0, HW + 3, Math.PI), mk(W, -HL - 4, 0, Math.PI / 2), mk(W, HL + 4, 0, -Math.PI / 2)];
      }

      // ---------- stands ----------
      const rnd = mulberry(42);
      const concrete = new THREE.MeshLambertMaterial({ color: 0x9aa3b5 });
      const darkband = new THREE.MeshLambertMaterial({ color: 0x23263a });
      const fanBodies = [], fanHeads = [];
      const shirtCols = [0xf4f4f2, 0xf4f4f2, 0xf4f4f2, 0xe8e8ee, 0x6a3fa0, 0x1a1a2e, 0xffd23f, 0xd0d4e0];
      const skinCols = [0xf1c9a5, 0xe0ac7e, 0xc68863, 0x8d5a3b, 0x5a3825];
      const TIERS = [ { d0: 0, rows: 26, run: 0.85, rise: 0.42, y0: 1.2 }, { d0: 26, rows: 22, run: 0.85, rise: 0.75, y0: 15.5 } ];

      function stand(len, ox, oz, ry) {
        const grp = new THREE.Group(); grp.position.set(ox, 0, oz); grp.rotation.y = ry; scene.add(grp);
        // profile in (d = distance outward, y = height), extruded along x (length)
        for (const T of TIERS) {
          const sh = new THREE.Shape(); sh.moveTo(T.d0, 0); sh.lineTo(T.d0, T.y0);
          for (let r = 0; r < T.rows; r++) { const d = T.d0 + r * T.run, y = T.y0 + r * T.rise; sh.lineTo(d + T.run, y); sh.lineTo(d + T.run, y + T.rise); }
          sh.lineTo(T.d0 + T.rows * T.run + 2, T.y0 + T.rows * T.rise); sh.lineTo(T.d0 + T.rows * T.run + 2, 0); sh.closePath();
          const geo = new THREE.ExtrudeGeometry(sh, { depth: len, bevelEnabled: false });
          const m = new THREE.Mesh(geo, concrete); m.rotation.y = -Math.PI / 2; m.position.x = len / 2; grp.add(m);
          // fans on every step
          for (let r = 0; r < T.rows; r++) for (let x = -len / 2 + 0.4; x < len / 2 - 0.4; x += 0.72) {
            if (rnd() < 0.06) continue; // empty seat
            const d = T.d0 + r * T.run + T.run * 0.5, y = T.y0 + (r + 1) * T.rise;
            fanBodies.push({ grp, x: x + (rnd() - 0.5) * 0.15, y, d, c: shirtCols[(rnd() * shirtCols.length) | 0], ph: rnd() });
            fanHeads.push(skinCols[(rnd() * skinCols.length) | 0]);
          }
        }
        // VIP band between tiers
        const band = new THREE.Mesh(new THREE.BoxGeometry(len, 4, 1.2), darkband); band.position.set(0, 14.6, 23.6); grp.add(band);
        const glass = new THREE.Mesh(new THREE.PlaneGeometry(len, 2.2), new THREE.MeshBasicMaterial({ color: 0xffd9a0 }));
        glass.position.set(0, 14.4, 22.95); glass.rotation.y = Math.PI; grp.add(glass);
        // roof with floodlight strip
        const roof = new THREE.Mesh(new THREE.BoxGeometry(len + 6, 1.4, 36), new THREE.MeshLambertMaterial({ color: 0xd8dde8 }));
        roof.position.set(0, 38, 32); grp.add(roof);
        const strip = new THREE.Mesh(new THREE.BoxGeometry(len, 0.6, 0.8), new THREE.MeshBasicMaterial({ color: 0xfff6dd }));
        strip.position.set(0, 37.2, 14.6); grp.add(strip);
        const back = new THREE.Mesh(new THREE.BoxGeometry(len + 6, 38, 1), new THREE.MeshLambertMaterial({ color: 0x5a6276 }));
        back.position.set(0, 19, 47); grp.add(back);
        return grp;
      }
      // inner edge 7 m behind the lines; the stand's local +z points away from the pitch
      const g1 = stand(L + 20, 0, -HW - 7, Math.PI);     // far long side
      const g2 = stand(L + 20, 0, HW + 7, 0);            // near long side (behind camera)
      const g3 = stand(W + 14, -HL - 7, 0, -Math.PI / 2); // left end
      const g4 = stand(W + 14, HL + 7, 0, Math.PI / 2);   // right end
      scene.updateMatrixWorld(true);

      // instanced crowd: body box + head box, world matrices baked once
      const NB = fanBodies.length;
      const bodyGeo = new THREE.BoxGeometry(0.5, 0.62, 0.3), headGeo = new THREE.BoxGeometry(0.3, 0.3, 0.3);
      const bodies = new THREE.InstancedMesh(bodyGeo, new THREE.MeshLambertMaterial(), NB);
      const heads = new THREE.InstancedMesh(headGeo, new THREE.MeshLambertMaterial(), NB);
      const base = new Float32Array(NB * 3);
      const tmp = new THREE.Object3D(), col = new THREE.Color(), v = new THREE.Vector3();
      fanBodies.forEach((f, i) => {
        v.set(f.x, f.y, f.d).applyMatrix4(f.grp.matrixWorld); base.set([v.x, v.y, v.z], i * 3);
        bodies.setColorAt(i, col.setHex(f.c)); heads.setColorAt(i, col.setHex(fanHeads[i]));
      });
      scene.add(bodies, heads);
      const crowdAt = (t) => {
        for (let i = 0; i < NB; i++) {
          const f = fanBodies[i];
          // gentle bounce; a Mexican wave rolls round the far stand
          const wave = Math.max(0, Math.sin((base[i * 3] * 0.08) - t * 3.2)) ** 6 * 0.55;
          const hop = Math.abs(Math.sin(t * 5 + f.ph * 6.28)) * 0.07 + wave;
          tmp.position.set(base[i * 3], base[i * 3 + 1] + 0.31 + hop, base[i * 3 + 2]); tmp.updateMatrix(); bodies.setMatrixAt(i, tmp.matrix);
          tmp.position.y += 0.47; tmp.updateMatrix(); heads.setMatrixAt(i, tmp.matrix);
        }
        bodies.instanceMatrix.needsUpdate = true; heads.instanceMatrix.needsUpdate = true;
      };

      // floodlight glows + camera flashes (sprites)
      const glowTex = (() => { const c = document.createElement("canvas"); c.width = c.height = 128; const g = c.getContext("2d");
        const gr = g.createRadialGradient(64, 64, 0, 64, 64, 64); gr.addColorStop(0, "rgba(255,250,235,1)"); gr.addColorStop(0.25, "rgba(255,240,200,0.55)");
        gr.addColorStop(1, "rgba(255,230,180,0)"); g.fillStyle = gr; g.fillRect(0, 0, 128, 128); return new THREE.CanvasTexture(c); })();
      const glowMat = new THREE.SpriteMaterial({ map: glowTex, blending: THREE.AdditiveBlending, depthWrite: false, transparent: true, fog: false });
      for (const [grp, len] of [[g1, L + 20], [g2, L + 20], [g3, W + 14], [g4, W + 14]])
        for (let x = -len / 2 + 6; x < len / 2 - 4; x += 9) { const s = new THREE.Sprite(glowMat); s.scale.set(9, 9, 1);
          s.position.set(x, 36.6, 14.2); grp.add(s); }
      const flashes = [];
      for (let i = 0; i < 70; i++) { const s = new THREE.Sprite(glowMat.clone()); s.scale.set(1.6, 1.6, 1);
        const f = fanBodies[(hash(i, 1) * NB) | 0]; s.position.set(base[((hash(i, 1) * NB) | 0) * 3], 0, 0);
        const k = (hash(i, 1) * NB) | 0; s.position.set(base[k * 3], base[k * 3 + 1] + 1.2, base[k * 3 + 2]); scene.add(s); flashes.push(s); }

      // ---------- camera path ----------
      const MX = (t) => -12 + 5.2 * Math.max(0, t - 3.5); // Messi x
      const K = [ // t, position, target
        [0.0, [22, 62, 18], [0, 0, -8]],
        [1.7, [14, 30, 44], [-4, 0, 0]],
        [3.0, [-6, 2.4, 14], [-7, 2.4, 0]],
        [3.8, [-10.1, 1.5, 11], [-9.2, 2.7, 0]],
        [8.0, [12.4, 1.5, 11], [13.0, 3.2, 0]],
      ];
      const posC = new THREE.CatmullRomCurve3(K.map((k) => new THREE.Vector3(...k[1])), false, "centripetal");
      const tgtC = new THREE.CatmullRomCurve3(K.map((k) => new THREE.Vector3(...k[2])), false, "centripetal");
      const camAt = (t) => {
        let i = 0; while (i < K.length - 2 && t > K[i + 1][0]) i++;
        let f = clamp((t - K[i][0]) / (K[i + 1][0] - K[i][0]), 0, 1);
        if (i === 0) f = 1 - (1 - f) ** 1.6;
        const u = (i + f) / (K.length - 1);
        if (t >= 3.8) { const x = MX(t) + 0.3; cam.position.set(x, 1.5, 11); cam.lookAt(x + 0.9, 2.7, 0); return; }
        cam.position.copy(posC.getPoint(u)); cam.lookAt(tgtC.getPoint(u));
      };

      // ---------- 2D characters ----------
      const el = (id) => document.getElementById(id);
      const chars = { messi: el("c-messi"), ball: el("c-ball") };
      const LINE = Array.from({ length: 11 }, (_, i) => ({ el: el("c-r" + i), x: -9 + i * 1.8, z: 0 }));
      const rig = (id) => document.getElementById(id);
      const mL = rig("t-m-legL"), mR = rig("t-m-legR"), maL = rig("t-m-armL"), maR = rig("t-m-armR");
      const spin = rig("t-ball-spin");
      const pA = new THREE.Vector3(), pB = new THREE.Vector3();
      function place(node, x, y, z, hM, rot = 0, sx = 1, unitH = 330) {
        pA.set(x, y, z).project(cam); pB.set(x, y + hM, z).project(cam);
        if (pA.z > 1 || pA.z < -1) { node.style.display = "none"; return; }
        node.style.display = "block";
        const X = (pA.x + 1) * 540, Y = (1 - pA.y) * 960, h = (pA.y - pB.y) * -960;
        const k = Math.abs(h) / unitH;
        node.style.transform = `translate(${X}px, ${Y}px) scale(${k * sx}, ${k}) rotate(${rot}deg)`;
        node.style.zIndex = String(1000 - Math.round(cam.position.distanceTo(pA.set(x, y, z)) * 10));
      }
      
      function charsAt(t) {
        const run = t > 3.5, ph = (t - 3.5) * 2.7 * Math.PI * 2;
        const mx = MX(t);
        place(chars.messi, mx, 0, 5, 1.7, 0, 1, 330);
        const sw = run ? Math.sin(ph) * 30 : Math.sin(t * 2) * 3;
        mL.style.transform = `rotate(${sw}deg)`; mR.style.transform = `rotate(${-sw}deg)`;
        maL.style.transform = `rotate(${-sw * 0.8}deg)`; maR.style.transform = `rotate(${sw * 0.8}deg)`;
        // ball: juggled before kick-off, then dribbled 0.9 m ahead; chipped over the defender's leg at x = 0
        let bx = mx + 0.6, by = run ? Math.abs(Math.sin(ph)) * 0.12 : Math.abs(Math.sin(t * 4.2)) * 0.9 + 0.1;
        if (!run) bx = mx + 0.35;
        const chip = sstep(-1.4, 0, bx) * (1 - sstep(0, 1.4, bx)); by += chip * 0.9;
        place(chars.ball, bx, by, 5.15, 0.22, 0, 1, 76);
        spin.style.transform = `rotate(${t * 720}deg)`;
        LINE.forEach((p, i) => {
          let x = p.x, z = p.z, rot = 0, sx = 1;
          const bob = Math.sin(t * 3 + i) * 0.02;
          if (i === 5) { // the defender who steps out, gets beaten and spins dizzy into the grass
            z = lerp(0, 3.9, sstep(4.1, 4.9, t)); x = lerp(p.x, 0.4, sstep(4.1, 4.9, t));
            const sp = sstep(5.75, 6.6, t); sx = Math.cos(sp * Math.PI * 6); rot = -78 * sstep(6.6, 7.0, t);
          } else if (t > 5.9) { // the rest turn and give chase, far too late
            x += (t - 5.9) * 2.4 * (i < 5 ? 1.1 : 0.6); z += Math.min(1, (t - 5.9)) * 1.2;
          }
          place(p.el, x, bob, z, 1.85, rot, Math.abs(sx) < 0.15 ? 0.15 * Math.sign(sx || 1) : sx, 345);
        });
      }

      function renderAt(t) {
        t = clamp(t, 0, 8);
        camAt(t); cam.updateMatrixWorld(); cam.updateProjectionMatrix();
        crowdAt(t);
        for (const b of window.__boards) b.offset.x = -t * 0.12;
        flashes.forEach((s, i) => { s.material.opacity = hash(i, Math.floor(t * 9)) > 0.86 ? 1 : 0; });
        renderer.render(scene, cam);
        charsAt(t);
        // depth of field: background sharp on the crane, soft behind the players at pitch level
        canvas.style.filter = `blur(${(2.6 * sstep(2.2, 3.4, t)).toFixed(2)}px) saturate(1.08)`;
        const tag = document.getElementById("tag"); tag.style.opacity = String(sstep(0.3, 0.7, t) * (1 - sstep(2.4, 2.8, t)));
      }
      window.addEventListener("hf-seek", (e) => renderAt(e.detail.time));
      renderAt(0);
      window.__stadiumReady();
    </script>
  </body>
</html>
