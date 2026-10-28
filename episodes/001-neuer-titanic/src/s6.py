import sys; sys.path.insert(0, __file__.rsplit('/episodes/', 1)[0] + '/tools')  # noqa: E702
from scene import *  # noqa: F403
sid = "s6-bucket"
rivets = "".join(f'<circle cx="{x}" cy="{y}" r="7" fill="#3d3a36" />' for y in (330, 630, 930, 1230) for x in range(60, 1080, 120))
drops = "".join(f'<circle id="{sid}-d{i}" cx="0" cy="0" r="{14 - 2 * i}" fill="#7fc4e8" stroke="#1a1a2e" stroke-width="4" />' for i in range(5))
world = f"""
<rect x="0" y="0" width="1080" height="1920" fill="#5b4a3a" />
<g stroke="#3d3a36" stroke-width="8"><path d="M0,300 L1080,300 M0,600 L1080,600 M0,900 L1080,900 M0,1200 L1080,1200 M0,1500 L1080,1500 M270,0 L270,1920 M660,0 L660,1920" /></g>
{rivets}
<g transform="translate(940,760)"><path d="M-50,-60 L20,-76 L52,-14 L36,60 L-30,76 L-62,16 Z" fill="#0a1428" stroke="#1a1a2e" stroke-width="7" /></g>
<g id="{sid}-jet"><path d="M920,760 Q760,750 700,1120 L770,1120 Q820,800 930,790 Z" fill="#7fc4e8" stroke="#1a1a2e" stroke-width="5" opacity="0.92" /></g>
<g id="{sid}-water"><rect x="0" y="0" width="1080" height="1000" fill="#2f6fa8" opacity="0.92" /><path d="M0,0 q30,-14 60,0 t60,0 t60,0 t60,0 t60,0 t60,0 t60,0 t60,0 t60,0 t60,0 t60,0 t60,0 t60,0 t60,0 t60,0 t60,0 t60,0 t60,0 t60,0 t60,0" fill="none" stroke="#1a1a2e" stroke-width="5" /></g>
<g transform="translate(500,1300)"><g id="{sid}-kwrap"><g transform="scale(1.2)">{part("keeper", sid + "-k")}</g></g></g>
<g id="{sid}-wfront" opacity="0.55"><rect x="0" y="0" width="1080" height="1000" fill="#2f6fa8" /></g>
<g id="{sid}-drops" transform="translate(400,930)">{drops}</g>
"""
cards = (banner(sid, "b", "PLAN C", "The Bucket", 60, 330)
         + card(sid, "in", "WATER IN (EST.)", "~400 t / min", 330, 420)
         + card(sid, "sc", "ONE SCOOP", "2 L", 80, 420)
         + card(sid, "nd", "NEEDED", "3,300 scoops / s", 80, 420, "gold")
         + card(sid, "tag", "MODEL", 'NEUER 3300™<div style="font: 900 40px/1.2 Inter; color: #e0412f;">INDUSTRIAL PUMP</div>', 300, 560))
js = """
      fly("b", C.t, C.in + 1.4);
      fly("in", C.in + 0.3, C.scoop - 0.1, { from: "right" });
      fly("sc", C.scoop, C.rate - 0.1);
      fly("nd", C.rate, C.is - 0.1, { from: "right" });
      fly("tag", C.is + 0.45, null, { from: "top", rot: 4 });
      // water rises the whole time, whatever he does
      tl.fromTo([S + "water", S + "wfront"], { y: 1500 }, { y: 1085, duration: D, ease: "power1.in" }, 0);
      tl.fromTo(S + "jet", { scaleX: 0.96, transformOrigin: "100% 0%" }, { scaleX: 1.04, duration: 0.12, ease: "none", repeat: R(D, 0.12), yoyo: true }, 0);
      tl.fromTo(S + "water path", { x: 0 }, { x: -120, duration: 1.2, ease: "none", repeat: R(D, 1.2) }, 0);
      // worried look at the hole
      tl.to([S + "k-pupL", S + "k-pupR"], { x: 6, duration: 0.3 }, C.in + 0.2);
      swap(S + "k-m-smile", S + "k-m-o", C.in + 0.4);
      // scooping: one arm swing per scoop, drops fly out to the left
      const scoop = (at, dur) => {
        tl.fromTo(S + "k-armL", { rotation: 20 }, { rotation: 170, duration: dur, ease: "power2.out" }, at);
        tl.fromTo(S + "k-armR", { rotation: -20 }, { rotation: -170, duration: dur, ease: "power2.out" }, at);
        tl.fromTo(S + "drops circle", { x: 0, y: 0, opacity: 1 }, { x: (i) => -360 - i * 50, y: (i) => -120 + i * 40, opacity: 0, duration: dur * 2, ease: "power1.out", stagger: dur * 0.15 }, at + dur * 0.6);
      };
      [0, 1, 2, 3].forEach((i) => scoop(C.scoop + i * 0.7, 0.35));
      // 3,300 per second: a blur of gloves
      const fast = C.rate + 0.2, stop = C.pump;
      tl.fromTo(S + "k-armL", { rotation: 30 }, { rotation: 170, duration: 0.05, ease: "none", repeat: R(stop - fast, 0.05), yoyo: true }, fast);
      tl.fromTo(S + "k-armR", { rotation: -30 }, { rotation: -170, duration: 0.05, ease: "none", repeat: R(stop - fast, 0.05), yoyo: true }, fast);
      tl.fromTo(S + "kwrap", { x: -4 }, { x: 4, duration: 0.05, repeat: R(stop - fast, 0.05), yoyo: true }, fast);
      // he is not a goalkeeper ... he is a pump
      tl.set([S + "k-armL", S + "k-armR", S + "kwrap"], { rotation: 0, x: 0 }, stop + 0.01);
      tl.to(S + "k-armL", { rotation: 20, duration: 0.3 }, stop + 0.05);
      tl.to(S + "k-armR", { rotation: -20, duration: 0.3 }, stop + 0.05);
      tl.to([S + "k-pupL", S + "k-pupR"], { x: 0, y: 0, duration: 0.3 }, stop + 0.2);
      swap(S + "k-m-o", S + "k-m-flat", stop + 0.3);
      tl.to(S + "k-lids", { opacity: 1, duration: 0.01 }, stop + 1.2);
"""
scene(sid, world, js, cards)
