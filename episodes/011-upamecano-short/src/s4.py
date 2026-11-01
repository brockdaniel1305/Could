import sys; sys.path.insert(0, __file__.rsplit("/episodes/", 1)[0] + "/tools")  # noqa: E702
from scene import *  # noqa: F403
from field import forest, board, defender, tank, GY  # noqa: E402
sid = "s4-defend"
D = TIMING[sid]["duration"]
T = TIMING[sid]["cues"]
hit = T["clean"] - 0.35
flag = f'<g transform="translate(980,{GY - 420})"><g id="{sid}-flag" opacity="0"><path d="M0,0 L0,260" stroke="#1a1a2e" stroke-width="10" /><path d="M0,0 L90,20 L0,70 Z" fill="#ffd23f" stroke="#1a1a2e" stroke-width="5" /></g></g>'
w = (forest(sid) + tank(sid, "k1", 820, 1.0) + defender(sid, 240)
     + f'<g transform="translate(620,{GY - 220}) scale(1.2)">{part("burst", sid + "-bang", WORD="CLEAN!")}</g>'
     + f'<g transform="translate(720,{GY - 20})"><g id="{sid}-ball"><g transform="scale(1.1)">{part("football", sid + "-fb")}</g></g></g>'
     + flag + board(sid))
cards = (card(sid, "hl", "HIGH LINE", "The whole forest", 40, 380, "gold")
         + card(sid, "tk", "ONE TANK", "~20 tonnes", 560, 380)
         + card(sid, "cl", "TACKLE", "All ball.", 40, 560, "gold")
         + card(sid, "of", "OFFSIDE", "3,000,000", 40, 380, "red"))
js = f"""
      tl.fromTo(S + "k1t-body", {{ y: 0 }}, {{ y: -3, duration: 0.12, repeat: R(D, 0.12), yoyo: true }}, 0);
      // the high line: he shifts across the whole width, the blue dots on the board follow
      fly("hl", 0.2, C.tank - 0.1);
      tl.to(S + "kwrap", {{ x: 520, duration: 0.7, ease: "sine.inOut" }}, C.line - 0.6);
      tl.to(S + "kwrap", {{ x: 0, duration: 0.7, ease: "sine.inOut" }}, C.line + 0.2);
      tl.to(S + "def", {{ x: 160, duration: 0.6, ease: "sine.inOut", yoyo: true, repeat: 1 }}, C.line - 0.6);
      // a twenty-tonne tank? sliding tackle. all ball.
      fly("tk", C.tank, C.off - 0.1, {{ from: "right" }});
      tl.to(S + "kwrap", {{ x: 120, duration: 0.6, ease: "power2.in" }}, C.slide);
      tl.to(S + "kwrap", {{ x: 360, rotation: -72, transformOrigin: "50% 100%", y: -20, duration: 0.45, ease: "power2.out" }}, {hit - 0.45:.3f});
      tl.to(S + "u-legR", {{ rotation: -60, duration: 0.3 }}, {hit - 0.45:.3f});
      tl.fromTo(S + "bang", {{ scale: 0, opacity: 0, transformOrigin: "50% 50%" }}, {{ scale: 1, opacity: 1, duration: 0.25, ease: "back.out(3)" }}, {hit:.3f});
      tl.to(S + "bang", {{ opacity: 0, duration: 0.2 }}, {hit + 0.9:.3f});
      tl.fromTo(S + "ball", {{ x: 0, y: 0 }}, {{ x: -520, y: -60, rotation: -720, duration: 0.9, ease: "power2.out" }}, {hit:.3f});
      tl.to(S + "k1", {{ rotation: 18, transformOrigin: "50% 100%", duration: 0.25, ease: "power2.out", yoyo: true, repeat: 1 }}, {hit:.3f});
      swap(S + "k1t-smirk", S + "k1t-o", {hit + 0.1:.3f});
      fly("cl", C.clean, C.off - 0.1);
      tl.to(S + "kwrap", {{ rotation: 0, y: 0, x: 0, duration: 0.4, ease: "back.out(2)" }}, {hit + 1.1:.3f});
      tl.to(S + "u-legR", {{ rotation: 0, duration: 0.3 }}, {hit + 1.1:.3f});
      // three million soldiers: offside
      tl.fromTo(S + "flag", {{ opacity: 0, y: 120 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)" }}, C.off);
      tl.fromTo(S + "flag", {{ rotation: -8 }}, {{ rotation: 8, transformOrigin: "0% 100%", duration: 0.15, yoyo: true, repeat: 5 }}, C.off + 0.3);
      fly("of", C.off + 0.1, null);
      tl.to(S + "u-armL", {{ rotation: 160, duration: 0.25 }}, C.off + 0.2);
"""
scene(sid, w, js, cards)
