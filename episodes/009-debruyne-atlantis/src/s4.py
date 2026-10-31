import sys; sys.path.insert(0, __file__.rsplit("/episodes/", 1)[0] + "/tools")  # noqa: E702
from scene import *  # noqa: F403
from ocean import *  # noqa: E402,F403
sid = "s4-pass"
D = TIMING[sid]["duration"]
ball = f'<g transform="translate(312,{CLIFF - 16})"><g id="{sid}-ball"><g transform="scale(0.7)">{part("football", sid + "-fb")}</g></g></g>'
dball = f'<g transform="translate(540,560)"><g id="{sid}-dball" opacity="0"><g id="{sid}-dspin"><g transform="scale(1.2)">{part("football", sid + "-db")}</g></g></g></g>'
splash = f'<g transform="translate(860,902)"><g id="{sid}-spl" opacity="0"><path d="M-60,0 Q-50,-50 -20,-20 Q0,-80 20,-20 Q50,-50 60,0" fill="#d8f0fa" stroke="#1a1a2e" stroke-width="4" /></g></g>'
heart = '<svg class="heart" id="s4-pass-heart" viewBox="0 0 100 92"><path d="M50,88 C10,60 0,40 0,25 C0,10 12,0 26,0 C38,0 46,8 50,16 C54,8 62,0 74,0 C88,0 100,10 100,25 C100,40 90,60 50,88 Z" fill="#ff3b5c" stroke="#1a1a2e" stroke-width="5" /></svg>'
w = surface(sid) + splash + kdb(sid) + ball + deep(sid) + dball
cards = (card(sid, "a", "ASSISTS", '<span id="s4-pass-an">20</span>', 40, 380, "gold")
         + card(sid, "lk", "ATLANTIS", "Liked this.", 600, 560)
         + card(sid, "cm", "WRITE YOUR SCENARIO IN THE COMMENTS", "↓ ↓ ↓", 60, 380, "gold")
         + card(sid, "fl", "FOR THE NEXT CASE", "Like · Follow", 470, 560, "red")
         + f'\n    <div class="stamp" id="{sid}-stamp">FOUND.</div>' + heart)
js = JS + """
      tl.fromTo(S + "waves", { x: 0 }, { x: -120, duration: D, ease: "none" }, 0);
      // "Perfect." - a small nod; "No look." - he turns his head away
      tl.to(S + "m-head", { rotation: 6, duration: 0.15, yoyo: true, repeat: 1 }, 0.3);
      tl.to(S + "m-head", { rotation: -14, duration: 0.25 }, C.look);
      look("m", -8, 0, C.look);
      // "One pass." - over the horizon, splash
      kickR(C.pass + 0.1);
      arc(S + "ball", C.pass + 0.1, 0.9, 548, -90, 260, 0.25);
      tl.to(S + "ball", { opacity: 0, duration: 0.05 }, C.pass + 1.0);
      tl.fromTo(S + "spl", { opacity: 0, scale: 0.3, transformOrigin: "50% 100%" }, { opacity: 1, scale: 1, duration: 0.2, ease: "back.out(2)" }, C.pass + 1.0);
      // the dive: bubbles and fish stream up, the sea floor rises into view, the ball lands on the X
      const T0 = C.pass + 1.2;
      tl.set(S + "deep", { opacity: 1 }, T0);
      tl.set(S + "dball", { opacity: 1 }, T0);
      tl.fromTo(S + "bub", { y: 0 }, { y: -1920, duration: 1.4, ease: "none" }, T0);
      tl.fromTo(S + "fish", { y: 400 }, { y: -900, duration: 1.4, ease: "none" }, T0);
      tl.fromTo(S + "floor", { y: 1100 }, { y: 0, duration: C.found - 0.2 - T0, ease: "power2.out" }, T0);
      tl.fromTo(S + "dspin", { rotation: 0 }, { rotation: 540, transformOrigin: "50% 50%", duration: C.found - T0, ease: "power1.out" }, T0);
      tl.to(S + "dball", { y: 1164 - 26 - 560, duration: 0.5, ease: "bounce.out" }, C.found - 0.45);
      // Atlantis: found - the city lights up, the statue opens its eyes
      tl.fromTo(S + "glow", { opacity: 0 }, { opacity: 0.8, duration: 0.4 }, C.found);
      tl.set(S + "slids", { opacity: 0 }, C.found + 0.2);
      tl.to([S + "spL", S + "spR"], { y: 8, duration: 0.2 }, C.found + 0.3);
      tl.fromTo(S + "stamp", { opacity: 0, scale: 2.4, rotation: -4 }, { opacity: 1, scale: 1, rotation: -8, duration: 0.18, ease: "power4.in" }, C.found + 0.1);
      tl.to(S + "stamp", { opacity: 0, duration: 0.25 }, C.a21 - 0.15);
      // assist number 21
      fly("a", C.a21, C.like + 1.2);
      const an = document.querySelector(S + "an");
      tl.to({}, { duration: D, ease: "none", onUpdate() { const v = this.time() >= C.a21 + 0.4 ? "21" : "20"; if (an.textContent !== v) an.textContent = v; } }, 0);
      tl.fromTo(S + "an", { scale: 1 }, { scale: 1.6, duration: 0.15, yoyo: true, repeat: 1, transformOrigin: "50% 50%" }, C.a21 + 0.4);
      // even Atlantis left a like: thumbs up and a big heart
      tl.to(S + "sarm", { rotation: -160, transformOrigin: "50% 0%", duration: 0.3, ease: "back.out(2)" }, C.like);
      tl.fromTo(S + "heart", { opacity: 0, scale: 0.2, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2.5)" }, C.like + 0.2);
      tl.to(S + "heart", { scale: 1.12, duration: 0.25, yoyo: true, repeat: 3 }, C.like + 0.6);
      fly("lk", C.like + 0.3, C.like + 1.2, { from: "right" });
      tl.to(S + "heart", { opacity: 0, y: -200, duration: 0.3 }, C.like + 1.5);
      // end cards
      fly("cm", C.like + 1.4, null);
      fly("fl", C.like + 1.6, null, { from: "right" });
"""
scene(sid, w, js, cards, extra_css=CSS)
