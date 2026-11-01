import sys; sys.path.insert(0, __file__.rsplit("/episodes/", 1)[0] + "/tools")  # noqa: E702
from scene import *  # noqa: F403
from battle import *  # noqa: E402,F403
from cold import *  # noqa: E402,F403
sid = "s6-end"
D = TIMING[sid]["duration"]
fallen = [(560, 84), (760, -80), (930, 86), (130, -84), (300, 82)]
standing = ["s1", "s2", "s3"]
heart = '<svg class="heart" id="s6-end-heart" viewBox="0 0 100 92" style="position:absolute;left:560px;top:790px;width:150px;height:138px;opacity:0"><path d="M50,88 C10,60 0,40 0,25 C0,10 12,0 26,0 C38,0 46,8 50,16 C54,8 62,0 74,0 C88,0 100,10 100,25 C100,40 90,60 50,88 Z" fill="#ff3b5c" stroke="#1a1a2e" stroke-width="5" /></svg>'
w = (field(sid)
     + "".join(roman(sid, f"x{i}", x, GY - 10) for i, (x, a) in enumerate(fallen))
     + "".join(roman(sid, s, 640 + i * 150, GY - 120, 0.62) for i, s in enumerate(standing))
     + f'<g transform="translate(900,{GY - 120})"><g id="{sid}-flag" opacity="0"><path d="M0,0 L0,-300" stroke="#6b4a2a" stroke-width="10" /><path d="M0,-300 Q60,-320 120,-290 Q90,-250 120,-210 Q60,-230 0,-210 Z" fill="#f4f4f2" stroke="#1a1a2e" stroke-width="5" /></g></g>'
     + messi(sid, 420) + ball(sid, 470, GY - 16)
     + cold_world(sid, name="c", hidden=True))
cards = (card(sid, "q", "WHO SHOULD MESSI DRIBBLE PAST NEXT?", "Comment ↓", 40, 380, "gold")
         + card(sid, "fl", "COULD? CASE FILES", "Follow for more", 470, 540, "red") + heart
         + title(sid) + card(sid, "dz", "DIZZY ROMANS", "61,000", 40, 760, "gold"))
js = JS + f"""
      const fallen = {[a for _, a in fallen]};
      const standing = {standing};
""" + """
      fallen.forEach((a, i) => { tl.set(S + "x" + i, { rotation: a, transformOrigin: "50% 100%" }, 0); dizzy("x" + i, 0, 1); });
      standing.forEach((s, i) => dizzy(s, 0.1 + i * 0.2, 2));
      tl.set(S + "m-armL", { rotation: -62 }, 0); tl.set(S + "m-armR", { rotation: 62 }, 0);
      standing.forEach((s) => { look(s + "p", -6, 0, C.nobody); face(s + "p", "m-o", C.nobody); });
      standing.forEach((s, i) => tl.to(S + s + "p-sword", { y: 140, rotation: 70, duration: 0.35, ease: "power2.in" }, C.nobody + 0.4 + i * 0.08));
      tl.fromTo(S + "flag", { opacity: 0, y: 300 }, { opacity: 1, y: 0, duration: 0.5, ease: "back.out(1.6)" }, C.nobody + 0.6);
      // even the Romans left a like
      tl.to(S + "s1p-armR", { rotation: -165, duration: 0.25, ease: "back.out(2)" }, C.like);
      tl.fromTo(S + "heart", { opacity: 0, scale: 0.2, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2.5)" }, C.like + 0.15);
      fly("q", C.like + 0.3, null);
      fly("fl", C.like + 0.5, null, { from: "right" });
      // the last 0.4 s: hard cut to the cold open's first frame (same picture, so the loop is seamless)
      const CUT = D - 0.4;
      tl.set(S + "cold", { opacity: 1 }, CUT);
      tl.set([S + "c-q", S + "c-fl", S + "heart"], { opacity: 0 }, CUT);
      tl.set(S + "title", { opacity: 0 }, 0); tl.set(S + "title", { opacity: 1 }, CUT);
      tl.set(S + "c-dz", { opacity: 0 }, 0); tl.set(S + "c-dz", { opacity: 1, x: 0, y: 0, rotation: -3 }, CUT);
""" + cold_js("c", 0, freeze=True)
scene(sid, w, js, cards, extra_css=CSS + TITLE_CSS, loop_out="cut")
