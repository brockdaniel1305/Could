import sys; sys.path.insert(0, __file__.rsplit('/episodes/', 1)[0] + '/tools')  # noqa: E702
from scene import *  # noqa: F403
from field import forest, board, defender, tank, GY  # noqa: E402
sid = "s3-army"
D = TIMING[sid]["duration"]
tanks = "".join(tank(sid, f"k{i}", 1300 + i * 330, 0.85, GY - (i % 2) * 40) for i in range(5))
w = (forest(sid, ard=False)
     + f'<g id="{sid}-forest" opacity="0">' + "".join(f'<g transform="translate({x},{y}) scale({s})">{part("tree", f"{sid}-ft{i}")}</g>' for i, (x, y, s) in enumerate([(80, 1000, 1.0), (300, 1020, 1.1), (560, 1000, 1.0), (820, 1020, 1.15), (1010, 1000, 1.0)])) + '</g>'
     + f'<g transform="translate(260,{GY})"><g id="{sid}-mag">{part("maginot", sid + "-mg")}</g></g>'
     + tanks + board(sid)
     + f'<g id="{sid}-mline" opacity="0"><rect x="300" y="1440" width="34" height="360" rx="8" fill="#9aa0a6" stroke="#e8efe6" stroke-width="4" /></g>'
     + f'<path id="{sid}-route" d="M940,1600 Q860,1420 600,1440 Q380,1440 300,1400 Q200,1390 140,1460" fill="none" stroke="#c9ccc2" stroke-width="10" stroke-linecap="round" stroke-dasharray="1200" stroke-dashoffset="1200" />')
cards = (banner(sid, "b", "IN ATTACK", "The German Army, 1940", 40, 330)
         + card(sid, "m", "SOLDIERS", "~3 million", 560, 540)
         + card(sid, "t", "TANKS", "~2,500", 560, 540, "gold")
         + card(sid, "mg", "MAGINOT LINE", "~320 km of bunkers", 60, 380)
         + card(sid, "ar", "ROUTE", "Around it", 560, 380, "red")
         + card(sid, "ad", "VIA", "The Ardennes", 60, 560, "gold"))
js = """
      tl.set(S + "a0", { opacity: 0 }, 0); tl.set([S + "a1", S + "a2"], { opacity: 0 }, 0);
      fly("b", C.name, C.mag - 0.1);
      fly("m", C.men, C.tanks - 0.1, { from: "right" });
      fly("t", C.tanks, C.mag - 0.1, { from: "right" });
      // the column rolls in from the east
      for (let i = 0; i < 5; i++) {
        tl.fromTo(S + "k" + i, { x: 0 }, { x: -840, duration: 4.2, ease: "power1.out" }, C.name + i * 0.35);
        tl.fromTo(S + "k" + i + "t-body", { y: 0 }, { y: -3, duration: 0.12, repeat: R(D, 0.12), yoyo: true }, 0);
      }
      // the Maginot Line rises ... the arrow goes around it
      tl.fromTo(S + "mag", { y: 260, opacity: 0 }, { y: 0, opacity: 1, duration: 0.6, ease: "back.out(1.6)" }, C.mag);
      tl.fromTo(S + "mline", { opacity: 0 }, { opacity: 1, duration: 0.3 }, C.mag + 0.2);
      fly("mg", C.mag + 0.2, C.ard - 0.1);
      tl.fromTo(S + "route", { strokeDashoffset: 1200 }, { strokeDashoffset: 0, duration: 1.6, ease: "power2.inOut" }, C.around);
      fly("ar", C.around + 0.3, null, { from: "right" });
      for (let i = 0; i < 5; i++) tl.to(S + "k" + i, { x: -840 - 1400, duration: 2.2, ease: "power2.in" }, C.around + 0.6 + i * 0.15);
      // ... through the Ardennes
      tl.fromTo(S + "forest", { opacity: 0, y: 80 }, { opacity: 1, y: 0, duration: 0.5, ease: "back.out(1.6)" }, C.ard);
      fly("ad", C.ard + 0.2, null);
      tl.to(S + "mag", { y: 260, duration: 0.5, ease: "power2.in" }, C.ard);
"""
scene(sid, w, js, cards, extra_css=".banner .bt { font-size: 74px; }")
