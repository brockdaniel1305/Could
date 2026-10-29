import sys; sys.path.insert(0, __file__.rsplit("/episodes/", 1)[0] + "/tools")  # noqa: E702
from scene import *  # noqa: F403
from rev import *  # noqa: E402,F403
sid = "s7-madrid"
D = TIMING[sid]["duration"]
goal = (f'<g transform="translate(900,{GY})"><g id="{sid}-goal"><path d="M0,0 L0,-170 L150,-170" fill="none" stroke="#f4f4f2" stroke-width="10" />'
        f'<path d="M0,-170 L150,0 M40,-170 L150,-50 M80,-170 L150,-110 M0,-50 L80,0 M0,-110 L130,0" stroke="#f4f4f2" stroke-width="3" opacity="0.8" /></g></g>')
wa = (f'<g id="{sid}-A">' + part("paris-street", sid + "-ps") + mb(sid, 420) + "</g>")
wb = (f'<g id="{sid}-B" opacity="0">' + part("pitch-day", sid + "-pd", GY=1010) + goal
      + mate(sid, "t1", 640, 5) + mate(sid, "t2", 790, 8, hair="#d9b46a")
      + mb(sid, 300, kit=WHITE, name="r") + f'<g transform="translate(372,{GY - 16})"><g id="{sid}-ball"><g transform="scale(0.75)">{part("football", sid + "-fb")}</g></g></g>'
      + "</g>")
w = wa + wb + gauge(sid)
cards = (card(sid, "en", "REVOLUTIONS", "Enough", 40, 380)
         + card(sid, "rd", "HIS REAL DICTATORSHIP", "Real Madrid", 40, 380, "gold")
         + card(sid, "q", "WHO TAKES PENALTIES?", "…", 40, 560)
         + card(sid, "hm", "PENALTY TAKER", "Him.", 560, 380, "red")
         + calendar(sid, "", "BRUMAIRE", "1799"))
js = JS + """
      needle(10, 0, 0.01);
      tl.set(S + "m-sash", { opacity: 1 }, 0);
      // enough: off comes the sash, he turns and walks out of the revolution
      fly("en", 0.3, C.go - 0.1);
      tl.to(S + "m-armR", { rotation: -150, duration: 0.25 }, 0.5);
      tl.to(S + "m-sash", { y: -300, x: 200, rotation: 60, opacity: 0, duration: 0.6, ease: "power2.out" }, 0.7);
      tl.to(S + "m-armR", { rotation: 0, duration: 0.25 }, 0.9);
      tl.set(S + "m-m-smile", { opacity: 0 }, 0.3); tl.set(S + "m-m-flat", { opacity: 1 }, 0.3);
      run(C.go + 0.2, C.go + 1.6);
      tl.to(S + "mw", { x: 900, duration: 1.4, ease: "power1.in" }, C.go + 0.2);
      // the calendar races to today
      label("cm", [[0, "BRUMAIRE"], [C.go + 0.8, "JANUARY"], [C.rm - 0.2, "TODAY"]]);
      label("cy", [[0, "1799"], [C.go + 0.8, "1850"], [C.go + 1.2, "1914"], [C.go + 1.6, "1969"], [C.go + 2.0, "2018"], [C.rm - 0.2, "2025"]]);
      tl.fromTo(S + "cal", { rotation: 0 }, { rotation: -6, duration: 0.1, yoyo: true, repeat: 9 }, C.go + 0.8);
      // Madrid
      tl.set(S + "A", { opacity: 0 }, C.rm - 0.15); tl.set(S + "B", { opacity: 1 }, C.rm - 0.15);
      fly("rd", C.rm, C.q - 0.1);
      needle(40, C.rm + 0.2);
      tl.set(S + "r-armL", { rotation: -62 }, 0); tl.set(S + "r-armR", { rotation: 62 }, 0);
      // who takes the penalties? the team-mates want it; he shakes his head
      fly("q", C.q, null);
      ["t1", "t2"].forEach((t, i) => {
        tl.to(S + t + "-armR", { rotation: -165, duration: 0.2, ease: "back.out(2)" }, C.q + 0.3 + i * 0.1);
        tl.fromTo(S + t + "w", { y: 0 }, { y: -30, duration: 0.15, yoyo: true, repeat: 3 }, C.q + 0.3 + i * 0.1);
        look(t, -6, 0, C.q + 0.2);
      });
      look("r", 6, 0, C.q + 0.6);
      tl.fromTo(S + "r-head", { rotation: 0 }, { rotation: 10, duration: 0.15, yoyo: true, repeat: 3 }, C.q + 0.9);
      // he does: penalty, goal, arms crossed, crown back on
      uncross(C.him - 0.3, "r");
      kickR(C.him + 0.2, "r");
      arc(S + "ball", C.him + 0.2, 0.55, 600, -90, 60);
      tl.fromTo(S + "goal", { scaleX: 1 }, { scaleX: 1.2, transformOrigin: "0% 100%", duration: 0.12, yoyo: true, repeat: 1 }, C.him + 0.75);
      fly("hm", C.him + 0.1, null, { from: "right" });
      ["t1", "t2"].forEach((t) => { tl.to(S + t + "-armR", { rotation: 0, duration: 0.3 }, C.him + 0.5); tl.set(S + t + "-m-smile", { opacity: 0 }, C.him + 0.5); tl.set(S + t + "-m-flat", { opacity: 1 }, C.him + 0.5); });
      cross(C.him + 1.0, "r");
      tl.set(S + "r-crown", { opacity: 1 }, C.him + 1.3);
      tl.fromTo(S + "r-crown", { y: -500 }, { y: 0, duration: 0.4, ease: "bounce.out", immediateRender: false }, C.him + 1.3);
      needle(80, C.him + 0.9);
"""
scene(sid, w, js, cards, extra_css=CSS)
