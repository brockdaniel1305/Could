import sys; sys.path.insert(0, __file__.rsplit("/episodes/", 1)[0] + "/tools")  # noqa: E702
from scene import *  # noqa: F403
from rev import *  # noqa: E402,F403
sid = "s8-outro"
D = TIMING[sid]["duration"]
w = (part("pitch-day", sid + "-pd", GY=1010) + mb(sid, 300, kit=WHITE)
     + f'<g transform="translate(820,{GY})"><g id="{sid}-nw"><g transform="scale(0.62)">{part("napoleon-horse", sid + "-n")}</g></g></g>')
cards = (banner(sid, "b", "NEXT CASE", "Could you imagine<br>another scenario?", 50, 330)
         + card(sid, "c", "WRITE IT IN THE COMMENTS", "↓ ↓ ↓", 330, 640, "gold"))
js = JS + """
      fly("b", 0.05, null, { from: "top" });
      fly("c", C.c, null, { from: "right" });
      tl.set(S + "m-crown", { opacity: 1 }, 0); tl.set(S + "n-crown", { opacity: 1 }, 0);
      cross(0.2);
      // Napoleon trots on the spot and waves
      gallop(0, D, "n", 0.35);
      tl.fromTo(S + "n-narm", { rotation: -150 }, { rotation: -120, duration: 0.3, yoyo: true, repeat: R(D, 0.3) }, 0);
"""
scene(sid, w, js, cards, extra_css=CSS)
