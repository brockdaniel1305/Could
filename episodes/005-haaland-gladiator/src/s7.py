import sys; sys.path.insert(0, __file__.rsplit('/episodes/', 1)[0] + '/tools')  # noqa: E702
from scene import *  # noqa: F403
from arena import arena, haaland, fighter, MEDITATE_JS, GY  # noqa: E402
sid = "s7-verdict"
D = TIMING[sid]["duration"]
w = (arena(sid) + haaland(sid, 420) + f'<g transform="translate(0,{GY})"><g id="{sid}-lwrap"><g transform="translate(760,0) scale(0.9)">{part("lion", sid + "-l")}</g></g></g>')
cards = (banner(sid, "b", "THE VERDICT", "Could he survive?", 60, 330)
         + card(sid, "hs", "1ST-CENTURY FIGHTS WITHOUT A DEATH", "~9 in 10", 40, 380, "gold")
         + card(sid, "cw", "CROWD", "50,000 × HAALAND", 300, 560)
         + card(sid, "p1", "CHANCE OF SURVIVAL", "High", 60, 380)
         + card(sid, "p2", "CHANCE HE MEDITATES IN THE COLOSSEUM", '<span id="s7-verdict-p3v">100 %</span>', 40, 560, "gold"))
cards += f'\n    <div class="stamp" id="{sid}-stamp">YES.</div>'
css = """
    .stamp { position: absolute; left: 150px; top: 520px; width: 780px; height: 420px; border: 26px solid #1f9d55; border-radius: 34px;
             display: flex; align-items: center; justify-content: center; font: 900 270px/1 "Inter"; color: #1f9d55; opacity: 0;
             background: rgba(244, 239, 230, 0.2); }"""
js = MEDITATE_JS + """
      fly("b", 0.1, C.yes - 0.15, { from: "top" });
      tl.set(S + "l-stand", { opacity: 0 }, 0); tl.set(S + "l-sit", { opacity: 1 }, 0);
      tl.fromTo(S + "stamp", { opacity: 0, scale: 2.4, rotation: -4 }, { opacity: 1, scale: 1, rotation: -9, duration: 0.18, ease: "power4.in" }, C.yes);
      tl.fromTo(S + "svg", { x: 0 }, { x: 10, duration: 0.04, repeat: 5, yoyo: true }, C.yes + 0.18);
      tl.to(S + "stamp", { opacity: 0, scale: 0.9, duration: 0.25, ease: "power2.in" }, C.hist - 0.1);
      fly("hs", C.hist, C.p1 - 0.1);
      fly("cw", C.crowd, C.p1 - 0.1, { from: "right" });
      tl.fromTo(S + "col-crowd", { y: 0 }, { y: -14, duration: 0.22, ease: "sine.inOut", repeat: R(D - C.crowd, 0.22), yoyo: true }, C.crowd);
      cheer(C.crowd + 0.2);
      tl.to(S + "h-armL", { rotation: 160, duration: 0.3, ease: "back.out(2)" }, C.crowd + 0.3);
      tl.to(S + "h-armR", { rotation: -160, duration: 0.3, ease: "back.out(2)" }, C.crowd + 0.35);
      tl.to([S + "h-armL", S + "h-armR"], { rotation: 0, duration: 0.3 }, C.p2 - 0.3);
      fly("p1", C.p1, null);
      fly("p2", C.p2, null, { from: "right" });
      meditate(C.p2 + 0.1);
      tl.fromTo(S + "p3v", { opacity: 0 }, { opacity: 1, duration: 0.15 }, C.p3);
"""
scene(sid, w, js, cards, extra_css=css)
