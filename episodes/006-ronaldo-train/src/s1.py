import sys; sys.path.insert(0, __file__.rsplit("/episodes/", 1)[0] + "/tools")  # noqa: E702
from scene import *  # noqa: F403
from rail import *  # noqa: E402,F403
sid = "s1-hook"
D = TIMING[sid]["duration"]
w = station(sid) + ruler(sid) + ronaldo(sid) + train(sid, 720)
cards = (banner(sid, "q", "CASE FILE 006", "Could Cristiano Ronaldo<br>jump high enough to<br>dodge a moving train?", 40, 300)
         + card(sid, "t", "TRAINS TESTED", "3", 120, 470)
         + card(sid, "f", "FORMAT", "Best of three", 150, 640, "gold")
         + scorebug(sid, 0, 0))
js = SIU_JS + SCORE_JS + """
      boardName("ICE 7");
      tl.fromTo(S + "c-q", { opacity: 1, x: 0, y: 0, rotation: -2 }, { y: -1100, rotation: 8, duration: 0.4, ease: "power3.in" }, C.three - 0.45);
      fly("t", C.three, null);
      fly("f", C.rounds, null, { from: "right" });
      tl.fromTo(S + "score", { opacity: 0, scale: 0.3, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2.4)" }, C.score);
      tl.fromTo(S + "train", { x: 0 }, { x: -40, duration: D, ease: "sine.inOut" }, 0);
      tl.fromTo(S + "r-armR", { rotation: -150 }, { rotation: -120, duration: 0.3, ease: "sine.inOut", repeat: 5, yoyo: true }, 0);
      tl.to(S + "r-armR", { rotation: 0, duration: 0.3 }, 1.9);
      blink(S + "r-lids", 2.4);
      tl.to([S + "r-pupL", S + "r-pupR"], { x: 6, duration: 0.3 }, C.ev);
      tl.to([S + "tt-browL", S + "tt-browR"], { y: -8, duration: 0.25, ease: "back.out(3)" }, C.score);
      // ready stance on "best of three"
      tl.to(S + "r-armL", { rotation: 50, duration: 0.3 }, C.score + 0.2);
      tl.to(S + "r-armR", { rotation: -50, duration: 0.3 }, C.score + 0.2);
"""
scene(sid, w, js, cards, extra_css=".banner .bt { font-size: 74px; }" + SCORE_CSS)
