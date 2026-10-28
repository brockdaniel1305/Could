import sys; sys.path.insert(0, __file__.rsplit('/episodes/', 1)[0] + '/tools')  # noqa: E702
from scene import *  # noqa: F403
from race import course, driver, tracker, PX  # noqa: E402
sid = "s2-bolt"
D = TIMING[sid]["duration"]
medals = "".join(f'<g id="{sid}-md{i}" transform="translate({-60 + 40 * (i % 4)},{-330 - 44 * (i // 4)})"><circle r="17" fill="#ffd23f" stroke="#1a1a2e" stroke-width="4" /><text data-layout-ignore y="7" text-anchor="middle" font-family="Inter" font-weight="900" font-size="18" fill="#1a1a2e">1</text></g>' for i in range(8))
world = f"""
{part("track-day", sid + "-track")}
{course(sid)}
<mask id="{sid}-mask"><rect x="0" y="0" width="1080" height="1920" fill="#fff" /><circle id="{sid}-hole" cx="150" cy="970" r="300" fill="#000" /></mask>
<rect id="{sid}-spot" x="0" y="0" width="1080" height="1920" fill="#000" opacity="0" mask="url(#{sid}-mask)" />
<g transform="translate(127,1180)"><g transform="scale(1.3)">{medals}</g></g>
<g id="{sid}-zap" transform="translate(380,640)"><path d="M30,-90 L-30,10 L5,10 L-25,100 L50,-20 L12,-20 L40,-90 Z" fill="#ffd23f" stroke="#1a1a2e" stroke-width="6" stroke-linejoin="round" /></g>
"""
cards = (banner(sid, "b", "LANE 4", "Usain Bolt", 60, 330)
         + card(sid, "h", "HEIGHT", "1.95 m", 520, 520, )
         + card(sid, "wr", "WORLD RECORD", "9.58 s", 470, 380, "gold")
         + card(sid, "g", "OLYMPIC GOLD", "8 medals", 470, 380))
js = driver([[0, 0], [D, 0]], [[0, 5.5]]) + """
      tl.fromTo(S + "spot", { opacity: 0 }, { opacity: 0.6, duration: 0.4 }, C.name - 0.2);
      fly("b", C.name, C.wr - 0.1);
      fly("h", C.h, C.wr - 0.1, { from: "right" });
      fly("wr", C.wr, C.gold - 0.1, { from: "right" });
      fly("g", C.gold, C.pose - 0.1, { from: "right" });
      // eight gold medals pop on, one by one
      for (let i = 0; i < 8; i++) pop(S + "md" + i, C.gold + 0.35 + i * 0.12);
      tl.to(S + "b-armL", { rotation: 25, duration: 0.3 }, C.h);
      swap(S + "b-m-smile", S + "b-m-o", C.wr + 0.2); swap(S + "b-m-o", S + "b-m-smile", C.wr + 1.2);
      blink(S + "b-lids", 2.0); blink(S + "b-lids", 7.2);
      // the pose: one arm to the sky, the other across
      tl.to(S + "b-armR", { rotation: -135, duration: 0.25, ease: "back.out(2)" }, C.pose + 0.2);
      tl.to(S + "b-armL", { rotation: -70, duration: 0.25, ease: "back.out(2)" }, C.pose + 0.28);
      tl.to(S + "b-head", { rotation: 8, duration: 0.25 }, C.pose + 0.3);
      pop(S + "zap", C.pose + 0.4);
      tl.fromTo(S + "zap", { rotation: -6, svgOrigin: "380 640" }, { rotation: 6, duration: 0.15, repeat: 9, yoyo: true }, C.pose + 0.85);
      // T-Rex in the dark, unimpressed
      tl.fromTo(S + "r-tail", { rotation: -3, svgOrigin: "-70 -208" }, { rotation: 3, duration: 0.8, ease: "sine.inOut", repeat: R(D, 0.8), yoyo: true }, 0);
"""
scene(sid, world, js, cards)
