import sys; sys.path.insert(0, __file__.rsplit('/episodes/', 1)[0] + '/tools')  # noqa: E702
from scene import *  # noqa: F403
sid = "s5-sprint"
WL = 470
world = f"""
{part("sea-night", sid + "-sea", WL=WL)}
<g transform="translate(0,{WL + 20})"><g id="{sid}-pan"><g transform="scale(1.55)">
  {part("titanic", sid + "-tit")}
  <g id="{sid}-bridge" transform="translate(520,-126)"><rect x="0" y="-40" width="64" height="40" fill="#f4efe6" stroke="#0d0d14" stroke-width="3" />
    <rect x="8" y="-32" width="14" height="12" fill="#7fc4e8" /><rect x="26" y="-32" width="14" height="12" fill="#7fc4e8" /><rect x="44" y="-32" width="14" height="12" fill="#7fc4e8" />
  </g>
  <g id="{sid}-bell" transform="translate(590,-216)"><text x="22" y="-8" font-family="Inter" font-weight="900" font-size="30" fill="#ffd23f" stroke="#1a1a2e" stroke-width="2">!!</text></g>
  <g transform="translate(60,-126) scale(0.3)"><g id="{sid}-kwrap">{part("keeper", sid + "-k")}</g></g>
</g></g></g>
<g id="{sid}-lines" stroke="#f4efe6" stroke-width="5" stroke-linecap="round" opacity="0">
  <path d="M120,200 L220,200 M90,240 L210,240 M130,280 L200,280" />
</g>
<g id="{sid}-bubble" transform="translate(300,128)"><path d="M150,50 L230,112 L200,50 Z" fill="#fff" stroke="#1a1a2e" stroke-width="6" stroke-linejoin="round" /><rect x="-200" y="-60" width="460" height="120" rx="30" fill="#fff" stroke="#1a1a2e" stroke-width="6" />
  <text x="30" y="18" text-anchor="middle" font-family="Inter" font-weight="900" font-size="54" fill="#e0412f">LEFT!! LEFT!!</text></g>
"""
js = """
      waves(S + "sea-waves1");
      puffs(S + "tit");
      tl.fromTo(S + "head", { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.2, ease: "power4.out" }, C.t);
      show(S + "r1", C.look); show(S + "r2", C.run); show(S + "r3", C.spare);
      // countdown in the score bug: 37 s from the lookout's call, compressed to the sprint
      const clock = document.getElementById("s5-sprint-clock");
      const ctr = { v: 37 };
      tl.fromTo(S + "timer", { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2.5)" }, C.look + 0.4);
      tl.fromTo(ctr, { v: 37 }, { v: 3, duration: C.spare - C.run, ease: "none", onUpdate() { clock.textContent = Math.round(ctr.v) + " s"; } }, C.run);
      tl.set(clock, { textContent: "37 s" }, C.look + 0.39);
      // the lookout shouts
      tl.fromTo(S + "bell", { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(3)" }, C.look + 0.3);
      tl.fromTo(S + "bell", { x: 0 }, { x: 4, duration: 0.06, repeat: 13, yoyo: true }, C.look + 0.6);
      tl.to(S + "bell", { opacity: 0, duration: 0.2 }, C.run);
      // stretch before the sprint
      tl.fromTo(S + "k-armL", { rotation: 0 }, { rotation: 170, duration: 0.4, ease: "power2.inOut", repeat: 3, yoyo: true }, C.look + 1);
      tl.fromTo(S + "k-armR", { rotation: 0 }, { rotation: -170, duration: 0.4, ease: "power2.inOut", repeat: 3, yoyo: true }, C.look + 1);
      // the sprint: keeper runs stern to bridge, camera follows
      const r0 = C.run, r1 = C.spare;
      const n = Math.floor((r1 - r0) / 0.14);
      tl.fromTo(S + "kwrap", { x: 0, rotation: 0 }, { x: 1560, rotation: 12, duration: r1 - r0, ease: "power1.inOut" }, r0);
      tl.fromTo(S + "pan", { x: 0 }, { x: -200, duration: r1 - r0, ease: "power1.inOut" }, r0);
      ["legL", "armR"].forEach((p) => tl.fromTo(S + "k-" + p, { rotation: -35 }, { rotation: 35, duration: 0.14, ease: "sine.inOut", repeat: n - 1, yoyo: true }, r0));
      ["legR", "armL"].forEach((p) => tl.fromTo(S + "k-" + p, { rotation: 35 }, { rotation: -35, duration: 0.14, ease: "sine.inOut", repeat: n - 1, yoyo: true }, r0));
      tl.fromTo(S + "lines", { opacity: 0 }, { opacity: 0.8, duration: 0.2 }, r0 + 0.1);
      tl.fromTo(S + "lines", { x: 0 }, { x: -40, duration: 0.2, ease: "none", repeat: Math.floor((r1 - r0) / 0.2) - 2 }, r0 + 0.1);
      tl.to(S + "lines", { opacity: 0, duration: 0.15 }, r1 - 0.2);
      swap(S + "k-m-smile", S + "k-m-o", r0);
      // arrives with 3 s to spare: skid, settle
      tl.to(S + "kwrap", { rotation: -10, duration: 0.15, ease: "power2.out" }, r1);
      tl.to(S + "kwrap", { rotation: 0, duration: 0.4, ease: "back.out(2)" }, r1 + 0.15);
      tl.set([S + "k-legL", S + "k-legR", S + "k-armL", S + "k-armR"], { rotation: 0 }, r1 + 0.01);
      tl.to(S + "timer", { backgroundColor: "#f3c55b", duration: 0.2 }, r1);
      swap(S + "k-m-o", S + "k-m-smile", r1 + 0.3);
      // what goalkeepers do best: deep breath ... SHOUT
      tl.to(S + "kwrap", { scale: 1.12, transformOrigin: "50% 100%", duration: 1.6, ease: "power2.inOut" }, C.shout + 0.6);
      tl.to(S + "k-armL", { rotation: 40, duration: 0.6 }, C.shout + 0.6);
      tl.to(S + "k-armR", { rotation: -40, duration: 0.6 }, C.shout + 0.6);
      swap(S + "k-m-smile", S + "k-m-o", C.he + 0.2);
      tl.to(S + "kwrap", { scale: 1, duration: 0.2, ease: "power4.out" }, C.he + 0.2);
      tl.to(S + "k-armL", { rotation: 140, duration: 0.15, ease: "power4.out" }, C.he + 0.2);
      tl.to(S + "k-armR", { rotation: -140, duration: 0.15, ease: "power4.out" }, C.he + 0.2);
      pop(S + "bubble", C.he + 0.2);
      tl.fromTo(S + "pan", { y: 0 }, { y: 6, duration: 0.05, repeat: 9, yoyo: true }, C.he + 0.25);
"""
scene(sid, "PLAN B", "The Sweeper-Keeper",
      [("WARNING TIME", "~37 s"), ("269 M DECK, SPRINTED IN", "~34 s"), ("MARGIN", "+3 s", "gold")], world, js,
      extra_css=".head { font-size: 74px; }",
      overlay=f'    <div class="bug" id="{sid}-timer">IMPACT IN <b id="{sid}-clock">37 s</b></div>')
