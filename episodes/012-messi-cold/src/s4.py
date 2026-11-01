import sys; sys.path.insert(0, __file__.rsplit("/episodes/", 1)[0] + "/tools")  # noqa: E702
from scene import *  # noqa: F403
from battle import *  # noqa: E402,F403
from cold import *  # noqa: E402,F403
import json
sid = "s4-dribble"
D = TIMING[sid]["duration"]
C0 = TIMING[sid]["cues"]
P = [0.45 + i * 0.7 for i in range(5)]
front = [f"f{i}" for i in range(len(P))]
MASS_X = FRONT_X0 + FRONT_DX * len(P) + 60
w = (field(sid) + army_defs(sid) + f'<g id="{sid}-cam">' + army(sid, MASS_X, cols=6, rows=5, dx=110)
     + "".join(roman(sid, f, FRONT_X0 + i * FRONT_DX) for i, f in enumerate(front))
     + roman(sid, "g0", MASS_X - 120) + "</g>" + messi(sid, MX) + ball(sid, MX + 44))
cards = card(sid, "dz", "DIZZY ROMANS", counter(sid, "dn"), 40, 380, "gold")
js = JS + f"""
      const P = {json.dumps(P)}, MX = {MX}, X0 = {FRONT_X0}, DX = {FRONT_DX};
      const front = {json.dumps(front)};
""" + """
      const camAt = (t) => -(X0 + DX * (t - P[0]) / (P[1] - P[0]) - (MX + 50));
      const tEnd = P[P.length - 1] + 0.5;
      tl.fromTo(S + "cam", { x: camAt(0) }, { x: camAt(tEnd), duration: tEnd, ease: "none" }, 0);
      run(0.05, tEnd, 0.14);
      tl.fromTo(S + "ball", { x: 0 }, { x: 34, duration: 0.14, ease: "power1.out", yoyo: true, repeat: R(tEnd, 0.14) }, 0);
      fly("dz", 0.2, null);
      const steps = [[0, "0"]];
      P.forEach((tp, i) => {
        const f = front[i], p = f + "p";
        tl.to(S + f, { x: -24, duration: 0.2, ease: "power2.out" }, tp - 0.4);
        tl.to(S + p + "-armR", { rotation: -60, duration: 0.15 }, tp - 0.35);
        if (i % 2) tl.to(S + "mw", { y: -36, duration: 0.15, yoyo: true, repeat: 1, ease: "power2.out" }, tp - 0.25);
        else tl.to(S + "m-legR", { rotation: 40, duration: 0.08, yoyo: true, repeat: 3 }, tp - 0.35);
        tl.to(S + p + "-armR", { rotation: 0, duration: 0.15 }, tp - 0.05);
        dizzy(f, tp + 0.05, 2);
        steps.push([tp + 0.25, String(i + 1)]);
      });
      label("dn", steps.concat([[C.fall + 0.4, "12,000"], [C.fall + 0.8, "61,000"], [C.into, "140,000"], [C.into + 0.5, "260,000"], [C.into + 1.0, "380,000"]]));
      // dizzy Romans fall over ... into other Romans
      tl.to(S + "g0p-armR", { rotation: -60, duration: 0.15 }, C.fall - 0.5);
      dizzy("g0", C.fall - 0.35, 2);
      tl.to(S + "g0", { rotation: 78, transformOrigin: "50% 100%", duration: 0.4, ease: "power2.in" }, C.fall + 0.15);
      for (let c = 0; c < 6; c++) for (let r = 0; r < 5; r++)
        tl.to(S + "a" + r + "-" + c, { rotation: 74, transformOrigin: "50% 100%", duration: 0.35, ease: "power2.in" }, C.fall + 0.45 + c * 0.22 + r * 0.08);
      tl.to(S + "cam", { x: camAt(tEnd) - 240, duration: 1.6, ease: "power1.inOut" }, C.fall + 0.45);
"""
scene(sid, w, js, cards, extra_css=CSS)
