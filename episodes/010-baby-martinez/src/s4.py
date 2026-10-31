import sys; sys.path.insert(0, __file__.rsplit("/episodes/", 1)[0] + "/tools")  # noqa: E702
from scene import *  # noqa: F403
from pitch import *  # noqa: E402,F403
sid = "s4-end"
D = TIMING[sid]["duration"]
w = pitch(sid) + opp(sid, 700, 1.3) + baby(sid, 380, 0.58)
cards = (card(sid, "fo", "FOUL", "<s>Yes</s> No", 40, 380)
         + card(sid, "pe", "PENALTY", "<s>Yes</s> No", 560, 380)
         + card(sid, "st", "STILL ON THE PITCH", "Yes ✓", 40, 560, "gold")
         + card(sid, "wm", "WITH MARTÍNEZ", "Chelsea 2–0", 40, 380, "red")
         + card(sid, "wb", "WITH THE BABY", "Chelsea 1–0", 560, 560, "gold")
         + card(sid, "cm", "WRITE YOUR SCENARIO IN THE COMMENTS", "↓ ↓ ↓", 60, 380, "gold")
         + card(sid, "fl", "FOR THE NEXT CASE", "Like · Follow", 470, 560, "red")
         + f'\n    <div class="stamp" id="{sid}-stamp">UPGRADE.</div>' + HEART.replace("HID", sid + "-heart"))
js = JS + """
      tl.fromTo(S + "b-armR", { rotation: -150 }, { rotation: -170, duration: 0.3, yoyo: true, repeat: 3 }, 0.2);
      tl.to(S + "b-armR", { rotation: 0, duration: 0.3 }, 1.5);
      look("op", -6, 6, 0.3);
      fly("fo", C.nof, C.m - 0.1);
      fly("pe", C.nop, C.m - 0.1, { from: "right" });
      fly("st", C.still, C.m - 0.1);
      tl.fromTo(S + "b-armL", { rotation: 0 }, { rotation: 160, duration: 0.2, yoyo: true, repeat: 5 }, C.still + 0.1);
      tl.set(S + "b-dummy", { opacity: 0 }, C.still); face("b", "m-smile", C.still);
      fly("wm", C.m, C.like + 1.0);
      fly("wb", C.b, C.like + 1.0, { from: "right" });
      tl.fromTo(S + "stamp", { opacity: 0, scale: 2.4, rotation: -4 }, { opacity: 1, scale: 1, rotation: -8, duration: 0.18, ease: "power4.in" }, C.up);
      tl.fromTo(S + "svg", { x: 0 }, { x: 10, duration: 0.04, repeat: 5, yoyo: true }, C.up + 0.18);
      tl.to(S + "stamp", { opacity: 0, duration: 0.25 }, C.like - 0.15);
      // it even left a like
      tl.to(S + "b-armR", { rotation: -160, duration: 0.25, ease: "back.out(2)" }, C.like);
      tl.set(S + "b-thumb", { opacity: 1 }, C.like + 0.1);
      tl.fromTo(S + "heart", { opacity: 0, scale: 0.2, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2.5)" }, C.like + 0.2);
      tl.to(S + "heart", { scale: 1.12, duration: 0.25, yoyo: true, repeat: 3 }, C.like + 0.6);
      tl.to(S + "heart", { opacity: 0, y: -200, duration: 0.3 }, C.like + 1.6);
      fly("cm", C.like + 1.4, null);
      fly("fl", C.like + 1.6, null, { from: "right" });
"""
scene(sid, w, js, cards, extra_css=CSS, loop_out=True)
