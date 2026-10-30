import sys; sys.path.insert(0, __file__.rsplit('/episodes/', 1)[0] + '/tools')  # noqa: E702
from scene import *  # noqa: F403
from arena import arena, haaland, fighter, MEDITATE_JS, GY  # noqa: E402
sid = "s4-murmillo"
D = TIMING[sid]["duration"]
w = (arena(sid) + fighter(sid, "murmillo", "mur", 720, 1.15) + haaland(sid, 250)
     + f'<g transform="translate(330,{GY - 18})"><g id="{sid}-ball"><g transform="scale(1.2)">{part("football", sid + "-fb")}</g></g></g>'
     + f'<g transform="translate(640,{GY - 300}) scale(1.3)">{part("burst", sid + "-boom", WORD="BOOM")}</g>')
cards = (banner(sid, "b", "ROUND 1", "The Murmillo", 60, 330)
         + card(sid, "ar", "EQUIPMENT", "Sword, helmet, door", 420, 520)
         + card(sid, "sh", "SHIELD", "0 % intact", 560, 380, "red")
         + card(sid, "cf", "MURMILLO CONFIDENCE", "0 %", 60, 560, "red"))
js = MEDITATE_JS + """
      fly("b", C.t, C.arm + 1.0);
      fly("ar", C.arm, C.kick - 0.1, { from: "right" });
      tl.fromTo(S + "murp-sword", { rotation: 0 }, { rotation: -30, svgOrigin: "0 86", duration: 0.35, yoyo: true, repeat: 3 }, C.arm + 0.3);
      // he does what he does best: wind-up ... shot
      swap(S + "h-m-smile", S + "h-m-flat", C.shot);
      tl.to(S + "h-legR", { rotation: 50, duration: 0.5, ease: "power2.out" }, C.shot + 0.6);
      tl.to(S + "h-legR", { rotation: -70, duration: 0.12, ease: "power4.in" }, C.kick);
      tl.to(S + "h-legR", { rotation: 0, duration: 0.3 }, C.kick + 0.4);
      const hit = C.hit - 0.05;
      tl.fromTo(S + "ball", { x: 0, y: 0, rotation: 0 }, { x: 330, y: -150, rotation: 900, duration: hit - C.kick - 0.1, ease: "power1.in" }, C.kick + 0.1);
      // the shield does not survive
      tl.fromTo(S + "boom", { scale: 0, opacity: 0, transformOrigin: "50% 50%" }, { scale: 1, opacity: 1, duration: 0.2, ease: "back.out(3)" }, hit);
      tl.to(S + "boom", { opacity: 0, duration: 0.2 }, hit + 0.9);
      tl.to(S + "murp-shieldL", { x: -140, y: 220, rotation: -70, duration: 0.6, ease: "power2.in" }, hit);
      tl.to(S + "murp-shieldR", { x: 160, y: 240, rotation: 80, duration: 0.6, ease: "power2.in" }, hit);
      tl.to(S + "ball", { x: 200, y: 40, duration: 0.5, ease: "power2.in" }, hit);
      tl.to(S + "mur", { x: 40, duration: 0.2, yoyo: true, repeat: 1 }, hit);
      fly("sh", C.hit + 0.2, C.goal - 0.1, { from: "right" });
      cheer(C.hit + 0.2);
      // neither does his confidence: sword drops, eyes wide
      tl.to(S + "murp-sword", { y: 120, rotation: 80, duration: 0.5, ease: "power2.in" }, C.goal);
      tl.to([S + "murp-pupL", S + "murp-pupR"], { scale: 1.6, transformOrigin: "50% 50%", duration: 0.2 }, C.goal + 0.2);
      fly("cf", C.goal + 0.2, null);
      swap(S + "h-m-flat", S + "h-m-smile", C.goal);
"""
scene(sid, w, js, cards)
