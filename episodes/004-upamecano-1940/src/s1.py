import sys; sys.path.insert(0, __file__.rsplit('/episodes/', 1)[0] + '/tools')  # noqa: E702
from scene import *  # noqa: F403
from field import forest, board, defender, tank, GY  # noqa: E402
sid = "s1-hook"
D = TIMING[sid]["duration"]
w = forest(sid) + defender(sid, 270) + tank(sid, "k1", 800) + tank(sid, "k2", 1080, 0.8, GY - 40) + board(sid)
cards = (banner(sid, "q", "CASE FILE 004", "Could Dayot Upamecano<br>have stopped Hitler<br>from conquering France?", 40, 320)
         + card(sid, "m", "METHOD", "Scientific", 500, 420)
         + card(sid, "s", "SOURCES", "Mostly highlights", 330, 600, "gold"))
js = """
      // v3: opening punch-in (new first frame)
      tl.fromTo(S + "svg", { scale: 1.14 }, { scale: 1, transformOrigin: "50% 60%", duration: 0.8, ease: "power2.out" }, 0);
      tl.fromTo(S + "c-q", { opacity: 1, x: 0, y: 0, rotation: -2 }, { y: -1100, rotation: 8, duration: 0.4, ease: "power3.in" }, C.sci - 0.45);
      fly("m", C.sci, null, { from: "right" });
      fly("s", C.long, null, { from: "right" });
      ["k1", "k2"].forEach((k, i) => tl.fromTo(S + k + "t-body", { y: 0 }, { y: -3, duration: 0.12 + i * 0.03, repeat: R(D, 0.12 + i * 0.03), yoyo: true }, 0));
      tl.fromTo([S + "u-armL"], { rotation: 25 }, { rotation: 35, duration: 0.5, ease: "sine.inOut", repeat: R(D, 0.5), yoyo: true }, 0);
      tl.fromTo([S + "u-armR"], { rotation: -25 }, { rotation: -35, duration: 0.55, ease: "sine.inOut", repeat: R(D, 0.55), yoyo: true }, 0);
      blink(S + "u-lids", 1.5); blink(S + "u-lids", 5.2);
      tl.to([S + "u-pupL", S + "u-pupR"], { x: 6, duration: 0.3 }, C.ev);
      swap(S + "k1t-smirk", S + "k1t-grin", C.sci + 0.2);
      tl.to([S + "k1t-browL", S + "k1t-browR"], { y: -6, duration: 0.2 }, C.sci + 0.2);
"""
scene(sid, w, js, cards, extra_css=".banner .bt { font-size: 74px; }")
