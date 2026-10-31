import sys; sys.path.insert(0, __file__.rsplit("/episodes/", 1)[0] + "/tools")  # noqa: E702
from scene import *  # noqa: F403
from ocean import *  # noqa: E402,F403
sid = "s3-atlantis"
D = TIMING[sid]["duration"]
w = surface(sid) + kdb(sid, 300) + plato(sid, 110)
cards = (banner(sid, "b", "THE TARGET", "Atlantis", 40, 330)
         + card(sid, "ls", "LAST SEEN", "~360 BC (Plato)", 520, 560)
         + card(sid, "vs", "VISIBLE", "Not at all", 40, 380, "red"))
js = JS + """
      tl.fromTo(S + "waves", { x: 0 }, { x: -120, duration: D, ease: "none" }, 0);
      fly("b", 0.05, C.see - 0.1, { from: "top" });
      // Plato pops up and shrugs
      tl.fromTo(S + "pl", { y: 260, opacity: 0 }, { y: 0, opacity: 1, duration: 0.4, ease: "back.out(1.8)" }, C.lost - 0.2);
      fly("ls", C.lost + 0.1, null, { from: "right" });
      tl.to(S + "plL", { rotation: 120, duration: 0.2, yoyo: true, repeat: 1 }, C.see + 0.2);
      tl.to(S + "plR", { rotation: -120, duration: 0.2, yoyo: true, repeat: 1 }, C.see + 0.2);
      fly("vs", C.see, null);
      look("m", 8, 2, C.see);
"""
scene(sid, w, js, cards, extra_css=CSS)
