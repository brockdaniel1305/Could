import sys; sys.path.insert(0, __file__.rsplit("/episodes/", 1)[0] + "/tools")  # noqa: E702
from scene import *  # noqa: F403
from rail import *  # noqa: E402,F403
sid = "s4-round2"
D = TIMING[sid]["duration"]
w = (station(sid) + ruler(sid) + ronaldo(sid, 400, GY, 0.9)
     + f'<g transform="translate(480,{GY - 360})"><g id="{sid}-zz" opacity="0"><text font-family="Inter" font-weight="900" font-size="54" fill="#1a1a2e">z z Z</text></g></g>')
cards = (banner(sid, "b", "ROUND 2 OF 3", "The Intercity", 60, 330)
         + card(sid, "v", "TOP SPEED", "200 km/h", 60, 560, "gold")
         + card(sid, "db", "LONG-DISTANCE TRAINS ON TIME, 2025", "~60 %", 40, 380, "gold")
         + card(sid, "wt", "WAITING", f'<span id="{sid}-wclk">0 min</span>', 560, 560)
         + card(sid, "cx", "IC 2024", "Cancelled", 60, 380, "red")
         + card(sid, "lo", "TRAINS THAT HIT HIM", "0", 560, 560, "gold")
         + scorebug(sid, 0, 1))
js = SIU_JS + SCORE_JS + """
      boardName("IC 2024");
      board([[0, "on time"], [C.db + 0.8, "+10 min"], [C.wait, "+25 min"], [C.again, "+47 min"], [C.cancel, "cancelled"]]);
      fly("b", C.name, C.db - 0.1);
      fly("v", C.v, C.db - 0.1);
      // ready: crouch, arms out, eyes right
      tl.to(S + "kwrap", { y: 14, duration: 0.3, ease: "power2.out" }, C.ready);
      tl.to(S + "r-armL", { rotation: 55, duration: 0.3 }, C.ready);
      tl.to(S + "r-armR", { rotation: -55, duration: 0.3 }, C.ready);
      tl.to([S + "r-pupL", S + "r-pupR"], { x: 7, duration: 0.2 }, C.ready);
      fly("db", C.db, C.wait - 0.1);
      // he waits ... and waits
      fly("wt", C.wait, C.cancel - 0.1, { from: "right" });
      const wc = document.getElementById("s4-round2-wclk"), wv = { v: 0 };
      tl.fromTo(wv, { v: 0 }, { v: 47, duration: C.cancel - C.wait, ease: "power1.in", onUpdate() { wc.textContent = Math.round(wv.v) + " min"; } }, C.wait);
      tl.to(S + "kwrap", { y: 0, duration: 0.4 }, C.wait);
      tl.to(S + "r-armL", { rotation: -30, duration: 0.4 }, C.wait);
      tl.to(S + "r-armR", { rotation: 30, duration: 0.4 }, C.wait);
      tl.to(S + "r-lids", { opacity: 1, duration: 0.01 }, C.again);
      tl.fromTo(S + "zz", { opacity: 0, y: 0 }, { opacity: 1, y: -40, duration: 0.7 }, C.again);
      // cancelled: he wakes up
      tl.to(S + "zz", { opacity: 0, duration: 0.1 }, C.cancel);
      tl.to(S + "r-lids", { opacity: 0, duration: 0.01 }, C.cancel);
      swap(S + "r-m-smile", S + "r-m-o", C.cancel);
      tl.to(S + "r-head", { rotation: -8, duration: 0.2, yoyo: true, repeat: 1 }, C.cancel + 0.1);
      fly("cx", C.cancel + 0.1, C.score - 0.1);
      tl.fromTo(S + "st-board", { rotation: 0 }, { rotation: 3, transformOrigin: "50% 0%", duration: 0.1, yoyo: true, repeat: 3 }, C.cancel);
      // ... a train that never arrives cannot hit you
      fly("lo", C.logic, null, { from: "right" });
      swap(S + "r-m-o", S + "r-m-smile", C.logic + 0.4);
      tl.to(S + "r-armR", { rotation: -165, duration: 0.25, ease: "back.out(2)" }, C.score);
      tl.fromTo(S + "r-armR", { rotation: -165 }, { rotation: -140, duration: 0.2, yoyo: true, repeat: 3 }, C.score + 0.25);
      score(C.score, 1, 1, "sa");
"""
scene(sid, w, js, cards, extra_css=SCORE_CSS)
