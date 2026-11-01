import sys; sys.path.insert(0, __file__.rsplit("/episodes/", 1)[0] + "/tools")  # noqa: E702
from scene import *  # noqa: F403
from battle import *  # noqa: E402,F403
from cold import *  # noqa: E402,F403
sid = "s3-messi"
D = TIMING[sid]["duration"]
shots = "".join(ball(sid, 380, GY - 18, 0.7, f"sh{i}") for i in range(7))
w = (field(sid) + f'<g transform="translate(940,{GY})"><g transform="scale(0.85)">{part("goal", sid + "-gl")}</g></g>' + shots
     + messi(sid, 330, s=0.81) + ball(sid, 380, GY - 18, 0.7)
     + f'<mask id="{sid}-mask"><rect width="1080" height="1920" fill="#fff" /><circle cx="330" cy="{GY - 140}" r="290" fill="#000" /></mask>'
     + f'<rect id="{sid}-dim" width="1080" height="1920" fill="#000" opacity="0" mask="url(#{sid}-mask)" />')
cards = (banner(sid, "b", "IN THE BLUE CORNER", "Prime Messi", 40, 330)
         + card(sid, "g", "GOALS IN 2012", counter(sid, "gn"), 40, 380, "gold")
         + card(sid, "wr", "WORLD RECORD", "Guinness", 560, 560, "red"))
js = JS + """
      tl.fromTo(S + "dim", { opacity: 0 }, { opacity: 0.5, duration: 0.3 }, 0);
      fly("b", 0.05, C.g - 0.1, { from: "top" });
      fly("g", C.g, null);
      count("gn", 0, 91, C.g + 0.1, C.wr - C.g + 0.4, "power1.in");
      [0, 0.4, 0.75, 1.05, 1.3, 1.5, 1.68].forEach((s, i) => {
        const t0 = C.g + s;
        tl.set(S + "sh" + i, { opacity: 0 }, 0);
        kickR(t0);
        tl.set(S + "sh" + i, { opacity: 1 }, t0);
        arc(S + "sh" + i, t0, 0.4, 600, -60, 120, S + "sh" + i + "-spin");
        tl.set(S + "sh" + i, { opacity: 0 }, t0 + 0.45);
      });
      fly("wr", C.wr, null, { from: "right" });
"""
scene(sid, w, js, cards, extra_css=CSS)
