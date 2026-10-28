import sys; sys.path.insert(0, __file__.rsplit('/episodes/', 1)[0] + '/tools')  # noqa: E702
from scene import *  # noqa: F403
from field import forest, board, defender, tank, GY  # noqa: E402
sid = "s4-space"
D = TIMING[sid]["duration"]
tanks = "".join(tank(sid, f"k{i}", 820 + i * 190, 0.75, GY - 60 + i * 40) for i in range(3))
w = (forest(sid) + tanks + defender(sid, 260)
     + f'<g id="{sid}-line" opacity="0"><path d="M0,0 L0,-720" transform="translate(260,{GY + 60})" stroke="#4f7cff" stroke-width="10" stroke-dasharray="26 18" /></g>'
     + f'<g transform="translate(330,{GY - 400})"><g id="{sid}-heart"><path d="M0,30 C-60,-10 -40,-60 0,-30 C40,-60 60,-10 0,30 Z" fill="#e0412f" stroke="#1a1a2e" stroke-width="5" /></g></g>'
     + f'<g id="{sid}-speed" stroke="#f4efe6" stroke-width="7" stroke-linecap="round" opacity="0"><path d="M120,{GY - 200} L200,{GY - 200} M100,{GY - 140} L190,{GY - 140} M130,{GY - 80} L200,{GY - 80}" /></g>'
     + board(sid))
cards = (banner(sid, "b", "PHASE 1", "Space Defending", 60, 330)
         + card(sid, "sp", "THE ARDENNES", "A lot of space", 500, 540)
         + card(sid, "lv", "UPAMECANO", "♥ space", 560, 380, "gold")
         + card(sid, "hl", "DEFENSIVE LINE", "Very high", 60, 540)
         + card(sid, "no", "TANKS THROUGH THE HALF-SPACE", "0", 60, 380, "gold"))
js = """
      fly("b", C.t, C.space + 1.2);
      fly("sp", C.space, C.loves - 0.1, { from: "right" });
      fly("lv", C.loves, C.line - 0.1, { from: "right" });
      pop(S + "heart", C.loves + 0.3);
      tl.to(S + "heart", { y: -60, opacity: 0, duration: 1.0 }, C.loves + 1.2);
      swap(S + "u-m-smile", S + "u-m-o", C.space + 0.3); swap(S + "u-m-o", S + "u-m-smile", C.loves + 0.2);
      for (let i = 0; i < 3; i++) tl.fromTo(S + "k" + i + "t-body", { y: 0 }, { y: -3, duration: 0.12, repeat: R(D, 0.12), yoyo: true }, 0);
      // the high line: he steps up, the board's back four step up with him
      fly("hl", C.line, C.shift - 0.1);
      tl.fromTo(S + "line", { opacity: 0 }, { opacity: 1, duration: 0.3 }, C.line);
      tl.to([S + "kwrap", S + "line"], { x: 160, duration: 0.6, ease: "power2.inOut" }, C.line + 0.4);
      tl.to(S + "def", { x: 160, duration: 0.6, ease: "power2.inOut" }, C.line + 0.4);
      // shifts across the entire forest (and the board)
      const s0 = C.shift + 0.2, n = R(C.none - s0, 0.5);
      tl.fromTo(S + "kwrap", { x: 160 }, { x: 560, duration: 0.5, ease: "sine.inOut", repeat: n, yoyo: true }, s0);
      tl.fromTo(S + "def", { y: 0 }, { y: -70, duration: 0.5, ease: "sine.inOut", repeat: n, yoyo: true }, s0);
      tl.fromTo(S + "speed", { opacity: 0 }, { opacity: 0.85, duration: 0.2 }, s0);
      tl.to(S + "speed", { opacity: 0, duration: 0.2 }, C.none - 0.2);
      // not one tank gets through
      fly("no", C.none, null, { from: "top" });
      for (let i = 0; i < 3; i++) { swap(S + "k" + i + "t-smirk", S + "k" + i + "t-o", C.none + 0.3 + i * 0.1); tl.to(S + "k" + i, { x: 40, duration: 0.3, ease: "power2.out" }, C.none + 0.2); }
      tl.to([S + "a0", S + "a1", S + "a2"], { opacity: 0.25, duration: 0.3 }, C.none + 0.3);
"""
scene(sid, w, js, cards)
