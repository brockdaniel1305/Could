import sys; sys.path.insert(0, __file__.rsplit('/episodes/', 1)[0] + '/tools')  # noqa: E702
from scene import *  # noqa: F403
sid = "s8-outro"
WL = 430
world = f"""
{part("sea-night", sid + "-sea", WL=WL)}
<g transform="translate(492,{WL})"><g id="{sid}-icewrap">{part("iceberg", sid + "-ice")}
  <g transform="translate(-20,-226) scale(0.5)"><g id="{sid}-kwrap">{part("keeper", sid + "-k")}</g></g></g></g>
<g fill="#9cc9ea" stroke="#1a1a2e" stroke-width="3"><circle id="{sid}-bub1" cx="200" cy="480" r="10" /><circle id="{sid}-bub2" cx="230" cy="500" r="7" /><circle id="{sid}-bub3" cx="180" cy="510" r="6" /></g>
{part("sea-front", sid + "-front", WL=WL + 18)}
"""
js = """
      waves(S + "sea-waves1", S + "front-waves2");
      tl.fromTo(S + "head", { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.2, ease: "power4.out" }, 0.1);
      show(S + "r1", C.c);
      tl.fromTo(S + "icewrap", { x: -40, y: 0 }, { x: 40, y: 4, duration: D, ease: "sine.inOut" }, 0);
      tl.fromTo(S + "k-armR", { rotation: -150 }, { rotation: -115, duration: 0.3, ease: "sine.inOut", repeat: Math.max(0, Math.floor(D / 0.3) - 1), yoyo: true }, 0);
      tl.fromTo([S + "bub1", S + "bub2", S + "bub3"], { y: 0, opacity: 1 }, { y: -70, opacity: 0, duration: 1.4, ease: "power1.out", stagger: 0.3, repeat: 1 }, 0.2);
      // the iceberg winks
      tl.to(S + "ice-browR", { y: 8, duration: 0.12, yoyo: true, repeat: 1 }, C.c + 0.6);
      swap(S + "ice-smirk", S + "ice-grin", C.c + 0.6);
"""
scene(sid, "NEXT CASE", "Who should we send next?", [("COMMENT YOUR MATCHUP", "↓", "gold")], world, js)
