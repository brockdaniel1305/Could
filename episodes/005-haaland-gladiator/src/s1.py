import sys; sys.path.insert(0, __file__.rsplit('/episodes/', 1)[0] + '/tools')  # noqa: E702
from scene import *  # noqa: F403
from arena import arena, haaland, fighter, MEDITATE_JS, GY  # noqa: E402
sid = "s1-hook"
D = TIMING[sid]["duration"]
w = (arena(sid) + fighter(sid, "retiarius", "ret", 900, 0.95) + fighter(sid, "murmillo", "mur", 690) + haaland(sid))
cards = (banner(sid, "q", "CASE FILE 005", "Could Erling Haaland<br>survive as a gladiator<br>in ancient Rome?", 40, 300)
         + card(sid, "m", "METHOD", "Scientific", 560, 400)
         + card(sid, "d", "OUR DISTANCE", "Very safe", 470, 580, "gold"))
js = MEDITATE_JS + """
      tl.fromTo(S + "c-q", { opacity: 1, x: 0, y: 0, rotation: -2 }, { y: -1100, rotation: 8, duration: 0.4, ease: "power3.in" }, C.sci - 0.45);
      fly("m", C.sci, null, { from: "right" });
      fly("d", C.long, null, { from: "right" });
      tl.fromTo(S + "col-crowd", { y: 0 }, { y: -6, duration: 0.3, ease: "sine.inOut", repeat: R(D, 0.3), yoyo: true }, 0);
      tl.fromTo(S + "h-armR", { rotation: -150 }, { rotation: -120, duration: 0.3, ease: "sine.inOut", repeat: 5, yoyo: true }, 0);
      tl.to(S + "h-armR", { rotation: 0, duration: 0.3 }, 1.9);
      blink(S + "h-lids", 2.2); blink(S + "h-lids", 5.6);
      tl.to([S + "h-pupL", S + "h-pupR"], { x: 6, duration: 0.3 }, C.ev);
      tl.fromTo(S + "murp-sword", { rotation: 0 }, { rotation: -25, svgOrigin: "0 86", duration: 0.3, yoyo: true, repeat: 3 }, C.sci);
      tl.fromTo(S + "retp-trident", { y: 0 }, { y: -10, duration: 0.3, yoyo: true, repeat: 3 }, C.sci + 0.2);
"""
scene(sid, w, js, cards, extra_css=".banner .bt { font-size: 74px; }")
