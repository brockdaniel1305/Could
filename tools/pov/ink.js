// COULD? POV series: the "comic" look. Turns the plain three.js render into an inked, cel-shaded illustration:
//  1. toonify(scene): every lit material gets banded (cel) lighting via onBeforeCompile - flat colour areas with a hard shadow step.
//  2. createInk(renderer, scene, cam): a post pass. The scene is rendered in colour (MSAA) and once more as view-space normals
//     with a depth texture; a full-screen shader draws dark ink lines wherever depth or normal jumps (silhouettes, creases,
//     object borders), plus a light paper grain. Objects with userData.noInk (glass, smoke, water) are left out of the line pass.
export function toonify(THREE, scene, bands = 3) {
  const seen = new Set();
  scene.traverse((o) => {
    const ms = o.material ? (Array.isArray(o.material) ? o.material : [o.material]) : [];
    for (const m of ms) {
      if (!m || seen.has(m) || !(m.isMeshLambertMaterial || m.isMeshStandardMaterial || m.isMeshPhongMaterial)) continue;
      seen.add(m);
      const prev = m.onBeforeCompile;
      m.onBeforeCompile = (sh, r) => {
        if (prev) prev(sh, r);
        sh.fragmentShader = sh.fragmentShader.replace("#include <lights_fragment_end>", `#include <lights_fragment_end>
          {
            // cel shading: quantise the direct light by its brightness, keep the hue
            vec3 dd = reflectedLight.directDiffuse; float l = max(max(dd.r, dd.g), max(dd.b, 1e-4));
            float q = (floor(l * ${bands.toFixed(1)} + 0.55)) / ${bands.toFixed(1)};
            reflectedLight.directDiffuse = dd * (q / l);
            vec3 id = reflectedLight.indirectDiffuse; float li = max(max(id.r, id.g), max(id.b, 1e-4));
            reflectedLight.indirectDiffuse = id * (floor(li * 4.0 + 0.6) / 4.0 / li);
          }`);
      };
      m.needsUpdate = true;
    }
  });
}

export function createInk(THREE, renderer, scene, cam, W, H, opts = {}) {
  const rtColor = new THREE.WebGLRenderTarget(W, H, { samples: 4, type: THREE.HalfFloatType });
  rtColor.texture.colorSpace = THREE.LinearSRGBColorSpace;
  const rtN = new THREE.WebGLRenderTarget(W, H, { type: THREE.HalfFloatType });
  rtN.depthTexture = new THREE.DepthTexture(W, H); rtN.depthTexture.type = THREE.UnsignedIntType;
  const normalMat = new THREE.MeshNormalMaterial();
  const quadScene = new THREE.Scene(), quadCam = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
  const mat = new THREE.ShaderMaterial({
    uniforms: { tColor: { value: rtColor.texture }, tN: { value: rtN.texture }, tD: { value: rtN.depthTexture },
                near: { value: cam.near }, far: { value: cam.far }, res: { value: new THREE.Vector2(W, H) },
                ink: { value: new THREE.Color(opts.ink ?? 0x1b1712) }, width: { value: opts.width ?? 1.6 }, time: { value: 0 } },
    vertexShader: "varying vec2 vUv; void main(){ vUv = uv; gl_Position = vec4(position.xy, 0.0, 1.0); }",
    fragmentShader: `
      precision highp float; varying vec2 vUv;
      uniform sampler2D tColor, tN, tD; uniform float near, far, width, time; uniform vec2 res; uniform vec3 ink;
      float lin(float d){ float z = d * 2.0 - 1.0; return (2.0 * near * far) / (far + near - z * (far - near)); }
      float hash(vec2 p){ return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453); }
      void main(){
        vec2 px = width / res;
        float d0 = lin(texture2D(tD, vUv).r); vec3 n0 = texture2D(tN, vUv).rgb * 2.0 - 1.0;
        float de = 0.0, ne = 0.0;
        vec2 o[8]; o[0]=vec2(1,0); o[1]=vec2(-1,0); o[2]=vec2(0,1); o[3]=vec2(0,-1); o[4]=vec2(1,1); o[5]=vec2(-1,-1); o[6]=vec2(1,-1); o[7]=vec2(-1,1);
        for (int i = 0; i < 8; i++) {
          vec2 uv = vUv + o[i] * px;
          float d = lin(texture2D(tD, uv).r); vec3 n = texture2D(tN, uv).rgb * 2.0 - 1.0;
          de = max(de, abs(d - d0) / max(min(d, d0), 0.05));
          ne = max(ne, 1.0 - dot(n, n0));
        }
        float e = max(smoothstep(0.06, 0.16, de), smoothstep(0.25, 0.55, ne));
        e *= 1.0 - smoothstep(far * 0.35, far * 0.8, d0);            // lines fade into the distance
        vec4 c = texture2D(tColor, vUv);
        vec3 col = c.rgb;
        // light paper grain + a hint of hatching in the darkest areas, like a printed illustration
        float g = hash(floor(vUv * res / 2.0) + floor(time * 8.0)) - 0.5;
        float lum = dot(col, vec3(0.299, 0.587, 0.114));
        float hatch = step(0.5, fract((gl_FragCoord.x + gl_FragCoord.y) / 7.0)) * (1.0 - smoothstep(0.03, 0.12, lum)) * 0.25;
        col = col * (1.0 + g * 0.035) - hatch * col;
        col = mix(col, ink, e * 0.92);
        gl_FragColor = vec4(col, 1.0);
        #include <colorspace_fragment>
      }`,
  });
  quadScene.add(new THREE.Mesh(new THREE.PlaneGeometry(2, 2), mat));
  const hidden = [];
  return (t) => {
    mat.uniforms.near.value = cam.near; mat.uniforms.far.value = cam.far; mat.uniforms.time.value = t;
    renderer.setRenderTarget(rtColor); renderer.render(scene, cam);
    // normal + depth pass without glass / water / smoke / sky
    hidden.length = 0;
    scene.traverse((o) => { if (!o.visible) return; const m = o.material;
      if (o.userData.noInk || (m && !Array.isArray(m) && ((m.transparent && m.opacity < 0.7) || m.isMeshBasicMaterial && m.side === THREE.BackSide))) { o.visible = false; hidden.push(o); } });
    const bg = scene.background, fog = scene.fog; scene.background = null; scene.fog = null;
    scene.overrideMaterial = normalMat; renderer.setRenderTarget(rtN); renderer.setClearColor(0x8080ff, 1); renderer.clear(); renderer.render(scene, cam);
    scene.overrideMaterial = null; scene.background = bg; scene.fog = fog; hidden.forEach((o) => (o.visible = true));
    renderer.setRenderTarget(null); renderer.render(quadScene, quadCam);
  };
}
