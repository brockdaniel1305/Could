import sys; sys.path.insert(0, __file__.rsplit('/episodes/', 1)[0] + '/tools')  # noqa: E702
from scene import *  # noqa: F403
from arena import arena, haaland, fighter, MEDITATE_JS, GY  # noqa: E402
sid = "s8-outro"
D = TIMING[sid]["duration"]
w = (arena(sid) + fighter(sid, "murmillo", "mur", 900, 0.9) + haaland(sid, 300)
     + f'<g transform="translate(0,{GY})"><g transform="translate(640,0) scale(0.85)">{part("lion", sid + "-l")}</g></g>')
cards = (banner(sid, "b", "NEXT CASE", "Could you imagine<br>another scenario?", 50, 330)
         + card(sid, "c", "WRITE IT IN THE COMMENTS", "↓ ↓ ↓", 330, 640, "gold"))
js = MEDITATE_JS + """
      fly("b", 0.05, null, { from: "top" });
      fly("c", C.c, null, { from: "right" });
      tl.set(S + "l-stand", { opacity: 0 }, 0); tl.set(S + "l-sit", { opacity: 1 }, 0);
      tl.fromTo(S + "h-armR", { rotation: -150 }, { rotation: -115, duration: 0.3, ease: "sine.inOut", repeat: R(D, 0.3), yoyo: true }, 0);
      tl.fromTo(S + "col-crowd", { y: 0 }, { y: -10, duration: 0.25, ease: "sine.inOut", repeat: R(D, 0.25), yoyo: true }, 0);
      cheer(0.2);
"""
scene(sid, w, js, cards)
