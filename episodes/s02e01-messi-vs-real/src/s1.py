import sys; sys.path.insert(0, __file__.rsplit("/episodes/", 1)[0] + "/tools")  # noqa: E702
from scene import *  # noqa: F403
from match import *  # noqa: E402,F403
sid = "s1-slam"
D = TIMING[sid]["duration"]
wide = (f'<g id="{sid}-wide" opacity="0">' + world(sid + "-w", lineup(sid, FEET, 0.5) + messi_fig(sid, 540, FEET + 160, 0.72, name="m")) + "</g>")
w = closeup(sid) + wide
cards = slam(sid, "s1", "PRIME<br>MESSI", 430, 150) + slam(sid, "s2", "VS 11<br>REAL MADRID", 430, 118, "#f4f4f2")
js = JS + CLOSE_JS + """
      juggle("cu", 0, 0.85);
      // frame 0: the first slam is already there (pulses in)
      tl.fromTo(S + "s1", { opacity: 1, scale: 1.12, rotation: -3, transformOrigin: "50% 50%" }, { scale: 1, duration: 0.25, ease: "back.out(3)" }, 0);
      tl.set(S + "s1", { opacity: 0 }, 0.85);
      // hard cut to the line-up: 11 white shirts, Messi alone in front
      tl.set(S + "cu", { opacity: 0 }, 0.85); tl.set(S + "wide", { opacity: 1 }, 0.85);
      slamIn("s2", 0.85, null);
      flashes(0, D);
      for (let j = 0; j < 24; j++) tl.fromTo(S + "w-fc" + j, { y: 0 }, { y: -6, duration: 0.3, yoyo: true, repeat: R(D, 0.3) }, (j % 5) * 0.06);
      tl.fromTo(S + "w-zoom", { scale: 1.08, svgOrigin: "540 1200" }, { scale: 1, duration: 2.0, ease: "power2.out" }, 0.85);
"""
scene(sid, w, js, cards, extra_css=CSS)
