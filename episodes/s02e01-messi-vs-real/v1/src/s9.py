import sys; sys.path.insert(0, __file__.rsplit("/episodes/", 1)[0] + "/tools")  # noqa: E702
from scene import *  # noqa: F403
from match import *  # noqa: E402,F403
sid = "s9-shirt"
D = TIMING[sid]["duration"]
shirt = (f'<g transform="translate(540,{FEET - 330})"><g id="{sid}-shirt"><path d="M-110,-70 L-60,-100 L60,-100 L110,-70 L90,-30 L70,-40 L70,90 L-70,90 L-70,-40 L-90,-30 Z" fill="#a50044" stroke="#1a1a2e" stroke-width="6" />'
         f'<path d="M-40,-100 L-40,90 M0,-100 L0,90 M40,-100 L40,90" stroke="#1d3f9b" stroke-width="16" />'
         f'<text data-layout-ignore x="0" y="-40" text-anchor="middle" font-family="Inter" font-weight="900" font-size="34" fill="#ffd23f" stroke="#1a1a2e" stroke-width="2">MESSI</text>'
         f'<text data-layout-ignore x="0" y="56" text-anchor="middle" font-family="Inter" font-weight="900" font-size="84" fill="#ffd23f" stroke="#1a1a2e" stroke-width="3">10</text></g></g>')
fan = (f'<g transform="translate(190,800)"><g id="{sid}-fan" opacity="0"><rect x="-70" y="-60" width="140" height="80" rx="10" fill="#f4f4f2" stroke="#1a1a2e" stroke-width="4" />'
       f'<path d="M0,10 C-30,-10 -40,-30 -26,-44 C-14,-54 -4,-46 0,-38 C4,-46 14,-54 26,-44 C40,-30 30,-10 0,10 Z" fill="#ff3b5c" stroke="#1a1a2e" stroke-width="3" /></g></g>')
w = world(sid, messi_fig(sid, 540, FEET + 120, 0.95, name="m", tag=False) + shirt + fan)
cards = (hud(sid, h=2, a=3, minute="92'") + card(sid, "y17", "23 APRIL 2017", "Real 2–3 Barça · 92'", 40, 380, "gold")
         + card(sid, "sm", "TODAY", "Same score", 560, 560, "red"))
js = JS + """
      stamina(3);
      tl.set(S + "fans", { opacity: 0.6 }, 0);
      tl.fromTo(S + "shirt", { y: 220, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4, ease: "back.out(1.8)" }, 0.3);
      tl.to([S + "m-armL", S + "m-armR"], { rotation: (i) => (i ? -165 : 165), duration: 0.3 }, 0.3);
      tl.fromTo(S + "shirt", { rotation: -3 }, { rotation: 3, transformOrigin: "50% 100%", duration: 0.5, yoyo: true, repeat: R(D, 0.5), ease: "sine.inOut" }, 0.7);
      tl.fromTo(S + "zoom", { scale: 1 }, { scale: 1.15, svgOrigin: "540 900", duration: D, ease: "sine.inOut" }, 0);
      fly("y17", C.y17, null);
      fly("sm", C.same, null, { from: "right" });
      // one Madrid fan holds up a heart: the like
      tl.fromTo(S + "fan", { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)" }, C.same + 0.4);
"""
scene(sid, w, js, cards, extra_css=CSS)
