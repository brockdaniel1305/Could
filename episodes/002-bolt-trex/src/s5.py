import sys; sys.path.insert(0, __file__.rsplit('/episodes/', 1)[0] + '/tools')  # noqa: E702
from scene import *  # noqa: F403
from race import course, driver, tracker, PX  # noqa: E402
sid = "s5-speed"
D = TIMING[sid]["duration"]
T = TIMING[sid]["cues"]
world = f"""
{part("track-day", sid + "-track")}
{course(sid, start_blocks=False)}
{tracker(sid)}
<g id="{sid}-lines" stroke="#f4efe6" stroke-width="7" stroke-linecap="round" opacity="0"><path d="M60,960 L240,960 M30,1020 L220,1020 M90,1080 L230,1080" /></g>
"""
clock = '<span id="s5-speed-clock">3.00 s</span>'
cards = (banner(sid, "b", "30–80 M", "Top Speed", 60, 330)
         + card(sid, "clk", "RACE CLOCK · SLOW-MO", clock, 560, 330)
         + card(sid, "vb", "TOP SPEED, BOLT", "44.7 km/h", 60, 520, "gold")
         + card(sid, "vr", "TOP SPEED, T-REX (EST.)", "~19 km/h", 60, 520)
         + card(sid, "ps", "LEAD CHANGE", "~35 m", 60, 520, "red")
         + card(sid, "dc", "DECISION", "Correct ✓", 60, 520, "gold"))
keys = [[0, 3.0], [T["pass"], 4.17], [T["look"], 5.4], [D, 7.9]]
js = driver(keys, [[0, "mid"], [T["pass"] + 0.5, "bolt"]]) + """
      fly("b", C.t, C.bolt + 1.6);
      fly("clk", 0.1, null, { from: "right" });
      fly("vb", C.bolt + 0.4, C.rex - 0.1);
      fly("vr", C.rex, C.pass - 0.1);
      fly("ps", C.pass, C.look - 0.1, { from: "top" });
      fly("dc", C.wise, null);
      swap(S + "b-m-smile", S + "b-m-flat", 0);
      tl.to(S + "r-brow", { rotation: 14, svgOrigin: "74 -43", duration: 0.2 }, 0);
      tl.fromTo(S + "lines", { opacity: 0 }, { opacity: 0.8, duration: 0.2 }, C.bolt);
      tl.fromTo(S + "lines", { x: 0 }, { x: -60, duration: 0.25, ease: "none", repeat: R(D - C.bolt, 0.25) }, C.bolt);
      // the overtake: the T-Rex snaps at nothing
      tl.fromTo(S + "r-jaw", { rotation: 0, svgOrigin: "0 18" }, { rotation: 26, duration: 0.25, ease: "power2.out", repeat: 5, yoyo: true }, C.pass + 0.4);
      swap(S + "b-m-flat", S + "b-m-smile", C.pass + 0.6);
      // he does not look back (eyes forward, chin up)
      tl.to([S + "b-pupL", S + "b-pupR"], { x: 7, duration: 0.2 }, C.look);
      tl.to(S + "b-browL", { y: -5, duration: 0.2 }, C.look + 0.2);
"""
scene(sid, world, js, cards)
