import sys; sys.path.insert(0, __file__.rsplit('/episodes/', 1)[0] + '/tools')  # noqa: E702
from scene import *  # noqa: F403
from shot import world, ball, dots, fly, player_js, J, sx, sy, v_for, X0, GY  # noqa: E402
import math  # noqa: E402
sid = "s1-hook"
D = TIMING[sid]["duration"]
w = world(sid) + ball(sid)
cards = (banner(sid, "q", "CASE FILE 003", "Could Steph Curry<br>make a three over<br>the Great Wall?", 50, 330)
         + card(sid, "m", "METHOD", "Scientific", 560, 420)
         + card(sid, "pr", "EQUIPMENT", "1 protractor", 520, 600, "gold"))
js = """
      // frame 0 is the thumbnail: the question is already on screen
      tl.fromTo(S + "c-q", { opacity: 1, x: 0, y: 0, rotation: -2 }, { y: -1100, rotation: 8, duration: 0.4, ease: "power3.in" }, C.sci - 0.45);
      fly("m", C.sci, null, { from: "right" });
      fly("pr", C.long, null, { from: "right" });
      // Curry dribbles, the wall looks down on him
      const bx = 150 + 46, n = R(D, 0.5);
      tl.fromTo(S + "ball", { x: bx, y: 1060 }, { x: bx, y: 1232, duration: 0.25, ease: "power2.in", repeat: n * 2 + 1, yoyo: true }, 0);
      tl.fromTo(S + "p-armR", { rotation: -10 }, { rotation: -30, duration: 0.25, ease: "sine.inOut", repeat: n * 2 + 1, yoyo: true }, 0);
      blink(S + "p-lids", 1.5); blink(S + "p-lids", 5.0);
      tl.to([S + "p-pupL", S + "p-pupR"], { x: 6, y: -7, duration: 0.3 }, C.ev);
      tl.to([S + "w-browL", S + "w-browR"], { y: -16, duration: 0.25, ease: "back.out(3)" }, C.sci);
      swap(S + "w-smirk", S + "w-grin", C.sci + 0.2);
"""
scene(sid, w, js, cards)
