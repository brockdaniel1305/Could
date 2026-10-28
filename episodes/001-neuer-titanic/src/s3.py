import sys; sys.path.insert(0, __file__.rsplit('/episodes/', 1)[0] + '/tools')  # noqa: E702
from scene import *  # noqa: F403
sid = "s3-neuer"
GY, FY = 900, 1250
ball = lambda n: f'<g id="{sid}-b{n}"><g transform="scale(1.5)">{part("football", sid + "-fb" + str(n))}</g></g>'
world = f"""
{part("pitch-day", sid + "-pitch", GY=GY)}
<g id="{sid}-box" fill="none" stroke="#f4efe6" stroke-width="10" stroke-linejoin="round" opacity="0.9">
  <path d="M-80,{FY} L-200,1700 L860,1700 L740,{FY}" /><path d="M110,{FY} L80,1420 L580,1420 L550,{FY}" />
  <circle cx="330" cy="1560" r="10" fill="#f4efe6" /><path d="M150,1700 Q330,1800 510,1700" />
</g>
<g transform="translate(330,{FY}) scale(2.3)">{part("goal", sid + "-goal")}</g>
<g transform="translate(330,{FY})"><g id="{sid}-kwrap">{part("keeper", sid + "-k")}</g></g>
<g id="{sid}-ruler" transform="translate(490,{FY})">
  <path d="M0,0 L0,-300 M-16,0 L16,0 M-16,-300 L16,-300 M-9,-75 L9,-75 M-9,-150 L9,-150 M-9,-225 L9,-225" stroke="#1a1a2e" stroke-width="6" stroke-linecap="round" />
  <rect x="22" y="-180" width="170" height="64" rx="12" fill="#fff" stroke="#1a1a2e" stroke-width="5" />
  <text x="107" y="-135" text-anchor="middle" font-family="Inter" font-weight="900" font-size="40" fill="#1a1a2e">1.93 m</text>
</g>
<g transform="translate(330,{FY - 330}) scale(1.4)"><g id="{sid}-cup">{part("trophy", sid + "-tro")}</g></g>
<g id="{sid}-q" transform="translate(330,{FY - 140})"><circle r="52" fill="#fff" stroke="#1a1a2e" stroke-width="6" /><text y="22" text-anchor="middle" font-family="Inter" font-weight="900" font-size="64" fill="#1a1a2e">?</text></g>
<g transform="translate(1200,{FY - 200})">{ball(1)}</g>
<g transform="translate(1200,{FY - 140})">{ball(2)}</g>
<g transform="translate(1200,{FY - 260})">{ball(3)}</g>
<g transform="translate(0,{FY})"><g id="{sid}-miniice"><g transform="translate(1260,0) scale(0.45)">{part("iceberg", sid + "-ice")}</g></g></g>
"""
cards = (banner(sid, "b", "SUBJECT B", "Manuel Neuer", 60, 330)
         + card(sid, "wc", "WORLD CUP", "2014 ✓", 470, 360)
         + card(sid, "hab", "HABITAT", "Outside his box", 90, 400, "gold")
         + card(sid, "sv", "SHOTS STOPPED", "Thousands", 300, 360)
         + card(sid, "z", "ICEBERGS STOPPED", "0", 160, 420, "red"))
js = """
      fly("b", C.name, C.wc - 0.1);
      fly("wc", C.wc, C.out, { from: "right" });
      fly("hab", C.out + 0.4, C.ice - 0.1);
      fly("sv", C.ice, C.zero - 0.1, { from: "right" });
      fly("z", C.zero + 0.9, null, { from: "top", rot: 3 });
      // idle in goal: ready stance, blinking
      tl.fromTo(S + "k-armL", { rotation: 25 }, { rotation: 40, duration: 0.5, ease: "sine.inOut", repeat: 3, yoyo: true }, 0);
      tl.fromTo(S + "k-armR", { rotation: -25 }, { rotation: -40, duration: 0.55, ease: "sine.inOut", repeat: 3, yoyo: true }, 0.1);
      blink(S + "k-lids", 1.4); blink(S + "k-lids", 3.6);
      // height ruler grows next to him
      tl.fromTo(S + "ruler", { opacity: 0, scaleY: 0, transformOrigin: "50% 100%" }, { opacity: 1, scaleY: 1, duration: 0.5, ease: "expo.out" }, C.h);
      tl.to(S + "ruler", { opacity: 0, duration: 0.25 }, C.wc);
      // world champion: cup + arms up
      pop(S + "cup", C.wc + 0.3);
      tl.to(S + "k-armL", { rotation: 160, duration: 0.35, ease: "back.out(2)" }, C.wc + 0.3);
      tl.to(S + "k-armR", { rotation: -160, duration: 0.35, ease: "back.out(2)" }, C.wc + 0.38);
      tl.to(S + "cup", { opacity: 0, duration: 0.2 }, C.out);
      // leaves his goal for no reason: sprint right, the goal stays empty
      const run0 = C.out + 0.4, run1 = run0 + 1.6;
      tl.to([S + "k-armL", S + "k-armR"], { rotation: 0, duration: 0.2 }, C.out);
      tl.fromTo(S + "kwrap", { x: 0, rotation: 0 }, { x: 540, rotation: 8, duration: run1 - run0, ease: "power2.inOut" }, run0);
      tl.to(S + "kwrap", { rotation: 0, duration: 0.3, ease: "back.out(2)" }, run1);
      tl.fromTo(S + "k-legL", { rotation: -30 }, { rotation: 30, duration: 0.16, ease: "sine.inOut", repeat: 9, yoyo: true }, run0);
      tl.fromTo(S + "k-legR", { rotation: 30 }, { rotation: -30, duration: 0.16, ease: "sine.inOut", repeat: 9, yoyo: true }, run0);
      tl.fromTo(S + "k-armL", { rotation: 40 }, { rotation: -40, duration: 0.16, ease: "sine.inOut", repeat: 9, yoyo: true }, run0);
      tl.fromTo(S + "k-armR", { rotation: -40 }, { rotation: 40, duration: 0.16, ease: "sine.inOut", repeat: 9, yoyo: true }, run0);
      tl.set([S + "k-legL", S + "k-legR", S + "k-armL", S + "k-armR"], { rotation: 0 }, run1 + 0.02);
      swap(S + "k-m-smile", S + "k-m-o", run0); swap(S + "k-m-o", S + "k-m-smile", run1);
      pop(S + "q", run1 + 0.5);
      tl.to(S + "k-armL", { rotation: 30, duration: 0.3 }, run1 + 0.3);
      tl.to(S + "k-armR", { rotation: -30, duration: 0.3 }, run1 + 0.3);
      // stops fast-moving objects: three balls, three saves (glove at x ~ 870)
      [0, 1, 2].forEach((i) => {
        const at = C.ice + 0.4 + i * 0.9;
        tl.fromTo(S + "b" + (i + 1), { x: 0, rotation: 0 }, { x: -270, rotation: -540, duration: 0.45, ease: "power2.in" }, at);
        tl.to(S + "k-armR", { rotation: -120 + i * 25, duration: 0.15, ease: "power3.out" }, at + 0.3);
        tl.to(S + "b" + (i + 1), { x: -200, y: 300, duration: 0.5, ease: "power2.in" }, at + 0.46);
        tl.to(S + "k-armR", { rotation: -30, duration: 0.3 }, at + 0.6);
      });
      // none of them were icebergs
      tl.fromTo(S + "miniice", { x: 0 }, { x: -270, duration: 0.9, ease: "power3.out" }, C.zero);
      tl.to([S + "k-pupL", S + "k-pupR"], { x: 6, y: 5, duration: 0.25 }, C.zero + 0.6);
      tl.to(S + "k-browL", { y: -8, duration: 0.25 }, C.zero + 0.7);
      swap(S + "k-m-smile", S + "k-m-flat", C.zero + 0.7);
"""
scene(sid, world, js, cards)
