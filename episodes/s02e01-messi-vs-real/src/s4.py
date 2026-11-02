import sys; sys.path.insert(0, __file__.rsplit("/episodes/", 1)[0] + "/tools")  # noqa: E702
from scene import *  # noqa: F403
from match import *  # noqa: E402,F403
sid = "s4-counter"
D = TIMING[sid]["duration"]
w = world(sid, goal_side(sid, 70, FEET, 230, 150, facing="right") + player(sid, "a", 760, FEET, 0.55, num=9, **REAL)
          + player(sid, "b", 900, FEET + 30, 0.55, num=7, **REAL) + football(sid, 700, FEET - 14, 0.5))
cards = hud(sid, h=0, a=0, minute="11'") + card(sid, "em", "MESSI'S GOAL", "Empty", 560, 380, "red")
js = JS + """
      crowdIdle(); stamina(90);
      run("ap", 0, 1.2); run("bp", 0, 1.2);
      tl.fromTo([S + "a", S + "b"], { x: 200 }, { x: -60, duration: 1.2, ease: "power1.out" }, 0);
      tl.fromTo(S + "ball", { x: 160 }, { x: -520, duration: 1.9, ease: "power1.out" }, 0.2);
      tl.fromTo(S + "ball-spin", { rotation: 0 }, { rotation: -720, duration: 1.9, ease: "power1.out", transformOrigin: "50% 50%" }, 0.2);
      fly("em", C.empty, null, { from: "right" });
      const g = 2.1;
      tl.fromTo(S + "goal", { scaleX: 1 }, { scaleX: 1.2, transformOrigin: "0% 100%", duration: 0.12, yoyo: true, repeat: 1 }, g);
      score(1, 0, "12'", g); jump(g); flashes(g, 0.8);
"""
scene(sid, w, js, cards, extra_css=CSS)
