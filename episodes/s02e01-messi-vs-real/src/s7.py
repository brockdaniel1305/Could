import sys; sys.path.insert(0, __file__.rsplit("/episodes/", 1)[0] + "/tools")  # noqa: E702
from scene import *  # noqa: F403
from match import *  # noqa: E402,F403
sid = "s7-laces"
D = TIMING[sid]["duration"]
far = (goal_side(sid, 980, FEET - 60, 120, 80, facing="left") + football(sid, 760, FEET - 66, 0.3, name="fb")
       + player(sid, "a", 700, FEET - 60, 0.3, num=9, tag=False, **REAL))
w = world(sid, far + messi_fig(sid, 330, FEET + 80, 0.6, name="m") + football(sid, 380, FEET + 64, 0.5), zoom=(330, 1100, 1.8))
cards = hud(sid, h=1, a=2, minute="89'") + card(sid, "mn", "MINUTE 89", "Tying laces", 40, 380)
js = JS + """
      crowdIdle();
      stamina(40); stamina(8, 0.3, 1.2);
      // he crouches and ties his laces
      tl.to(S + "m", { y: 30, duration: 0.3 }, C.laces);
      tl.to(S + "m-body", { rotation: 22, transformOrigin: "50% 100%", duration: 0.3 }, C.laces);
      tl.fromTo(S + "m-armR", { rotation: -30 }, { rotation: -10, duration: 0.15, yoyo: true, repeat: 9 }, C.laces + 0.3);
      fly("mn", C.laces, null);
      // meanwhile, far away: Real score
      tl.fromTo(S + "fb", { x: 0 }, { x: 240, duration: 0.8, ease: "power1.in" }, C.two - 0.8);
      tl.fromTo(S + "goal", { scaleX: 1 }, { scaleX: 1.25, transformOrigin: "0% 100%", duration: 0.12, yoyo: true, repeat: 1 }, C.two);
      score(2, 2, "89'", C.two); jump(C.two); flashes(C.two, 0.6);
      look("m", 6, -4, C.two + 0.2);
"""
scene(sid, w, js, cards, extra_css=CSS)
