import sys; sys.path.insert(0, __file__.rsplit("/episodes/", 1)[0] + "/tools")  # noqa: E702
from scene import *  # noqa: F403
from pitch import *  # noqa: E402,F403
sid = "s3-baby"
D = TIMING[sid]["duration"]
PXM = 300
ruler = (f'<path d="M90,{GY} L90,{GY - 2 * PXM}" stroke="#f4f4f2" stroke-width="6" />'
         + "".join(f'<path d="M90,{GY - m * PXM:.0f} L{120 if m % 1 == 0 else 108},{GY - m * PXM:.0f}" stroke="#f4f4f2" stroke-width="5" />' for m in (0, 0.5, 1, 1.5, 2))
         + "".join(f'<text data-layout-ignore x="130" y="{GY - m * PXM + 10:.0f}" font-family="Inter" font-weight="900" font-size="30" fill="#f4f4f2" stroke="#1a1a2e" stroke-width="2" paint-order="stroke">{m} m</text>' for m in (0.5, 1, 1.5, 2)))
face_line = f'<g id="{sid}-fl" opacity="0"><path d="M90,{GY - 1.8 * PXM:.0f} L1080,{GY - 1.8 * PXM:.0f}" stroke="#e0412f" stroke-width="8" stroke-dasharray="22 14" /></g>'
reach = f'<g id="{sid}-rl" opacity="0"><path d="M90,{GY - 0.62 * PXM:.0f} L1080,{GY - 0.62 * PXM:.0f}" stroke="#ffd23f" stroke-width="8" stroke-dasharray="22 14" /></g>'
w = pitch(sid) + ruler + face_line + reach + opp(sid, 780, 1.75) + baby(sid, 430, 0.79)
cards = (banner(sid, "b", "THE REPLACEMENT", "A baby", 40, 330)
         + card(sid, "h", "BABY", "50 cm", 40, 380, "gold")
         + card(sid, "f", "OPPONENT'S FACE", "1.8 m up", 560, 380, "red"))
js = JS + """
      fly("b", 0.05, C.h - 0.1, { from: "top" });
      fly("h", C.h, null);
      tl.fromTo(S + "fl", { opacity: 0 }, { opacity: 1, duration: 0.3 }, C.face);
      fly("f", C.face, null, { from: "right" });
      // the baby reaches up as high as it can: knee height
      tl.to(S + "b-armR", { rotation: -170, duration: 0.3, ease: "back.out(2)" }, C.face + 0.5);
      tl.fromTo(S + "bw", { y: 0 }, { y: -14, duration: 0.15, yoyo: true, repeat: 5 }, C.face + 0.6);
      tl.fromTo(S + "rl", { opacity: 0 }, { opacity: 1, duration: 0.3 }, C.face + 0.8);
      look("b", 4, -6, C.face + 0.4);
      look("op", -6, 6, C.face + 0.8);
"""
scene(sid, w, js, cards, extra_css=CSS)
