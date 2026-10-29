import sys; sys.path.insert(0, __file__.rsplit("/episodes/", 1)[0] + "/tools")  # noqa: E702
from scene import *  # noqa: F403
from battle import *  # noqa: E402,F403
import json
sid = "s5-dribble"
D = TIMING[sid]["duration"]
P = pass_times()
front = [f"f{i}" for i in range(PASSES)]
MASS_X = 2663
sky_steps = []
w = (field(sid) + army_defs(sid)
     + f'<g id="{sid}-cam">' + army(sid, MASS_X, cols=6, rows=5, dx=110)
     + "".join(roman(sid, f, FRONT_X0 + i * FRONT_DX) for i, f in enumerate(front))
     + roman(sid, "g0", MASS_X - 120) + "</g>"
     + messi(sid, MX) + ball(sid, MX + 44))
cards = (banner(sid, "b", "THE BATTLE", "The dribble", 40, 330)
         + card(sid, "dz", "DIZZY ROMANS", counter(sid, "dn"), 40, 380, "gold")
         + card(sid, "gf", "GETAFE, 2007", "5 + keeper, ~12 s", 420, 560)
         + card(sid, "tm", "TIME NEEDED", '<span id="s5-dribble-day">~9 days</span>', 560, 560, "red")
         + scorebug(sid, 0, 0))
js = JS + f"""
      const P = {json.dumps(P)}, MOVES = {json.dumps(MOVES)}, MX = {MX}, X0 = {FRONT_X0}, DX = {FRONT_DX}, MASS = {MASS_X};
      const front = {json.dumps(front)};
""" + """
      fly("b", 0.05, P[0] - 0.2, { from: "top" });
      // the camera: soldier i reaches Messi's front foot exactly at P[i]
      const camAt = (t) => -(X0 + DX * (t - P[0]) / (P[1] - P[0]) - (MX + 50));
      const tEnd = P[P.length - 1] + 0.7;
      tl.fromTo(S + "cam", { x: camAt(0) }, { x: camAt(tEnd), duration: tEnd, ease: "none" }, 0);
      run(0.1, tEnd, 0.15);
      // ball at his left foot: a touch every 0.3 s
      tl.fromTo(S + "ball", { x: 0 }, { x: 34, duration: 0.15, ease: "power1.out", yoyo: true, repeat: R(tEnd, 0.15) }, 0);
      tl.fromTo(S + "ball-spin", { rotation: 0 }, { rotation: 360, duration: 0.6, ease: "none", repeat: R(tEnd, 0.6), transformOrigin: "50% 50%" }, 0);
      fly("dz", P[0] + 0.3, null);
      const steps = [[0, "0"]];
      P.forEach((tp, i) => {
        const f = front[i], p = f + "p", mv = MOVES[i];
        // the Roman lunges in with his sword
        tl.to(S + f, { x: -26, duration: 0.25, ease: "power2.out" }, tp - 0.55);
        tl.to(S + p + "-armR", { rotation: -60, duration: 0.2 }, tp - 0.5);
        face(p, "m-o", tp - 0.5);
        // ... Messi's move
        if (mv === "stepover") {
          tl.to(S + "m-legR", { rotation: 40, duration: 0.1, yoyo: true, repeat: 3 }, tp - 0.45);
        } else if (mv === "feint") {
          tl.to(S + "m-body", { x: -18, rotation: -8, transformOrigin: "50% 100%", duration: 0.12, yoyo: true, repeat: 1 }, tp - 0.45);
          tl.to(S + p + "-head", { rotation: -18, duration: 0.15 }, tp - 0.35);
        } else if (mv === "nutmeg") {
          tl.to(S + "ball", { x: 140, y: 4, duration: 0.3, ease: "power2.out" }, tp - 0.3);
          tl.to(S + "ball", { x: 0, y: 0, duration: 0.2 }, tp + 0.1);
          tl.to(S + "mw", { y: -40, duration: 0.18, yoyo: true, repeat: 1, ease: "power2.out" }, tp - 0.25);
        } else if (mv === "roulette") {
          tl.to(S + "mw", { scaleX: -1, transformOrigin: "50% 100%", duration: 0.12, yoyo: true, repeat: 1, ease: "none" }, tp - 0.35);
          tl.to(S + "m-num", { scaleX: -1, transformOrigin: "50% 50%", duration: 0.12, yoyo: true, repeat: 1, ease: "none" }, tp - 0.35);
        } else {
          tl.to(S + "ball", { y: -60, duration: 0.15, yoyo: true, repeat: 1, ease: "power2.out" }, tp - 0.35);
          tl.to(S + "m-legL", { rotation: -40, duration: 0.1, yoyo: true, repeat: 1 }, tp - 0.4);
        }
        tl.to(S + p + "-armR", { rotation: 0, duration: 0.2 }, tp - 0.1);
        // ... and the Roman spins around and stays dizzy
        dizzy(f, tp + 0.05);
        steps.push([tp + 0.35, String(i + 1)]);
      });
      label("dn", steps.concat([[C.fall + 0.3, "12,000"], [C.fall + 0.8, "61,000"], [C.fall + 1.4, "140,000"], [C.into, "260,000"], [C.into + 0.6, "380,000"]]));
      // Getafe 2007
      fly("gf", C.get, C.rate - 0.1, { from: "right" });
      // nine days: the sun and the moon race across the sky
      fly("tm", C.rate, C.fall - 0.1, { from: "right" });
      label("day", [[0, "~9 days"], [C.rate + 0.8, "Day 1"], [C.rate + 1.6, "Day 4"], [C.rate + 2.4, "Day 7"], [C.rate + 3.2, "Day 9"]]);
      for (let k = 0; k < 4; k++) {
        const t0 = C.rate + 0.4 + k * 0.8;
        tl.to(S + "bf-sky", { fill: "#1d2a5c", duration: 0.3 }, t0);
        tl.to(S + "bf-haze", { opacity: 0.1, duration: 0.3 }, t0);
        tl.to(S + "bf-sun", { y: 500, duration: 0.3, ease: "power1.in" }, t0);
        tl.set(S + "bf-moon", { opacity: 1 }, t0 + 0.2);
        tl.fromTo(S + "bf-moon", { y: 500 }, { y: 0, duration: 0.2 }, t0 + 0.2);
        tl.to(S + "bf-moon", { y: 500, duration: 0.2 }, t0 + 0.45);
        tl.to(S + "bf-sky", { fill: "#f6c58a", duration: 0.25 }, t0 + 0.55);
        tl.to(S + "bf-haze", { opacity: 0.7, duration: 0.25 }, t0 + 0.55);
        tl.to(S + "bf-sun", { y: 0, duration: 0.25, ease: "power1.out" }, t0 + 0.55);
      }
      // luckily, dizzy Romans fall over: one feint at the first Roman of the mass, he spins, topples right ... domino
      tl.to(S + "g0p-armR", { rotation: -60, duration: 0.2 }, C.fall - 0.6);
      tl.to(S + "m-body", { x: -18, rotation: -8, transformOrigin: "50% 100%", duration: 0.12, yoyo: true, repeat: 1 }, C.fall - 0.5);
      dizzy("g0", C.fall - 0.25, 2);
      tl.to(S + "g0", { rotation: 78, transformOrigin: "50% 100%", duration: 0.45, ease: "power2.in" }, C.fall + 0.3);
      for (let c = 0; c < 6; c++) for (let r = 0; r < 5; r++) {
        tl.to(S + "a" + r + "-" + c, { rotation: 74, transformOrigin: "50% 100%", duration: 0.35, ease: "power2.in" }, C.fall + 0.6 + c * 0.32 + r * 0.12);
      }
      // ... into other Romans, all the way to the horizon
      tl.to(S + "cam", { x: camAt(tEnd) - 260, duration: 2.0, ease: "power1.inOut" }, C.fall + 0.6);
      look("m", 7, -2, C.fall + 0.5);
      tl.to(S + "m-armL", { rotation: 30, duration: 0.3 }, C.into + 0.4);
      tl.to(S + "m-armR", { rotation: -30, duration: 0.3 }, C.into + 0.4);
      score(C.into + 0.9, 0, 1);
"""
scene(sid, w, js, cards, extra_css=CSS)
