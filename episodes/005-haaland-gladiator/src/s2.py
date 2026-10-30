import sys; sys.path.insert(0, __file__.rsplit('/episodes/', 1)[0] + '/tools')  # noqa: E702
from scene import *  # noqa: F403
from arena import arena, haaland, fighter, MEDITATE_JS, GY  # noqa: E402
sid = "s2-haaland"
D = TIMING[sid]["duration"]
w = (arena(sid) + haaland(sid, 300, 1.3)
     + f'<mask id="{sid}-mask"><rect x="0" y="0" width="1080" height="1920" fill="#fff" /><circle cx="300" cy="960" r="320" fill="#000" /></mask>'
     + f'<rect id="{sid}-spot" x="0" y="0" width="1080" height="1920" fill="#000" opacity="0" mask="url(#{sid}-mask)" />'
     + f'<g transform="translate(470,860)"><g id="{sid}-food"><path d="M0,-40 C-50,-80 -90,-10 0,40 C90,-10 50,-80 0,-40 Z" fill="#b8352a" stroke="#1a1a2e" stroke-width="6" /><ellipse cx="80" cy="30" rx="44" ry="22" fill="#8a3a2a" stroke="#1a1a2e" stroke-width="5" /></g></g>')
cards = (banner(sid, "b", "IN THE RED CORNER", "Erling Haaland", 60, 330)
         + card(sid, "h", "HEIGHT", "1.94 m", 560, 520)
         + card(sid, "sp", "TOP SPEED", "~36 km/h", 560, 520)
         + card(sid, "g", "PREMIER LEAGUE GOALS, ONE SEASON", "36", 300, 380, "gold")
         + card(sid, "di", "DIET", "Cow heart & liver", 480, 380, "red")
         + card(sid, "z", "THEN", "Meditates", 560, 560))
js = MEDITATE_JS + """
      tl.fromTo(S + "spot", { opacity: 0 }, { opacity: 0.6, duration: 0.4 }, C.name - 0.2);
      fly("b", C.name, C.goals - 0.1);
      fly("h", C.h, C.sp - 0.1, { from: "right" });
      fly("sp", C.sp, C.goals - 0.1, { from: "right" });
      fly("g", C.goals, C.diet - 0.1, { from: "right" });
      fly("di", C.diet, C.zen - 0.1, { from: "right" });
      fly("z", C.zen, null, { from: "right" });
      cheer(C.goals + 0.3);
      // the goal celebration arms, then the snack
      tl.to(S + "h-armL", { rotation: 160, duration: 0.3, ease: "back.out(2)" }, C.goals + 0.4);
      tl.to(S + "h-armR", { rotation: -160, duration: 0.3, ease: "back.out(2)" }, C.goals + 0.45);
      tl.to([S + "h-armL", S + "h-armR"], { rotation: 0, duration: 0.3 }, C.diet - 0.1);
      pop(S + "food", C.diet + 0.3);
      tl.to(S + "food", { opacity: 0, duration: 0.2 }, C.zen);
      swap(S + "h-m-smile", S + "h-m-o", C.diet + 0.6); swap(S + "h-m-o", S + "h-m-smile", C.diet + 1.4);
      blink(S + "h-lids", 2.0); blink(S + "h-lids", 7.5);
      meditate(C.zen + 0.2, 1.3);
"""
scene(sid, w, js, cards)
