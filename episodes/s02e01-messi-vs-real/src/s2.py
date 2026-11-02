import sys; sys.path.insert(0, __file__.rsplit("/episodes/", 1)[0] + "/tools")  # noqa: E702
from scene import *  # noqa: F403
from match import *  # noqa: E402,F403
sid = "s2-bernabeu"
D = TIMING[sid]["duration"]
w = world(sid, f'<g id="{sid}-team">' + lineup(sid, FEET, 0.5) + "</g>" + messi_fig(sid, 540, FEET + 160, 0.72, name="m"))
cards = (hud(sid, h=0, a=0, minute="1'")
         + card(sid, "fa", "BERNABÉU", "~80,000 fans", 40, 380)
         + card(sid, "el", "REAL MADRID", "11 players", 560, 560, "red")
         + card(sid, "cg", "CLÁSICO GOALS", "26 (most ever)", 40, 380, "gold"))
js = JS + """
      crowdIdle();
      flashes(0, D);
      fly("fa", C.fans, C.eleven - 0.1);
      wave(C.fans + 0.2);
      fly("el", C.eleven, C.messi - 0.1, { from: "right" });
      tl.fromTo(S + "team", { x: 900 }, { x: 0, duration: 0.8, ease: "power3.out" }, C.eleven - 0.2);
      // ... and Messi. Alone: zoom in on him
      tl.to(S + "zoom", { scale: 1.9, svgOrigin: "540 1330", duration: 0.7, ease: "power2.inOut" }, C.messi - 0.1);
      fly("cg", C.messi + 0.2, null);
      tl.to([S + "m-armL", S + "m-armR"], { rotation: (i) => (i ? -20 : 20), duration: 0.2, yoyo: true, repeat: 1 }, C.alone + 0.1);
      look("m", -5, 0, C.alone);
"""
scene(sid, w, js, cards, extra_css=CSS)
