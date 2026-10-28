import sys; sys.path.insert(0, __file__.rsplit('/episodes/', 1)[0] + '/tools')  # noqa: E702
from scene import *  # noqa: F403
from rail import station, ruler, ronaldo, train, hline, y_m, SIU_JS, GY, PLAT, M  # noqa: E402
sid = "s5-hang"
D = TIMING[sid]["duration"]
w = (station(sid) + ruler(sid) + hline(sid, "seven", 7.0)
     + f'<g transform="translate(700,{GY})"><g id="{sid}-wall"><g transform="scale(0.8,1.2)">{part("great-wall", sid + "-w")}</g></g></g>'
     + train(sid, 1300)
     + f'<g transform="translate(250,{GY})"><g id="{sid}-ghost" opacity="0"><g transform="scale(0.9)">{part("forward", sid + "-g")}</g></g></g>'
     + ronaldo(sid))
cards = (banner(sid, "b", "PROBLEM 2", "Hang Time", 60, 330)
         + card(sid, "ps", "TRAIN PASSES IN", "2.4 s", 520, 380, "red")
         + card(sid, "ar", "HIS HANG TIME", "~0.75 s", 520, 560, "gold")
         + card(sid, "nd", "REQUIRED JUMP", "7 m", 560, 380, "red")
         + card(sid, "gw", "THAT IS", "The Great Wall of China", 40, 560, "gold"))
js = SIU_JS + """
      fly("b", C.t, C.pass - 0.1);
      // the train passes: 200 m at 300 km/h (slow motion)
      fly("ps", C.pass, C.air - 0.1, { from: "right" });
      tl.fromTo(S + "train", { x: 0 }, { x: -2900, duration: 4.0, ease: "none" }, C.pass + 0.4);
      fly("ar", C.air, C.need - 0.1, { from: "right" });
      jump(C.air + 0.6);
      // the jump he would need: 7 m
      tl.fromTo(S + "seven", { opacity: 0 }, { opacity: 1, duration: 0.3 }, C.need);
      fly("nd", C.need + 0.2, C.wall - 0.1, { from: "right" });
      tl.fromTo(S + "ghost", { opacity: 0, y: 0 }, { opacity: 0.55, y: -840, duration: 1.2, ease: "power2.out" }, C.need + 0.4);
      // ... the height of the Great Wall (episode 003)
      tl.fromTo(S + "wall", { y: 900, opacity: 0 }, { y: 0, opacity: 1, duration: 0.8, ease: "back.out(1.4)" }, C.wall);
      fly("gw", C.wall + 0.3, null);
      tl.to(S + "ghost", { opacity: 0, duration: 0.3 }, C.wall + 0.6);
      swap(S + "w-smirk", S + "w-grin", C.wall + 0.9);
"""
scene(sid, w, js, cards)
