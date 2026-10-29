import sys; sys.path.insert(0, __file__.rsplit("/episodes/", 1)[0] + "/tools")  # noqa: E702
from scene import *  # noqa: F403
from rev import *  # noqa: E402,F403
sid = "s2-france"
D = TIMING[sid]["duration"]
sign = (f'<g transform="translate(540,822)"><g id="{sid}-sign"><path d="M-150,0 L-150,-30 M150,0 L150,-30" stroke="#1a1a2e" stroke-width="6" />'
        f'<rect x="-190" y="-14" width="380" height="96" rx="10" fill="#f4efe6" stroke="#1a1a2e" stroke-width="6" />'
        f'<text data-layout-ignore x="0" y="48" text-anchor="middle" font-family="Inter" font-weight="900" font-size="40" fill="#c0262d">WANTED: LEADER</text></g></g>')
w = (part("palace", sid + "-pa") + f'<g transform="translate(540,900)"><g id="{sid}-kw"><g transform="scale(0.8)">{part("king", sid + "-k")}</g></g></g>'
     + part("palace-rail", sid + "-rl") + sign + crowd_defs(sid)
     + crowd(sid, [(1330, 0.66, 9), (1440, 0.76, 8), (1560, 0.88, 7)], x0=-30, dx=120))
cards = (banner(sid, "b", "PARIS, 1789", "The situation", 40, 330)
         + card(sid, "pop", "POPULATION", counter(sid, "pn"), 40, 380)
         + card(sid, "br", "BREAD COSTS", '<span id="s2-france-bp">0 %</span> of a wage<div class="bar"><i id="s2-france-bar"></i></div>', 40, 380, "gold")
         + card(sid, "jb", "JOB OF LEADER", "Vacant", 560, 380, "red")
         + calendar(sid, "14", "JULY", "1789"))
js = JS + """
      fly("b", 0.1, C.pop - 0.1, { from: "top" });
      // the king eats cake
      tl.fromTo(S + "k-armR", { rotation: 0 }, { rotation: -100, duration: 0.4, yoyo: true, repeat: R(C.job, 0.8), ease: "sine.inOut" }, 0.3);
      tl.fromTo(S + "k-jaw", { y: 0 }, { y: 5, duration: 0.15, yoyo: true, repeat: R(C.job, 0.3) }, 0.5);
      shakeCrowd(S + "cr", 0, D, 1.2);
      fly("pop", C.pop, C.bread - 0.1);
      count("pn", 0, 28000000, C.pop + 0.2, 1.8);
      fly("br", C.bread, C.job - 0.1);
      tl.fromTo(S + "bar", { width: "0%" }, { width: "88%", duration: 1.2, ease: "power1.inOut" }, C.bread + 0.8);
      count("bp", 0, 88, C.bread + 0.8, 1.2, "power1.inOut", " %");
      tl.fromTo(S + "cr", { y: 0 }, { y: -20, duration: 0.15, yoyo: true, repeat: 5 }, C.bread + 2.0);
      // the king sneaks off with his cake; a sign drops onto the balcony
      tl.to(S + "kw", { x: -380, duration: 1.2, ease: "power1.in" }, C.job + 0.1);
      tl.fromTo(S + "sign", { y: -900 }, { y: 0, duration: 0.45, ease: "bounce.out" }, C.job + 0.3);
      fly("jb", C.job + 0.2, null, { from: "right" });
"""
scene(sid, w, js, cards, extra_css=CSS)
