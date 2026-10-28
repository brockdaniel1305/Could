import sys; sys.path.insert(0, __file__.rsplit('/episodes/', 1)[0] + '/tools')  # noqa: E702
from scene import *  # noqa: F403
sid = "s2-titanic"
WL = 420
world = f"""
{part("sea-night", sid + "-sea", WL=WL)}
<rect id="{sid}-day" x="0" y="0" width="984" height="{WL}" fill="#9fd4f5" />
<g id="{sid}-sun"><circle cx="160" cy="110" r="46" fill="#ffe27a" stroke="#1a1a2e" stroke-width="4" /></g>
<g transform="translate(40,{WL + 10}) scale(0.9)"><g id="{sid}-ship">
  {part("titanic", sid + "-tit")}
  <g id="{sid}-flag" transform="translate(590,-262)"><path d="M0,0 L150,14 L0,34 Z" fill="#e0412f" stroke="#1a1a2e" stroke-width="4" /><text data-layout-ignore x="12" y="23" font-family="Inter" font-weight="900" font-size="15" fill="#fff">UNSINKABLE</text></g>
</g></g>
<g transform="translate(0,{WL})"><g id="{sid}-icewrap"><g transform="translate(800,0) scale(0.8)">{part("iceberg", sid + "-ice")}</g></g></g>
<g transform="translate(640,250)">{part("burst", sid + "-bonk", WORD="BONK")}</g>
{part("sea-front", sid + "-front", WL=WL + 16)}
"""
js = """
      waves(S + "sea-waves1", S + "front-waves2");
      puffs(S + "tit");
      // proud sailing
      tl.fromTo(S + "ship", { x: -40, rotation: -0.6, svgOrigin: "325 0" }, { x: 20, rotation: 0.6, duration: C.date + 1.6, ease: "sine.inOut" }, 0);
      tl.fromTo(S + "flag", { scaleX: 0, opacity: 0 }, { scaleX: 1, opacity: 1, duration: 0.5, ease: "back.out(2)" }, C.uns);
      tl.fromTo(S + "flag", { skewY: 0 }, { skewY: 6, duration: 0.5, ease: "sine.inOut", repeat: 7, yoyo: true }, C.uns + 0.5);
      // day turns to night: 14 April 1912
      tl.fromTo([S + "day", S + "sun"], { opacity: 1 }, { opacity: 0, duration: 0.6, ease: "power2.inOut" }, C.date);
      tl.fromTo(S + "sun", { y: 0 }, { y: 220, duration: 0.6, ease: "power2.in" }, C.date);
      // the iceberg slides in and meets the bow
      const hit = C.won - 1.1;
      tl.fromTo(S + "icewrap", { x: 460 }, { x: -30, duration: hit - C.date - 0.2, ease: "power1.inOut" }, C.date + 0.2);
      tl.fromTo(S + "bonk", { scale: 0, opacity: 0, transformOrigin: "50% 50%" }, { scale: 1, opacity: 1, duration: 0.3, ease: "back.out(3)" }, hit);
      tl.to(S + "bonk", { opacity: 0, duration: 0.2 }, hit + 0.8);
      tl.to(S + "ship", { rotation: -3, x: 6, duration: 0.12, ease: "power2.out", yoyo: true, repeat: 3 }, hit);
      // the iceberg won
      swap(S + "ice-smirk", S + "ice-grin", C.won);
      tl.to([S + "ice-browL", S + "ice-browR"], { y: -12, duration: 0.25, ease: "back.out(3)" }, C.won);
      tl.to(S + "ship", { rotation: 4, duration: 1.2, ease: "power2.in" }, C.won + 0.3);
      tl.fromTo(S + "score", { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2.5)" }, C.won + 0.3);
      // facts
      tl.fromTo(S + "head", { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.2, ease: "power4.out" }, C.name);
      show(S + "r1", C.tons); show(S + "r2", C.uns); show(S + "r3", C.date);
"""
scene(sid, "SUBJECT A", "RMS Titanic",
      [("WEIGHT", "52,310 t"), ("STATUS", "Practically unsinkable"), ("MET AN ICEBERG", "14 Apr 1912")], world, js,
      overlay=f'    <div class="bug" id="{sid}-score">ICEBERG <b>1</b> : 0 TITANIC</div>')
