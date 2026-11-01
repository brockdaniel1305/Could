import sys; sys.path.insert(0, __file__.rsplit("/episodes/", 1)[0] + "/tools")  # noqa: E702
from scene import *  # noqa: F403
from field import forest, board, defender, tank, GY  # noqa: E402
STAMP = """
    .stamp { position: absolute; left: 150px; top: 540px; width: 780px; height: 380px; border: 26px solid #1f9d55; border-radius: 34px;
             display: flex; align-items: center; justify-content: center; font: 900 240px/1 "Inter"; color: #1f9d55; opacity: 0;
             background: rgba(244, 239, 230, 0.2); }
    .heart { position: absolute; left: 740px; top: 790px; width: 160px; height: 147px; opacity: 0; }"""
sid = "s5-end"
D = TIMING[sid]["duration"]
tanks = "".join(tank(sid, f"k{i}", 820 + i * 150, 0.7, GY - 60 + (i % 2) * 70) for i in range(4))
thumb = (f'<g transform="translate(820,{GY - 210})"><g id="{sid}-thumb" opacity="0"><rect x="-14" y="-90" width="28" height="90" rx="12" fill="#6b7177" stroke="#1a1a2e" stroke-width="5" />'
         f'<rect x="-26" y="-130" width="52" height="44" rx="14" fill="#f2c9a0" stroke="#1a1a2e" stroke-width="5" /><rect x="-8" y="-170" width="18" height="44" rx="9" fill="#f2c9a0" stroke="#1a1a2e" stroke-width="5" /></g></g>')
heart = '<svg class="heart" id="s5-end-heart" viewBox="0 0 100 92"><path d="M50,88 C10,60 0,40 0,25 C0,10 12,0 26,0 C38,0 46,8 50,16 C54,8 62,0 74,0 C88,0 100,10 100,25 C100,40 90,60 50,88 Z" fill="#ff3b5c" stroke="#1a1a2e" stroke-width="5" /></svg>'
w = (forest(sid) + tanks + thumb + defender(sid, 330)
     + f'<g transform="translate(380,{GY - 14})"><g id="{sid}-ball"><g transform="scale(1.1)">{part("football", sid + "-fb")}</g></g></g>'
     + f'<g transform="translate(600,{GY - 300}) scale(1.3)">{part("burst", sid + "-oops", WORD="OOPS")}</g>'
     + board(sid))
cards = (card(sid, "ps", "UNDER PRESSURE", "None at all", 40, 380)
         + card(sid, "cm", "WRITE YOUR SCENARIO IN THE COMMENTS", "↓ ↓ ↓", 40, 380, "gold")
         + card(sid, "fl", "FOR THE NEXT CASE", "Like · Follow", 470, 540, "red")
         + f'\n    <div class="stamp" id="{sid}-stamp">YES.</div>' + heart)
js = """
      for (let i = 0; i < 4; i++) tl.fromTo(S + "k" + i + "t-body", { y: 0 }, { y: -3, duration: 0.12, repeat: R(D, 0.12), yoyo: true }, 0);
      tl.fromTo(S + "stamp", { opacity: 0, scale: 2.4, rotation: -4 }, { opacity: 1, scale: 1, rotation: -9, duration: 0.18, ease: "power4.in" }, C.yes);
      tl.fromTo(S + "svg", { x: 0 }, { x: 10, duration: 0.04, repeat: 5, yoyo: true }, C.yes + 0.18);
      tl.to(S + "stamp", { opacity: 0, scale: 0.9, duration: 0.25, ease: "power2.in" }, C.risk - 0.1);
      tl.to(S + "u-armL", { rotation: -60, duration: 0.3 }, C.yes + 0.3); tl.to(S + "u-armR", { rotation: 60, duration: 0.3 }, C.yes + 0.35);
      // no pressure at all ... one simple pass, straight to a tank
      fly("ps", C.risk, C.like - 0.1);
      tl.to([S + "u-armL", S + "u-armR"], { rotation: 0, duration: 0.3 }, C.risk);
      const pass = C.walk - 1.0;
      tl.to(S + "u-legR", { rotation: -40, duration: 0.15, yoyo: true, repeat: 1 }, pass);
      tl.fromTo(S + "ball", { x: 0, rotation: 0 }, { x: 420, rotation: 720, duration: 0.6, ease: "power1.out" }, pass + 0.1);
      tl.fromTo(S + "oops", { scale: 0, opacity: 0, transformOrigin: "50% 50%" }, { scale: 1, opacity: 1, duration: 0.25, ease: "back.out(3)" }, pass + 0.7);
      tl.to(S + "oops", { opacity: 0, duration: 0.2 }, C.walk + 0.6);
      swap(S + "u-m-smile", S + "u-m-o", pass + 0.7);
      tl.to(S + "u-armL", { rotation: 165, duration: 0.25 }, C.walk); tl.to(S + "u-armR", { rotation: -165, duration: 0.25 }, C.walk + 0.05);
      // the whole army walks past him; the last tank stops for a like
      for (let i = 1; i < 4; i++) { swap(S + "k" + i + "t-smirk", S + "k" + i + "t-grin", C.walk); tl.to(S + "k" + i, { x: -1500, duration: 2.0, ease: "power1.in" }, C.walk + 0.1 + (i - 1) * 0.2); }
      tl.to(S + "ball", { x: -1100, duration: 2.0, ease: "power1.in" }, C.walk + 0.1);
      tl.to([S + "u-pupL", S + "u-pupR"], { x: -7, duration: 0.5 }, C.walk + 0.6);
      swap(S + "k0t-smirk", S + "k0t-grin", C.like);
      tl.fromTo(S + "thumb", { opacity: 0, y: 80 }, { opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)" }, C.like + 0.1);
      tl.fromTo(S + "heart", { opacity: 0, scale: 0.2, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2.5)" }, C.like + 0.3);
      fly("cm", C.like + 0.5, null);
      fly("fl", C.like + 0.7, null, { from: "right" });
"""
scene(sid, w, js, cards, extra_css=STAMP, loop_out=True)
