import sys; sys.path.insert(0, __file__.rsplit('/episodes/', 1)[0] + '/tools')  # noqa: E702
from scene import *  # noqa: F403
from shot import world, ball, dots, fly, player_js, J, sx, sy, v_for, X0, GY  # noqa: E402
import math  # noqa: E402
sid = "s2-curry"
D = TIMING[sid]["duration"]
T = TIMING[sid]["cues"]
up = fly(52, until=0.6)
w = (world(sid) + ball(sid)
     + f'<mask id="{sid}-mask"><rect x="0" y="0" width="1080" height="1920" fill="#fff" /><circle cx="{X0}" cy="1080" r="290" fill="#000" /></mask>'
     + f'<rect id="{sid}-spot" x="0" y="0" width="1080" height="1920" fill="#000" opacity="0" mask="url(#{sid}-mask)" />'
     + f'''<g id="{sid}-prot" transform="translate({sx(0.15)},{sy(2.4)})"><path d="M0,0 L200,0" stroke="#f4efe6" stroke-width="6" />
  <path d="M0,0 L{200 * math.cos(math.radians(52)):.0f},{-200 * math.sin(math.radians(52)):.0f}" stroke="#ffd23f" stroke-width="7" />
  <path d="M120,0 A120,120 0 0 0 {120 * math.cos(math.radians(52)):.0f},{-120 * math.sin(math.radians(52)):.0f}" fill="none" stroke="#ffd23f" stroke-width="6" />
  <rect x="130" y="-112" width="110" height="54" rx="10" fill="#ffd23f" stroke="#1a1a2e" stroke-width="4" /><text x="185" y="-74" text-anchor="middle" font-family="Inter" font-weight="900" font-size="34" fill="#1a1a2e">52°</text></g>''')
cards = (banner(sid, "b", "ON OFFENCE", "Stephen Curry", 60, 330)
         + card(sid, "h", "HEIGHT", "1.88 m", 560, 520)
         + card(sid, "tp", "THREE-POINTERS MADE", '<span id="s2-curry-cnt">0</span>', 360, 380, "gold")
         + card(sid, "ar", "RELEASE ANGLE", "~52°", 560, 380))
js = player_js() + f"""
      const UP = {J(up["pts"])};
      tl.fromTo(S + "spot", {{ opacity: 0 }}, {{ opacity: 0.6, duration: 0.4 }}, C.name - 0.2);
      fly("b", C.name, C.rec - 0.1);
      fly("h", C.h, C.rec - 0.1, {{ from: "right" }});
      fly("tp", C.rec, C.arc - 0.1, {{ from: "right" }});
      // the counter runs to 4,000
      const cnt = document.getElementById("s2-curry-cnt"), k = {{ v: 0 }};
      tl.fromTo(k, {{ v: 0 }}, {{ v: 4000, duration: 1.6, ease: "power2.out", onUpdate() {{ cnt.textContent = Math.round(k.v).toLocaleString("en-US") + (k.v > 3999 ? "+" : ""); }} }}, C.rec + 0.5);
      // ball in hands, arms up: the release angle
      tl.set(S + "ball", {{ x: {sx(0.15)}, y: {sy(2.4)} }}, 0);
      tl.fromTo(S + "p-armL", {{ rotation: 0 }}, {{ rotation: 170, duration: 0.35, ease: "power2.out" }}, C.arc - 0.4);
      tl.fromTo(S + "p-armR", {{ rotation: 0 }}, {{ rotation: -170, duration: 0.35, ease: "power2.out" }}, C.arc - 0.4);
      fly("ar", C.arc, C.walk - 0.1, {{ from: "right" }});
      tl.fromTo(S + "prot", {{ opacity: 0, scale: 0.3, transformOrigin: "0% 100%" }}, {{ opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }}, C.arc + 0.2);
      tl.to(S + "prot", {{ opacity: 0, duration: 0.25 }}, C.walk - 0.1);
      // shoots, turns around before it lands
      play("ball", UP, C.walk + 0.2, 1);
      tl.to(S + "kwrap", {{ y: -30, duration: 0.18, ease: "power2.out", yoyo: true, repeat: 1 }}, C.walk + 0.1);
      tl.to(S + "kwrap", {{ scaleX: -1, transformOrigin: "50% 100%", duration: 0.2, ease: "power2.inOut" }}, C.walk + 0.9);
      tl.to(S + "p-num", {{ scaleX: -1, transformOrigin: "50% 50%", duration: 0.2 }}, C.walk + 0.9);
      tl.to([S + "p-armL", S + "p-armR"], {{ rotation: 0, duration: 0.3 }}, C.walk + 0.9);
      swap(S + "p-m-smile", S + "p-m-o", C.walk + 1.4); swap(S + "p-m-o", S + "p-m-smile", C.walk + 1.8);
      tl.to(S + "p-lids", {{ opacity: 1, duration: 0.01 }}, C.walk + 1.2);
"""
scene(sid, w, js, cards)
