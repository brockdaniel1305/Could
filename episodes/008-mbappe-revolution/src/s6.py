import sys; sys.path.insert(0, __file__.rsplit("/episodes/", 1)[0] + "/tools")  # noqa: E702
from scene import *  # noqa: F403
from rev import *  # noqa: E402,F403
sid = "s6-horse"
D = TIMING[sid]["duration"]
dust = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#cfc8b8" stroke="#1a1a2e" stroke-width="4" />' for x, y, r in ((-40, -20, 34), (10, -40, 44), (60, -18, 30)))
w = (part("paris-street", sid + "-ps")
     + mb(sid, 460) + f'<g transform="translate(460,{GY})"><g id="{sid}-dust" opacity="0">{dust}</g></g>'
     + f'<g transform="translate(160,{GY})"><g id="{sid}-nw"><g transform="scale(0.62)">{part("napoleon-horse", sid + "-n")}</g></g></g>'
    )
cards = (card(sid, "np", "NAPOLEON", "Bonaparte", 40, 380)
         + card(sid, "hs", "TRANSPORT", "1 horse", 560, 380, "gold")
         + card(sid, "s1", "MBAPPÉ", "38 km/h", 40, 380)
         + card(sid, "s2", "HORSE", "45 km/h", 560, 380, "red")
         + card(sid, "fm", "FASTEST MAN IN FRANCE", "No. 2", 40, 560, "red")
         + calendar(sid, "", "BRUMAIRE", "1799"))
js = JS + """
      tl.set(S + "m-crown", { opacity: 1 }, 0); tl.set(S + "m-sash", { opacity: 1 }, 0);
      tl.set(S + "m-armL", { rotation: -62 }, 0); tl.set(S + "m-armR", { rotation: 62 }, 0);
      // Napoleon gallops in from the left and rears up
      gallop(C.nap - 0.5, C.nap + 0.5);
      tl.fromTo(S + "nw", { x: -900 }, { x: 0, duration: 1.0, ease: "power2.out" }, C.nap - 0.5);
      tl.to(S + "n-horse", { rotation: -16, transformOrigin: "20% 100%", duration: 0.35, yoyo: true, repeat: 1, ease: "power2.out" }, C.nap + 0.55);
      tl.to(S + "n-narm", { rotation: -150, duration: 0.3 }, C.nap + 0.6);
      tl.to(S + "n-narm", { rotation: 0, duration: 0.3 }, C.nap + 1.4);
      fly("np", C.nap, C.spd - 0.1);
      look("m", -6, 0, C.nap + 0.2);
      tl.to([S + "m-browL", S + "m-browR"], { y: -6, duration: 0.2 }, C.nap + 0.2);
      fly("hs", C.horse, C.spd - 0.1, { from: "right" });
      // the race: the street scrolls, Mbappé at 38 km/h, the horse at 45 overtakes and takes the crown
      const R0 = C.spd + 0.1, R1 = C.spd + 3.0;
      uncross(R0);
      run(R0, R1);
      gallop(R0, R1 + 0.3);
      tl.fromTo(S + "ps-houses", { x: 0 }, { x: -1100, duration: 0.9, ease: "none", repeat: R(R1 - R0, 0.9) }, R0);
      tl.to(S + "nw", { x: 1200, duration: R1 - R0 + 0.3, ease: "power2.in" }, R0);
      fly("s1", C.spd + 0.2, C.second - 0.1);
      fly("s2", C.spd + 0.6, C.second - 0.1, { from: "right" });
      const grab = R0 + (R1 - R0 + 0.3) * 0.56;
      tl.to(S + "n-narm", { rotation: -110, duration: 0.15 }, grab - 0.2);
      tl.set(S + "m-crown", { opacity: 0 }, grab); tl.set(S + "n-crown", { opacity: 1 }, grab);
      tl.to(S + "n-narm", { rotation: 0, duration: 0.3 }, grab + 0.2);
      // he stops in a cloud of dust and crosses his arms, offended
      tl.fromTo(S + "dust", { opacity: 1, scale: 0.4, transformOrigin: "50% 100%" }, { opacity: 0, scale: 1.8, duration: 0.8, immediateRender: false }, R1);
      cross(R1 + 0.3);
      tl.to([S + "m-browL", S + "m-browR"], { y: 4, rotation: 10, duration: 0.2 }, R1 + 0.3);
      tl.set(S + "m-m-smile", { opacity: 0 }, R1 + 0.3); tl.set(S + "m-m-flat", { opacity: 1 }, R1 + 0.3);
      look("m", 6, 0, R1);
      fly("fm", C.second, null);
"""
scene(sid, w, js, cards, extra_css=CSS)
