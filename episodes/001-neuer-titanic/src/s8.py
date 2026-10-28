import sys; sys.path.insert(0, __file__.rsplit('/episodes/', 1)[0] + '/tools')  # noqa: E702
from scene import *  # noqa: F403
sid = "s8-outro"
WL = 1150
world = f"""
{part("sea-night", sid + "-sea", WL=WL)}
<g transform="translate(640,{WL})"><g id="{sid}-icewrap"><g transform="scale(1.6)">{part("iceberg-under", sid + "-iu")}{part("iceberg", sid + "-ice")}
  <g transform="translate(-20,-226) scale(0.5)"><g id="{sid}-kwrap">{part("keeper", sid + "-k")}</g></g></g></g></g>
<g fill="#9cc9ea" stroke="#1a1a2e" stroke-width="4"><circle id="{sid}-bub1" cx="200" cy="1240" r="14" /><circle id="{sid}-bub2" cx="240" cy="1270" r="10" /><circle id="{sid}-bub3" cx="175" cy="1285" r="8" /></g>
{part("sea-front", sid + "-front", WL=WL + 22)}
"""
cards = (banner(sid, "b", "NEXT CASE", "Who should we<br>send next?", 60, 330)
         + card(sid, "c", "COMMENT YOUR MATCHUP", "↓ ↓ ↓", 50, 620, "gold"))
js = """
      waves(S + "sea-waves1", S + "front-waves2");
      fly("b", 0.05, null, { from: "top" });
      fly("c", C.c, null, { from: "right" });
      tl.fromTo(S + "icewrap", { x: -40, y: 0 }, { x: 40, y: 4, duration: D, ease: "sine.inOut" }, 0);
      tl.fromTo(S + "k-armR", { rotation: -150 }, { rotation: -115, duration: 0.3, ease: "sine.inOut", repeat: R(D, 0.3), yoyo: true }, 0);
      tl.fromTo([S + "bub1", S + "bub2", S + "bub3"], { y: 0, opacity: 1 }, { y: -90, opacity: 0, duration: 1.4, ease: "power1.out", stagger: 0.3, repeat: 1 }, 0.2);
      // the iceberg winks
      tl.to(S + "ice-browR", { y: 8, duration: 0.12, yoyo: true, repeat: 1 }, C.c + 0.6);
      swap(S + "ice-smirk", S + "ice-grin", C.c + 0.6);
"""
scene(sid, world, js, cards)
