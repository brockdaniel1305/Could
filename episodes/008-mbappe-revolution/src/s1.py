import sys; sys.path.insert(0, __file__.rsplit("/episodes/", 1)[0] + "/tools")  # noqa: E702
from scene import *  # noqa: F403
from rev import *  # noqa: E402,F403
sid = "s1-hook"
D = TIMING[sid]["duration"]
rings = "".join(f'<circle r="{r}" fill="none" stroke="{c}" stroke-width="22" stroke-dasharray="60 30" />' for r, c in ((60, "#ffd23f"), (120, "#7b5cff"), (180, "#ffd23f"), (240, "#7b5cff")))
w = (part("paris-street", sid + "-ps") + crowd_defs(sid)
     + crowd(sid, [(1200, 0.62, 5), (1200, 0.72, 4)], x0=560, dx=120)
     + cit(sid, "c1", 640) + cit(sid, "c2", 800, cap="#1d3f9b") + cit(sid, "c3", 960)
     + f'<g transform="translate(300,760)"><g id="{sid}-tun"><g id="{sid}-tunr">{rings}</g></g></g>'
     + mb(sid, 300))
cards = (banner(sid, "q", "CASE FILE 008", "Could Mbappé<br>dictate the French<br>Revolution?", 40, 300)
         + card(sid, "dst", "DESTINATION", "Paris, 1789", 40, 380)
         + card(sid, "me", "METHOD", "Scientifically", 560, 560, "gold")
         + calendar(sid, "14", "JULY", "1789"))
js = JS + """
      // the crowd is angry: pitchforks shake
      ["c1", "c2", "c3"].forEach((c, i) => tl.fromTo(S + c + "p-fork", { rotation: -8 }, { rotation: 8, transformOrigin: "50% 60%", duration: 0.2, yoyo: true, repeat: R(D, 0.2), ease: "sine.inOut" }, 0.1 * i));
      shakeCrowd(S + "cr", 0, D, 1.5);
      // the time tunnel opens, Mbappé drops out of it, lands, crosses his arms
      tl.fromTo(S + "tun", { scale: 0, opacity: 0, transformOrigin: "50% 50%" }, { scale: 1, opacity: 1, duration: 0.5, ease: "back.out(1.6)" }, C.back - 0.6);
      tl.fromTo(S + "tunr", { rotation: 0 }, { rotation: 540, transformOrigin: "50% 50%", duration: 2.2, ease: "none" }, C.back - 0.6);
      tl.to(S + "tun", { scale: 0, opacity: 0, duration: 0.35, ease: "power2.in" }, C.back + 1.3);
      tl.fromTo(S + "mw", { y: -1300 }, { y: 0, duration: 0.6, ease: "power2.in" }, C.back + 0.6);
      tl.fromTo(S + "m-body", { scaleY: 1 }, { scaleY: 0.86, transformOrigin: "50% 100%", duration: 0.08, yoyo: true, repeat: 1 }, C.back + 1.2);
      cross(C.back + 1.7);
      ["c1p", "c2p", "c3p"].forEach((p) => look(p, -6, 0, C.back + 1.3));
      tl.fromTo(S + "cal", { opacity: 0, y: -60 }, { opacity: 1, y: 0, duration: 0.4, ease: "back.out(2)" }, C.back + 1.2);
      tl.fromTo(S + "c-q", { opacity: 1, x: 0, y: 0, rotation: -2 }, { y: -1100, rotation: 8, duration: 0.4, ease: "power3.in" }, C.back - 0.4);
      fly("dst", C.back + 0.1, null);
      fly("me", C.sci, null, { from: "right" });
"""
scene(sid, w, js, cards, extra_css=".banner .bt { font-size: 74px; }" + CSS, loop_in=True)
