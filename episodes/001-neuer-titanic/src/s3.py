import sys; sys.path.insert(0, __file__.rsplit('/episodes/', 1)[0] + '/tools')  # noqa: E702
from scene import *  # noqa: F403
sid = "s3-neuer"
GY = 300
ball = lambda n: f'<g id="{sid}-b{n}">{part("football", sid + "-fb" + str(n))}</g>'
world = f"""
{part("pitch-day", sid + "-pitch", GY=GY)}
<g transform="translate(190,{GY + 170})">{part("goal", sid + "-goal")}</g>
<g transform="translate(190,{GY + 200})"><g id="{sid}-kwrap"><g transform="scale(0.78)">{part("keeper", sid + "-k")}</g></g></g>
<g id="{sid}-ruler" transform="translate(300,{GY + 200})">
  <path d="M0,0 L0,-236 M-12,0 L12,0 M-12,-236 L12,-236 M-7,-59 L7,-59 M-7,-118 L7,-118 M-7,-177 L7,-177" stroke="#1a1a2e" stroke-width="5" stroke-linecap="round" />
  <rect x="16" y="-142" width="118" height="44" rx="8" fill="#fff" stroke="#1a1a2e" stroke-width="4" />
  <text x="75" y="-108" text-anchor="middle" font-family="Inter" font-weight="900" font-size="30" fill="#1a1a2e">1.93 m</text>
</g>
<g transform="translate(190,{GY - 60})"><g id="{sid}-cup">{part("trophy", sid + "-tro")}</g></g>
<g id="{sid}-q" transform="translate(190,{GY + 90})"><circle r="38" fill="#fff" stroke="#1a1a2e" stroke-width="5" /><text y="16" text-anchor="middle" font-family="Inter" font-weight="900" font-size="48" fill="#1a1a2e">?</text></g>
<g transform="translate(1060,{GY - 40})">{ball(1)}</g>
<g transform="translate(1060,{GY + 10})">{ball(2)}</g>
<g transform="translate(1060,{GY - 80})">{ball(3)}</g>
<g transform="translate(0,{GY + 200})"><g id="{sid}-miniice"><g transform="translate(1100,0) scale(0.34)">{part("iceberg", sid + "-ice")}</g></g></g>
"""
js = """
      // facts
      tl.fromTo(S + "head", { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.2, ease: "power4.out" }, C.name);
      show(S + "r1", C.h); show(S + "r2", C.wc); show(S + "r3", C.out + 0.4);
      // idle in goal: ready stance, blinking
      tl.fromTo([S + "k-armL"], { rotation: 25 }, { rotation: 40, duration: 0.5, ease: "sine.inOut", repeat: 3, yoyo: true }, 0);
      tl.fromTo([S + "k-armR"], { rotation: -25 }, { rotation: -40, duration: 0.55, ease: "sine.inOut", repeat: 3, yoyo: true }, 0.1);
      blink(S + "k-lids", 1.4); blink(S + "k-lids", 3.6);
      // height ruler
      tl.fromTo(S + "ruler", { opacity: 0, scaleY: 0, svgOrigin: "300 500" }, { opacity: 1, scaleY: 1, duration: 0.5, ease: "expo.out" }, C.h);
      tl.to(S + "ruler", { opacity: 0, duration: 0.25 }, C.wc);
      // world champion: cup + arms up
      pop(S + "cup", C.wc + 0.3);
      tl.to(S + "k-armL", { rotation: 160, duration: 0.35, ease: "back.out(2)" }, C.wc + 0.3);
      tl.to(S + "k-armR", { rotation: -160, duration: 0.35, ease: "back.out(2)" }, C.wc + 0.38);
      tl.to(S + "cup", { opacity: 0, duration: 0.2 }, C.out);
      // leaves his goal for no reason: sprint right, goal left empty
      const run0 = C.out + 0.4, run1 = run0 + 1.6;
      tl.to([S + "k-armL", S + "k-armR"], { rotation: 0, duration: 0.2 }, C.out);
      tl.fromTo(S + "kwrap", { x: 0, rotation: 0 }, { x: 560, rotation: 8, duration: run1 - run0, ease: "power2.inOut" }, run0);
      tl.to(S + "kwrap", { rotation: 0, duration: 0.3, ease: "back.out(2)" }, run1);
      tl.fromTo(S + "k-legL", { rotation: -30 }, { rotation: 30, duration: 0.16, ease: "sine.inOut", repeat: 9, yoyo: true }, run0);
      tl.fromTo(S + "k-legR", { rotation: 30 }, { rotation: -30, duration: 0.16, ease: "sine.inOut", repeat: 9, yoyo: true }, run0);
      tl.fromTo(S + "k-armL", { rotation: 40 }, { rotation: -40, duration: 0.16, ease: "sine.inOut", repeat: 9, yoyo: true }, run0);
      tl.fromTo(S + "k-armR", { rotation: -40 }, { rotation: 40, duration: 0.16, ease: "sine.inOut", repeat: 9, yoyo: true }, run0);
      tl.set([S + "k-legL", S + "k-legR", S + "k-armL", S + "k-armR"], { rotation: 0 }, run1 + 0.02);
      swap(S + "k-m-smile", S + "k-m-o", run0); swap(S + "k-m-o", S + "k-m-smile", run1);
      pop(S + "q", run1 + 0.5);
      // hands on hips, pleased
      tl.to(S + "k-armL", { rotation: 30, duration: 0.3 }, run1 + 0.3);
      tl.to(S + "k-armR", { rotation: -30, duration: 0.3 }, run1 + 0.3);
      // stops fast-moving objects: three balls, three saves (glove at keeper x 750)
      [0, 1, 2].forEach((i) => {
        const at = C.ice + 0.4 + i * 0.9;
        tl.fromTo(S + "b" + (i + 1), { x: 0, rotation: 0 }, { x: -260, rotation: -540, duration: 0.45, ease: "power2.in" }, at);
        tl.to(S + "k-armR", { rotation: -120 + i * 25, duration: 0.15, ease: "power3.out" }, at + 0.3);
        tl.to(S + "b" + (i + 1), { x: -200, y: 260, duration: 0.5, ease: "power2.in" }, at + 0.46);
        tl.to(S + "k-armR", { rotation: -30, duration: 0.3 }, at + 0.6);
      });
      // none of them were icebergs
      tl.fromTo(S + "miniice", { x: 0 }, { x: -260, duration: 0.9, ease: "power3.out" }, C.zero);
      tl.to([S + "k-pupL", S + "k-pupR"], { x: 6, y: 5, duration: 0.25 }, C.zero + 0.6);
      tl.to(S + "k-browL", { y: -8, rotation: -12, svgOrigin: "-17 -19", duration: 0.25 }, C.zero + 0.7);
      swap(S + "k-m-smile", S + "k-m-flat", C.zero + 0.7);
      tl.fromTo(S + "zero", { opacity: 0, scale: 0.4 }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2.5)" }, C.zero + 0.9);
"""
scene(sid, "SUBJECT B", "Manuel Neuer",
      [("HEIGHT", "1.93 m"), ("WORLD CUP", "2014 ✓"), ("HABITAT", "Outside his box", "gold")], world, js,
      overlay=f'    <div class="bug" id="{sid}-zero">ICEBERGS STOPPED: <b>0</b></div>')
