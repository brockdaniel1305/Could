import sys; sys.path.insert(0, __file__.rsplit("/episodes/", 1)[0] + "/tools")  # noqa: E702
from scene import *  # noqa: F403
from rail import *  # noqa: E402,F403
sid = "s2-ronaldo"
D = TIMING[sid]["duration"]
w = (station(sid) + ruler(sid) + hline(sid, "hdr", 2.56, "#ffd23f") + ronaldo(sid, 300, GY, 0.9)
     + f'<g transform="translate(330,{y_m(2.56) - 14})"><g id="{sid}-ball"><g transform="scale(1.1)">{part("football", sid + "-fb")}</g></g></g>'
     + f'<mask id="{sid}-mask"><rect x="0" y="0" width="1080" height="1920" fill="#fff" /><circle cx="300" cy="{GY - 170}" r="300" fill="#000" /></mask>'
     + f'<rect id="{sid}-spot" x="0" y="0" width="1080" height="1920" fill="#000" opacity="0" mask="url(#{sid}-mask)" />'
     + f'<g transform="translate(560,{GY - 420}) scale(1.4)">{part("burst", sid + "-siu", WORD="SIUUU!")}</g>')
cards = (banner(sid, "b", "THE CHALLENGER", "Cristiano Ronaldo", 40, 330)
         + card(sid, "h", "HEIGHT", "1.87 m", 560, 520)
         + card(sid, "hd", "HEADER HEIGHT (2019)", "2.56 m", 520, 380, "gold")
         + card(sid, "wd", "LANDING WORD", "Always the same", 480, 380)
         + scorebug(sid, 0, 0))
js = SIU_JS + SCORE_JS + """
      boardName("ICE 7");
      tl.fromTo(S + "spot", { opacity: 0 }, { opacity: 0.6, duration: 0.4 }, C.name - 0.2);
      fly("b", C.name, C.hdr - 0.1);
      fly("h", C.h, C.hdr - 0.1, { from: "right" });
      fly("hd", C.hdr, C.siu - 0.1, { from: "right" });
      // the 2.56 m header: line, ball, jump, header
      tl.fromTo(S + "hdr", { opacity: 0 }, { opacity: 1, duration: 0.3 }, C.hdr + 0.3);
      tl.fromTo(S + "ball", { x: 500, y: -200, opacity: 1 }, { x: 0, y: 0, duration: 0.7, ease: "power1.in" }, C.hdr + 1.0);
      jump(C.hdr + 1.25, 96, 0.9);
      tl.to(S + "ball", { x: 900, y: -260, duration: 0.6, ease: "power2.out" }, C.hdr + 1.72);
      tl.to(S + "hdr", { opacity: 0, duration: 0.3 }, C.siu);
      fly("wd", C.siu, null, { from: "right" });
      siu(C.word - 0.3);
      tl.fromTo(S + "siu", { scale: 0, opacity: 0, transformOrigin: "50% 50%" }, { scale: 1, opacity: 1, duration: 0.25, ease: "back.out(3)" }, C.word + 0.1);
      blink(S + "r-lids", 2.0); blink(S + "r-lids", 8.0);
"""
scene(sid, w, js, cards, extra_css=SCORE_CSS)
