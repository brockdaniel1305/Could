import sys; sys.path.insert(0, __file__.rsplit("/episodes/", 1)[0] + "/tools")  # noqa: E702
from scene import *  # noqa: F403
from battle import *  # noqa: E402,F403
from cold import *  # noqa: E402,F403
import json
sid = "s2-rome"
D = TIMING[sid]["duration"]
front = ["r1", "r2", "r3", "r4"]
w = (field(sid) + army_defs(sid) + f'<g id="{sid}-pan">' + army(sid, 120, cols=9, rows=5, dx=118)
     + "".join(roman(sid, r, 160 + i * 250, s=0.95) for i, r in enumerate(front)) + "</g>")
cards = (banner(sid, "b", "IN THE RED CORNER", "The Roman Empire", 40, 330)
         + card(sid, "ar", "SOLDIERS", counter(sid, "n"), 40, 380, "red")
         + card(sid, "kit", "EQUIPMENT", '<span id="s2-rome-kitv">Shields</span>', 560, 560))
js = JS + f"""
      const front = {json.dumps(front)};
""" + """
      tl.fromTo(S + "pan", { x: 0 }, { x: -110, duration: D, ease: "sine.inOut" }, 0);
      fly("b", 0.05, C.army - 0.1, { from: "top" });
      fly("ar", C.army, null);
      count("n", 0, 380000, C.army + 0.1, 1.2);
      fly("kit", C.sh, null, { from: "right" });
      label("kitv", [[0, "Shields"], [C.ar, "Armour"], [C.sw, "Swords"]]);
      front.forEach((r) => stompR(r, C.sh + 0.05));
      front.forEach((r) => tl.fromTo(S + r + "p-shield", { x: 0 }, { x: 10, duration: 0.1, yoyo: true, repeat: 1 }, C.ar));
      front.forEach((r) => tl.to(S + r + "p-armR", { rotation: -165, duration: 0.18, ease: "back.out(2)" }, C.sw));
      front.forEach((r) => stompR(r, C.sw + 0.05));
"""
scene(sid, w, js, cards, extra_css=CSS)
