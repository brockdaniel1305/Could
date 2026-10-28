import sys; sys.path.insert(0, __file__.rsplit('/episodes/', 1)[0] + '/tools')  # noqa: E702
from scene import *  # noqa: F403
from field import forest, board, defender, tank, GY  # noqa: E402
sid = "s2-upa"
D = TIMING[sid]["duration"]
w = (forest(sid) + defender(sid, 300, 1.35) + tank(sid, "k1", 880) + board(sid)
     + f'<mask id="{sid}-mask"><rect x="0" y="0" width="1080" height="1920" fill="#fff" /><circle cx="300" cy="990" r="300" fill="#000" /></mask>'
     + f'<rect id="{sid}-spot" x="0" y="0" width="1080" height="1920" fill="#000" opacity="0" mask="url(#{sid}-mask)" />'
     + f'<g id="{sid}-star" transform="translate(300,720)"><path d="M0,-60 L17,-20 L60,-18 L26,10 L38,52 L0,28 L-38,52 L-26,10 L-60,-18 L-17,-20 Z" fill="#ffd23f" stroke="#1a1a2e" stroke-width="6" stroke-linejoin="round" /></g>'
     + f'<g transform="translate(-60,{GY - 16})"><g id="{sid}-ball"><g transform="scale(1.1)">{part("football", sid + "-fb")}</g></g></g>')
cards = (banner(sid, "b", "IN DEFENCE", "Dayot Upamecano", 60, 330)
         + card(sid, "best", "RANKING", "One of the best", 470, 520, "gold")
         + card(sid, "rl", "SARCASM LEVEL", "Genuinely zero", 470, 520)
         + card(sid, "h", "HEIGHT", "1.86 m", 560, 380)
         + card(sid, "em", "EASY MISTAKES", "0", 560, 380)
         + card(sid, "mo", "FOOTNOTE", "*mostly", 650, 560, "red"))
js = """
      tl.fromTo(S + "spot", { opacity: 0 }, { opacity: 0.6, duration: 0.4 }, C.name - 0.2);
      fly("b", C.name, C.h - 0.1);
      fly("best", C.best, C.really - 0.1, { from: "right" });
      pop(S + "star", C.best + 0.3);
      tl.to(S + "star", { opacity: 0, duration: 0.2 }, C.h);
      fly("rl", C.really, C.calm - 0.1, { from: "right" });
      fly("h", C.h, C.calm - 0.1, { from: "right" });
      fly("em", C.calm, null, { from: "right" });
      fly("mo", C.wink, null, { from: "top", rot: 8 });
      // proud pose: arms crossed, chin up
      tl.to(S + "u-armL", { rotation: -60, duration: 0.3, ease: "back.out(2)" }, C.best + 0.2);
      tl.to(S + "u-armR", { rotation: 60, duration: 0.3, ease: "back.out(2)" }, C.best + 0.28);
      tl.to(S + "u-head", { rotation: -6, duration: 0.3 }, C.best + 0.3);
      blink(S + "u-lids", 3.4); blink(S + "u-lids", 8.8);
      // ... while a loose ball rolls straight past him, unnoticed
      tl.fromTo(S + "ball", { x: 0, rotation: 0 }, { x: 1250, rotation: 900, duration: 2.4, ease: "none" }, C.wink - 0.6);
      swap(S + "k1t-smirk", S + "k1t-grin", C.wink + 0.6);
"""
scene(sid, w, js, cards)
