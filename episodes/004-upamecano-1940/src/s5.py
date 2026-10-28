import sys; sys.path.insert(0, __file__.rsplit('/episodes/', 1)[0] + '/tools')  # noqa: E702
from scene import *  # noqa: F403
from field import forest, board, defender, tank, GY  # noqa: E402
sid = "s5-tackle"
D = TIMING[sid]["duration"]
T = TIMING[sid]["cues"]
w = (forest(sid) + tank(sid, "k1", 800, 1.1) + defender(sid, 240)
     + f'<g transform="translate(600,{GY - 220}) scale(1.2)">{part("burst", sid + "-bang", WORD="CLEAN!")}</g>'
     + f'<g transform="translate(700,{GY - 20})"><g id="{sid}-ball"><g transform="scale(1.1)">{part("football", sid + "-fb")}</g></g></g>'
     + f'<g transform="translate(860,{GY - 520})"><g id="{sid}-yc"><rect x="-55" y="-80" width="110" height="160" rx="12" fill="#ffd23f" stroke="#1a1a2e" stroke-width="7" /></g></g>'
     + board(sid))
cards = (banner(sid, "b", "PHASE 2", "The Tackle", 60, 330)
         + card(sid, "tk", "ONE TANK", "~20 tonnes", 500, 540)
         + card(sid, "up", "UPAMECANO", "~90 kg", 60, 540, "gold")
         + card(sid, "cl", "TACKLE", "Clean. All ball.", 60, 380, "gold")
         + card(sid, "bk", "BOOKED", "The tank (simulation)", 60, 560, "red"))
hit = T["clean"] - 0.35
js = f"""
      fly("b", C.t, C.tank + 1.0);
      fly("tk", C.tank, C.slide - 0.1, {{ from: "right" }});
      fly("up", C.upa, C.slide - 0.1);
      tl.fromTo(S + "k1t-body", {{ y: 0 }}, {{ y: -3, duration: 0.12, repeat: R(D, 0.12), yoyo: true }}, 0);
      tl.fromTo(S + "k1", {{ x: 160 }}, {{ x: 0, duration: 2.5, ease: "power1.out" }}, 0);
      // the run-up and the slide
      swap(S + "u-m-smile", S + "u-m-flat", C.slide);
      tl.to(S + "kwrap", {{ x: 120, duration: 0.8, ease: "power2.in" }}, C.slide + 0.4);
      tl.to(S + "kwrap", {{ x: 360, rotation: -72, transformOrigin: "50% 100%", y: -20, duration: 0.5, ease: "power2.out" }}, {hit - 0.5:.3f});
      tl.to(S + "u-legR", {{ rotation: -60, duration: 0.3 }}, {hit - 0.5:.3f});
      tl.fromTo(S + "bang", {{ scale: 0, opacity: 0, transformOrigin: "50% 50%" }}, {{ scale: 1, opacity: 1, duration: 0.25, ease: "back.out(3)" }}, {hit:.3f});
      tl.to(S + "bang", {{ opacity: 0, duration: 0.2 }}, {hit + 1.0:.3f});
      // all ball: the ball pops out, the tank spins round
      tl.fromTo(S + "ball", {{ x: 0, y: 0 }}, {{ x: -520, y: -60, rotation: -720, duration: 0.9, ease: "power2.out" }}, {hit:.3f});
      tl.to(S + "k1", {{ rotation: 18, transformOrigin: "50% 100%", duration: 0.25, ease: "power2.out", yoyo: true, repeat: 1 }}, {hit:.3f});
      swap(S + "k1t-smirk", S + "k1t-o", {hit + 0.1:.3f});
      fly("cl", C.clean, C.card - 0.1);
      tl.to(S + "kwrap", {{ rotation: 0, y: 0, duration: 0.4, ease: "back.out(2)" }}, {hit + 1.4:.3f});
      tl.to(S + "u-legR", {{ rotation: 0, duration: 0.3 }}, {hit + 1.4:.3f});
      swap(S + "u-m-flat", S + "u-m-smile", {hit + 1.5:.3f});
      // the tank goes down holding its ... turret. Yellow card.
      tl.to(S + "k1t-turret", {{ rotation: -10, svgOrigin: "0 -120", duration: 0.3, yoyo: true, repeat: 3 }}, C.card - 0.6);
      tl.fromTo(S + "yc", {{ opacity: 0, y: 80, rotation: 0 }}, {{ opacity: 1, y: 0, rotation: 8, duration: 0.35, ease: "back.out(2)" }}, C.card + 0.25);
      fly("bk", C.card + 0.3, null, {{ from: "right" }});
"""
scene(sid, w, js, cards)
