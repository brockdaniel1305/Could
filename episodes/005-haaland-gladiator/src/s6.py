import sys; sys.path.insert(0, __file__.rsplit('/episodes/', 1)[0] + '/tools')  # noqa: E702
from scene import *  # noqa: F403
from arena import arena, gauge, haaland, fighter, MEDITATE_JS, GY  # noqa: E402
sid = "s6-lion"
D = TIMING[sid]["duration"]
w = (arena(sid) + haaland(sid, 300)
     + f'<g transform="translate(0,{GY})"><g id="{sid}-lwrap"><g transform="translate(700,0) scale(1.0)">{part("lion", sid + "-l")}</g></g></g>' + gauge(sid))
cards = (banner(sid, "b", "ROUND 3", "The Lion", 60, 330)
         + card(sid, "lv", "LION SPRINT", "up to 80 km/h", 520, 380, "red")
         + card(sid, "hv", "HAALAND", "~36 km/h", 520, 560)
         + card(sid, "rn", "RUNNING AWAY", "Not an option", 60, 380)
         + card(sid, "md", "PLAN", "Meditation", 60, 380, "gold")
         + card(sid, "ls", "LION", "Also meditating", 480, 560, "gold"))
js = MEDITATE_JS + """
      fly("b", C.t, C.v - 0.1);
      // the lion comes out of the gate
      tl.fromTo(S + "lwrap", { x: 700 }, { x: 0, duration: 1.4, ease: "power2.out" }, C.t);
      tl.fromTo(S + "l-legF", { rotation: -25 }, { rotation: 25, duration: 0.14, repeat: 9, yoyo: true }, C.t);
      tl.fromTo(S + "l-legB", { rotation: 25 }, { rotation: -25, duration: 0.14, repeat: 9, yoyo: true }, C.t);
      tl.fromTo(S + "l-tail", { rotation: -8, svgOrigin: "130 -120" }, { rotation: 8, duration: 0.5, ease: "sine.inOut", repeat: R(D, 0.5), yoyo: true }, 0);
      fly("lv", C.v, C.run - 0.1, { from: "right" });
      fly("hv", C.h, C.run - 0.1, { from: "right" });
      tl.fromTo(S + "l-jaw", { y: 0 }, { y: 10, duration: 0.2, yoyo: true, repeat: 5 }, C.v + 0.4);
      needle(-80, C.v + 0.4);
      swap(S + "h-m-smile", S + "h-m-o", C.v + 0.5);
      fly("rn", C.run, C.zen - 0.1);
      // so he sits down and meditates
      fly("md", C.zen, null);
      swap(S + "h-m-o", S + "h-m-smile", C.zen + 0.1);
      meditate(C.zen + 0.2);
      tl.to(S + "lwrap", { x: -160, duration: 0.8, ease: "power2.out" }, C.zen + 0.6);
      tl.fromTo(S + "l-q", { opacity: 0, scale: 0.3, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2.5)" }, C.zen + 1.3);
      // the lion, confused, sits down next to him
      tl.to(S + "l-q", { opacity: 0, duration: 0.2 }, C.lion + 0.2);
      tl.set(S + "l-stand", { opacity: 0 }, C.lion + 0.4); tl.set(S + "l-sit", { opacity: 1 }, C.lion + 0.4);
      fly("ls", C.lion + 0.5, null, { from: "right" });
      needle(70, C.lion + 0.6);
"""
scene(sid, w, js, cards)
