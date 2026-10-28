import sys; sys.path.insert(0, __file__.rsplit('/episodes/', 1)[0] + '/tools')  # noqa: E702
from scene import *  # noqa: F403
from rail import station, ruler, ronaldo, train, hline, y_m, SIU_JS, GY, PLAT, M  # noqa: E402
sid = "s6-timetable"
D = TIMING[sid]["duration"]
w = (station(sid) + train(sid, 1300) + ronaldo(sid, 300, PLAT, 0.8)
     + f'<g transform="translate(470,{PLAT - 330})"><g id="{sid}-zz"><text font-family="Inter" font-weight="900" font-size="54" fill="#1a1a2e">z z Z</text></g></g>'
     + f'<g transform="translate(560,{PLAT - 120})"><g id="{sid}-door" opacity="0"><rect x="-60" y="-200" width="120" height="200" rx="10" fill="#2e3b4e" stroke="#1a1a2e" stroke-width="5" /></g></g>')
cards = (banner(sid, "b", "PROBLEM 3", "The Timetable", 60, 330)
         + card(sid, "db", "LONG-DISTANCE TRAINS ON TIME, 2025", "~60 %", 40, 380, "gold")
         + card(sid, "wt", "WAITING", '<span id="s6-timetable-wclk">0 min</span>', 520, 560)
         + card(sid, "so", "SOLUTION", "Take the train", 60, 380, "gold"))
js = SIU_JS + """
      fly("b", C.t, C.db - 0.1);
      fly("db", C.db, C.board - 0.1);
      board([[0, "on time"], [C.db + 0.8, "+10 min"], [C.wait, "+30 min"], [C.again, "+55 min"], [C.again + 0.5, "+90 min"], [C.board, "arriving"]]);
      // he waits ... and waits
      fly("wt", C.wait, C.board - 0.1, { from: "right" });
      const wc = document.getElementById("s6-timetable-wclk"), w = { v: 0 };
      tl.fromTo(w, { v: 0 }, { v: 90, duration: C.board - C.wait, ease: "power1.in", onUpdate() { wc.textContent = Math.round(w.v) + " min"; } }, C.wait);
      tl.to(S + "r-armL", { rotation: -40, duration: 0.3 }, C.wait);
      tl.to(S + "r-armR", { rotation: 40, duration: 0.3 }, C.wait);
      tl.to(S + "r-lids", { opacity: 1, duration: 0.01 }, C.again);
      tl.fromTo(S + "zz", { opacity: 0, y: 0 }, { opacity: 1, y: -40, duration: 1.0, repeat: 1 }, C.again);
      // the train finally rolls in, stops, door opens, he gets on
      tl.fromTo(S + "train", { x: 0 }, { x: -1100, duration: 1.4, ease: "power3.out" }, C.board - 1.2);
      tl.to(S + "zz", { opacity: 0, duration: 0.1 }, C.board - 0.3);
      tl.to(S + "r-lids", { opacity: 0, duration: 0.01 }, C.board);
      tl.to([S + "r-armL", S + "r-armR"], { rotation: 0, duration: 0.3 }, C.board);
      tl.fromTo(S + "door", { opacity: 0 }, { opacity: 1, duration: 0.2 }, C.board + 0.3);
      tl.to(S + "kwrap", { x: 260, duration: 1.0, ease: "power1.inOut" }, C.board + 0.6);
      tl.to(S + "kwrap", { opacity: 0, duration: 0.3 }, C.board + 1.5);
      fly("so", C.board + 0.4, null);
"""
scene(sid, w, js, cards)
