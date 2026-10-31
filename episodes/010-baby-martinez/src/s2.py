import sys; sys.path.insert(0, __file__.rsplit("/episodes/", 1)[0] + "/tools")  # noqa: E702
from scene import *  # noqa: F403
from pitch import *  # noqa: E402,F403
sid = "s2-lisandro"
D = TIMING[sid]["duration"]
cardsvg = (f'<g transform="translate(925,{GY - 330})"><g id="{sid}-yc" opacity="0"><rect x="-22" y="-34" width="44" height="64" rx="6" fill="#ffd23f" stroke="#1a1a2e" stroke-width="4" /></g>'
           f'<g id="{sid}-rc" opacity="0"><rect x="-22" y="-34" width="44" height="64" rx="6" fill="#e0412f" stroke="#1a1a2e" stroke-width="4" /></g></g>')
spot = f'<g id="{sid}-spot" opacity="0"><ellipse cx="540" cy="{GY + 40}" rx="26" ry="10" fill="#fff" /></g>'
w = pitch(sid) + spot + martinez(sid, 380) + opp(sid, 590) + ref(sid, 1300) + cardsvg
cards = (banner(sid, "b", "THE DEFENDER", "Lisandro Martínez", 40, 330)
         + card(sid, "nk", "NICKNAME", "The Butcher", 40, 380, "red")
         + card(sid, "td", "TODAY", "At Chelsea", 560, 380)
         + card(sid, "pn", "RESULT", "Penalty", 40, 380, "red"))
js = JS + """
      fly("b", 0.05, C.nick - 0.1, { from: "top" });
      fly("nk", C.nick, C.today - 0.1);
      fly("td", C.today, C.pen - 0.1, { from: "right" });
      look("li", 6, -2, C.today);
      // an arm in an opponent's face: the opponent's head snaps back, he goes down
      tl.to(S + "li-armR", { rotation: -125, duration: 0.15, ease: "power3.out" }, C.arm + 0.1);
      tl.to(S + "liw", { x: 40, duration: 0.15 }, C.arm + 0.1);
      tl.to(S + "op-head", { rotation: 25, duration: 0.12 }, C.arm + 0.22);
      face("op", "m-o", C.arm + 0.22);
      tl.to(S + "opw", { rotation: 70, transformOrigin: "50% 100%", x: 80, duration: 0.4, ease: "power2.in" }, C.arm + 0.35);
      tl.to(S + "li-armR", { rotation: 0, duration: 0.3 }, C.arm + 0.6);
      // second yellow ... red
      tl.to(S + "rfw", { x: -400, duration: 0.6, ease: "power2.out" }, C.card - 0.7);
      tl.to(S + "rf-armR", { rotation: -165, duration: 0.15 }, C.card - 0.05);
      tl.set(S + "yc", { opacity: 1 }, C.card); tl.set(S + "yc", { opacity: 0 }, C.card + 0.55); tl.set(S + "rc", { opacity: 1 }, C.card + 0.55);
      face("li", "m-o", C.card + 0.1);
      // penalty
      tl.fromTo(S + "spot", { opacity: 0 }, { opacity: 1, duration: 0.1, yoyo: true, repeat: 5 }, C.pen);
      fly("pn", C.pen, null);
      tl.to(S + "liw", { x: -700, duration: 0.9, ease: "power1.in" }, C.pen + 0.3);
"""
scene(sid, w, js, cards, extra_css=CSS)
