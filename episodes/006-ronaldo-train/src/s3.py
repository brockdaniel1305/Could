import sys; sys.path.insert(0, __file__.rsplit('/episodes/', 1)[0] + '/tools')  # noqa: E702
from scene import *  # noqa: F403
from rail import station, ruler, ronaldo, train, hline, y_m, SIU_JS, GY, PLAT, M  # noqa: E402
sid = "s3-train"
D = TIMING[sid]["duration"]
w = station(sid) + ruler(sid) + hline(sid, "roof", 3.89) + train(sid, 200) + ronaldo(sid, 90, PLAT, 0.6)
cards = (banner(sid, "b", "ON THE TRACKS", "A German high-speed train", 30, 300)
         + card(sid, "h", "HEIGHT", "3.89 m", 120, 470, "red")
         + card(sid, "l", "LENGTH", "~200 m", 520, 470)
         + card(sid, "v", "TOP SPEED IN SERVICE", "300 km/h", 120, 470, "gold")
         + card(sid, "t", "ARRIVAL TIME", "Theoretical", 520, 470, "red"))
js = SIU_JS + """
      fly("b", C.name, C.v - 0.1);
      tl.fromTo(S + "train", { x: 1100 }, { x: 0, duration: 1.6, ease: "power3.out" }, 0.2);
      tl.fromTo(S + "roof", { opacity: 0 }, { opacity: 1, duration: 0.3 }, C.h);
      fly("h", C.h, C.v - 0.1);
      fly("l", C.len, C.late - 0.1, { from: "right" });
      fly("v", C.v, null);
      tl.to(S + "roof", { opacity: 0, duration: 0.3 }, C.v);
      fly("t", C.late, null, { from: "right" });
      board([[0, "on time"], [C.late + 0.4, "+5 min"], [C.late + 1.2, "+? min"]]);
      tl.to([S + "tt-browL", S + "tt-browR"], { y: -8, duration: 0.25, ease: "back.out(3)" }, C.h + 0.3);
"""
scene(sid, w, js, cards, extra_css=".banner .bt { font-size: 70px; }")
