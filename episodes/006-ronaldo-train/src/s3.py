import sys; sys.path.insert(0, __file__.rsplit("/episodes/", 1)[0] + "/tools")  # noqa: E702
from scene import *  # noqa: F403
from rail import *  # noqa: E402,F403
sid = "s3-round1"
D = TIMING[sid]["duration"]
w = (station(sid) + ruler(sid) + hline(sid, "roof", 3.9) + hline(sid, "feet", 0.7, "#ffd23f")
     + f'<g id="{sid}-gap" opacity="0"><path d="M420,{y_m(0.7)} L420,{y_m(3.9)} M396,{y_m(0.7)} L444,{y_m(0.7)} M396,{y_m(3.9)} L444,{y_m(3.9)}" stroke="#e0412f" stroke-width="10" stroke-linecap="round" /></g>'
     + ronaldo(sid) + train(sid, 720))
cards = (banner(sid, "b", "ROUND 1 OF 3", "High-speed train", 60, 330)
         + card(sid, "h", "HEIGHT", "3.89 m", 60, 560, "red")
         + card(sid, "v", "SPEED", "300 km/h", 520, 560, "gold")
         + card(sid, "nd", "FEET MUST CLEAR", "3.9 m", 520, 380, "red")
         + card(sid, "hs", "HIS JUMP (FEET)", "~0.7 m", 520, 560, "gold")
         + card(sid, "sh", "SHORT BY", "~3 m", 520, 380, "red")
         + card(sid, "lg", "TRAIN'S RESPECT FOR LEGENDS", "None", 60, 380)
         + scorebug(sid, 0, 0))
js = SIU_JS + SCORE_JS + """
      boardName("ICE 7");
      board([[0, "on time"], [C.slow, "passing"]]);
      fly("b", C.name, C.need - 0.1);
      // the train rolls into view and creeps closer
      tl.fromTo(S + "train", { x: 560 }, { x: 0, duration: 1.4, ease: "power2.out" }, C.name);
      tl.to(S + "train", { x: -60, duration: C.slow - C.name - 1.4, ease: "none" }, C.name + 1.4);
      fly("h", C.h, C.need - 0.1);
      fly("v", C.v, C.need - 0.1, { from: "right" });
      tl.fromTo(S + "roof", { opacity: 0 }, { opacity: 1, duration: 0.3 }, C.need);
      fly("nd", C.need + 0.3, C.short - 0.1, { from: "right" });
      jump(C.has + 0.4);
      tl.fromTo(S + "feet", { opacity: 0 }, { opacity: 1, duration: 0.2 }, C.has + 0.75);
      fly("hs", C.has + 0.5, C.slow - 0.1, { from: "right" });
      jump(C.has + 2.0);
      tl.fromTo(S + "gap", { opacity: 0, scaleY: 0, transformOrigin: "50% 100%" }, { opacity: 1, scaleY: 1, duration: 0.5, ease: "expo.out" }, C.short);
      fly("sh", C.short + 0.2, C.slow - 0.1, { from: "right" });
      swap(S + "r-m-smile", S + "r-m-o", C.short + 0.6);
      tl.to([S + "r-pupL", S + "r-pupR"], { x: 7, duration: 0.2 }, C.short + 0.6);
      // it does not slow down: he scrambles back onto the platform, the train blasts through
      tl.to([S + "roof", S + "feet", S + "gap"], { opacity: 0, duration: 0.2 }, C.slow);
      tl.to(S + "kwrap", { x: -130, duration: 0.5, ease: "power1.inOut" }, C.slow + 0.1);
      tl.to(S + "kwrap", { y: -230, duration: 0.25, ease: "power2.out" }, C.slow + 0.1);
      tl.to(S + "kwrap", { y: -(GY - PLAT), duration: 0.25, ease: "power2.in" }, C.slow + 0.35);
      tl.to(S + "train", { x: -2800, duration: 1.7, ease: "power1.in" }, C.slow + 0.3);
      tl.to([S + "tt-browL", S + "tt-browR"], { y: -10, duration: 0.2 }, C.slow);
      fly("lg", C.slow + 0.3, C.score - 0.1);
      score(C.score, 0, 1, "sb");
""".replace("GY - PLAT", str(GY - PLAT))
scene(sid, w, js, cards, extra_css=SCORE_CSS)
