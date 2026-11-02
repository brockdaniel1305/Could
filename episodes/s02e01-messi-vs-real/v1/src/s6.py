import sys; sys.path.insert(0, __file__.rsplit("/episodes/", 1)[0] + "/tools")  # noqa: E702
from scene import *  # noqa: F403
from match import *  # noqa: E402,F403
sid = "s6-freekick"
D = TIMING[sid]["duration"]
goal = f'<g transform="translate(540,{FEET - 40}) scale(2.2)"><g id="{sid}-goal">{part("goal", sid + "-gl")}</g></g>'
keeper = player(sid, "k", 470, FEET - 40, 0.45, kit="#b6f04a", shorts="#1a1a2e", socks="#b6f04a", numc="#1a1a2e", num=1, tag=False)
wall = "".join(player(sid, f"w{i}", x, 1760, 1.25, num=REAL_NUMS[i + 3], tag=False, **REAL) for i, x in enumerate((300, 470, 640, 810)))
w = world(sid, goal + keeper + f'<g id="{sid}-wall">{wall}</g>' + football(sid, 560, 1820, 1.4))
cards = hud(sid, h=1, a=1, minute="60'") + card(sid, "fk", "FREE KICK", "Top corner", 40, 380, "gold")
js = JS + """
      crowdIdle(); stamina(55);
      label("min", [[0, "60'"], [C.fk, "61'"]]);
      // the wall jumps, the ball curls over it into the top corner, the keeper dives too late
      tl.to(S + "wall", { y: -70, duration: 0.25, yoyo: true, repeat: 1, ease: "power2.out" }, C.fk + 0.15);
      arc(S + "ball", C.fk + 0.2, C.top - C.fk - 0.15, 180, -1020, 260, S + "ball-spin");
      tl.to(S + "ball", { scale: 0.3, duration: C.top - C.fk - 0.15, ease: "none" }, C.fk + 0.2);
      tl.to(S + "k", { x: 160, y: -40, rotation: 60, transformOrigin: "50% 100%", duration: 0.35, ease: "power2.out" }, C.top - 0.2);
      tl.fromTo(S + "goal", { scale: 1 }, { scale: 1.04, transformOrigin: "50% 100%", duration: 0.1, yoyo: true, repeat: 1 }, C.top + 0.05);
      score(1, 2, "61'", C.top + 0.05); jump(C.top + 0.1); flashes(C.top, 0.8);
      fly("fk", C.top + 0.1, null);
"""
scene(sid, w, js, cards, extra_css=CSS)
