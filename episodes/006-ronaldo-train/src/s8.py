import sys; sys.path.insert(0, __file__.rsplit('/episodes/', 1)[0] + '/tools')  # noqa: E702
from scene import *  # noqa: F403
from rail import station, ruler, ronaldo, train, hline, y_m, SIU_JS, GY, PLAT, M  # noqa: E402
sid = "s8-outro"
D = TIMING[sid]["duration"]
w = station(sid) + train(sid, 260) + ronaldo(sid, 200, PLAT, 0.85)
cards = (banner(sid, "b", "NEXT CASE", "Could you imagine<br>another scenario?", 50, 330)
         + card(sid, "c", "WRITE IT IN THE COMMENTS", "↓ ↓ ↓", 330, 640, "gold"))
js = SIU_JS + """
      fly("b", 0.05, null, { from: "top" });
      fly("c", C.c, null, { from: "right" });
      board([[0, "+150 min"]]);
      tl.fromTo(S + "r-armR", { rotation: -150 }, { rotation: -115, duration: 0.3, ease: "sine.inOut", repeat: R(D, 0.3), yoyo: true }, 0);
      tl.fromTo(S + "tt-browL", { y: 0 }, { y: 6, duration: 0.12, yoyo: true, repeat: 1 }, C.c + 0.6);
"""
scene(sid, w, js, cards)
