import sys; sys.path.insert(0, __file__.rsplit("/episodes/", 1)[0] + "/tools")  # noqa: E702
from scene import *  # noqa: F403
from rail import *  # noqa: E402,F403
sid = "s6-twist"
D = TIMING[sid]["duration"]
mini_board = (f'<g transform="translate(700,{FY - 250})"><rect x="0" y="0" width="230" height="90" rx="8" fill="#1d2a5c" stroke="#1a1a2e" stroke-width="5" />'
              f'<path d="M60,90 L60,250 M170,90 L170,250" stroke="#3a3f48" stroke-width="10" />'
              f'<text data-layout-ignore id="{sid}-mbt" x="22" y="60" font-family="CouldMono" font-weight="700" font-size="40" fill="#ffd23f">on time</text></g>')
w = room(sid) + mini_board + model_train(sid, 380) + boots(sid, 120)
cards = (banner(sid, "b", "ONE MORE THING", "Round 3, timetable", 60, 330)
         + card(sid, "lt", "MODEL TRAIN DELAY", "+3 min", 60, 380, "red")
         + card(sid, "md", "MADE IN", '<span class="flag"></span>Germany', 520, 560, "gold")
         + scorebug(sid, 2, 1))
css = SCORE_CSS + MINI_CSS + """
    .flag { display: inline-block; width: 84px; height: 54px; margin-right: 18px; vertical-align: -4px; border: 4px solid #1a1a2e;
            background: linear-gradient(#1a1a2e 0 33.3%, #e0412f 33.3% 66.6%, #ffd23f 66.6%); }"""
js = SIU_JS + SCORE_JS + """
      const mb = document.getElementById("s6-twist-mbt");
      tl.to({}, { duration: D, ease: "none", onUpdate() { const t = this.time(); mb.textContent = t >= C.late ? "+3 min" : "on time"; } }, 0);
      fly("b", 0.1, C.late - 0.1, { from: "top" });
      // the model finally rolls in and stops
      tl.fromTo(S + "mt", { x: 900 }, { x: 0, duration: 1.0, ease: "power2.out" }, C.late);
      tl.fromTo(S + "kwrap", { rotation: 0 }, { rotation: -2, transformOrigin: "50% 100%", duration: 0.25, yoyo: true, repeat: R(D - C.late, 0.25) }, C.late);
      fly("lt", C.late + 0.2, null);
      fly("md", C.why, null, { from: "right" });
      tl.to([S + "mtt-browL", S + "mtt-browR"], { y: -10, duration: 0.2 }, C.why + 0.3);
"""
scene(sid, w, js, cards, extra_css=css)
