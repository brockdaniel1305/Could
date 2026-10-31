import sys; sys.path.insert(0, __file__.rsplit("/episodes/", 1)[0] + "/tools")  # noqa: E702
from scene import *  # noqa: F403
from ocean import *  # noqa: E402,F403
sid = "s1-hook"
D = TIMING[sid]["duration"]
ball = f'<g transform="translate(312,{CLIFF - 16})"><g id="{sid}-ball"><g transform="scale(0.7)">{part("football", sid + "-fb")}</g></g></g>'
q = '<g transform="translate(760,760)"><g id="s1-hook-q"><text data-layout-ignore x="0" y="0" text-anchor="middle" font-family="Inter" font-weight="900" font-size="150" fill="#ffd23f" stroke="#1a1a2e" stroke-width="8" paint-order="stroke">?</text></g></g>'
w = surface(sid) + q + kdb(sid) + ball
cards = banner(sid, "q", "CASE FILE 009", "Could prime De Bruyne<br>find Atlantis<br>with a pass?", 40, 300)
js = JS + """
      tl.fromTo(S + "c-q", { opacity: 1, x: 0, y: 0, rotation: -2 }, { opacity: 1, duration: 0.01 }, 0);
      tl.fromTo(S + "waves", { x: 0 }, { x: -120, duration: D, ease: "none" }, 0);
      tl.fromTo(S + "q", { y: 0 }, { y: -24, duration: 0.6, yoyo: true, repeat: R(D, 0.6), ease: "sine.inOut" }, 0);
      look("m", 7, 0, 0.8);
      tl.fromTo(S + "m-legR", { rotation: 0 }, { rotation: -12, duration: 0.5, yoyo: true, repeat: R(D, 0.5), ease: "sine.inOut" }, 0);
"""
scene(sid, w, js, cards, extra_css=".banner .bt { font-size: 72px; }" + CSS, loop_in=True)
