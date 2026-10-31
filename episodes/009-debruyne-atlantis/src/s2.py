import sys; sys.path.insert(0, __file__.rsplit("/episodes/", 1)[0] + "/tools")  # noqa: E702
from scene import *  # noqa: F403
from ocean import *  # noqa: E402,F403
sid = "s2-kdb"
D = TIMING[sid]["duration"]
ball = f'<g transform="translate(312,{CLIFF - 16})"><g id="{sid}-ball"><g transform="scale(0.7)">{part("football", sid + "-fb")}</g></g></g>'
w = surface(sid) + fog(sid) + kdb(sid) + ball
cards = (banner(sid, "b", "THE PASSER", "Kevin De Bruyne", 40, 330)
         + card(sid, "as", "ASSISTS IN ONE SEASON", '<span id="s2-kdb-an">0</span>', 40, 380, "gold")
         + card(sid, "un", "FINDS", "The unseen", 600, 560))
js = JS + """
      tl.fromTo(S + "waves", { x: 0 }, { x: -120, duration: D, ease: "none" }, 0);
      fly("b", 0.05, C.n - 0.1, { from: "top" });
      fly("as", C.n, null);
      count("an", 0, 20, C.n + 0.2, 1.2);
      // a pass into thick fog; a hand comes out of it and catches the ball
      tl.fromTo(S + "fog", { opacity: 0 }, { opacity: 1, duration: 0.5 }, C.fog - 0.4);
      kickR(C.fog + 0.3);
      arc(S + "ball", C.fog + 0.3, 0.8, 540, -170, 160, 0.6);
      tl.to(S + "ball", { opacity: 0, duration: 0.05 }, C.fog + 1.1);
      tl.fromTo(S + "hand", { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)" }, C.fog + 0.9);
      fly("un", C.fog + 1.2, null, { from: "right" });
"""
scene(sid, w, js, cards, extra_css=CSS)
