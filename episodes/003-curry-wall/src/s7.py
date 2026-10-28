import sys; sys.path.insert(0, __file__.rsplit('/episodes/', 1)[0] + '/tools')  # noqa: E702
from scene import *  # noqa: F403
from shot import world, ball, dots, fly, player_js, J, sx, sy, v_for, X0, GY  # noqa: E402
import math  # noqa: E402
sid = "s7-verdict"
D = TIMING[sid]["duration"]
T = TIMING[sid]["cues"]
moon = fly(76.7, until=3.2)
sw = moon["events"]["swish"]
SLOW = 1.3
launch = T["yes"] + 0.18 - sw * SLOW          # swish lands with the stamp on "Technically"
w = world(sid) + ball(sid) + f'<g transform="translate({sx(7.24)},{sy(3.6)}) scale(1.1)">{part("burst", sid + "-swish", WORD="SWISH")}</g>'
cards = (banner(sid, "b", "THE VERDICT", "Could he make it?", 60, 330)
         + card(sid, "p", "CHANCE PER SHOT (EST.)", "2 %", 60, 400)
         + card(sid, "tr", "CHANCE HE TURNS AROUND", '<span id="s7-verdict-p3v">100 %</span>', 60, 580, "gold"))
cards += f'\n    <div class="stamp" id="{sid}-stamp">TECHNICALLY.</div>'
css = """
    .stamp { position: absolute; left: 80px; top: 600px; width: 920px; height: 300px; border: 22px solid #d9a441; border-radius: 30px;
             display: flex; align-items: center; justify-content: center; font: 900 118px/1 "Inter"; color: #d9a441; opacity: 0;
             background: rgba(26, 26, 46, 0.35); }"""
js = player_js() + f"""
      const MOON = {J(moon["pts"])};
      fly("b", 0.1, C.yes - 0.15, {{ from: "top" }});
      tl.set(S + "ball", {{ x: {sx(0.15)}, y: {sy(2.4)} }}, 0);
      tl.fromTo(S + "p-armL", {{ rotation: 0 }}, {{ rotation: 170, duration: 0.3 }}, {max(0.05, launch - 0.6):.3f});
      tl.fromTo(S + "p-armR", {{ rotation: 0 }}, {{ rotation: -170, duration: 0.3 }}, {max(0.05, launch - 0.6):.3f});
      tl.to(S + "kwrap", {{ y: -40, duration: 0.25, ease: "power2.out", yoyo: true, repeat: 1 }}, {launch - 0.05:.3f});
      play("ball", MOON, {launch:.3f}, {SLOW}, 3.2);
      // he turns around long before it lands
      tl.to(S + "kwrap", {{ scaleX: -1, transformOrigin: "50% 100%", duration: 0.2, ease: "power2.inOut" }}, {launch + 0.8:.3f});
      tl.to(S + "p-num", {{ scaleX: -1, transformOrigin: "50% 50%", duration: 0.2 }}, {launch + 0.8:.3f});
      tl.to([S + "p-armL", S + "p-armR"], {{ rotation: 0, duration: 0.3 }}, {launch + 0.8:.3f});
      tl.to(S + "p-lids", {{ opacity: 1, duration: 0.01 }}, {launch + 1.0:.3f});
      // SWISH + TECHNICALLY.
      const sw = {launch + sw * SLOW:.3f};
      tl.fromTo(S + "h-net", {{ scaleY: 1, transformOrigin: "50% 0%" }}, {{ scaleY: 1.5, duration: 0.12, yoyo: true, repeat: 1 }}, sw);
      tl.fromTo(S + "swish", {{ scale: 0, opacity: 0, transformOrigin: "50% 50%" }}, {{ scale: 1, opacity: 1, duration: 0.25, ease: "back.out(3)" }}, sw);
      tl.to(S + "swish", {{ opacity: 0, duration: 0.2 }}, sw + 1.0);
      tl.fromTo(S + "stamp", {{ opacity: 0, scale: 2.4, rotation: -4 }}, {{ opacity: 1, scale: 1, rotation: -7, duration: 0.18, ease: "power4.in" }}, C.yes);
      tl.fromTo(S + "svg", {{ x: 0 }}, {{ x: 10, duration: 0.04, repeat: 5, yoyo: true }}, C.yes + 0.18);
      tl.to(S + "stamp", {{ opacity: 0, scale: 0.9, duration: 0.25, ease: "power2.in" }}, C.prob - 0.1);
      swap(S + "w-smirk", S + "w-grin", 0);
      swap(S + "w-grin", S + "w-smirk", sw + 0.2);
      tl.to([S + "w-browL", S + "w-browR"], {{ y: 14, duration: 0.3 }}, sw + 0.2);
      fly("p", C.prob, null);
      fly("tr", C.turn, null, {{ from: "right" }});
      tl.fromTo(S + "p3v", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.15 }}, C.p3);
"""
scene(sid, w, js, cards, extra_css=css)
