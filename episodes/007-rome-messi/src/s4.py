import sys; sys.path.insert(0, __file__.rsplit("/episodes/", 1)[0] + "/tools")  # noqa: E702
from scene import *  # noqa: F403
from battle import *  # noqa: E402,F403
import json
sid = "s4-standoff"
D = TIMING[sid]["duration"]
front = ["r1", "r2", "r3", "r4"]
cu_r = (f'<g id="{sid}-cuR" opacity="0"><rect width="1080" height="1920" fill="#1a1a2e" /><rect x="0" y="560" width="1080" height="560" fill="#d9a77a" />'
        f'<rect x="0" y="560" width="1080" height="110" fill="#c9a24a" stroke="#1a1a2e" stroke-width="8" />'
        + "".join(f'<ellipse cx="{x}" cy="880" rx="140" ry="96" fill="#fff" stroke="#1a1a2e" stroke-width="10" /><circle class="cuRp" cx="{x}" cy="890" r="48" fill="#1a1a2e" />' for x in (310, 770))
        + '<path d="M150,740 L440,800 M640,800 L930,740" stroke="#1a1a2e" stroke-width="30" stroke-linecap="round" /></g>')
cu_m = (f'<g id="{sid}-cuM" opacity="0"><rect width="1080" height="1920" fill="#1a1a2e" /><rect x="0" y="560" width="1080" height="560" fill="#e3b48c" />'
        f'<path d="M0,560 L1080,560 L1080,650 Q540,700 0,650 Z" fill="#3b2416" />'
        + "".join(f'<ellipse cx="{x}" cy="890" rx="130" ry="86" fill="#fff" stroke="#1a1a2e" stroke-width="10" /><circle cx="{x + 10}" cy="900" r="44" fill="#1a1a2e" />'
                  f'<path d="M{x - 140},880 Q{x},780 {x + 140},880 L{x + 140},800 L{x - 140},800 Z" fill="#e3b48c" stroke="#1a1a2e" stroke-width="10" />' for x in (310, 770))
        + '<path d="M170,770 Q310,740 450,770 M630,770 Q770,740 910,770" stroke="#3b2416" stroke-width="22" fill="none" stroke-linecap="round" /></g>')
tumble = f'<g transform="translate(-160,{GY - 50})"><g id="{sid}-tw"><g id="{sid}-twr"><circle r="46" fill="none" stroke="#b5845a" stroke-width="7" /><path d="M-40,-10 Q0,-60 40,8 M-30,30 Q0,-20 34,-30 M-20,-40 Q10,10 -10,44" fill="none" stroke="#8a6f52" stroke-width="6" /></g></g></g>'
w = (field(sid) + army_defs(sid) + army(sid, 560, cols=5, rows=4)
     + "".join(roman(sid, r, 580 + i * 140) for i, r in enumerate(front))
     + messi(sid, 200) + ball(sid, 244) + tumble + cu_r + cu_m)
cards = (banner(sid, "b", "THE BATTLE", "The standoff", 40, 330)
         + card(sid, "ro", "ROMANS", "380,000", 560, 560, "red")
         + card(sid, "me", "MESSI", "1", 40, 560, "gold")
         + card(sid, "od", "THE ODDS", "380,000 : 1", 40, 380, "red")
         + scorebug(sid, 0, 0))
js = JS + f"""
      const front = {json.dumps(front)};
""" + """
      fly("b", 0.1, C.line + 1.6, { from: "top" });
      // they close ranks: step together, shields lock (clang)
      front.forEach((r, i) => tl.to(S + r, { x: -14 * i, duration: 0.3, ease: "power2.out" }, C.line + 0.6));
      front.forEach((r) => tl.fromTo(S + r + "p-shield", { x: 0 }, { x: 14, duration: 0.15, ease: "power2.out" }, C.line + 0.6));
      front.forEach((r) => stompR(r, C.line + 0.9));
      fly("ro", C.line + 0.3, C.odds - 0.1, { from: "right" });
      fly("me", C.one, C.odds - 0.1);
      look("m", 6, 0, C.one);
      fly("od", C.odds, C.still - 1.4);
      // extreme close-ups: Roman eyes (scanning), then Messi's (calm)
      tl.set(S + "cuR", { opacity: 1 }, C.still - 1.3); tl.set(S + "cuR", { opacity: 0 }, C.still - 0.1);
      tl.fromTo(S + "cuR .cuRp", { x: -30 }, { x: 30, duration: 0.3, yoyo: true, repeat: 3, ease: "sine.inOut" }, C.still - 1.3);
      tl.set(S + "cuM", { opacity: 1 }, C.still - 0.1); tl.set(S + "cuM", { opacity: 0 }, C.still + 1.0);
      // tumbleweed, wind, a drop of sweat
      tl.fromTo(S + "tw", { x: 0 }, { x: 1400, duration: 2.6, ease: "none" }, C.still + 0.3);
      tl.fromTo(S + "twr", { rotation: 0 }, { rotation: 720, duration: 2.6, ease: "none", transformOrigin: "50% 50%" }, C.still + 0.3);
      tl.fromTo(S + "tw", { y: 0 }, { y: -30, duration: 0.32, yoyo: true, repeat: 7, ease: "sine.out" }, C.still + 0.3);
      tl.set(S + "r1p-sweat", { opacity: 1 }, C.still + 1.1);
      tl.fromTo(S + "r1p-sweat", { y: 0 }, { y: 40, duration: 0.9, ease: "power1.in" }, C.still + 1.1);
      tl.set(S + "r1p-sweat", { opacity: 0 }, C.still + 2.0);
      // Messi checks his laces (crouch, hand to the boot), the whole army leans in to look
      tl.to(S + "mw", { y: 30, duration: 0.3, ease: "power2.out" }, C.laces);
      tl.to(S + "m-body", { rotation: 22, transformOrigin: "50% 100%", duration: 0.3 }, C.laces);
      tl.to(S + "m-armR", { rotation: -30, duration: 0.3 }, C.laces);
      tl.fromTo(S + "m-armR", { rotation: -30 }, { rotation: -10, duration: 0.15, yoyo: true, repeat: 3 }, C.laces + 0.3);
      tl.to(S + "mw", { y: 0, duration: 0.3 }, C.laces + 1.3);
      tl.to(S + "m-body", { rotation: 0, duration: 0.3 }, C.laces + 1.3);
      tl.to(S + "m-armR", { rotation: 0, duration: 0.3 }, C.laces + 1.3);
      front.forEach((r) => tl.to(S + r, { rotation: -7, transformOrigin: "50% 100%", duration: 0.5, ease: "power2.out" }, C.laces + 0.4));
      tl.to(S + "a", { skewX: 6, transformOrigin: "50% 100%", duration: 0.6, ease: "power2.out" }, C.laces + 0.5);
      front.forEach((r) => look(r + "p", -6, 6, C.laces + 0.4));
"""
scene(sid, w, js, cards, extra_css=CSS)
