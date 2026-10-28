import sys; sys.path.insert(0, __file__.rsplit("/episodes/", 1)[0] + "/tools")  # noqa: E702
from scene import *  # noqa: F403
from rail import *  # noqa: E402,F403
sid = "s5-round3"
D = TIMING[sid]["duration"]
w = (room(sid) + ruler_cm(sid) + hline_cm(sid, "h4", 4.5) + hline_cm(sid, "j70", 70, "#ffd23f")
     + f'<g id="{sid}-gap" opacity="0"><path d="M800,{y_cm(4.5)} L800,{y_cm(70)} M776,{y_cm(4.5)} L824,{y_cm(4.5)} M776,{y_cm(70)} L824,{y_cm(70)}" stroke="#1f9d55" stroke-width="10" stroke-linecap="round" /></g>'
     + model_train(sid, 1100) + boots(sid, 430)
     + f'<g transform="translate(800,{FY - 520}) scale(1.6)">{part("burst", sid + "-siu", WORD="SIUUU!")}</g>')
cards = (banner(sid, "b", "ROUND 3 OF 3 · DECIDER", "A model train", 60, 330)
         + card(sid, "sc", "SCALE", "1 : 87", 560, 560)
         + card(sid, "h", "HEIGHT", "4.5 cm", 60, 380, "red")
         + card(sid, "v", "SCALE SPEED", "300 km/h", 520, 560)
         + card(sid, "rl", "REAL SPEED", "1 m/s", 60, 560, "gold")
         + card(sid, "hs", "HIS JUMP", "70 cm", 560, 380, "gold")
         + card(sid, "cl", "TO SPARE", "65 cm", 560, 380, "gold")
         + scorebug(sid, 1, 1)
         + f'\n    <div class="slowmo" id="{sid}-slow">SLOW MOTION</div>')
css = SCORE_CSS + MINI_CSS + """
    .slowmo { position: absolute; left: 56px; top: 300px; padding: 8px 14px; border-radius: 10px; background: #e0412f;
              font: 700 28px/1 "CouldMono"; letter-spacing: 0.1em; color: #fff; opacity: 0; }"""
J = TIMING[sid]["cues"]["jump"]
js = SIU_JS + SCORE_JS + """
      fly("b", C.name, C.h - 0.1);
      // the model whizzes past once at its real speed (1 m/s = 1200 px/s)
      tl.fromTo(S + "mt", { x: 50 }, { x: -1700, duration: 1.25, ease: "none" }, C.name + 0.3);
      fly("sc", C.scale, C.v - 0.1, { from: "right" });
      tl.fromTo(S + "h4", { opacity: 0 }, { opacity: 1, duration: 0.3 }, C.h);
      fly("h", C.h, C.real - 0.1);
      fly("v", C.v, C.has - 0.1, { from: "right" });
      fly("rl", C.real, C.go - 0.1);
      tl.fromTo(S + "j70", { opacity: 0 }, { opacity: 1, duration: 0.3 }, C.has);
      fly("hs", C.has, C.go - 0.1, { from: "right" });
      // position: the boots bounce on the spot, the train appears on the right
      tl.fromTo(S + "kwrap", { y: 0 }, { y: -26, duration: 0.22, ease: "sine.inOut", yoyo: true, repeat: 5 }, C.go + 0.2);
      tl.to(S + "h4", { opacity: 0.5, duration: 0.2 }, C.go);
      // the jump, in slow motion (x0.5): 70 cm up, 1.4 s in the air; the train passes under at 700 px/s
      tl.fromTo(S + "slow", { opacity: 0 }, { opacity: 1, duration: 0.15 }, C.jump - 0.4);
      tl.to(S + "slow", { opacity: 0, duration: 0.15 }, C.clear + 0.6);
      tl.fromTo(S + "mt", { x: 50 }, { x: -1700, duration: 2.5, ease: "none" }, C.jump - 0.35);
      jump(C.jump + 0.1, 840, 1.4);
      swap(S + "mtt-smirk", S + "mtt-o", C.jump + 0.4);
      tl.fromTo(S + "gap", { opacity: 0, scaleY: 0, transformOrigin: "50% 100%" }, { opacity: 1, scaleY: 1, duration: 0.4, ease: "expo.out" }, C.clear);
      fly("cl", C.clear + 0.1, C.score - 0.1, { from: "right" });
      // landed: SIUUU, 2 : 1
      tl.to([S + "gap", S + "j70", S + "h4"], { opacity: 0, duration: 0.2 }, C.score);
      tl.to(S + "legB", { x: 120, duration: 0.15, ease: "power2.out" }, C.score);
      tl.fromTo(S + "siu", { scale: 0, opacity: 0, transformOrigin: "50% 50%" }, { scale: 1, opacity: 1, duration: 0.25, ease: "back.out(3)" }, C.score);
      score(C.score, 2, 1, "sa");
"""
scene(sid, w, js, cards, extra_css=css)
