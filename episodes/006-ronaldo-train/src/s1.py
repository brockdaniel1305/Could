import sys; sys.path.insert(0, __file__.rsplit('/episodes/', 1)[0] + '/tools')  # noqa: E702
from scene import *  # noqa: F403
from rail import station, ruler, ronaldo, train, hline, y_m, SIU_JS, GY, PLAT, M  # noqa: E402
sid = "s1-hook"
D = TIMING[sid]["duration"]
w = station(sid) + ruler(sid) + train(sid, 720) + ronaldo(sid)
cards = (banner(sid, "q", "CASE FILE 006", "Could Cristiano Ronaldo<br>jump high enough to<br>dodge a moving train?", 40, 300)
         + card(sid, "m", "METHOD", "Scientific", 120, 470)
         + card(sid, "p", "OUR POSITION", "The platform", 150, 640, "gold"))
js = SIU_JS + """
      tl.fromTo(S + "c-q", { opacity: 1, x: 0, y: 0, rotation: -2 }, { y: -1100, rotation: 8, duration: 0.4, ease: "power3.in" }, C.sci - 0.45);
      fly("m", C.sci, null);
      fly("p", C.long, null);
      tl.fromTo(S + "train", { x: 0 }, { x: -40, duration: D, ease: "sine.inOut" }, 0);
      tl.fromTo(S + "r-armR", { rotation: -150 }, { rotation: -120, duration: 0.3, ease: "sine.inOut", repeat: 5, yoyo: true }, 0);
      tl.to(S + "r-armR", { rotation: 0, duration: 0.3 }, 1.9);
      blink(S + "r-lids", 2.4);
      tl.to([S + "r-pupL", S + "r-pupR"], { x: 6, duration: 0.3 }, C.ev);
      tl.to([S + "tt-browL", S + "tt-browR"], { y: -8, duration: 0.25, ease: "back.out(3)" }, C.sci);
"""
scene(sid, w, js, cards, extra_css=".banner .bt { font-size: 74px; }")
