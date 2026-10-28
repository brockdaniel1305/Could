import sys; sys.path.insert(0, __file__.rsplit('/episodes/', 1)[0] + '/tools')  # noqa: E702
from scene import *  # noqa: F403
from shot import world, ball, dots, fly, player_js, J, sx, sy, v_for, X0, GY  # noqa: E402
import math  # noqa: E402
sid = "s8-outro"
D = TIMING[sid]["duration"]
w = world(sid) + ball(sid)
cards = (banner(sid, "b", "NEXT CASE", "Who should we<br>send next?", 60, 330)
         + card(sid, "c", "COMMENT YOUR MATCHUP", "↓ ↓ ↓", 520, 620, "gold"))
js = """
      fly("b", 0.05, null, { from: "top" });
      fly("c", C.c, null, { from: "right" });
      const bx = 150 + 46, n = R(D, 0.5);
      tl.fromTo(S + "ball", { x: bx, y: 1060 }, { x: bx, y: 1232, duration: 0.25, ease: "power2.in", repeat: n * 2 + 1, yoyo: true }, 0);
      tl.fromTo(S + "p-armR", { rotation: -10 }, { rotation: -30, duration: 0.25, ease: "sine.inOut", repeat: n * 2 + 1, yoyo: true }, 0);
      tl.fromTo(S + "p-armL", { rotation: 150 }, { rotation: 120, duration: 0.3, ease: "sine.inOut", repeat: R(D, 0.3), yoyo: true }, 0);
      tl.to(S + "w-browR", { y: 10, duration: 0.12, yoyo: true, repeat: 1 }, C.c + 0.6);
      swap(S + "w-smirk", S + "w-grin", C.c + 0.6);
"""
scene(sid, w, js, cards)
