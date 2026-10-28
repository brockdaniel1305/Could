import sys; sys.path.insert(0, __file__.rsplit('/episodes/', 1)[0] + '/tools')  # noqa: E702
from scene import *  # noqa: F403
from race import course, driver, tracker, PX  # noqa: E402
sid = "s6-finish"
T = TIMING[sid]["cues"]
world = f"""
{part("track-day", sid + "-track")}
{course(sid, start_blocks=False)}
{tracker(sid)}
<rect id="{sid}-flash" x="0" y="0" width="1080" height="1920" fill="#fff" opacity="0" />
"""
clock = '<span id="s6-finish-clock">7.90 s</span>'
cards = (banner(sid, "b", "80–100 M", "The Finish", 60, 330)
         + card(sid, "clk", "RACE CLOCK", clock, 560, 330)
         + card(sid, "bt", "BOLT", "9.58 s", 60, 520, "gold")
         + card(sid, "rp", "T-REX AT", "64 m", 60, 520, "red")
         + card(sid, "p1", "PHOTO 1", "Bolt, 9.58 s", 60, 400)
         + card(sid, "p2", "PHOTO 2", "T-Rex, 16.3 s", 300, 600, "gold"))
keys = [[0, 7.9], [T["win"], 9.58], [T["where"], 9.58], [T["where"] + 0.01, 9.58]]
js = driver(keys, [[0, "bolt"], [T["win"] + 0.4, 101], [T["where"], "rex"]]) + """
      fly("b", 0.2, C.win - 0.1);
      fly("clk", 0.1, C.where - 0.1, { from: "right" });
      fly("bt", C.win, C.where - 0.1);
      fly("rp", C.where + 0.5, C.photo - 0.1);
      fly("p1", C.photo, null, { rot: -5 });
      fly("p2", C.photo + 0.9, null, { from: "right", rot: 4 });
      // Bolt breaks the tape, the race clock freezes
      tl.to(S + "tape", { opacity: 0, duration: 0.05 }, C.win);
      tl.fromTo(S + "flash", { opacity: 0 }, { opacity: 0.7, duration: 0.05, yoyo: true, repeat: 1 }, C.win);
      tl.set([S + "b-legL", S + "b-legR", S + "b-armL", S + "b-armR"], { rotation: 0 }, C.win + 0.6);
      tl.set(S + "b-body", { rotation: 0 }, C.win + 0.6);
      tl.to(S + "b-armR", { rotation: -160, duration: 0.3, ease: "back.out(2)" }, C.win + 0.7);
      tl.to(S + "b-armL", { rotation: 160, duration: 0.3, ease: "back.out(2)" }, C.win + 0.8);
      swap(S + "b-m-flat", S + "b-m-smile", C.win + 0.7);
      // freeze frame back at 64 m: the T-Rex tries a dip finish with no arms
      tl.fromTo(S + "r-body", { rotation: 0 }, { rotation: 14, svgOrigin: "0 -176", duration: 0.5, ease: "power2.inOut" }, C.lean);
      tl.fromTo([S + "r-armL", S + "r-armR"], { rotation: -20 }, { rotation: 30, duration: 0.1, ease: "sine.inOut", repeat: 13, yoyo: true }, C.lean + 0.3);
      tl.to(S + "r-pup", { x: 6, y: 4, duration: 0.2 }, C.lean);
      tl.fromTo(S + "flash", { opacity: 0 }, { opacity: 0.6, duration: 0.05, yoyo: true, repeat: 1 }, C.photo);
      tl.fromTo(S + "flash", { opacity: 0 }, { opacity: 0.6, duration: 0.05, yoyo: true, repeat: 1 }, C.photo + 0.9);
"""
scene(sid, world, js, cards)
