import sys; sys.path.insert(0, __file__.rsplit('/episodes/', 1)[0] + '/tools')  # noqa: E702
from scene import *  # noqa: F403
sid = "s1-hook"
WL = 400
world = f"""
{part("sea-night", sid + "-sea", WL=WL)}
<g transform="translate(860,{WL}) scale(0.95)">{part("iceberg", sid + "-ice")}</g>
<g transform="translate(-260,{WL + 20}) scale(1.3)"><g id="{sid}-ship">
  {part("titanic", sid + "-tit")}
  <g transform="translate(585,-64) scale(0.46)">{part("keeper", sid + "-k")}</g>
</g></g>
{part("sea-front", sid + "-front", WL=WL + 14)}
"""
js = """
      waves(S + "sea-waves1", S + "front-waves2");
      puffs(S + "tit");
      tl.fromTo(S + "ship", { x: 0, rotation: -0.8, svgOrigin: "325 0" }, { x: 40, rotation: 0.8, duration: D, ease: "sine.inOut" }, 0);
      // keeper waves at the camera, then notices the iceberg
      tl.fromTo(S + "k-armR", { rotation: -150 }, { rotation: -120, duration: 0.3, ease: "sine.inOut", repeat: 5, yoyo: true }, 0);
      tl.to(S + "k-armR", { rotation: 0, duration: 0.4, ease: "power2.inOut" }, 1.9);
      tl.to([S + "k-pupL", S + "k-pupR"], { x: 5, duration: 0.25, ease: "power2.out" }, C.ev - 0.3);
      swap(S + "k-m-smile", S + "k-m-o", C.ev);
      blink(S + "k-lids", 1.2); blink(S + "k-lids", 4.4);
      // iceberg: smug at 'Scientifically', creeping closer for 'far too long'
      tl.fromTo([S + "ice-browL", S + "ice-browR"], { y: 0 }, { y: -10, duration: 0.25, ease: "back.out(3)" }, C.sci);
      swap(S + "ice-smirk", S + "ice-grin", C.sci + 0.2);
      tl.fromTo(S + "ice", { x: 0 }, { x: -60, duration: D - C.long, ease: "power1.in" }, C.long);
      // facts
      tl.fromTo(S + "head .hl", { color: "#f4efe6" }, { color: "#f3c55b", duration: 0.3 }, 1.9);
      show(S + "r1", C.sci);
      show(S + "r2", C.long);
"""
scene(sid, "THE QUESTION", 'Could Manuel Neuer save the <span class="hl">Titanic</span>?',
      [("METHOD", "Scientific"), ("TIME SPENT", "Far too long", "gold")], world, js,
      extra_css=".head { font-size: 76px; } #s1-hook-head .hl { color: #f4efe6; }")
