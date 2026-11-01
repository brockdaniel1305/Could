import sys; sys.path.insert(0, __file__.rsplit("/episodes/", 1)[0] + "/tools")  # noqa: E702
from scene import *  # noqa: F403
from field import forest, board, defender, tank, GY  # noqa: E402
sid = "s1-hook"
D = TIMING[sid]["duration"]
w = forest(sid) + tank(sid, "k1", 800, 0.8) + tank(sid, "k2", 980, 0.7, GY - 60) + defender(sid, 300) + board(sid)
cards = banner(sid, "q", "CASE FILE 004", "Could Upamecano have<br>stopped Hitler from<br>conquering France?", 40, 300)
js = """
      tl.fromTo(S + "c-q", { opacity: 1, x: 0, y: 0, rotation: -2 }, { opacity: 1, duration: 0.01 }, 0);
      for (const k of ["k1", "k2"]) tl.fromTo(S + k + "t-body", { y: 0 }, { y: -3, duration: 0.12, repeat: R(D, 0.12), yoyo: true }, 0);
      tl.to(S + "u-armL", { rotation: -60, duration: 0.3 }, 0.8); tl.to(S + "u-armR", { rotation: 60, duration: 0.3 }, 0.85);
"""
scene(sid, w, js, cards, extra_css=".banner .bt { font-size: 64px; }", loop_in=True)
