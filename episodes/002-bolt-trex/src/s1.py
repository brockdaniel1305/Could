import sys; sys.path.insert(0, __file__.rsplit('/episodes/', 1)[0] + '/tools')  # noqa: E702
from scene import *  # noqa: F403
from race import course, driver, tracker, PX  # noqa: E402
sid = "s1-hook"
D = TIMING[sid]["duration"]
world = f"""
{part("track-day", sid + "-track")}
{course(sid)}
"""
cards = (banner(sid, "q", "CASE FILE 002", "Could Usain Bolt beat<br>a T-Rex in a 100 m race?", 50, 330)
         + card(sid, "m", "METHOD", "Scientific", 110, 420)
         + card(sid, "sw", "EQUIPMENT", "1 stopwatch", 250, 600, "gold"))
js = driver([[0, 0], [D, 0]], [[0, 5.5]]) + """
      // v3: opening punch-in (new first frame)
      tl.fromTo(S + "svg", { scale: 1.14 }, { scale: 1, transformOrigin: "50% 60%", duration: 0.8, ease: "power2.out" }, 0);
      // frame 0 is the thumbnail: the question is already on screen
      tl.fromTo(S + "c-q", { opacity: 1, x: 0, y: 0, rotation: -2 }, { y: -1100, rotation: 8, duration: 0.4, ease: "power3.in" }, C.sci - 0.45);
      fly("m", C.sci, null, { from: "right" });
      fly("sw", C.long, null);
      // Bolt stretches and waves, the T-Rex sizes him up
      tl.fromTo(S + "b-armR", { rotation: -150 }, { rotation: -120, duration: 0.3, ease: "sine.inOut", repeat: 5, yoyo: true }, 0);
      tl.to(S + "b-armR", { rotation: 0, duration: 0.4 }, 1.9);
      blink(S + "b-lids", 1.3); blink(S + "b-lids", 4.6);
      tl.to(S + "r-pup", { x: -8, y: 6, duration: 0.3 }, 0.8);
      tl.fromTo(S + "r-jaw", { rotation: 0, svgOrigin: "0 18" }, { rotation: 16, duration: 0.25, ease: "power2.out", yoyo: true, repeat: 1 }, C.ev);
      tl.to(S + "r-brow", { rotation: 10, svgOrigin: "74 -43", duration: 0.25, ease: "back.out(3)" }, C.sci);
      tl.to([S + "b-pupL", S + "b-pupR"], { x: 6, y: -4, duration: 0.25 }, C.ev + 0.4);
      swap(S + "b-m-smile", S + "b-m-o", C.ev + 0.5);
      tl.fromTo(S + "r-tail", { rotation: -3, svgOrigin: "-70 -208" }, { rotation: 3, duration: 0.8, ease: "sine.inOut", repeat: R(D, 0.8), yoyo: true }, 0);
"""
scene(sid, world, js, cards)
