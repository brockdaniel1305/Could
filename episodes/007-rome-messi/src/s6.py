import sys; sys.path.insert(0, __file__.rsplit("/episodes/", 1)[0] + "/tools")  # noqa: E702
from scene import *  # noqa: F403
from battle import *  # noqa: E402,F403
sid = "s6-strike"
D = TIMING[sid]["duration"]
C0 = TIMING[sid]["cues"]
# plan A world: Messi + testudo at normal scale (zooms to the legs)
wa = (f'<g id="{sid}-A"><g id="{sid}-zoom">' + field(sid)
      + messi(sid, 230) + ball(sid, 274)
      + f'<g transform="translate(1340,{GY})"><g id="{sid}-tw"><g transform="scale(0.8)">{part("testudo", sid + "-t")}</g></g></g>'
      + "</g></g>")
# plan B world: wide shot at 65 px/m. Ball 9.15 m from the wall, goal behind it
PX = 65
ms = PX * 1.70 / 316
bx = 150
wall_x = bx + 9.15 * PX + 1.5 * PX     # wall centre (3 m thick)
goal_x = wall_x + 1.5 * PX + 50
wb = (f'<g id="{sid}-B" opacity="0">' + part("battlefield", sid + "-bf2")
      + f'<g id="{sid}-dash" opacity="0"><path d="M{bx},{GY + 8} L{wall_x - 1.5 * PX:.0f},{GY + 8}" stroke="#f4f4f2" stroke-width="6" stroke-dasharray="16 12" />'
      + f'<text data-layout-ignore x="{(bx + wall_x) / 2 - 60:.0f}" y="{GY - 24}" font-family="Inter" font-weight="900" font-size="34" fill="#f4f4f2" stroke="#1a1a2e" stroke-width="2">9.15 m</text></g>'
      + f'<g transform="translate({goal_x:.0f},{GY})"><g id="{sid}-goal"><path d="M0,0 L0,{-2.44 * PX:.0f} L140,{-2.44 * PX:.0f}" fill="none" stroke="#f4f4f2" stroke-width="9" />'
      + f'<path d="M0,{-2.44 * PX:.0f} L140,0 M30,{-2.44 * PX:.0f} L140,-40 M60,{-2.44 * PX:.0f} L140,-80 M0,-40 L60,0 M0,-80 L110,0 M0,-120 L140,-10" stroke="#f4f4f2" stroke-width="3" opacity="0.8" /></g></g>'
      + f'<g transform="translate({wall_x:.0f},{GY})"><g id="{sid}-wall"><g transform="scale({PX / 100})">{part("hadrian-wall", sid + "-hw")}</g>'
      + "".join(f'<g transform="translate({dx},{-4.7 * PX:.0f})"><g id="{sid}-w{i}"><g transform="scale(0.28)">{part("legionary", sid + "-w" + str(i) + "p")}</g></g></g>' for i, dx in enumerate((-60, 0, 60)))
      + "</g></g>"
      + f'<clipPath id="{sid}-trc"><rect id="{sid}-trr" x="0" y="0" width="0" height="1920" /></clipPath>'
      + f'<path id="{sid}-trail" clip-path="url(#{sid}-trc)" d="M{bx},{GY - 10} Q{(bx + goal_x + 80) / 2:.0f},{GY - 2 * 470} {goal_x + 80:.0f},{GY - 70}" fill="none" stroke="#ffd23f" stroke-width="6" stroke-dasharray="4 16" stroke-linecap="round" />'
      + messi(sid + "-b", bx - 40, s=ms) + ball(sid + "-b", bx, GY - 10, 0.45)
      + "</g>")
w = wa + wb
cards = (banner(sid, "a", "ROME STRIKES BACK", "Plan A: the testudo", 30, 330)
         + card(sid, "to", "A TORTOISE MADE OF", "Shields", 560, 600, "gold")
         + card(sid, "lg", "LEGS UNDERNEATH", "40", 560, 380, "red")
         + card(sid, "nt", "PLAN A", "Nutmegged", 40, 380, "gold")
         + banner(sid, "b", "PLAN B", "Build a wall", 40, 330)
         + card(sid, "hw", "HADRIAN'S WALL", "Built from AD 122", 40, 380)
         + card(sid, "km", "LENGTH", map_britain(sid) + "117 km", 600, 300, "red")
         + card(sid, "fk", "MESSI FREE-KICK GOALS", "65+", 40, 380, "gold")
         + card(sid, "lo", "THIS WALL", "Just longer", 560, 560, "red")
         + scorebug(sid, 0, 1))
js = JS + f"""
      const FK_RUN = {FK_RUN}, FK_KICK = {FK_KICK}, FL = {FK_FLIGHT}, GX = {goal_x + 80 - bx:.0f};
      const SB = "#{sid}-b-";
""" + """
      // ---- Plan A: the testudo shuffles in
      fly("a", C.a, C.legs - 0.1, { from: "top" });
      tl.fromTo(S + "tw", { x: 0 }, { x: -700, duration: 3.4, ease: "power1.out" }, 0.3);
      tl.fromTo(S + "tw .tlA", { y: 0 }, { y: -12, duration: 0.14, yoyo: true, repeat: R(3.4, 0.14), ease: "sine.inOut" }, 0.3);
      tl.fromTo(S + "tw .tlB", { y: -12 }, { y: 0, duration: 0.14, yoyo: true, repeat: R(3.4, 0.14), ease: "sine.inOut" }, 0.3);
      tl.fromTo(S + "tw .tpup", { x: 0 }, { x: -3, duration: 0.3 }, 1.0);
      fly("to", C.tort, C.legs - 0.1, { from: "right" });
      look("m", 6, 0, 0.6);
      // ... unfortunately, it has legs: the camera drops to ground level
      tl.to(S + "zoom", { scale: 1.8, transformOrigin: "420px 1200px", duration: 0.7, ease: "power2.inOut" }, C.legs);
      fly("lg", C.legs + 0.5, C.nut - 0.1, { from: "right" });
      // nutmeg: the ball goes between the legs, Messi runs round the back
      kickR(C.nut);
      tl.to(S + "ball", { x: 900, duration: 0.8, ease: "power1.out" }, C.nut);
      tl.to(S + "ball-spin", { rotation: 900, duration: 0.8, ease: "power1.out" }, C.nut);
      run(C.nut + 0.1, C.nut + 0.9);
      tl.to(S + "mw", { x: 900, duration: 0.8, ease: "power1.in" }, C.nut + 0.1);
      tl.to(S + "tw .tpup", { x: 4, duration: 0.15 }, C.nut + 0.5);
      tl.to(S + "zoom", { scale: 1, duration: 0.5, ease: "power2.inOut" }, C.nut + 0.6);
      tl.to(S + "tw", { scaleX: -1, transformOrigin: "50% 100%", duration: 0.2 }, C.nut + 0.9);
      // the shell falls apart
      [1, 2, 3, 4, 5].forEach((i) => {
        tl.to(S + "t-r" + i, { y: -200 - i * 30, x: (i - 3) * 80, rotation: (i - 3) * 50, duration: 0.35, ease: "power2.out" }, C.nut + 1.1);
        tl.to(S + "t-r" + i, { y: 320, duration: 0.4, ease: "power2.in" }, C.nut + 1.45);
        tl.to(S + "t-s" + i, { rotation: (i % 2 ? 1 : -1) * 80, y: 60, x: (i - 3) * 40, transformOrigin: "50% 100%", duration: 0.4, ease: "power2.in" }, C.nut + 1.15 + i * 0.04);
      });
      fly("nt", C.nut + 0.3, C.b - 0.1);
      score(C.nut + 0.5, 0, 2);
      // ---- Plan B: wide shot (65 px/m)
      tl.set(S + "A", { opacity: 0 }, C.b);
      tl.set(S + "B", { opacity: 1 }, C.b);
      fly("b", C.b, C.hw - 0.1, { from: "top" });
      // they build a wall: it rises out of the ground, the ground shakes
      tl.fromTo(S + "wall", { scaleY: 0, transformOrigin: "50% 100%" }, { scaleY: 1, duration: 0.9, ease: "back.out(1.3)" }, C.wall);
      tl.fromTo(S + "B", { y: 0 }, { y: 6, duration: 0.05, yoyo: true, repeat: 15 }, C.wall);
      fly("hw", C.hw, C.fk - 0.1);
      fly("km", C.km, C.fk - 0.1, { from: "right" });
      drawOn(S + "hwline", C.km + 0.4, 0.9);
      // free kick: 9.15 m, run-up, curl over the wall into the goal
      fly("fk", C.fk, null);
      tl.fromTo(S + "dash", { opacity: 0 }, { opacity: 1, duration: 0.3 }, C.fk + 0.1);
      tl.to(SB + "mw", { x: -50, duration: 0.4 }, C.fk + 0.3);
      tl.to(SB + "mw", { x: -8, duration: FK_KICK - FK_RUN, ease: "power1.in" }, C.fk + FK_RUN);
      tl.fromTo(SB + "m-legR", { rotation: 30 }, { rotation: -30, duration: 0.12, yoyo: true, repeat: 3 }, C.fk + FK_RUN);
      tl.to(SB + "m-legR", { rotation: -55, duration: 0.1, ease: "power3.out" }, C.fk + FK_KICK - 0.05);
      tl.to(SB + "m-legR", { rotation: 0, duration: 0.3 }, C.fk + FK_KICK + 0.3);
      arc(SB + "ball", C.fk + FK_KICK, FL, GX, -63, 470, SB + "ball-spin");
      tl.fromTo(S + "trr", { attr: { width: 0 } }, { attr: { width: 1080 }, duration: FL, ease: "none" }, C.fk + FK_KICK);
      [0, 1, 2].forEach((i) => { look("w" + i + "p", -5, -4, C.fk + FK_KICK); look("w" + i + "p", 6, -2, C.fk + FK_KICK + 0.6); face("w" + i + "p", "m-o", C.fk + FK_KICK + 0.4); });
      const goalT = C.fk + FK_KICK + FL;
      tl.fromTo(S + "goal", { scaleX: 1 }, { scaleX: 1.25, transformOrigin: "0% 100%", duration: 0.12, yoyo: true, repeat: 1 }, goalT);
      score(goalT + 0.1, 0, 3);
      tl.to(SB + "m-armL", { rotation: 150, duration: 0.25 }, goalT + 0.2);
      tl.to(SB + "m-armR", { rotation: -150, duration: 0.25 }, goalT + 0.2);
      // this one is just longer
      fly("lo", C.long, null, { from: "right" });
      [0, 1, 2].forEach((i) => dizzy("w" + i, C.long + 0.3 + i * 0.15, 2));
"""
scene(sid, w, js, cards, extra_css=CSS)
