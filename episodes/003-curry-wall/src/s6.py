import sys; sys.path.insert(0, __file__.rsplit('/episodes/', 1)[0] + '/tools')  # noqa: E702
from scene import *  # noqa: F403
from shot import world, ball, dots, fly, player_js, J, sx, sy, v_for, X0, GY  # noqa: E402
import math  # noqa: E402
sid = "s6-blind"
D = TIMING[sid]["duration"]
T = TIMING[sid]["cues"]
v0 = v_for(math.radians(76.7))
short = fly(77.7, v=v0, until=4.0, can_score=False)
long_ = fly(75.7, v=v0, until=2.36, can_score=False)
sd, sn, st = dots(sid, "s", short, step=6)
ld, ln, lt = dots(sid, "l", long_, step=6)
eye = (sx(0.05), sy(2.15))
w = (world(sid) + sd + ld
     + f'<g id="{sid}-sight" opacity="0"><path d="M{eye[0]},{eye[1]} L{sx(1.35)},{sy(2.5)}" stroke="#e0412f" stroke-width="6" stroke-dasharray="14 10" />'
       f'<path d="M{sx(1.35) - 22},{sy(2.5) - 22} l44,44 m0,-44 l-44,44" stroke="#e0412f" stroke-width="10" stroke-linecap="round" /></g>'
     + f'<g id="{sid}-q" transform="translate({X0 + 70},{GY - 340})"><circle r="40" fill="#fff" stroke="#1a1a2e" stroke-width="5" /><text y="18" text-anchor="middle" font-family="Inter" font-weight="900" font-size="52" fill="#1a1a2e">?</text></g>'
     + ball(sid))
cards = (banner(sid, "b", "ATTEMPT 3", "The Blind Shot", 60, 330)
         + card(sid, "e", "1° TOO STEEP", "50 cm short", 560, 320, "red")
         + card(sid, "t", "MARGIN OF ERROR", "± 0.2°", 60, 360, "gold")
         + card(sid, "m", "EVERY MISS LANDS IN", "China", 560, 330)
         + card(sid, "wk", "FETCHING THE BALL", "88 days on foot", 60, 520, "red"))
js = player_js() + f"""
      const SHORT = {J(short["pts"])};
      fly("b", C.t, C.see + 0.8);
      // he cannot see the rim: the sight line ends in the wall
      tl.fromTo(S + "sight", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3 }}, C.see);
      pop(S + "q", C.see + 0.4);
      tl.to(S + "sight", {{ opacity: 0, duration: 0.3 }}, C.err);
      tl.to(S + "q", {{ opacity: 0, duration: 0.3 }}, C.err);
      // one degree off: two ghost arcs, both wrong
      trail("s", {sn}, {J(st)}, C.err + 0.2, 0.7);
      trail("l", {ln}, {J(lt)}, C.err + 0.5, 0.7);
      fly("e", C.err + 0.8, C.tol - 0.1, {{ from: "right" }});
      fly("t", C.tol, C.miss - 0.1);
      tl.to([...Array.from({{ length: {sn} }}, (_, i) => S + "s" + i), ...Array.from({{ length: {ln} }}, (_, i) => S + "l" + i)], {{ opacity: 0, duration: 0.3 }}, C.miss - 0.6);
      // the real miss: short, bounces, rolls off towards the horizon
      tl.set(S + "ball", {{ x: {sx(0.15)}, y: {sy(2.4)} }}, 0);
      tl.fromTo(S + "p-armL", {{ rotation: 0 }}, {{ rotation: 170, duration: 0.3 }}, C.miss - 1.6);
      tl.fromTo(S + "p-armR", {{ rotation: 0 }}, {{ rotation: -170, duration: 0.3 }}, C.miss - 1.6);
      play("ball", SHORT, C.miss - 1.3, 0.75);
      tl.to([S + "p-armL", S + "p-armR"], {{ rotation: 0, duration: 0.3 }}, C.miss + 0.2);
      fly("m", C.miss + 0.3, C.walk + 2.2, {{ from: "right" }});
      fly("wk", C.walk, null);
      swap(S + "w-smirk", S + "w-grin", C.miss + 0.4);
      swap(S + "p-m-smile", S + "p-m-flat", C.walk + 0.2);
      tl.to([S + "p-pupL", S + "p-pupR"], {{ x: 7, duration: 0.3 }}, C.miss + 0.6);
"""
scene(sid, w, js, cards)
