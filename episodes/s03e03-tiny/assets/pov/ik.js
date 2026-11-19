// COULD? POV series: a two-bone arm (or leg) that always stays attached - shoulder -> elbow -> wrist, solved every frame.
// makeLimb(THREE, parent, { upper, lower, r1, r2, L1, L2 }) -> { set(shoulder, wrist, pole) } with all points in parent space.
export function makeLimb(THREE, parent, o) {
  const seg = (r0, r1, m) => { const k = new THREE.Mesh(new THREE.CylinderGeometry(r1, r0, 1, 20), m); parent.add(k); return k; };
  const up = seg(o.r1, o.r1 * 0.85, o.upper), lo = seg(o.r2, o.r2 * 0.85, o.lower);
  const elbowJ = new THREE.Mesh(new THREE.SphereGeometry(o.r1 * 0.9, 16, 12), o.upper); parent.add(elbowJ);
  const shoulderJ = new THREE.Mesh(new THREE.SphereGeometry(o.r1 * 1.15, 16, 12), o.upper); parent.add(shoulderJ);
  const Y = new THREE.Vector3(0, 1, 0);
  const place = (m, a, b) => { const d = b.clone().sub(a), L = d.length(); m.position.copy(a).add(b).multiplyScalar(0.5); m.scale.set(1, L, 1);
    m.quaternion.setFromUnitVectors(Y, d.normalize()); };
  return {
    set(S, W, pole) {
      const d = W.clone().sub(S), dist = Math.min(d.length(), o.L1 + o.L2 - 0.01), dir = d.clone().normalize();
      const a = (o.L1 * o.L1 - o.L2 * o.L2 + dist * dist) / (2 * dist), h = Math.sqrt(Math.max(0, o.L1 * o.L1 - a * a));
      const n = pole.clone().sub(dir.clone().multiplyScalar(pole.dot(dir))).normalize();
      const E = S.clone().add(dir.clone().multiplyScalar(a)).add(n.multiplyScalar(h));
      const Wc = S.clone().add(dir.clone().multiplyScalar(dist));          // wrist clamped to reach
      place(up, S, E); place(lo, E, Wc); elbowJ.position.copy(E); shoulderJ.position.copy(S);
      return Wc;
    },
    meshes: [up, lo, elbowJ, shoulderJ],
  };
}
