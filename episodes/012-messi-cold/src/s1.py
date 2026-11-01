import sys; sys.path.insert(0, __file__.rsplit("/episodes/", 1)[0] + "/tools")  # noqa: E702
from scene import *  # noqa: F403
from battle import *  # noqa: E402,F403
from cold import *  # noqa: E402,F403
sid = "s1-cold"
D = TIMING[sid]["duration"]
w = cold_world(sid)
cards = (title(sid) + card(sid, "dz", "DIZZY ROMANS", counter(sid, "dn", "61,000"), 40, 760, "gold")
         + f'\n    <div class="rew" id="{sid}-rew">◀◀ REWIND</div>')
js = JS + cold_js("a") + """
      // already mid-domino at frame 0: the counter races, Messi keeps dribbling
      tl.set(S + "c-dz", { opacity: 1, x: 0, y: 0, rotation: -3 }, 0);
      count("dn", 61000, 380000, 0, 2.2, "power1.out");
      const n = R(C.back, 0.15);
      tl.fromTo(S + "a-m-legL", { rotation: -26 }, { rotation: 26, duration: 0.15, yoyo: true, repeat: n, ease: "sine.inOut" }, 0);
      tl.fromTo(S + "a-m-legR", { rotation: 26 }, { rotation: -26, duration: 0.15, yoyo: true, repeat: n, ease: "sine.inOut" }, 0);
      tl.fromTo(S + "a-ball", { x: 0 }, { x: 30, duration: 0.15, yoyo: true, repeat: n }, 0);
      tl.fromTo(S + "title", { scale: 1.08, transformOrigin: "50% 50%" }, { scale: 1, duration: 0.25, ease: "back.out(3)" }, 0);
      // "Let's go back.": everything rewinds
      tl.set(S + "rew", { opacity: 1 }, C.back);
      tl.fromTo(S + "rew", { opacity: 1 }, { opacity: 0.3, duration: 0.15, yoyo: true, repeat: 5, immediateRender: false }, C.back);
      tl.set(S + "rew", { opacity: 0 }, 0);
      for (let c = 0; c < 6; c++) for (let r = 0; r < 5; r++) tl.to(S + "a" + r + "-" + c, { rotation: 0, duration: 0.5, ease: "power2.out", overwrite: false }, C.back + 0.05 + (5 - c) * 0.04);
      tl.to(S + "a-mw", { x: -260, duration: 0.6, ease: "power2.in" }, C.back + 0.1);
      tl.to(S + "title", { y: -900, duration: 0.4, ease: "power3.in" }, C.back + 0.2);
      tl.to(S + "c-dz", { x: -1200, duration: 0.4, ease: "power3.in" }, C.back + 0.2);
"""
scene(sid, w, js, cards, extra_css=CSS + TITLE_CSS)
