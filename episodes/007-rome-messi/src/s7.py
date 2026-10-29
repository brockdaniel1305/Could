import sys; sys.path.insert(0, __file__.rsplit("/episodes/", 1)[0] + "/tools")  # noqa: E702
from scene import *  # noqa: F403
from battle import *  # noqa: E402,F403
sid = "s7-end"
D = TIMING[sid]["duration"]
fallen = [(560, 84), (760, -80), (930, 86), (130, -84), (300, 82)]
standing = ["s1", "s2", "s3"]
w = (field(sid)
     + "".join(roman(sid, f"x{i}", x, GY - 10) for i, (x, a) in enumerate(fallen))
     + "".join(roman(sid, s, 640 + i * 150, GY - 120, 0.62) for i, s in enumerate(standing))
     + f'<g transform="translate(900,{GY - 120})"><g id="{sid}-flag" opacity="0"><path d="M0,0 L0,-300" stroke="#6b4a2a" stroke-width="10" /><path d="M0,-300 Q60,-320 120,-290 Q90,-250 120,-210 Q60,-230 0,-210 Z" fill="#f4f4f2" stroke="#1a1a2e" stroke-width="5" /></g></g>'
     + messi(sid, 420) + ball(sid, 470, GY - 16))
cards = stamp(sid, "UNSTOPPABLE.") + scorebug(sid, 0, 3)
js = JS + f"""
      const fallen = {[a for _, a in fallen]};
      const standing = {standing};
""" + """
      // everyone already on the ground, dizzy
      fallen.forEach((a, i) => { tl.set(S + "x" + i, { rotation: a, transformOrigin: "50% 100%" }, 0); dizzy("x" + i, 0, 1); });
      standing.forEach((s, i) => dizzy(s, 0.1 + i * 0.2, 2));
      // Messi, foot on the ball, arms folded
      tl.set(S + "m-armL", { rotation: 60 }, 0); tl.set(S + "m-armR", { rotation: -60 }, 0);
      tl.fromTo(S + "m-legR", { rotation: 0 }, { rotation: -12, duration: 0.6, yoyo: true, repeat: R(D, 0.6), ease: "sine.inOut" }, 0);
      // ... that nobody could stop Messi: the last Romans look at him, mouths open, swords drop, a white flag goes up
      standing.forEach((s, i) => { look(s + "p", -6, 0, C.nobody); face(s + "p", "m-o", C.nobody); });
      standing.forEach((s, i) => { tl.to(S + s + "p-sword", { y: 140, rotation: 70, duration: 0.35, ease: "power2.in" }, C.nobody + 0.6 + i * 0.08); });
      tl.fromTo(S + "flag", { opacity: 0, y: 300 }, { opacity: 1, y: 0, duration: 0.6, ease: "back.out(1.6)" }, C.nobody + 1.0);
      tl.fromTo(S + "flag", { rotation: -4 }, { rotation: 4, transformOrigin: "0% 100%", duration: 0.4, yoyo: true, repeat: R(D - C.nobody - 1.6, 0.4) }, C.nobody + 1.6);
      look("m", 4, -2, C.nobody + 0.5);
      stampIn(C.nobody + 1.8);
"""
scene(sid, w, js, cards, extra_css=CSS)
