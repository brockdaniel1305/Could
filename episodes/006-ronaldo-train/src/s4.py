import sys; sys.path.insert(0, __file__.rsplit('/episodes/', 1)[0] + '/tools')  # noqa: E702
from scene import *  # noqa: F403
from rail import station, ruler, ronaldo, train, hline, y_m, SIU_JS, GY, PLAT, M  # noqa: E402
sid = "s4-height"
D = TIMING[sid]["duration"]
w = (station(sid) + ruler(sid) + hline(sid, "roof", 3.9) + hline(sid, "feet", 0.7, "#ffd23f")
     + f'<g id="{sid}-gap" opacity="0"><path d="M420,{y_m(0.7)} L420,{y_m(3.9)} M396,{y_m(0.7)} L444,{y_m(0.7)} M396,{y_m(3.9)} L444,{y_m(3.9)}" stroke="#e0412f" stroke-width="10" stroke-linecap="round" /></g>'
     + train(sid, 1300) + ronaldo(sid))
cards = (banner(sid, "b", "PROBLEM 1", "The Height", 60, 330)
         + card(sid, "nd", "FEET MUST CLEAR", "3.9 m", 520, 380, "red")
         + card(sid, "hs", "HIS JUMP (FEET)", "~0.7 m", 520, 560, "gold")
         + card(sid, "sh", "SHORT BY", "~3 m", 480, 380, "red")
         + card(sid, "lg", "TRAIN'S RESPECT FOR LEGENDS", "None", 60, 560))
js = SIU_JS + """
      fly("b", C.t, C.need + 1.0);
      tl.fromTo(S + "roof", { opacity: 0 }, { opacity: 1, duration: 0.3 }, C.need);
      fly("nd", C.need + 0.3, C.short - 0.1, { from: "right" });
      // his real jump: feet 0.7 m up
      jump(C.has + 0.4);
      tl.fromTo(S + "feet", { opacity: 0 }, { opacity: 1, duration: 0.2 }, C.has + 0.75);
      fly("hs", C.has + 0.5, C.slow - 0.1, { from: "right" });
      jump(C.has + 2.0);
      tl.fromTo(S + "gap", { opacity: 0, scaleY: 0, transformOrigin: "50% 100%" }, { opacity: 1, scaleY: 1, duration: 0.5, ease: "expo.out" }, C.short);
      fly("sh", C.short + 0.2, C.slow - 0.1, { from: "right" });
      swap(S + "r-m-smile", S + "r-m-o", C.short + 0.6);
      // ... and the train does not slow down: it arrives, we cut before it does
      tl.to([S + "roof", S + "feet", S + "gap"], { opacity: 0, duration: 0.2 }, C.slow);
      tl.fromTo(S + "train", { x: 0 }, { x: -1250, duration: D - C.slow - 0.15, ease: "power2.in" }, C.slow);
      tl.to([S + "tt-browL", S + "tt-browR"], { y: -10, duration: 0.2 }, C.slow + 0.2);
      tl.to([S + "r-pupL", S + "r-pupR"], { x: 7, duration: 0.2 }, C.slow + 0.3);
      fly("lg", C.slow + 0.3, null);
"""
scene(sid, w, js, cards)
