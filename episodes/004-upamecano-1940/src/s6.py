import sys; sys.path.insert(0, __file__.rsplit('/episodes/', 1)[0] + '/tools')  # noqa: E702
from scene import *  # noqa: F403
from field import forest, board, defender, tank, GY  # noqa: E402
sid = "s6-offside"
D = TIMING[sid]["duration"]
mates = "".join(f'<g transform="translate({x},{GY + dy})"><g id="{sid}-m{i}"><g transform="scale({s})">{part("centre-back", sid + "-m" + str(i) + "p")}</g></g></g>'
                for i, (x, dy, s) in enumerate([(150, -70, 0.75), (230, 50, 0.9)]))
tanks = "".join(tank(sid, f"k{i}", 640 + i * 170, 0.7, GY - 50 + (i % 2) * 60) for i in range(3))
w = (forest(sid) + tanks + mates + defender(sid, 330)
     + f'<g id="{sid}-ol" opacity="0"><path d="M540,930 L540,{GY + 120}" stroke="#ffd23f" stroke-width="10" stroke-dasharray="26 16" /></g>'
     + f'<g id="{sid}-flag" transform="translate(990,{GY - 160})"><path d="M0,0 L0,-200" stroke="#1a1a2e" stroke-width="10" /><path d="M0,-200 L90,-170 L0,-140 Z" fill="#ffd23f" stroke="#1a1a2e" stroke-width="5" /></g>'
     + board(sid))
cards = (banner(sid, "b", "PHASE 3", "The Offside Trap", 60, 330)
         + card(sid, "off", "OFFSIDE", "~3,000,000 soldiers", 60, 540, "gold")
         + card(sid, "var", "VIDEO REVIEW", '<span id="s6-offside-var">checking…</span>', 380, 380, "red"))
js = """
      fly("b", C.t, C.off - 0.1);
      for (let i = 0; i < 3; i++) tl.fromTo(S + "k" + i + "t-body", { y: 0 }, { y: -3, duration: 0.12, repeat: R(D, 0.12), yoyo: true }, 0);
      // on his signal: arm up, the whole line steps up as one
      tl.to(S + "u-armR", { rotation: -165, duration: 0.25, ease: "back.out(2)" }, C.step);
      tl.to([S + "kwrap", S + "m0", S + "m1"], { x: 200, duration: 0.6, ease: "power3.out" }, C.step + 0.5);
      tl.to(S + "def", { x: 220, duration: 0.6, ease: "power3.out" }, C.step + 0.5);
      // flag up: all offside
      tl.fromTo(S + "flag", { rotation: -60, svgOrigin: "990 990" }, { rotation: 0, duration: 0.3, ease: "back.out(2)" }, C.off + 0.2);
      tl.fromTo(S + "ol", { opacity: 0 }, { opacity: 1, duration: 0.2 }, C.off + 0.2);
      fly("off", C.off + 0.3, null);
      for (let i = 0; i < 3; i++) swap(S + "k" + i + "t-smirk", S + "k" + i + "t-o", C.off + 0.4 + i * 0.1);
      // the video review: six weeks
      fly("var", C.var, null, { from: "right" });
      const vt = document.getElementById("s6-offside-var"), w = { v: 0 };
      tl.fromTo(w, { v: 0 }, { v: 6, duration: D - C.var - 0.6, ease: "power1.in", onUpdate() { vt.textContent = w.v < 0.2 ? "checking…" : "week " + Math.min(6, Math.ceil(w.v)) + " of 6"; } }, C.var + 0.4);
"""
scene(sid, w, js, cards)
