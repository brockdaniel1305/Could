import sys; sys.path.insert(0, __file__.rsplit("/episodes/", 1)[0] + "/tools")  # noqa: E702
from scene import *  # noqa: F403
from battle import *  # noqa: E402,F403
import json
sid = "s2-rome"
D = TIMING[sid]["duration"]
front = ["r1", "r2", "r3", "r4"]
w = (field(sid) + army_defs(sid) + f'<g id="{sid}-pan">' + army(sid, 120, cols=9, rows=5, dx=118)
     + "".join(roman(sid, r, 160 + i * 250, s=0.95) for i, r in enumerate(front)) + "</g>"
     + ball(sid, -80))
cards = (banner(sid, "b", "IN THE RED CORNER", "The Roman Empire", 40, 330)
         + card(sid, "mp", "THE EMPIRE, AD 117", map_empire(sid), 40, 330)
         + card(sid, "ar", "SOLDIERS", counter(sid, "n"), 560, 560, "red")
         + card(sid, "kit", "EQUIPMENT", '<span id="s2-rome-kitv">Shields</span>', 40, 380)
         + card(sid, "ce", "PRACTICE", "Centuries", 560, 560, "gold")
         + card(sid, "cq", "CONQUERED", "Britain → Egypt", 40, 380)
         + card(sid, "fb", "DEFENDED A FOOTBALL", "Never", 520, 560, "red")
         + scorebug(sid, 0, 0))
js = JS + f"""
      const front = {json.dumps(front)};
""" + """
      // slow camera pan along the legion
      tl.fromTo(S + "pan", { x: 0 }, { x: -110, duration: D, ease: "sine.inOut" }, 0);
      fly("b", C.name, C.area - 0.1);
      // the empire grows out of Rome
      fly("mp", C.area, C.army + 0.6);
      tl.fromTo(S + "mapclip", { attr: { r: 0 } }, { attr: { r: 520 }, duration: 2.2, ease: "power1.inOut" }, C.area + 0.4);
      fly("ar", C.army, C.cent - 0.1, { from: "right" });
      count("n", 0, 380000, C.army + 0.2, 1.6);
      // shields - armour - swords: all in sync
      fly("kit", C.sh, C.cent - 0.1);
      label("kitv", [[0, "Shields"], [C.ar, "Armour"], [C.sw, "Swords"]]);
      front.forEach((r) => stompR(r, C.sh + 0.05));
      front.forEach((r) => tl.fromTo(S + r + "p-shield", { x: 0 }, { x: 10, duration: 0.1, yoyo: true, repeat: 1 }, C.ar));
      front.forEach((r) => tl.fromTo(S + r + "p-body", { filter: "brightness(1)" }, { filter: "brightness(1.35)", duration: 0.12, yoyo: true, repeat: 1 }, C.ar));
      front.forEach((r) => { tl.to(S + r + "p-armR", { rotation: -165, duration: 0.18, ease: "back.out(2)" }, C.sw); tl.to(S + r + "p-armR", { rotation: 0, duration: 0.3 }, C.cent + 0.2); });
      front.forEach((r) => stompR(r, C.sw + 0.05));
      fly("ce", C.cent, C.conq - 0.1, { from: "right" });
      fly("cq", C.conq, C.ball - 0.1);
      // ... nobody ever asked them to defend a football: it rolls in, r2 looks down, prods it with his sword, it rolls away
      fly("fb", C.ball + 0.2, null, { from: "right" });
      tl.fromTo(S + "ball", { x: 0 }, { x: 460, duration: 0.8, ease: "power2.out" }, C.ball + 0.1);
      tl.fromTo(S + "ball-spin", { rotation: 0 }, { rotation: 540, duration: 0.8, ease: "power2.out", transformOrigin: "50% 50%" }, C.ball + 0.1);
      look("r2p", -4, 6, C.ball + 0.6);
      tl.to(S + "r2p-head", { rotation: -10, duration: 0.25 }, C.ball + 0.6);
      tl.to(S + "r2p-armR", { rotation: 55, duration: 0.2, ease: "power2.in" }, C.ball + 0.8);
      tl.to(S + "r2p-armR", { rotation: 0, duration: 0.3 }, C.ball + 1.1);
      tl.to(S + "ball", { x: -140, duration: 1.1, ease: "power2.out" }, C.ball + 1.0);
      tl.to(S + "ball-spin", { rotation: -200, duration: 1.1, ease: "power2.out" }, C.ball + 1.0);
      tl.to(S + "ball", { y: -50, duration: 0.2, yoyo: true, repeat: 1, ease: "power1.out" }, C.ball + 1.9);
      tl.to([S + "r2p-browL", S + "r2p-browR"], { y: -6, duration: 0.2 }, C.ball + 1.4);
      face("r2p", "m-o", C.ball + 1.4);
"""
scene(sid, w, js, cards, extra_css=CSS)
