import sys; sys.path.insert(0, __file__.rsplit('/episodes/', 1)[0] + '/tools')  # noqa: E702
from scene import *  # noqa: F403
from arena import arena, gauge, haaland, fighter, MEDITATE_JS, GY  # noqa: E402
sid = "s3-arena"
D = TIMING[sid]["duration"]
w = (arena(sid) + fighter(sid, "murmillo", "mur", 640) + fighter(sid, "retiarius", "ret", 880, 0.95) + haaland(sid, 220) + gauge(sid)
     + f'<g transform="translate(880,830)"><g id="{sid}-bowl"><path d="M-60,0 Q0,70 60,0 Z" fill="#8a5a24" stroke="#1a1a2e" stroke-width="6" /><ellipse cx="0" cy="0" rx="60" ry="14" fill="#e8d7b5" stroke="#1a1a2e" stroke-width="5" /></g></g>')
cards = (banner(sid, "b", "IN THE BLUE CORNER", "The Colosseum", 60, 330)
         + card(sid, "cap", "SPECTATORS", "~50,000", 560, 520, "gold")
         + card(sid, "op", "OPPONENTS", "Swords, nets, tridents", 120, 380)
         + card(sid, "nb", "GLADIATOR NICKNAME", "Barley men", 120, 380, "gold")
         + card(sid, "vg", "DIET", "Mostly vegetarian", 120, 560))
js = MEDITATE_JS + """
      fly("b", C.name, C.opp - 0.1);
      fly("cap", C.cap, C.opp - 0.1, { from: "right" });
      tl.fromTo(S + "col-crowd", { y: 0 }, { y: -12, duration: 0.25, ease: "sine.inOut", repeat: R(D - C.cap, 0.25), yoyo: true }, C.cap);
      needle(60, C.cap + 0.2);
      // the opponents walk in
      tl.fromTo([S + "mur", S + "ret"], { x: 500 }, { x: 0, duration: 1.2, ease: "power2.out", stagger: 0.2 }, C.opp - 0.2);
      fly("op", C.opp + 0.3, C.barley - 0.1);
      fly("nb", C.barley, C.veg - 0.1);
      fly("vg", C.veg, null);
      pop(S + "bowl", C.veg + 0.2);
      // Haaland (heart & liver) is visibly shaken
      tl.to([S + "h-pupL", S + "h-pupR"], { x: 7, duration: 0.25 }, C.veg + 0.3);
      swap(S + "h-m-smile", S + "h-m-o", C.veg + 0.4);
      blink(S + "h-lids", 1.8);
"""
scene(sid, w, js, cards)
