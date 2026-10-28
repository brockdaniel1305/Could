import sys; sys.path.insert(0, __file__.rsplit('/episodes/', 1)[0] + '/tools')  # noqa: E702
from scene import *  # noqa: F403
from race import course, driver, tracker, PX  # noqa: E402
sid = "s3-trex"
D = TIMING[sid]["duration"]
world = f"""
{part("track-day", sid + "-track")}
{course(sid)}
<mask id="{sid}-mask"><rect x="0" y="0" width="1080" height="1920" fill="#fff" /><ellipse cx="640" cy="850" rx="430" ry="340" fill="#000" /></mask>
<rect id="{sid}-spot" x="0" y="0" width="1080" height="1920" fill="#000" opacity="0" mask="url(#{sid}-mask)" />
<g id="{sid}-tape12" transform="translate(127,1130)">
  <path d="M0,0 L900,0 M0,-18 L0,18 M900,-18 L900,18" stroke="#ffd23f" stroke-width="8" stroke-linecap="round" />
  <rect x="380" y="-34" width="140" height="64" rx="12" fill="#ffd23f" stroke="#1a1a2e" stroke-width="5" />
  <text x="450" y="12" text-anchor="middle" font-family="Inter" font-weight="900" font-size="40" fill="#1a1a2e">12 m</text>
</g>
<g transform="translate(880,600) scale(1.3)">{part("burst", sid + "-chomp", WORD="CHOMP")}</g>
"""
cards = (banner(sid, "b", "LANE 5", "Tyrannosaurus rex", 50, 330)
         + card(sid, "kg", "WEIGHT", "~8 tonnes", 90, 360)
         + card(sid, "bite", "BITE FORCE (EST.)", "~35,000 N", 90, 360, "red")
         + card(sid, "arms", "ARMS", "Decorative", 90, 360)
         + card(sid, "ext", "LAST RACE", "66 million years ago", 60, 360, "gold"))
js = driver([[0, 0], [D, 0]], [[0, 5.5]]) + """
      tl.fromTo(S + "spot", { opacity: 0 }, { opacity: 0.6, duration: 0.4 }, C.name - 0.2);
      fly("b", C.name, C.len + 0.9);
      tl.fromTo(S + "tape12", { opacity: 0, scaleX: 0, svgOrigin: "127 1130" }, { opacity: 1, scaleX: 1, duration: 0.6, ease: "expo.out" }, C.len);
      tl.to(S + "tape12", { opacity: 0, duration: 0.25 }, C.kg + 0.4);
      fly("kg", C.kg, C.bite - 0.1);
      // the bite: jaw wide, CHOMP
      tl.to(S + "r-jaw", { rotation: 30, svgOrigin: "0 18", duration: 0.35, ease: "power2.out" }, C.bite);
      tl.to(S + "r-jaw", { rotation: 0, svgOrigin: "0 18", duration: 0.08, ease: "power4.in" }, C.bite + 0.42);
      tl.fromTo(S + "chomp", { scale: 0, opacity: 0, transformOrigin: "50% 50%" }, { scale: 1, opacity: 1, duration: 0.25, ease: "back.out(3)" }, C.bite + 0.5);
      tl.to(S + "chomp", { opacity: 0, duration: 0.2 }, C.bite + 1.4);
      fly("bite", C.bite + 0.5, C.arms - 0.1, { from: "right" });
      // Bolt, in the dark, is not enjoying this
      tl.to([S + "b-pupL", S + "b-pupR"], { x: 6, y: -6, duration: 0.25 }, C.bite + 0.5);
      swap(S + "b-m-smile", S + "b-m-o", C.bite + 0.5);
      // decorative arms
      fly("arms", C.arms, C.ext - 0.1);
      tl.fromTo([S + "r-armL", S + "r-armR"], { rotation: -20 }, { rotation: 25, duration: 0.12, ease: "sine.inOut", repeat: 11, yoyo: true }, C.arms + 0.8);
      tl.to(S + "r-brow", { rotation: -12, svgOrigin: "74 -43", duration: 0.25 }, C.arms + 0.8);
      // last race: 66 million years ago
      fly("ext", C.ext, null, { from: "top" });
      tl.to(S + "r-head", { rotation: -10, duration: 0.6, ease: "power2.inOut" }, C.ext + 0.6);
      tl.fromTo(S + "r-tail", { rotation: -3, svgOrigin: "-70 -208" }, { rotation: 3, duration: 0.8, ease: "sine.inOut", repeat: R(D, 0.8), yoyo: true }, 0);
"""
scene(sid, world, js, cards)
