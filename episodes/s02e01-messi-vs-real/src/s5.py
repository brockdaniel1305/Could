import sys; sys.path.insert(0, __file__.rsplit("/episodes/", 1)[0] + "/tools")  # noqa: E702
from scene import *  # noqa: F403
from match import *  # noqa: E402,F403
sid = "s5-dribble"
D = TIMING[sid]["duration"]
C0 = TIMING[sid]["cues"]
defs_x = [700 + i * 150 for i in range(10)]
keeper_x = defs_x[-1] + 260
gx = keeper_x + 200
row = "".join(player(sid, f"d{i}", x, FEET + (i % 2) * 30, 0.5, num=REAL_NUMS[i + 1], **REAL) for i, x in enumerate(defs_x))
keeper = player(sid, "k", keeper_x, FEET, 0.55, kit="#b6f04a", shorts="#1a1a2e", socks="#b6f04a", numc="#1a1a2e", num=1)
inner = f'<g id="{sid}-track">' + row + keeper + goal_side(sid, gx, FEET, 230, 150, facing="left") + "</g>" + messi_fig(sid, 300, FEET + 20, 0.6, name="m") + football(sid, 345, FEET + 6, 0.5)
w = world(sid, inner)
cards = (hud(sid, h=1, a=0, minute="33'") + card(sid, "pt", "PLAYERS PASSED", '<span id="s5-dribble-pn">0</span>', 40, 380, "gold")
         + card(sid, "sl", "STADIUM", "Silent", 560, 560))
js = JS + f"""
      const DX = {defs_x}, KX = {keeper_x}, GX = {gx};
""" + """
      crowdIdle(); stamina(70);
      // the camera tracks Messi: the line of defenders slides past him, each spins and falls as he goes by
      const T0 = 0.6, T1 = C.keeper + 0.3, MX = 345;
      run("m", 0.2, C.one);
      tl.fromTo(S + "ball", { x: 0 }, { x: 28, duration: 0.14, yoyo: true, repeat: R(C.one, 0.14) }, 0);
      tl.fromTo(S + "track", { x: 0 }, { x: MX - KX - 40, duration: T1 - T0, ease: "power1.inOut" }, T0);
      const steps = [[0, "0"]];
      DX.forEach((x, i) => { const at = T0 + (T1 - T0) * ((x - DX[0] + 120) / (KX - DX[0] + 160)); spinOut("d" + i, at); steps.push([at, String(i + 1)]); });
      fly("pt", C.past - 0.3, null);
      label("pn", steps.concat([[C.keeper + 0.2, "11"]]));
      tl.to(S + "k", { x: -160, rotation: -70, transformOrigin: "50% 100%", duration: 0.4, ease: "power2.in" }, C.keeper);
      // one-one
      tl.to(S + "ball", { x: GX - KX + 120, duration: 0.6, ease: "power1.in" }, C.one - 0.6);
      tl.fromTo(S + "goal", { scaleX: 1 }, { scaleX: 1.2, transformOrigin: "0% 100%", duration: 0.12, yoyo: true, repeat: 1 }, C.one);
      score(1, 1, "34'", C.one);
      tl.to(S + "fans", { opacity: 0.55, duration: 0.3 }, C.one + 0.1);
      fly("sl", C.one + 0.2, null, { from: "right" });
"""
scene(sid, w, js, cards, extra_css=CSS)
