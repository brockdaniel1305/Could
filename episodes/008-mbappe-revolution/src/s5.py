import sys; sys.path.insert(0, __file__.rsplit("/episodes/", 1)[0] + "/tools")  # noqa: E702
from scene import *  # noqa: F403
from rev import *  # noqa: E402,F403
sid = "s5-power"
D = TIMING[sid]["duration"]
week = ('\n    <div class="week" id="s5-power-wk"><div class="wk">THE REVOLUTIONARY WEEK (FROM 1793)</div><div class="row">'
        + "".join(f'<div class="d" id="s5-power-d{i}">{i}</div>' for i in range(1, 11))
        + '<div class="d r" id="s5-power-d11">REST</div></div></div>')
zz = f'<g transform="translate(800,560)"><g id="{sid}-zz" opacity="0"><text data-layout-ignore font-family="Inter" font-weight="900" font-size="48" fill="#1a1a2e">z z Z</text></g></g>'
w = (part("palace", sid + "-pa") + mb(sid, 700, 900, 0.75) + part("palace-rail", sid + "-rl") + zz + crowd_defs(sid)
     + crowd(sid, [(1330, 0.66, 9), (1440, 0.76, 8), (1560, 0.88, 7)], x0=-30, dx=120))
cards = (banner(sid, "b", "PLAN B", "Take power", 40, 330)
         + card(sid, "lw", "DECREE No. 1", "Arms crossed", 40, 380, "gold")
         + card(sid, "ac", "ARMS CROSSED", counter(sid, "an"), 40, 560, "red")
         + week + calendar(sid, "", "YEAR II", "1793"))
js = JS + """
      fly("b", C.t, C.law - 0.1, { from: "top" });
      // crown and sash
      tl.set(S + "m-crown", { opacity: 1 }, C.t + 0.1);
      tl.fromTo(S + "m-crown", { y: -500 }, { y: 0, duration: 0.4, ease: "bounce.out" }, C.t + 0.1);
      tl.fromTo(S + "m-sash", { opacity: 0 }, { opacity: 1, duration: 0.2 }, C.t + 0.3);
      cross(C.t + 0.6);
      // the decree, and the wave of crossed arms through the crowd
      fly("lw", C.law, C.cal - 0.1);
      tl.to(S + "m-armR", { rotation: -140, duration: 0.25 }, C.law);
      cross(C.law + 0.6);
      fly("ac", C.law + 0.8, C.cal - 0.1);
      count("an", 0, 28000000, C.law + 1.0, 2.0, "power1.inOut");
      crossWave("cr", 3, 9, C.law + 1.0, 0.45);
      // the ten-day week, day by day ... and an eleventh: rest
      tl.fromTo(S + "wk", { opacity: 0, y: -200 }, { opacity: 1, y: 0, duration: 0.4, ease: "back.out(1.6)" }, C.cal);
      for (let i = 1; i <= 10; i++) pop(S + "d" + i, C.cal + 0.4 + i * 0.16);
      tl.fromTo(S + "d11", { opacity: 0, x: 400 }, { opacity: 1, x: 0, duration: 0.4, ease: "back.out(1.8)" }, C.add + 0.2);
      tl.to(S + "m-armR", { rotation: -120, duration: 0.25 }, C.add);
      tl.to(S + "m-armR", { rotation: 62, duration: 0.25 }, C.add + 1.0);
      // rest day: he closes his eyes
      tl.set(S + "m-lids", { opacity: 1 }, C.rest + 0.2);
      tl.fromTo(S + "zz", { opacity: 0, y: 0 }, { opacity: 1, y: -40, duration: 0.8 }, C.rest + 0.3);
"""
scene(sid, w, js, cards, extra_css=CSS)
