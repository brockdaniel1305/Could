import sys; sys.path.insert(0, __file__.rsplit('/episodes/', 1)[0] + '/tools')  # noqa: E702
from scene import *  # noqa: F403
from shot import world, ball, dots, fly, player_js, J, sx, sy, v_for, X0, GY  # noqa: E402
import math  # noqa: E402
sid = "s5-moon"
D = TIMING[sid]["duration"]
T = TIMING[sid]["cues"]
moon = fly(76.7, until=2.5)
gd, gn, gt = dots(sid, "g", moon, step=6)
launch = T["ang"] + 0.5
apex_t = 12.6 * math.sin(math.radians(76.7)) / 9.81
SLOW = (T["bolt"] - launch) / apex_t          # the ball tops out on "Faster than Usain Bolt"
a = math.radians(76.7)
w = (world(sid) + gd
     + f'<g id="{sid}-ap" opacity="0"><path d="M40,{sy(10.1)} L900,{sy(10.1)}" stroke="#ffd23f" stroke-width="6" stroke-dasharray="16 12" /></g>'
     + f'''<g id="{sid}-prot" transform="translate({sx(0.15)},{sy(2.4)})"><path d="M0,0 L200,0" stroke="#f4efe6" stroke-width="6" />
  <path d="M0,0 L{230 * math.cos(a):.0f},{-230 * math.sin(a):.0f}" stroke="#ffd23f" stroke-width="7" />
  <path d="M120,0 A120,120 0 0 0 {120 * math.cos(a):.0f},{-120 * math.sin(a):.0f}" fill="none" stroke="#ffd23f" stroke-width="6" />
  <rect x="120" y="-120" width="110" height="54" rx="10" fill="#ffd23f" stroke="#1a1a2e" stroke-width="4" /><text x="175" y="-82" text-anchor="middle" font-family="Inter" font-weight="900" font-size="34" fill="#1a1a2e">77°</text></g>'''
     + ball(sid))
cards = (banner(sid, "b", "ATTEMPT 2", "The Moonball", 60, 330)
         + card(sid, "an", "LAUNCH ANGLE", "77°", 560, 560, "gold")
         + card(sid, "ap", "APEX", "10.1 m", 560, 330)
         + card(sid, "v", "LAUNCH SPEED", "46 km/h", 60, 340, "gold")
         + card(sid, "bo", "BOLT'S TOP SPEED", "44.7 km/h", 60, 540)
         + card(sid, "air", "HANG TIME", '<span id="s5-moon-hang">0.00 s</span>', 560, 330))
js = player_js() + f"""
      const MOON = {J(moon["pts"])};
      fly("b", C.t, C.ang + 1.0);
      tl.set(S + "ball", {{ x: {sx(0.15)}, y: {sy(2.4)} }}, 0);
      tl.fromTo(S + "p-armL", {{ rotation: 0 }}, {{ rotation: 170, duration: 0.3 }}, C.ang - 0.5);
      tl.fromTo(S + "p-armR", {{ rotation: 0 }}, {{ rotation: -170, duration: 0.3 }}, C.ang - 0.5);
      tl.fromTo(S + "prot", {{ opacity: 0, scale: 0.3, transformOrigin: "0% 100%" }}, {{ opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2)" }}, C.ang);
      tl.to(S + "prot", {{ opacity: 0, duration: 0.3 }}, C.apex);
      fly("an", C.ang + 0.6, C.apex - 0.1, {{ from: "right" }});
      // the launch: knees, jump, slow motion
      tl.to(S + "kwrap", {{ y: 16, duration: 0.2, ease: "power2.in" }}, {launch - 0.25:.3f});
      tl.to(S + "kwrap", {{ y: -40, duration: 0.25, ease: "power2.out", yoyo: true, repeat: 1 }}, {launch - 0.05:.3f});
      play("ball", MOON, {launch:.3f}, {SLOW:.3f}, 2.5);
      trail("g", {gn}, {J(gt)}, {launch:.3f}, {SLOW:.3f});
      tl.to([S + "p-pupL", S + "p-pupR"], {{ y: -8, duration: 0.3 }}, {launch + 0.3:.3f});
      swap(S + "p-m-smile", S + "p-m-o", {launch + 0.4:.3f});
      tl.fromTo(S + "ap", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, C.apex);
      fly("ap", C.apex, C.v - 0.1, {{ from: "right" }});
      fly("v", C.v, C.air - 0.1);
      fly("bo", C.bolt, C.air - 0.1);
      // the wall looks up, worried
      tl.to([S + "w-browL", S + "w-browR"], {{ y: 10, duration: 0.3 }}, C.bolt);
      // hang time clock (real flight time)
      const hang = document.getElementById("s5-moon-hang"), h = {{ v: 0 }};
      tl.fromTo(h, {{ v: 0 }}, {{ v: (D - {launch:.3f}) / {SLOW:.3f}, duration: D - {launch:.3f}, ease: "none", onUpdate() {{ hang.textContent = h.v.toFixed(2) + " s"; }} }}, {launch:.3f});
      fly("air", C.air, null, {{ from: "right" }});
"""
scene(sid, w, js, cards)
