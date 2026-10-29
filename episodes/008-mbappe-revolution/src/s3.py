import sys; sys.path.insert(0, __file__.rsplit("/episodes/", 1)[0] + "/tools")  # noqa: E702
from scene import *  # noqa: F403
from rev import *  # noqa: E402,F403
sid = "s3-mbappe"
D = TIMING[sid]["duration"]
streaks = "".join(f'<path d="M{x},{y} L{x + 260},{y}" stroke="#fff" stroke-width="10" stroke-linecap="round" />' for x, y in ((80, 980), (300, 1060), (120, 1120), (500, 1010)))
w = (part("paris-street", sid + "-ps")
     + f'<g transform="translate(580,{GY})"><g id="{sid}-tro"><g transform="scale(1.3)">{part("trophy", sid + "-tr")}</g></g></g>'
     + f'<g id="{sid}-st" opacity="0">{streaks}</g>'
     + mb(sid, 330)
     + f'<mask id="{sid}-mask"><rect width="1080" height="1920" fill="#fff" /><circle cx="330" cy="{GY - 150}" r="300" fill="#000" /></mask>'
     + f'<rect id="{sid}-dim" width="1080" height="1920" fill="#000" opacity="0" mask="url(#{sid}-mask)" />'
    )
cards = (banner(sid, "b", "THE CANDIDATE", "Kylian Mbappé", 40, 330)
         + card(sid, "wc", "WORLD CHAMPION", "At 19 · 2018", 560, 380, "gold")
         + card(sid, "sp", "TOP SPEED", counter(sid, "kmh", "0 km/h"), 40, 380, "red")
         + card(sid, "ce", "CELEBRATION", "Arms crossed", 560, 380)
         + card(sid, "de", "DECIDED", "Already", 40, 560, "gold")
         + calendar(sid, "14", "JULY", "1789"))
js = JS + """
      tl.fromTo(S + "dim", { opacity: 0 }, { opacity: 0.5, duration: 0.4 }, C.name - 0.3);
      fly("b", C.name, C.wc - 0.1);
      // World Cup at 19
      pop(S + "tro", C.wc);
      fly("wc", C.wc + 0.1, C.spd - 0.1, { from: "right" });
      // 38 km/h: one sprint out to the right and back in from the left
      tl.to(S + "dim", { opacity: 0, duration: 0.3 }, C.spd);
      tl.to(S + "tro", { opacity: 0, duration: 0.2 }, C.spd);
      fly("sp", C.spd, C.cel - 0.1);
      count("kmh", 0, 38, C.spd + 0.3, 0.9, "power2.out", " km/h");
      run(C.spd + 0.3, C.spd + 1.6);
      tl.to(S + "mw", { x: 900, duration: 0.5, ease: "power2.in" }, C.spd + 0.35);
      tl.set(S + "mw", { x: -700 }, C.spd + 0.86);
      tl.to(S + "mw", { x: 0, duration: 0.6, ease: "power2.out" }, C.spd + 0.9);
      tl.fromTo(S + "st", { opacity: 0, x: 0 }, { opacity: 1, x: 200, duration: 0.25, yoyo: true, repeat: 3 }, C.spd + 0.35);
      tl.fromTo(S + "ps-houses", { x: 0 }, { x: 6, duration: 0.05, yoyo: true, repeat: 9 }, C.spd + 0.5);
      // arms crossed, like a man who has already decided
      cross(C.cel + 0.3);
      fly("ce", C.cel, null, { from: "right" });
      fly("de", C.dec, null);
      tl.to(S + "m-head", { rotation: -8, duration: 0.3 }, C.dec + 0.6);
      tl.to([S + "m-browL", S + "m-browR"], { y: -5, duration: 0.2 }, C.dec + 0.6);
      look("m", 4, -3, C.dec + 0.6);
"""
scene(sid, w, js, cards, extra_css=CSS)
