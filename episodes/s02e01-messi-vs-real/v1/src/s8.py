import sys; sys.path.insert(0, __file__.rsplit("/episodes/", 1)[0] + "/tools")  # noqa: E702
from scene import *  # noqa: F403
from match import *  # noqa: E402,F403
sid = "s8-last"
D = TIMING[sid]["duration"]
w = world(sid, goal_side(sid, 900, FEET, 230, 150, facing="left") + player(sid, "k", 820, FEET, 0.55, kit="#b6f04a", shorts="#1a1a2e", socks="#b6f04a", numc="#1a1a2e", num=1)
          + messi_fig(sid, 260, FEET + 20, 0.6, name="m") + football(sid, 305, FEET + 6, 0.5) + confetti(sid))
cards = (hud(sid, h=2, a=2, minute="92'") + slam(sid, "gl", "GOAL!!!", 520, 150)
         + '\n    <div class="slam" id="s8-last-sm" style="top: 330px; font-size: 40px; color: #f4f4f2;">SLOW MOTION</div>')
js = JS + """
      crowdIdle(); stamina(3);
      run("m", 0.1, C.last + 0.6);
      tl.to(S + "m", { x: 160, duration: C.last + 0.5, ease: "power1.in" }, 0.1);
      tl.to(S + "ball", { x: 170, duration: C.last + 0.5, ease: "power1.in" }, 0.1);
      // slow motion shot
      tl.fromTo(S + "sm", { opacity: 0 }, { opacity: 1, duration: 0.15 }, C.last + 0.4);
      tl.to(S + "sm", { opacity: 0, duration: 0.15 }, C.goal);
      tl.to(S + "m-legR", { rotation: -55, duration: 0.25 }, C.last + 0.6);
      arc(S + "ball", C.last + 0.75, C.goal - C.last - 0.75, 620, -90, 120, S + "ball-spin");
      tl.to(S + "k", { x: -60, y: -60, rotation: -70, transformOrigin: "50% 100%", duration: 0.6, ease: "power2.out" }, C.goal - 0.6);
      tl.fromTo(S + "goal", { scaleX: 1 }, { scaleX: 1.2, transformOrigin: "0% 100%", duration: 0.12, yoyo: true, repeat: 1 }, C.goal);
      score(2, 3, "92'", C.goal); flashes(C.goal, 1.0); confettiFall(C.goal);
      slamIn("gl", C.goal, null);
      tl.to([S + "m-armL", S + "m-armR"], { rotation: (i) => (i ? -160 : 160), duration: 0.25 }, C.goal + 0.1);
"""
scene(sid, w, js, cards, extra_css=CSS)
