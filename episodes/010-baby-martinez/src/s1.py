import sys; sys.path.insert(0, __file__.rsplit("/episodes/", 1)[0] + "/tools")  # noqa: E702
from scene import *  # noqa: F403
from pitch import *  # noqa: E402,F403
sid = "s1-hook"
D = TIMING[sid]["duration"]
w = pitch(sid) + martinez(sid, 360) + baby(sid, 640, 0.4)
cards = banner(sid, "q", "CASE FILE 010", "Could a baby<br>replace Lisandro<br>Martínez?", 40, 300)
js = JS + """
      tl.fromTo(S + "c-q", { opacity: 1, x: 0, y: 0, rotation: -2 }, { opacity: 1, duration: 0.01 }, 0);
      look("li", 7, 0, 0.6); look("b", -6, 0, 0.9);
      tl.fromTo(S + "bw", { y: 0 }, { y: -10, duration: 0.25, yoyo: true, repeat: R(D, 0.25), ease: "sine.inOut" }, 0);
"""
scene(sid, w, js, cards, extra_css=".banner .bt { font-size: 76px; }" + CSS, loop_in=True)
