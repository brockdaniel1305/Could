import sys; sys.path.insert(0, __file__.rsplit("/episodes/", 1)[0] + "/tools")  # noqa: E702
from scene import *  # noqa: F403
from battle import *  # noqa: E402,F403
sid = "s8-outro"
D = TIMING[sid]["duration"]
w = (field(sid) + army_defs(sid) + army(sid, 560, cols=5, rows=3)
     + "".join(roman(sid, f"r{i}", 620 + i * 160) for i in range(3))
     + messi(sid, 260) + ball(sid, 300, GY - 120, 0.75))
cards = (banner(sid, "b", "NEXT CASE", "Could you imagine<br>another scenario?", 50, 330)
         + card(sid, "c", "WRITE IT IN THE COMMENTS", "↓ ↓ ↓", 330, 640, "gold")
         + scorebug(sid, 0, 3))
js = JS + """
      fly("b", 0.05, null, { from: "top" });
      fly("c", C.c, null, { from: "right" });
      [0, 1, 2].forEach((i) => dizzy("r" + i, 0.1 + i * 0.25, 2));
      // keepy-uppies on the way out
      tl.fromTo(S + "ball", { y: 0 }, { y: 90, duration: 0.3, ease: "power2.in", yoyo: true, repeat: R(D, 0.3) }, 0);
      tl.fromTo(S + "m-legR", { rotation: 0 }, { rotation: -30, duration: 0.3, ease: "power2.in", yoyo: true, repeat: R(D, 0.3) }, 0);
      tl.fromTo(S + "ball-spin", { rotation: 0 }, { rotation: 360, duration: 0.6, ease: "none", repeat: R(D, 0.6), transformOrigin: "50% 50%" }, 0);
"""
scene(sid, w, js, cards, extra_css=CSS)
