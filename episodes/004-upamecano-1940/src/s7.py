import sys; sys.path.insert(0, __file__.rsplit('/episodes/', 1)[0] + '/tools')  # noqa: E702
from scene import *  # noqa: F403
from field import forest, board, defender, tank, GY  # noqa: E402
sid = "s7-verdict"
D = TIMING[sid]["duration"]
T = TIMING[sid]["cues"]
tanks = "".join(tank(sid, f"k{i}", 820 + i * 150, 0.7, GY - 60 + (i % 2) * 70) for i in range(4))
w = (forest(sid) + tanks + defender(sid, 330)
     + f'<g transform="translate(380,{GY - 14})"><g id="{sid}-ball"><g transform="scale(1.1)">{part("football", sid + "-fb")}</g></g></g>'
     + f'<g transform="translate(860,{GY - 230})"><g id="{sid}-zz"><text font-family="Inter" font-weight="900" font-size="56" fill="#f4efe6" stroke="#1a1a2e" stroke-width="3" paint-order="stroke">z z Z</text></g></g>'
     + f'<g transform="translate(600,{GY - 300}) scale(1.3)">{part("burst", sid + "-oops", WORD="OOPS")}</g>'
     + board(sid))
cards = (banner(sid, "b", "THE VERDICT", "Could he have stopped it?", 40, 330)
         + card(sid, "rk", "ONE SMALL RISK", "1 simple pass", 60, 380, "red")
         + card(sid, "p1", "CHANCE HE STOPS THEM", "99 %", 60, 380, "gold")
         + card(sid, "p2", "CHANCE OF ONE EASY MISTAKE", '<span id="s7-verdict-p3v">also 99 %</span>', 60, 560, "red"))
cards += f'\n    <div class="stamp" id="{sid}-stamp">YES.</div>'
css = """
    .banner .bt { font-size: 74px; }
    .stamp { position: absolute; left: 150px; top: 540px; width: 780px; height: 420px; border: 26px solid #1f9d55; border-radius: 34px;
             display: flex; align-items: center; justify-content: center; font: 900 270px/1 "Inter"; color: #1f9d55; opacity: 0;
             background: rgba(244, 239, 230, 0.2); }"""
js = """
      fly("b", 0.1, C.yes - 0.15, { from: "top" });
      for (let i = 0; i < 4; i++) tl.fromTo(S + "k" + i + "t-body", { y: 0 }, { y: -3, duration: 0.12, repeat: R(D, 0.12), yoyo: true }, 0);
      // YES.
      tl.fromTo(S + "stamp", { opacity: 0, scale: 2.4, rotation: -4 }, { opacity: 1, scale: 1, rotation: -9, duration: 0.18, ease: "power4.in" }, C.yes);
      tl.fromTo(S + "svg", { x: 0 }, { x: 10, duration: 0.04, repeat: 5, yoyo: true }, C.yes + 0.18);
      tl.to(S + "stamp", { opacity: 0, scale: 0.9, duration: 0.25, ease: "power2.in" }, C.but - 0.1);
      tl.to(S + "u-armL", { rotation: -60, duration: 0.3 }, C.yes + 0.3);
      tl.to(S + "u-armR", { rotation: 60, duration: 0.3 }, C.yes + 0.35);
      // the small risk: nobody presses him at all
      fly("rk", C.but, C.p1 - 0.1);
      tl.fromTo(S + "zz", { opacity: 0, y: 0 }, { opacity: 1, y: -40, duration: 1.2, ease: "sine.out", repeat: 2 }, C.risk);
      tl.to([S + "u-armL", S + "u-armR"], { rotation: 0, duration: 0.3 }, C.risk);
      // one simple pass ... straight to a tank
      const pass = C.oops - 0.6;
      tl.to(S + "u-legR", { rotation: -40, duration: 0.15, yoyo: true, repeat: 1 }, pass);
      tl.fromTo(S + "ball", { x: 0, rotation: 0 }, { x: 420, rotation: 720, duration: 0.6, ease: "power1.out" }, pass + 0.1);
      tl.fromTo(S + "oops", { scale: 0, opacity: 0, transformOrigin: "50% 50%" }, { scale: 1, opacity: 1, duration: 0.25, ease: "back.out(3)" }, C.oops + 0.15);
      tl.to(S + "oops", { opacity: 0, duration: 0.2 }, C.oops + 1.2);
      tl.to(S + "zz", { opacity: 0, duration: 0.1 }, C.oops);
      swap(S + "u-m-smile", S + "u-m-o", C.oops + 0.1);
      tl.to(S + "u-armL", { rotation: 165, duration: 0.25 }, C.oops + 0.3);
      tl.to(S + "u-armR", { rotation: -165, duration: 0.25 }, C.oops + 0.35);
      // ... and the entire army walks past him
      for (let i = 0; i < 4; i++) {
        swap(S + "k" + i + "t-smirk", S + "k" + i + "t-grin", C.oops + 0.4);
        tl.to(S + "k" + i, { x: -1500, duration: 2.6, ease: "power1.in" }, C.oops + 0.6 + i * 0.25);
      }
      tl.to(S + "ball", { x: -1100, duration: 2.6, ease: "power1.in" }, C.oops + 0.6);
      tl.to([S + "u-pupL", S + "u-pupR"], { x: -7, duration: 0.6 }, C.oops + 1.2);
      fly("p1", C.p1, null);
      fly("p2", C.p2, null, { from: "right" });
      tl.fromTo(S + "p3v", { opacity: 0 }, { opacity: 1, duration: 0.15 }, C.p3);
"""
scene(sid, w, js, cards, extra_css=css)
