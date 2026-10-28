import sys; sys.path.insert(0, __file__.rsplit('/episodes/', 1)[0] + '/tools')  # noqa: E702
from scene import *  # noqa: F403
from rail import station, ruler, ronaldo, train, hline, y_m, SIU_JS, GY, PLAT, M  # noqa: E402
sid = "s7-verdict"
D = TIMING[sid]["duration"]
w = (station(sid) + train(sid, 200) + ronaldo(sid, 300, PLAT, 0.85)
     + f'<g transform="translate(560,{PLAT - 380}) scale(1.4)">{part("burst", sid + "-siu", WORD="SIUUU!")}</g>')
cards = (banner(sid, "b", "THE VERDICT", "Could he dodge it?", 60, 330)
         + card(sid, "gm", "IN GERMANY", "The train might not move", 40, 380, "gold")
         + card(sid, "p1", "CHANCE HE CLEARS THE ROOF", "0 %", 60, 380, "red")
         + card(sid, "p2", "CHANCE HE CELEBRATES ANYWAY", '<span id="s7-verdict-p3v">100 %</span>', 60, 560, "gold")
         + card(sid, "sf", "PLEASE", "Don't try this. Anywhere.", 60, 380, "red"))
cards += f'\n    <div class="stamp" id="{sid}-stamp">NO.</div>'
css = """
    .stamp { position: absolute; left: 150px; top: 520px; width: 780px; height: 420px; border: 26px solid #d6332a; border-radius: 34px;
             display: flex; align-items: center; justify-content: center; font: 900 270px/1 "Inter"; color: #d6332a; opacity: 0;
             background: rgba(244, 239, 230, 0.2); }"""
js = SIU_JS + """
      fly("b", 0.1, C.no - 0.15, { from: "top" });
      board([[0, "+120 min"]]);
      tl.fromTo(S + "stamp", { opacity: 0, scale: 2.4, rotation: -4 }, { opacity: 1, scale: 1, rotation: -9, duration: 0.18, ease: "power4.in" }, C.no);
      tl.fromTo(S + "svg", { x: 0 }, { x: 10, duration: 0.04, repeat: 5, yoyo: true }, C.no + 0.18);
      tl.to(S + "stamp", { opacity: 0, scale: 0.9, duration: 0.25, ease: "power2.in" }, C.but - 0.1);
      swap(S + "r-m-smile", S + "r-m-o", C.no + 0.2); swap(S + "r-m-o", S + "r-m-smile", C.but + 0.4);
      fly("gm", C.but, C.p1 - 0.1);
      tl.to([S + "tt-browL", S + "tt-browR"], { y: 8, duration: 0.3 }, C.but + 0.3);
      swap(S + "tt-smirk", S + "tt-o", C.but + 0.3);
      fly("p1", C.p1, C.safe - 0.1);
      fly("p2", C.p2, C.safe - 0.1, { from: "right" });
      tl.fromTo(S + "p3v", { opacity: 0 }, { opacity: 1, duration: 0.15 }, C.p3);
      siu(C.p3 - 0.3);
      tl.fromTo(S + "siu", { scale: 0, opacity: 0, transformOrigin: "50% 50%" }, { scale: 1, opacity: 1, duration: 0.25, ease: "back.out(3)" }, C.p3 + 0.1);
      tl.to(S + "siu", { opacity: 0, duration: 0.2 }, C.safe - 0.1);
      fly("sf", C.safe, null, { from: "top" });
"""
scene(sid, w, js, cards, extra_css=css)
