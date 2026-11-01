import sys; sys.path.insert(0, __file__.rsplit("/episodes/", 1)[0] + "/tools")  # noqa: E702
from scene import *  # noqa: F403
from field import forest, board, defender, tank, GY  # noqa: E402
sid = "s3-army"
D = TIMING[sid]["duration"]
tanks = "".join(tank(sid, f"k{i}", 640 + i * 130, 0.62, GY - 70 + (i % 2) * 60) for i in range(5))
w = forest(sid) + f'<g id="{sid}-army">{tanks}</g>' + defender(sid, 220) + board(sid)
cards = (card(sid, "sd", "SOLDIERS", '<span id="s3-army-sn">0</span>', 40, 380, "red")
         + card(sid, "tk", "TANKS", '<span id="s3-army-tn">0</span>', 560, 380, "red")
         + card(sid, "rt", "ROUTE", "Through the Ardennes", 40, 560))
js = """
      const count = (id, b, t0, d) => { const el = document.querySelector(S + id), o = { v: 0 }; el.textContent = "0";
        tl.fromTo(o, { v: 0 }, { v: b, duration: d, ease: "power2.out", onUpdate() { el.textContent = Math.round(o.v).toLocaleString("en-US"); } }, t0); };
      for (let i = 0; i < 5; i++) tl.fromTo(S + "k" + i + "t-body", { y: 0 }, { y: -3, duration: 0.12, repeat: R(D, 0.12), yoyo: true }, 0);
      tl.fromTo(S + "army", { x: 700 }, { x: 0, duration: 2.4, ease: "power2.out" }, 0.2);
      fly("sd", C.men, C.ard - 0.1); count("sn", 3000000, C.men + 0.2, 1.0);
      fly("tk", C.tanks, C.ard - 0.1, { from: "right" }); count("tn", 2500, C.tanks + 0.2, 0.9);
      fly("rt", C.ard, null);
      tl.fromTo(S + "att", { x: 120, opacity: 0 }, { x: 0, opacity: 1, duration: 0.6 }, C.ard + 0.2);
      tl.to([S + "u-pupL", S + "u-pupR"], { x: 7, duration: 0.2 }, C.men);
"""
scene(sid, w, js, cards)
