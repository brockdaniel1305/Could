import sys; sys.path.insert(0, __file__.rsplit('/episodes/', 1)[0] + '/tools')  # noqa: E702
from scene import *  # noqa: F403
from shot import world, ball, dots, fly, player_js, J, sx, sy, v_for, X0, GY  # noqa: E402
import math  # noqa: E402
sid = "s4-normal"
D = TIMING[sid]["duration"]
T = TIMING[sid]["cues"]
real = fly(52, bounce_wall=True, until=2.6)
ghost = fly(52, until=1.4)
gd, gn, gt = dots(sid, "g", ghost, step=5)
SLOW = 2.0
hit_at = T["bonk"] - real["events"]["wall"] * SLOW - 0.05        # the wall stops the ball on "returned"
w = (world(sid) + gd
     + f'<g id="{sid}-ap" opacity="0"><path d="M40,{sy(4.9)} L900,{sy(4.9)}" stroke="#f4efe6" stroke-width="5" stroke-dasharray="16 12" /></g>'
     + f'<g id="{sid}-hl" opacity="0"><path d="M40,{sy(7)} L1080,{sy(7)}" stroke="#e0412f" stroke-width="6" stroke-dasharray="20 14" /></g>'
     + ball(sid)
     + f'<g transform="translate({sx(1.2)},{sy(4.1)}) scale(1.1)">{part("burst", sid + "-bonk", WORD="BONK")}</g>'
     + f'<g id="{sid}-bump" transform="translate({X0},{GY - 300})"><ellipse cx="0" cy="0" rx="22" ry="16" fill="#e8a07a" stroke="#1a1a2e" stroke-width="4" /></g>')
cards = (banner(sid, "b", "ATTEMPT 1", "The Normal Shot", 60, 330)
         + card(sid, "ap", "NORMAL APEX", "~5 m", 560, 520)
         + card(sid, "wl", "THE WALL", "7 m", 560, 330, "red")
         + card(sid, "rt", "RETURNED TO SENDER", "+ interest", 360, 400, "gold"))
js = player_js() + f"""
      const REAL = {J(real["pts"])};
      fly("b", C.t, C.apex + 1.0);
      // what a normal three would do (ghost dots through the wall)
      trail("g", {gn}, {J(gt)}, C.apex, 1.6);
      tl.fromTo(S + "ap", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, C.apex + 0.8);
      fly("ap", C.apex + 0.6, C.bonk - 0.1, {{ from: "right" }});
      tl.fromTo(S + "hl", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, C.wall);
      fly("wl", C.wall, C.bonk - 0.1, {{ from: "right" }});
      tl.to([S + "w-browL", S + "w-browR"], {{ y: -16, duration: 0.25, ease: "back.out(3)" }}, C.wall + 0.3);
      tl.to([S + "ap", S + "hl", ...Array.from({{ length: {gn} }}, (_, i) => S + "g" + i)], {{ opacity: 0, duration: 0.2 }}, hit_at - 0.6);
      // the real shot
      tl.set(S + "ball", {{ x: {sx(0.15)}, y: {sy(2.4)} }}, 0);
      tl.fromTo(S + "p-armL", {{ rotation: 0 }}, {{ rotation: 170, duration: 0.3 }}, hit_at - 0.8);
      tl.fromTo(S + "p-armR", {{ rotation: 0 }}, {{ rotation: -170, duration: 0.3 }}, hit_at - 0.8);
      play("ball", REAL, hit_at - 0.25 * 0 - 0.0, {SLOW});
      const wallT = hit_at + {real["events"]["wall"]} * {SLOW}, headT = hit_at + {real["events"]["head"]} * {SLOW};
      tl.fromTo(S + "bonk", {{ scale: 0, opacity: 0, transformOrigin: "50% 50%" }}, {{ scale: 1, opacity: 1, duration: 0.2, ease: "back.out(3)" }}, wallT);
      tl.to(S + "bonk", {{ opacity: 0, duration: 0.2 }}, wallT + 0.8);
      swap(S + "w-smirk", S + "w-grin", wallT + 0.2);
      tl.to([S + "p-armL", S + "p-armR"], {{ rotation: 0, duration: 0.3 }}, wallT + 0.3);
      tl.to([S + "p-pupL", S + "p-pupR"], {{ y: -7, duration: 0.2 }}, wallT + 0.4);
      swap(S + "p-m-smile", S + "p-m-o", wallT + 0.5);
      // ... with interest: bump on the head
      tl.fromTo(S + "kwrap", {{ y: 0 }}, {{ y: 14, duration: 0.08, yoyo: true, repeat: 1 }}, headT);
      pop(S + "bump", headT + 0.05);
      tl.to(S + "p-lids", {{ opacity: 1, duration: 0.01 }}, headT + 0.1);
      fly("rt", C.int, null, {{ from: "top" }});
""".replace("hit_at", f"{hit_at:.3f}")
scene(sid, w, js, cards)
