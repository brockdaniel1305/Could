import sys; sys.path.insert(0, __file__.rsplit('/episodes/', 1)[0] + '/tools')  # noqa: E702
from scene import *  # noqa: F403
from shot import world, ball, dots, fly, player_js, J, sx, sy, v_for, X0, GY  # noqa: E402
import math  # noqa: E402
sid = "s3-wall"
D = TIMING[sid]["duration"]
w = (world(sid)
     + f'<mask id="{sid}-mask"><rect x="0" y="0" width="1080" height="1920" fill="#fff" /><ellipse cx="{sx(3.62)}" cy="880" rx="330" ry="440" fill="#000" /></mask>'
     + f'<rect id="{sid}-spot" x="0" y="0" width="1080" height="1920" fill="#000" opacity="0" mask="url(#{sid}-mask)" />'
     + f'<g id="{sid}-hl" opacity="0"><path d="M40,{sy(7)} L1080,{sy(7)}" stroke="#e0412f" stroke-width="6" stroke-dasharray="20 14" /></g>'
     + f'<g id="{sid}-thk" opacity="0" transform="translate({sx(1.37)},{sy(7) - 90})"><path d="M0,0 L450,0 M0,-18 L0,18 M450,-18 L450,18" stroke="#ffd23f" stroke-width="8" stroke-linecap="round" /></g>')
cards = (banner(sid, "b", "ON DEFENCE", "The Great Wall", 60, 330)
         + card(sid, "h", "HEIGHT", "up to 7 m", 560, 320, "red")
         + card(sid, "w", "THICKNESS", "4–5 m", 560, 320)
         + card(sid, "l", "LENGTH", "21,196 km", 60, 340, "gold")
         + card(sid, "d", "BASKETS CONCEDED", "0", 560, 340, "red"))
js = """
      tl.fromTo(S + "spot", { opacity: 0 }, { opacity: 0.6, duration: 0.4 }, C.name - 0.2);
      fly("b", C.name, C.h - 0.1);
      fly("h", C.h, C.w - 0.1, { from: "right" });
      tl.fromTo(S + "hl", { opacity: 0 }, { opacity: 1, duration: 0.3 }, C.h);
      tl.to(S + "hl", { opacity: 0, duration: 0.3 }, C.w);
      fly("w", C.w, C.len - 0.1, { from: "right" });
      tl.fromTo(S + "thk", { opacity: 0, scaleX: 0, transformOrigin: "0% 50%" }, { opacity: 1, scaleX: 1, duration: 0.5, ease: "expo.out" }, C.w + 0.2);
      tl.to(S + "thk", { opacity: 0, duration: 0.3 }, C.len);
      fly("l", C.len, C.def - 0.1);
      fly("d", C.def, null, { from: "right" });
      tl.to([S + "w-browL", S + "w-browR"], { y: -16, duration: 0.25, ease: "back.out(3)" }, C.def + 0.4);
      swap(S + "w-smirk", S + "w-grin", C.def + 0.5);
      tl.fromTo(S + "w", { rotation: 0, svgOrigin: "512 1250" }, { rotation: 0.6, duration: 0.15, yoyo: true, repeat: 3 }, C.def + 0.6);
      blink(S + "p-lids", 2.5);
"""
scene(sid, w, js, cards)
