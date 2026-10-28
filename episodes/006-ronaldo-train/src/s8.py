import sys; sys.path.insert(0, __file__.rsplit("/episodes/", 1)[0] + "/tools")  # noqa: E702
from scene import *  # noqa: F403
from rail import *  # noqa: E402,F403
sid = "s8-outro"
D = TIMING[sid]["duration"]
w = station(sid) + ronaldo(sid, 200, PLAT, 0.85)
cards = (banner(sid, "b", "NEXT CASE", "Could you imagine<br>another scenario?", 50, 330)
         + card(sid, "c", "WRITE IT IN THE COMMENTS", "↓ ↓ ↓", 330, 640, "gold")
         + scorebug(sid, 2, 1))
js = SIU_JS + SCORE_JS + """
      boardName("IC 2024");
      fly("b", 0.05, null, { from: "top" });
      fly("c", C.c, null, { from: "right" });
      board([[0, "cancelled"]]);
      tl.fromTo(S + "r-armR", { rotation: -150 }, { rotation: -115, duration: 0.3, ease: "sine.inOut", repeat: R(D, 0.3), yoyo: true }, 0);
"""
scene(sid, w, js, cards, extra_css=SCORE_CSS)
