import sys; sys.path.insert(0, __file__.rsplit("/episodes/", 1)[0] + "/tools")  # noqa: E702
from scene import *  # noqa: F403
from rev import *  # noqa: E402,F403
sid = "s4-bastille"
D = TIMING[sid]["duration"]
pris = [(140, 1200, 0.7), (270, 1210, 0.72), (400, 1200, 0.7), (530, 1215, 0.72), (210, 1330, 0.85), (390, 1340, 0.86), (570, 1330, 0.85)]
wa = (f'<g id="{sid}-A">' + part("paris-street", sid + "-ps")
      + f'<g transform="translate(800,{GY}) scale(0.72)">{part("bastille", sid + "-bs")}</g>'
      + crowd_defs(sid) + f'<g id="{sid}-crowdA">' + crowd(sid, [(1200, 0.62, 5), (1200, 0.7, 4)], x0=-60, dx=110) + "</g>"
      + mb(sid, -150) + gauge(sid) + "</g>")
wb = (f'<g id="{sid}-B" opacity="0">' + part("cell", sid + "-ce")
      + "".join(cit(sid, f"p{i}", x, y, s, cap="#7a7a72") for i, (x, y, s) in enumerate(pris))
      + mb(sid, 880, 1200, 0.85, name="d") + "</g>")
w = wa + wb
cards = (banner(sid, "b", "PLAN A", "Storm the Bastille", 40, 330)
         + card(sid, "cr", "THE CROWD", "Most of the day", 40, 380)
         + card(sid, "mb", "MBAPPÉ", "~1 minute", 560, 380, "gold")
         + card(sid, "pr", "PRISONERS", "7", 40, 380)
         + card(sid, "fa", "NEW FANS", "7", 560, 380, "gold")
         + calendar(sid, "14", "JULY", "1789"))
js = JS + """
      fly("b", C.t, C.crowd - 0.1, { from: "top" });
      needle(45, 0, 0.01);
      // the crowd plods along while the sun crosses the sky
      tl.fromTo(S + "crowdA", { x: 0 }, { x: 180, duration: C.pris - C.crowd, ease: "none" }, C.crowd);
      tl.fromTo(S + "cr", { y: 0 }, { y: -6, duration: 0.3, yoyo: true, repeat: R(C.pris, 0.3) }, 0);
      fly("cr", C.crowd, C.mb - 0.1);
      tl.fromTo(S + "ps-sun", { x: -760, y: 160 }, { x: 0, y: 0, duration: C.mb - C.crowd, ease: "sine.out" }, C.crowd);
      tl.fromTo(S + "ps-sky", { fill: "#bfe0f2" }, { fill: "#f6b77a", duration: C.mb - C.crowd }, C.crowd);
      // Mbappé overtakes everyone; the drawbridge slams down; he is first inside
      run(C.mb - 0.1, C.mb + 0.9);
      tl.to(S + "mw", { x: 950, duration: 0.95, ease: "power1.in" }, C.mb);
      tl.to(S + "bs-bridge", { rotation: -90, transformOrigin: "0% 100%", duration: 0.35, ease: "bounce.out" }, C.mb + 0.15);
      tl.to(S + "mw", { opacity: 0, duration: 0.1 }, C.mb + 0.95);
      fly("mb", C.mb + 0.1, C.pris - 0.2, { from: "right" });
      needle(60, C.mb + 0.9);
      // inside: seven prisoners; the door creaks open, he stands in the light, arms crossed
      tl.set(S + "A", { opacity: 0 }, C.pris - 0.15); tl.set(S + "B", { opacity: 1 }, C.pris - 0.15);
      tl.set(S + "d-armL", { rotation: -62 }, 0); tl.set(S + "d-armR", { rotation: 62 }, 0);
      tl.fromTo(S + "ce-door", { scaleX: 1 }, { scaleX: 0.12, transformOrigin: "100% 50%", duration: 0.6, ease: "power2.out" }, C.pris);
      tl.fromTo(S + "ce-light", { opacity: 0 }, { opacity: 0.6, duration: 0.5 }, C.pris + 0.1);
      tl.fromTo(S + "dw", { opacity: 0 }, { opacity: 1, duration: 0.2 }, C.pris + 0.3);
      [0, 1, 2, 3, 4, 5, 6].forEach((i) => {
        const p = "p" + i + "p";
        tl.set(S + p + "-fork", { opacity: 0 }, 0);
        tl.set(S + p + "-m-o", { opacity: 0 }, 0);
        tl.set(S + p + "-lids", { opacity: 1 }, 0);
        tl.set(S + p + "-head", { rotation: 14 }, 0);
        tl.set(S + p + "-lids", { opacity: 0 }, C.pris + 0.6 + i * 0.05);
        tl.to(S + p + "-head", { rotation: 0, duration: 0.3 }, C.pris + 0.6 + i * 0.05);
        look(p, 6, 0, C.pris + 0.7);
        // ... seven new fans: they jump and cheer
        tl.set(S + p + "-m-smile", { opacity: 1 }, C.fans);
        tl.to(S + p + "-armL", { rotation: 150, duration: 0.2 }, C.fans + i * 0.04);
        tl.to(S + p + "-armR", { rotation: -150, duration: 0.2 }, C.fans + i * 0.04);
        tl.fromTo(S + "p" + i, { y: 0 }, { y: -60, duration: 0.2, yoyo: true, repeat: 3, ease: "power2.out" }, C.fans + i * 0.04);
      });
      fly("pr", C.pris + 0.2, C.fans - 0.1);
      fly("fa", C.fans, null, { from: "right" });
"""
scene(sid, w, js, cards, extra_css=CSS)
