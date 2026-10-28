import sys; sys.path.insert(0, __file__.rsplit("/episodes/", 1)[0] + "/tools")  # noqa: E702
from scene import *  # noqa: F403
from rail import *  # noqa: E402,F403
sid = "s7-verdict"
D = TIMING[sid]["duration"]
w = (station(sid) + ronaldo(sid, 300, PLAT, 0.85)
     + f'<g transform="translate(600,{PLAT - 380}) scale(1.4)">{part("burst", sid + "-siu", WORD="SIUUU!")}</g>')
cards = (banner(sid, "b", "THE VERDICT", "Could he dodge it?", 60, 330)
         + card(sid, "sm", "IF THE TRAIN IS", "Small enough", 60, 380, "gold")
         + card(sid, "lt", "OR", "Late enough", 520, 560, "red")
         + card(sid, "p1", "FINAL SCORE", "Ronaldo 2 · Trains 1", 60, 380, "gold")
         + card(sid, "sf", "PLEASE", "Don't try this. Any train.", 60, 380, "red")
         + scorebug(sid, 2, 1))
cards += f'\n    <div class="stamp" id="{sid}-stamp">YES.</div>'
css = SCORE_CSS + """
    .stamp { position: absolute; left: 150px; top: 520px; width: 780px; height: 420px; border: 26px solid #1f9d55; border-radius: 34px;
             display: flex; align-items: center; justify-content: center; font: 900 250px/1 "Inter"; color: #1f9d55; opacity: 0;
             background: rgba(244, 239, 230, 0.2); }"""
js = SIU_JS + SCORE_JS + """
      boardName("IC 2024");
      board([[0, "cancelled"]]);
      fly("b", 0.1, C.yes - 0.15, { from: "top" });
      tl.fromTo(S + "stamp", { opacity: 0, scale: 2.4, rotation: -4 }, { opacity: 1, scale: 1, rotation: -9, duration: 0.18, ease: "power4.in" }, C.yes);
      tl.fromTo(S + "svg", { x: 0 }, { x: 10, duration: 0.04, repeat: 5, yoyo: true }, C.yes + 0.18);
      tl.to(S + "stamp", { opacity: 0, scale: 0.9, duration: 0.25, ease: "power2.in" }, C.small - 0.1);
      swap(S + "r-m-smile", S + "r-m-o", C.yes + 0.2); swap(S + "r-m-o", S + "r-m-smile", C.small + 0.4);
      fly("sm", C.small, C.p1 - 0.1);
      fly("lt", C.late, C.p1 - 0.1, { from: "right" });
      fly("p1", C.p1, C.safe - 0.1);
      tl.fromTo(S + "score", { scale: 1, transformOrigin: "50% 50%" }, { scale: 1.15, duration: 0.2, yoyo: true, repeat: 1 }, C.p1 + 0.3);
      siu(C.siu - 0.3);
      tl.fromTo(S + "siu", { scale: 0, opacity: 0, transformOrigin: "50% 50%" }, { scale: 1, opacity: 1, duration: 0.25, ease: "back.out(3)" }, C.siu + 0.1);
      tl.to(S + "siu", { opacity: 0, duration: 0.2 }, C.safe - 0.1);
      fly("sf", C.safe, null, { from: "top" });
"""
scene(sid, w, js, cards, extra_css=css)
