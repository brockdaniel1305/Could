import sys; sys.path.insert(0, __file__.rsplit("/episodes/", 1)[0] + "/tools")  # noqa: E702
from scene import *  # noqa: F403
from battle import *  # noqa: E402,F403
sid = "s1-hook"
D = TIMING[sid]["duration"]
w = (field(sid) + army_defs(sid) + army(sid, 560, cols=5, rows=4)
     + roman(sid, "r1", 640) + roman(sid, "r2", 800) + roman(sid, "r3", 960)
     + messi(sid, 230) + ball(sid, 272))
cards = (banner(sid, "q", "CASE FILE 007", "Could the Roman<br>Empire stop<br>prime Messi?", 40, 300)
         + card(sid, "m", "METHOD", "Historically accurate", 60, 380)
         + card(sid, "g", "SURFACE", "Grass", 600, 560, "gold")
         + scorebug(sid, 0, 0))
js = JS + """
      // the front row stamps twice while the title is up
      ["r1", "r2", "r3"].forEach((r, i) => { stompR(r, 0.6 + i * 0.03); stompR(r, 1.1 + i * 0.03); });
      tl.fromTo(S + "a", { x: 0 }, { x: -30, duration: D, ease: "sine.inOut" }, 0);
      // Messi keeps the ball under his foot, then looks at the army
      tl.fromTo(S + "m-legR", { rotation: 0 }, { rotation: -14, duration: 0.5, ease: "sine.inOut", yoyo: true, repeat: R(D, 0.5) }, 0);
      tl.fromTo(S + "ball-spin", { rotation: 0 }, { rotation: -40, transformOrigin: "50% 50%", duration: 0.5, ease: "sine.inOut", yoyo: true, repeat: R(D, 0.5) }, 0);
      look("m", 6, 0, C.ev);
      ["r1p", "r2p", "r3p"].forEach((p) => { look(p, -5, 0, C.ev + 0.2); tl.to([S + p + "-browL", S + p + "-browR"], { y: 4, duration: 0.2 }, C.ev + 0.2); });
      showScore(C.ev);
      tl.fromTo(S + "c-q", { opacity: 1, x: 0, y: 0, rotation: -2 }, { y: -1100, rotation: 8, duration: 0.4, ease: "power3.in" }, C.acc - 0.45);
      fly("m", C.acc, null);
      // on grass: the chalk lines draw themselves under the army
      fly("g", C.grass, null, { from: "right" });
      drawOn(S + "bf-line1", C.grass + 0.1, 0.5);
      drawOn(S + "bf-line2", C.grass + 0.4, 0.7);
"""
scene(sid, w, js, cards, extra_css=".banner .bt { font-size: 76px; }" + CSS, loop_in=True)
