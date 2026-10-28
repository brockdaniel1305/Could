import sys; sys.path.insert(0, __file__.rsplit('/episodes/', 1)[0] + '/tools')  # noqa: E702
from scene import *  # noqa: F403
from race import course, PX, NOSE  # noqa: E402
sid = "s7-verdict"
world = f"""
{part("track-day", sid + "-track")}
{course(sid, start_blocks=False)}
"""
cards = (banner(sid, "b", "THE VERDICT", "Could he beat it?", 60, 330)
         + card(sid, "mg", "MARGIN", "≈ 6.7 s", 60, 380, "gold")
         + card(sid, "pb", "HOWEVER", "One problem", 60, 380, "red")
         + card(sid, "st", "T-REX STOPS AT THE FINISH", "No", 60, 380, "red"))
cards += f'\n    <div class="stamp" id="{sid}-stamp">YES.</div>'
css = """
    .stamp { position: absolute; left: 150px; top: 520px; width: 780px; height: 420px; border: 26px solid #1f9d55; border-radius: 34px;
             display: flex; align-items: center; justify-content: center; font: 900 270px/1 "Inter"; color: #1f9d55; opacity: 0;
             background: rgba(244, 239, 230, 0.2); }"""
js = f"""
      const PX = {PX}, NOSE = {NOSE};
      gsap.set(S + "course", {{ x: 540 - 106 * PX }});
      gsap.set(S + "tape", {{ opacity: 0 }});
      tl.fromTo(S + "bolt", {{ x: 110.4 * PX }}, {{ x: 110.4 * PX, duration: 0.01 }}, 0);
      // the T-Rex arrives ... and does not stop at the line
      tl.fromTo(S + "rex", {{ x: 84 * PX - NOSE }}, {{ x: 100 * PX - NOSE, duration: C.line - 0.5, ease: "none" }}, 0.5);
      tl.to(S + "rex", {{ x: 128 * PX - NOSE, duration: D - C.line, ease: "power1.in" }}, C.line);
      const rl = R(D, 0.36);
      tl.fromTo(S + "r-legL", {{ rotation: -24 }}, {{ rotation: 24, duration: 0.36, ease: "sine.inOut", repeat: rl, yoyo: true }}, 0);
      tl.fromTo(S + "r-legR", {{ rotation: 24 }}, {{ rotation: -24, duration: 0.36, ease: "sine.inOut", repeat: rl, yoyo: true }}, 0);
      tl.to(S + "r-brow", {{ rotation: 14, svgOrigin: "74 -43", duration: 0.2 }}, C.line);
      tl.fromTo(S + "r-jaw", {{ rotation: 0, svgOrigin: "0 18" }}, {{ rotation: 28, duration: 0.25, ease: "power2.out", repeat: 5, yoyo: true }}, C.rex);
      // Bolt celebrates, hears something, leaves
      tl.fromTo(S + "b-armR", {{ rotation: -160 }}, {{ rotation: -140, duration: 0.3, ease: "sine.inOut", repeat: 9, yoyo: true }}, 0);
      tl.fromTo(S + "b-armL", {{ rotation: 160 }}, {{ rotation: 140, duration: 0.3, ease: "sine.inOut", repeat: 9, yoyo: true }}, 0);
      tl.to([S + "b-armL", S + "b-armR"], {{ rotation: 0, duration: 0.2 }}, C.line + 0.6);
      tl.to([S + "b-pupL", S + "b-pupR"], {{ x: -7, duration: 0.2 }}, C.line + 0.6);
      swap(S + "b-m-smile", S + "b-m-o", C.line + 0.7);
      tl.to(S + "bolt", {{ x: 124 * PX, duration: D - C.rex - 0.2, ease: "power2.in" }}, C.rex + 0.2);
      const bl = R(D - C.rex, 0.14);
      ["legL", "armR"].forEach((p) => tl.fromTo(S + "b-" + p, {{ rotation: -38 }}, {{ rotation: 38, duration: 0.14, repeat: bl, yoyo: true }}, C.rex + 0.2));
      ["legR", "armL"].forEach((p) => tl.fromTo(S + "b-" + p, {{ rotation: 38 }}, {{ rotation: -38, duration: 0.14, repeat: bl, yoyo: true }}, C.rex + 0.2));
      // YES.
      fly("b", 0.1, C.yes - 0.15, {{ from: "top" }});
      const land = C.yes + 0.18;
      tl.fromTo(S + "stamp", {{ opacity: 0, scale: 2.4, rotation: -4 }}, {{ opacity: 1, scale: 1, rotation: -9, duration: 0.18, ease: "power4.in" }}, C.yes);
      tl.fromTo(S + "svg", {{ x: 0 }}, {{ x: 10, duration: 0.04, repeat: 5, yoyo: true }}, land);
      tl.to(S + "stamp", {{ opacity: 0, scale: 0.9, duration: 0.25, ease: "power2.in" }}, C.by - 0.1);
      fly("mg", C.by, C.but - 0.1);
      fly("pb", C.but, C.rex - 0.1, {{ from: "right" }});
      fly("st", C.rex, null, {{ from: "top" }});
"""
scene(sid, world, js, cards, extra_css=css)
