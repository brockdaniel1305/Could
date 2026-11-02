import sys; sys.path.insert(0, __file__.rsplit("/episodes/", 1)[0] + "/tools")  # noqa: E702
from scene import *  # noqa: F403
from match import *  # noqa: E402,F403
import random
sid = "s3-kickoff"
D = TIMING[sid]["duration"]
rnd = random.Random(5)
dots = "".join(f'<g transform="translate({x},{y})"><g id="{sid}-d{i}"><circle r="24" fill="#f4f4f2" stroke="#1a1a2e" stroke-width="5" />'
               f'<text data-layout-ignore x="0" y="9" text-anchor="middle" font-family="Inter" font-weight="900" font-size="26" fill="#1a1a2e">{n}</text></g></g>'
               for i, ((x, y), n) in enumerate(zip([(540, 420), (300, 520), (780, 520), (200, 680), (420, 650), (660, 650), (880, 680), (320, 820), (760, 820), (430, 930), (650, 930)], REAL_NUMS)))
top = (f'<g id="{sid}-top"><rect x="0" y="0" width="1080" height="1920" fill="#4f9a45" />'
       + "".join(f'<rect x="0" y="{y}" width="1080" height="120" fill="#5aa84f" />' for y in range(0, 1920, 240))
       + '<g fill="none" stroke="#f4f4f2" stroke-width="8"><rect x="60" y="200" width="960" height="1500" /><path d="M60,1100 L1020,1100" /><circle cx="540" cy="1100" r="140" /><rect x="340" y="200" width="400" height="220" /></g>'
       + dots + f'<g transform="translate(540,1100)"><g id="{sid}-me"><circle r="28" fill="#a50044" stroke="#1a1a2e" stroke-width="5" /><path d="M-10,-26 L-10,26 M10,-26 L10,26" stroke="#1d3f9b" stroke-width="8" /></g></g></g>')
side = (f'<g id="{sid}-side" opacity="0">' + world(sid + "-s", player(sid, "a", 560, 1040, 0.5, num=4, **REAL) + player(sid, "b", 700, 1060, 0.5, num=5, **REAL)
        + messi_fig(sid, 300, 1060, 0.55, name="m") + football(sid, 345, 1048, 0.5)
        + f'<g transform="translate(560,{1040 - 205})"><g id="{sid}-qa" opacity="0"><text data-layout-ignore x="0" y="0" text-anchor="middle" font-family="Inter" font-weight="900" font-size="44" fill="#ffd23f" stroke="#1a1a2e" stroke-width="3" paint-order="stroke">???</text></g></g>'
        + f'<g transform="translate(700,{1060 - 205})"><g id="{sid}-qb" opacity="0"><text data-layout-ignore x="0" y="0" text-anchor="middle" font-family="Inter" font-weight="900" font-size="44" fill="#ffd23f" stroke="#1a1a2e" stroke-width="3" paint-order="stroke">???</text></g></g>')
        + "</g>")
w = top + side
cards = (hud(sid, h=0, a=0, minute="1'") + card(sid, "pr", "REAL PRESS WITH", "All 11", 40, 380, "red")
         + card(sid, "pa", "PASSING OPTIONS", "0", 560, 560) + card(sid, "ot", "ONE-TWO WITH", "The ad board", 40, 380, "gold"))
js = JS + """
      stamina(95);
      // top-down: all eleven close in on Messi
      for (let i = 0; i < 11; i++) tl.to(S + "d" + i, { x: (i % 2 ? 1 : -1) * 20 + (540 - [540,300,780,200,420,660,880,320,760,430,650][i]) * 0.72,
        y: (1100 - [420,520,520,680,650,650,680,820,820,930,930][i]) * 0.72, duration: 1.6, ease: "power2.inOut" }, C.press);
      fly("pr", C.press, C.none - 0.1);
      tl.fromTo(S + "me", { scale: 1 }, { scale: 1.25, transformOrigin: "50% 50%", duration: 0.2, yoyo: true, repeat: 3 }, C.none);
      fly("pa", C.none, C.board - 0.1, { from: "right" });
      label("min", [[0, "1'"], [C.press, "2'"], [C.board, "4'"]]);
      // side view: the ball bounces off the ad board and back to him, past two baffled defenders
      tl.set(S + "top", { opacity: 0 }, C.board - 0.05); tl.set(S + "side", { opacity: 1 }, C.board - 0.05);
      fly("ot", C.board + 0.1, null);
      const K = C.board + 0.4;
      arc(S + "ball", K, 0.45, 170, -120, 20, S + "ball-spin");
      tl.to(S + "ball", { x: 420, y: 0, duration: 0.5, ease: "power1.out" }, K + 0.45);
      run("m", K, K + 1.6);
      tl.to(S + "m", { x: 520, duration: 1.4, ease: "power1.inOut" }, K + 0.1);
      tl.to(S + "ball", { x: 560, duration: 0.6 }, K + 0.95);
      for (const q of ["qa", "qb"]) tl.fromTo(S + q, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.2, ease: "back.out(3)" }, K + 0.5);
      look("ap", 6, 0, K + 0.4); look("bp", -6, 0, K + 0.4);
      for (let j = 0; j < 24; j++) tl.fromTo(S + "s-fc" + j, { y: 0 }, { y: -5, duration: 0.3, yoyo: true, repeat: R(D, 0.3) }, (j % 5) * 0.06);
"""
scene(sid, w, js, cards, extra_css=CSS)
