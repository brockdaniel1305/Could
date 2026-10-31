import sys; sys.path.insert(0, __file__.rsplit('/episodes/', 1)[0] + '/tools')  # noqa: E702
from scene import *  # noqa: F403
from field import forest, board, defender, tank, GY  # noqa: E402
sid = "s8-outro"
D = TIMING[sid]["duration"]
w = forest(sid) + tank(sid, "k1", 820, 0.8) + defender(sid, 300) + board(sid)
cards = (banner(sid, "b", "NEXT CASE", "Could you imagine<br>another scenario?", 50, 330)
         + card(sid, "c", "WRITE IT IN THE COMMENTS", "↓ ↓ ↓", 330, 640, "gold"))
js = """
      fly("b", 0.05, null, { from: "top" });
      fly("c", C.c, null, { from: "right" });
      tl.fromTo(S + "u-armR", { rotation: -150 }, { rotation: -115, duration: 0.3, ease: "sine.inOut", repeat: R(D, 0.3), yoyo: true }, 0);
      tl.fromTo(S + "k1t-turret", { rotation: -6, svgOrigin: "0 -120" }, { rotation: 6, duration: 0.4, ease: "sine.inOut", repeat: R(D, 0.4), yoyo: true }, 0);
      tl.fromTo(S + "k1t-body", { y: 0 }, { y: -3, duration: 0.12, repeat: R(D, 0.12), yoyo: true }, 0);
      swap(S + "k1t-smirk", S + "k1t-grin", C.c + 0.6);
"""
scene(sid, w, js, cards, loop_out=True)
