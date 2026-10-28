import sys; sys.path.insert(0, __file__.rsplit('/episodes/', 1)[0] + '/tools')  # noqa: E702
from scene import *  # noqa: F403
sid = "s6-bucket"
rivets = "".join(f'<circle cx="{x}" cy="{y}" r="5" fill="#3d3a36" />' for y in (60, 200, 340) for x in range(40, 984, 110))
drops = "".join(f'<circle id="{sid}-d{i}" cx="0" cy="0" r="{9 - i}" fill="#7fc4e8" stroke="#1a1a2e" stroke-width="3" />' for i in range(4))
world = f"""
<rect x="0" y="0" width="984" height="560" fill="#5b4a3a" />
<g stroke="#3d3a36" stroke-width="6"><path d="M0,130 L984,130 M0,270 L984,270 M0,410 L984,410 M250,0 L250,560 M560,0 L560,560 M870,0 L870,560" /></g>
{rivets}
<g id="{sid}-hole" transform="translate(900,250)"><path d="M-30,-40 L10,-50 L30,-10 L20,40 L-20,50 L-40,10 Z" fill="#0a1428" stroke="#1a1a2e" stroke-width="5" /></g>
<g id="{sid}-jet"><path d="M880,250 Q760,240 700,420 L740,420 Q790,280 890,270 Z" fill="#7fc4e8" stroke="#1a1a2e" stroke-width="4" opacity="0.9" /></g>
<g id="{sid}-water"><rect x="0" y="0" width="984" height="600" fill="#2f6fa8" opacity="0.92" /><path d="M0,0 q30,-12 60,0 t60,0 t60,0 t60,0 t60,0 t60,0 t60,0 t60,0 t60,0 t60,0 t60,0 t60,0 t60,0 t60,0 t60,0 t60,0 t60,0" fill="none" stroke="#1a1a2e" stroke-width="4" /></g>
<g transform="translate(400,520)"><g id="{sid}-kwrap"><g transform="scale(0.85)">{part("keeper", sid + "-k")}</g></g></g>
<g id="{sid}-wfront" opacity="0.55"><rect x="0" y="0" width="984" height="600" fill="#2f6fa8" /></g>
<g id="{sid}-drops" transform="translate(330,250)">{drops}</g>
<g id="{sid}-tag" transform="translate(560,170)"><path d="M-20,-10 L-110,60" stroke="#1a1a2e" stroke-width="4" /><rect x="-10" y="-40" width="320" height="96" rx="12" fill="#f4efe6" stroke="#1a1a2e" stroke-width="5" />
  <text x="150" y="-4" text-anchor="middle" font-family="Inter" font-weight="900" font-size="30" fill="#1a1a2e">NEUER 3300™</text>
  <text x="150" y="34" text-anchor="middle" font-family="Inter" font-weight="900" font-size="28" fill="#e0412f">INDUSTRIAL PUMP</text></g>
"""
js = """
      tl.fromTo(S + "head", { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.2, ease: "power4.out" }, C.t);
      show(S + "r1", C.in); show(S + "r2", C.scoop); show(S + "r3", C.rate);
      // water rises the whole time, whatever he does
      tl.fromTo([S + "water", S + "wfront"], { y: 470 }, { y: 345, duration: D, ease: "power1.in" }, 0);
      tl.fromTo(S + "jet", { scaleX: 0.96, transformOrigin: "100% 0%" }, { scaleX: 1.04, duration: 0.12, ease: "none", repeat: Math.floor(D / 0.12), yoyo: true }, 0);
      tl.fromTo(S + "water path", { x: 0 }, { x: -120, duration: 1.2, ease: "none", repeat: Math.floor(D / 1.2) }, 0);
      // worried look at the hole
      tl.to([S + "k-pupL", S + "k-pupR"], { x: 6, duration: 0.3 }, C.in + 0.2);
      swap(S + "k-m-smile", S + "k-m-o", C.in + 0.4);
      // scooping: one arm-swing per scoop, drops fly out to the left
      const scoop = (at, dur) => {
        tl.fromTo(S + "k-armL", { rotation: 20 }, { rotation: 170, duration: dur, ease: "power2.out" }, at);
        tl.fromTo(S + "k-armR", { rotation: -20 }, { rotation: -170, duration: dur, ease: "power2.out" }, at);
        tl.fromTo(S + "drops circle", { x: 0, y: 0, opacity: 1 }, { x: (i) => -260 - i * 40, y: (i) => -60 + i * 30, opacity: 0, duration: dur * 2, ease: "power1.out", stagger: dur * 0.15 }, at + dur * 0.6);
      };
      [0, 1, 2, 3].forEach((i) => scoop(C.scoop + i * 0.7, 0.35));
      // 3,300 per second: a blur of gloves
      const fast = C.rate + 0.2, stop = C.pump;
      tl.fromTo(S + "k-armL", { rotation: 30 }, { rotation: 170, duration: 0.05, ease: "none", repeat: Math.floor((stop - fast) / 0.05) - 1, yoyo: true }, fast);
      tl.fromTo(S + "k-armR", { rotation: -30 }, { rotation: -170, duration: 0.05, ease: "none", repeat: Math.floor((stop - fast) / 0.05) - 1, yoyo: true }, fast);
      tl.fromTo(S + "kwrap", { x: -3 }, { x: 3, duration: 0.05, repeat: Math.floor((stop - fast) / 0.05) - 1, yoyo: true }, fast);
      tl.fromTo(S + "rate", { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2.5)" }, fast);
      // he is not a goalkeeper ... he is a pump
      tl.set([S + "k-armL", S + "k-armR", S + "kwrap"], { rotation: 0, x: 0 }, stop + 0.01);
      tl.to(S + "k-armL", { rotation: 20, duration: 0.3 }, stop + 0.05);
      tl.to(S + "k-armR", { rotation: -20, duration: 0.3 }, stop + 0.05);
      tl.to([S + "k-pupL", S + "k-pupR"], { x: 0, y: 0, duration: 0.3 }, stop + 0.2);
      swap(S + "k-m-o", S + "k-m-flat", stop + 0.3);
      tl.to(S + "k-lids", { opacity: 1, duration: 0.01 }, stop + 1.2);
      tl.fromTo(S + "tag", { opacity: 0, scale: 0.3, transformOrigin: "0% 50%" }, { opacity: 1, scale: 1, duration: 0.45, ease: "back.out(2.2)" }, C.is + 0.45);
"""
scene(sid, "PLAN C", "The Bucket",
      [("WATER IN (EST.)", "~400 t / min"), ("ONE SCOOP", "2 L"), ("NEEDED", "3,300 scoops / s", "gold")], world, js,
      overlay=f'    <div class="bug" id="{sid}-rate">SCOOPS: <b>3,300 / s</b></div>')
