import sys; sys.path.insert(0, __file__.rsplit('/episodes/', 1)[0] + '/tools')  # noqa: E702
from scene import *  # noqa: F403
from race import course, PX, NOSE  # noqa: E402
sid = "s8-outro"
world = f"""
{part("track-day", sid + "-track")}
{course(sid, start_blocks=False)}
"""
cards = (banner(sid, "b", "NEXT RACE", "Who should we<br>race next?", 60, 330)
         + card(sid, "c", "COMMENT YOUR MATCHUP", "↓ ↓ ↓", 60, 640, "gold"))
js = f"""
      const PX = {PX}, NOSE = {NOSE};
      gsap.set(S + "tape", {{ opacity: 0 }});
      // the chase goes on: both run, the camera runs with them
      tl.fromTo(S + "course", {{ x: 540 - 150 * PX }}, {{ x: 540 - 175 * PX, duration: D, ease: "none" }}, 0);
      tl.fromTo(S + "bolt", {{ x: 152 * PX }}, {{ x: 177 * PX, duration: D, ease: "none" }}, 0);
      tl.fromTo(S + "rex", {{ x: 150 * PX - NOSE }}, {{ x: 175 * PX - NOSE, duration: D, ease: "none" }}, 0);
      const n = R(D, 0.14);
      ["legL", "armR"].forEach((p) => tl.fromTo(S + "b-" + p, {{ rotation: -38 }}, {{ rotation: 38, duration: 0.14, repeat: n, yoyo: true }}, 0));
      ["legR", "armL"].forEach((p) => tl.fromTo(S + "b-" + p, {{ rotation: 38 }}, {{ rotation: -38, duration: 0.14, repeat: n, yoyo: true }}, 0));
      tl.fromTo(S + "r-legL", {{ rotation: -24 }}, {{ rotation: 24, duration: 0.3, ease: "sine.inOut", repeat: R(D, 0.3), yoyo: true }}, 0);
      tl.fromTo(S + "r-legR", {{ rotation: 24 }}, {{ rotation: -24, duration: 0.3, ease: "sine.inOut", repeat: R(D, 0.3), yoyo: true }}, 0);
      tl.fromTo(S + "r-jaw", {{ rotation: 0, svgOrigin: "0 18" }}, {{ rotation: 26, duration: 0.25, repeat: R(D, 0.25), yoyo: true }}, 0);
      swap(S + "b-m-smile", S + "b-m-o", 0);
      fly("b", 0.05, null, {{ from: "top" }});
      fly("c", C.c, null, {{ from: "right" }});
"""
scene(sid, world, js, cards)
