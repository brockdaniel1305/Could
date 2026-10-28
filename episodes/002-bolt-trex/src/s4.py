import sys; sys.path.insert(0, __file__.rsplit('/episodes/', 1)[0] + '/tools')  # noqa: E702
from scene import *  # noqa: F403
from race import course, driver, tracker, PX  # noqa: E402
sid = "s4-start"
D = TIMING[sid]["duration"]
T = TIMING[sid]["cues"]
world = f"""
{part("track-day", sid + "-track")}
{course(sid)}
{tracker(sid)}
<g transform="translate(830,520) scale(1.3)">{part("burst", sid + "-bang", WORD="BANG!")}</g>
<g transform="translate(720,640) scale(1.1)">{part("burst", sid + "-roar", WORD="ROAR")}</g>
"""
clock = '<span id="s4-start-clock">0.00 s</span>'
cards = (banner(sid, "b", "0–30 M", "The Start", 60, 330)
         + card(sid, "clk", "RACE CLOCK · SLOW-MO", clock, 560, 330)
         + card(sid, "re", "REACTION, BOLT", "0.146 s", 60, 520, "gold")
         + card(sid, "hs", "HEAD START, T-REX", "+12 m (nose first)", 60, 520)
         + card(sid, "ld", "LEADER", "T-REX", 60, 520, "red"))
keys = [[0, 0], [T["gun"], 0], [T["react"], 0.146], [T["roar"], 1.0], [D, 3.0]]
js = driver(keys, [[0, 5.5], [T["react"], "mid"]]) + """
      fly("b", C.t, C.react - 0.1);
      fly("clk", C.gun - 0.6, null, { from: "right" });
      fly("re", C.react, C.rex - 0.1);
      fly("hs", C.lead, C.ahead - 0.1);
      fly("ld", C.ahead, null, { from: "top" });
      // set ... BANG
      tl.fromTo(S + "bang", { scale: 0, opacity: 0, transformOrigin: "50% 50%" }, { scale: 1, opacity: 1, duration: 0.2, ease: "back.out(3)" }, C.gun);
      tl.to(S + "bang", { opacity: 0, duration: 0.2 }, C.gun + 0.8);
      tl.to(S + "b-armL", { rotation: 30, duration: 0.3 }, 0.6);
      tl.to(S + "b-armR", { rotation: -30, duration: 0.3 }, 0.6);
      swap(S + "b-m-smile", S + "b-m-flat", C.t);
      // the T-Rex takes the pistol personally: head turns, ROAR
      tl.to(S + "r-pup", { x: 6, y: -4, duration: 0.2 }, C.gun + 0.1);
      tl.to(S + "r-brow", { rotation: 14, svgOrigin: "74 -43", duration: 0.2 }, C.rex + 0.6);
      tl.to(S + "r-jaw", { rotation: 32, svgOrigin: "0 18", duration: 0.3, ease: "power2.out" }, C.roar);
      tl.to(S + "r-jaw", { rotation: 0, svgOrigin: "0 18", duration: 0.25 }, C.roar + 1.3);
      tl.fromTo(S + "roar", { scale: 0, opacity: 0, transformOrigin: "50% 50%" }, { scale: 1, opacity: 1, duration: 0.25, ease: "back.out(3)" }, C.roar + 0.1);
      tl.to(S + "roar", { opacity: 0, duration: 0.2 }, C.roar + 1.3);
      // Bolt notices he is behind
      tl.to([S + "b-pupL", S + "b-pupR"], { x: 6, duration: 0.25 }, C.ahead);
      swap(S + "b-m-flat", S + "b-m-o", C.ahead + 0.1);
"""
scene(sid, world, js, cards)
