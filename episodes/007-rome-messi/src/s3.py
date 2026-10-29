import sys; sys.path.insert(0, __file__.rsplit("/episodes/", 1)[0] + "/tools")  # noqa: E702
from scene import *  # noqa: F403
from battle import *  # noqa: E402,F403
sid = "s3-messi"
D = TIMING[sid]["duration"]
PXM = 150   # px per metre for the height ruler
ms = 255 / 316
ruler = (f'<g id="{sid}-rul" opacity="0"><path d="M110,{GY} L110,{GY - 2 * PXM}" stroke="#1a1a2e" stroke-width="6" />'
         + "".join(f'<path d="M110,{GY - m * PXM:.0f} L{140 if m % 1 == 0 else 128},{GY - m * PXM:.0f}" stroke="#1a1a2e" stroke-width="5" />' for m in (0, 0.5, 1, 1.5, 2))
         + "".join(f'<text data-layout-ignore x="150" y="{GY - m * PXM + 10:.0f}" font-family="Inter" font-weight="900" font-size="30" fill="#1a1a2e">{m} m</text>' for m in (1, 2))
         + f'<path d="M110,{GY - 1.7 * PXM:.0f} L470,{GY - 1.7 * PXM:.0f}" stroke="#ffd23f" stroke-width="7" stroke-dasharray="20 12" /></g>')
gold = [(570, 1170), (632, 1170), (694, 1170), (756, 1170), (601, 1118), (663, 1118), (725, 1118), (663, 1066)]
balls = "".join(f'<g transform="translate({x},{y})"><g id="{sid}-gb{i}" opacity="0"><circle r="30" fill="#ffd23f" stroke="#1a1a2e" stroke-width="5" />'
                f'<path d="M0,-11 L10,-3 L6,9 L-6,9 L-10,-3 Z" fill="#c9a24a" /><path d="M-16,-18 Q-6,-26 6,-24" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round" /></g></g>'
                for i, (x, y) in enumerate(gold))
shots = "".join(ball(sid, 380, GY - 18, 0.7, f"sh{i}") for i in range(7))
defs_ = "".join(f'<g transform="translate({x},{GY})"><g id="{sid}-d{i}" opacity="0"><g transform="scale(0.8)">{part("centre-back", sid + "-d" + str(i) + "p")}</g></g></g>' for i, x in enumerate((600, 760, 920)))
w = (field(sid) + f'<g transform="translate(940,{GY})"><g transform="scale(0.85)">{part("goal", sid + "-gl")}</g></g>' + ruler + balls + shots + defs_
     + messi(sid, 330, s=ms) + ball(sid, 380, GY - 18, 0.7)
     + f'<g transform="translate(1180,{GY})"><g id="{sid}-goat">{part("goat", sid + "-gt")}</g></g>'
     + f'<mask id="{sid}-mask"><rect width="1080" height="1920" fill="#fff" /><circle id="{sid}-hole" cx="330" cy="{GY - 140}" r="290" fill="#000" /></mask>'
     + f'<rect id="{sid}-dim" width="1080" height="1920" fill="#000" opacity="0" mask="url(#{sid}-mask)" />')
cards = (banner(sid, "b", "IN THE BLUE CORNER", "Lionel Messi", 40, 330)
         + card(sid, "h", "HEIGHT", "1.70 m", 560, 560)
         + card(sid, "bd", "BALLON D'OR", '<span id="s3-messi-bdn">0</span>', 600, 380, "gold")
         + card(sid, "g", "GOALS IN 2012", counter(sid, "gn"), 40, 380, "gold")
         + card(sid, "wr", "WORLD RECORD", "Guinness", 560, 560, "red")
         + card(sid, "pr", "IN HIS PRIME", "Unstoppable", 40, 380, "red")
         + card(sid, "gt", "STATUS", "G.O.A.T.", 600, 560, "gold")
         + card(sid, "df", "DEFENDERS", "Watched", 40, 380)
         + scorebug(sid, 0, 0))
js = JS + """
      tl.fromTo(S + "dim", { opacity: 0 }, { opacity: 0.55, duration: 0.4 }, C.name - 0.3);
      fly("b", C.name, C.h - 0.1);
      // 1.70 m on the ruler
      tl.fromTo(S + "rul", { opacity: 0 }, { opacity: 1, duration: 0.3 }, C.h);
      fly("h", C.h + 0.1, C.yr - 0.1, { from: "right" });
      tl.to(S + "rul", { opacity: 0, duration: 0.3 }, C.yr);
      // eight golden balls drop onto a pile, one after another
      fly("bd", C.bd, C.yr - 0.1, { from: "right" });
      label("bdn", [[0, "0"]].concat([0, 1, 2, 3, 4, 5, 6, 7].map((i) => [C.bd + 0.25 + i * 0.16, String(i + 1)])));
      [0, 1, 2, 3, 4, 5, 6, 7].forEach((i) => { tl.set(S + "gb" + i, { opacity: 1 }, C.bd - 0.1 + i * 0.16); tl.fromTo(S + "gb" + i, { y: -900 }, { y: 0, duration: 0.35, ease: "bounce.out", immediateRender: false }, C.bd - 0.1 + i * 0.16); });
      [0, 1, 2, 3, 4, 5, 6, 7].forEach((i) => tl.to(S + "gb" + i, { opacity: 0, y: 40, duration: 0.3 }, C.def - 0.4));
      // 91 goals: shots into the goal, faster and faster, while the counter runs
      fly("g", C.yr, C.prime - 0.1);
      count("gn", 0, 91, C.g, C.wr - C.g, "power1.in");
      const st = [0, 0.55, 1.0, 1.35, 1.62, 1.84, 2.02];
      st.forEach((s, i) => {
        const t0 = C.g + s;
        kickR(t0);
        tl.set(S + "sh" + i, { opacity: 0 }, 0);
        tl.set(S + "sh" + i, { opacity: 1 }, t0);
        arc(S + "sh" + i, t0, 0.45, 600, -60, 120, S + "sh" + i + "-spin");
        tl.set(S + "sh" + i, { opacity: 0 }, t0 + 0.5);
      });
      tl.fromTo(S + "gl", { scaleX: 1 }, { scaleX: 1.05, transformOrigin: "50% 100%", duration: 0.08, yoyo: true, repeat: 13 }, C.g + 0.45);
      fly("wr", C.wr, C.prime - 0.1, { from: "right" });
      // prime: unstoppable, and a real goat walks in
      fly("pr", C.prime, C.def - 0.1);
      tl.fromTo(S + "goat", { x: 0 }, { x: -470, duration: 1.6, ease: "power1.out" }, C.prime + 0.2);
      tl.fromTo([S + "gt-legF", S + "gt-legB"], { rotation: -12 }, { rotation: 12, duration: 0.15, yoyo: true, repeat: 9, transformOrigin: "50% 0%" }, C.prime + 0.2);
      tl.to(S + "goat", { y: -40, duration: 0.15, yoyo: true, repeat: 1 }, C.prime + 1.9);
      fly("gt", C.prime + 0.6, C.def - 0.1, { from: "right" });
      tl.to(S + "goat", { x: 200, duration: 1.0, ease: "power1.in" }, C.def - 0.3);
      // defenders appear and simply watch him dribble past
      tl.to(S + "dim", { opacity: 0, duration: 0.4 }, C.def - 0.3);
      [0, 1, 2].forEach((i) => pop(S + "d" + i, C.def + i * 0.12));
      [0, 1, 2].forEach((i) => look("d" + i + "p", -5, 0, C.def + 0.4));
      fly("df", C.watch, null);
      run(C.watch, C.watch + 1.4);
      tl.to(S + "mw", { x: 820, duration: 1.4, ease: "none" }, C.watch);
      tl.to(S + "ball", { x: 820, duration: 1.4, ease: "none" }, C.watch);
      tl.to(S + "ball-spin", { rotation: 900, duration: 1.4, ease: "none" }, C.watch);
      [0, 1, 2].forEach((i) => { look("d" + i + "p", 6, 0, C.watch + 0.35 + i * 0.3, 0.15); tl.to(S + "d" + i + "p-head", { rotation: 14, duration: 0.25 }, C.watch + 0.4 + i * 0.3); });
      tl.to(S + "d2", { scaleX: -1, transformOrigin: "50% 100%", duration: 0.25 }, C.watch + 1.4);
"""
scene(sid, w, js, cards, extra_css=CSS)
