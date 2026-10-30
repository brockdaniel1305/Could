import sys; sys.path.insert(0, __file__.rsplit('/episodes/', 1)[0] + '/tools')  # noqa: E702
from scene import *  # noqa: F403
from arena import arena, haaland, fighter, MEDITATE_JS, GY  # noqa: E402
sid = "s5-retiarius"
D = TIMING[sid]["duration"]
mesh = "".join(f'<path d="M{-150 + i * 30},-150 L{-150 + i * 30},150" />' for i in range(11)) + "".join(f'<path d="M-150,{-150 + i * 30} L150,{-150 + i * 30}" />' for i in range(11))
w = (arena(sid) + fighter(sid, "retiarius", "ret", 760, 1.1) + haaland(sid, 280)
     + f'<g transform="translate(280,{GY - 200})"><g id="{sid}-net"><g stroke="#d8c59a" stroke-width="7" fill="none">{mesh}</g><g stroke="#1a1a2e" stroke-width="2" fill="none" opacity="0.6">{mesh}</g></g></g>'
     + f'<g transform="translate(400,{GY - 440})"><g id="{sid}-hearts" fill="#e0412f" stroke="#1a1a2e" stroke-width="4"><path d="M0,20 C-36,-6 -24,-36 0,-18 C24,-36 36,-6 0,20 Z" /><path transform="translate(70,-40) scale(0.7)" d="M0,20 C-36,-6 -24,-36 0,-18 C24,-36 36,-6 0,20 Z" /></g></g>')
cards = (banner(sid, "b", "ROUND 2", "The Retiarius", 60, 330)
         + card(sid, "wp", "WEAPONS", "Trident & net", 520, 520)
         + card(sid, "cr", "HAALAND'S CAREER", "In the back of the net", 60, 380, "gold")
         + card(sid, "fl", "FEELING", "Right at home", 420, 560))
js = MEDITATE_JS + f"""
      fly("b", C.t, C.net + 0.9);
      fly("wp", C.net, C.home - 0.1, {{ from: "right" }});
      tl.fromTo(S + "retp-trident", {{ y: 0 }}, {{ y: -12, duration: 0.3, yoyo: true, repeat: 3 }}, C.net + 0.3);
      // the throw: the net flies over and opens around Haaland
      tl.to(S + "retp-armL", {{ rotation: 160, duration: 0.25, ease: "power3.out" }}, C.throw - 0.1);
      tl.fromTo(S + "net", {{ x: 460, y: -60, scale: 0.15, rotation: -40, opacity: 1, transformOrigin: "50% 50%" }}, {{ x: 0, y: 0, scale: 1, rotation: 0, duration: 0.7, ease: "power2.out" }}, C.throw);
      tl.to(S + "retp-armL", {{ rotation: 0, duration: 0.3 }}, C.throw + 0.5);
      swap(S + "h-m-smile", S + "h-m-o", C.throw + 0.5);
      // ... he has spent his whole career in the back of the net
      fly("cr", C.home, C.feel - 0.1);
      swap(S + "h-m-o", S + "h-m-smile", C.home + 0.6);
      tl.to(S + "h-armL", {{ rotation: 160, duration: 0.3, ease: "back.out(2)" }}, C.home + 0.7);
      tl.to(S + "h-armR", {{ rotation: -160, duration: 0.3, ease: "back.out(2)" }}, C.home + 0.75);
      cheer(C.home + 0.8);
      fly("fl", C.feel, null, {{ from: "right" }});
      pop(S + "hearts", C.feel + 0.3);
      tl.to([S + "retp-pupL", S + "retp-pupR"], {{ x: -6, duration: 0.2 }}, C.feel);
      swap(S + "retp-m-smile", S + "retp-m-o", C.feel + 0.2);
"""
scene(sid, w, js, cards)
