import sys; sys.path.insert(0, __file__.rsplit('/episodes/', 1)[0] + '/tools')  # noqa: E702
from scene import *  # noqa: F403
sid = "s4-punch"
WL = 1150
world = f"""
{part("sea-night", sid + "-sea", WL=WL)}
<g transform="translate(0,{WL})"><g id="{sid}-icewrap"><g transform="translate(880,0) scale(3.4)">{part("iceberg-under", sid + "-iu")}{part("iceberg", sid + "-ice")}</g></g></g>
<g transform="translate(-1150,{WL + 30}) scale(2.4)"><g id="{sid}-ship">
  {part("titanic", sid + "-tit")}
  <g transform="translate(600,-64) scale(0.42)"><g id="{sid}-kwrap">{part("keeper", sid + "-k")}</g></g>
</g></g>
<g transform="translate(500,820) scale(1.4)">{part("burst", sid + "-bonk", WORD="BONK")}</g>
<g id="{sid}-stars" transform="translate(290,700) scale(2.6)" fill="#ffd23f" stroke="#1a1a2e" stroke-width="2">
  <path d="M-30,0 l5,-12 l5,12 l-12,-7 h14 z" /><path d="M22,-6 l5,-12 l5,12 l-12,-7 h14 z" /><path d="M-4,-22 l5,-12 l5,12 l-12,-7 h14 z" />
</g>
{part("sea-front", sid + "-front", WL=WL + 24)}
"""
cards = (banner(sid, "b", "PLAN A", "The Punch", 60, 330)
         + card(sid, "ball", "ONE FOOTBALL", "0.43 kg", 90, 520)
         + card(sid, "berg", "ICEBERG (EST.)", "1,500,000,000 kg", 90, 380)
         + card(sid, "r", "THAT IS", "≈ 3.5 billion footballs", 60, 400, "gold"))
js = """
      waves(S + "sea-waves1", S + "front-waves2");
      puffs(S + "tit");
      fly("b", C.t, C.berg - 0.1);
      fly("ball", C.ball, C.berg + 0.6, { from: "right" });
      fly("berg", C.berg + 0.9, C.ratio - 0.1);
      fly("r", C.ratio + 1.1, C.busy + 1.2, { from: "top", rot: -2 });
      tl.fromTo(S + "ship", { rotation: -0.5, svgOrigin: "325 0" }, { rotation: 0.5, duration: 1.8, ease: "sine.inOut", repeat: R(D, 1.8), yoyo: true }, 0);
      // keeper on the bow, ready
      tl.fromTo(S + "k-armL", { rotation: 30 }, { rotation: 45, duration: 0.4, ease: "sine.inOut", repeat: 3, yoyo: true }, 0);
      tl.fromTo(S + "k-armR", { rotation: -30 }, { rotation: -45, duration: 0.45, ease: "sine.inOut", repeat: 3, yoyo: true }, 0);
      // the iceberg looms, far too big
      tl.fromTo(S + "icewrap", { x: 720 }, { x: 0, duration: 1.4, ease: "power2.out" }, C.berg);
      tl.to([S + "k-pupL", S + "k-pupR"], { x: 5, y: -5, duration: 0.3 }, C.berg + 0.6);
      swap(S + "k-m-smile", S + "k-m-o", C.berg + 0.7);
      // the punch: wind-up, strike, nothing happens
      const hit = C.ratio + 0.5;
      swap(S + "k-m-o", S + "k-m-flat", C.ratio);
      tl.to(S + "k-armR", { rotation: 20, duration: 0.3, ease: "power2.inOut" }, C.ratio);
      tl.to(S + "kwrap", { x: -10, duration: 0.3, ease: "power2.inOut" }, C.ratio);
      tl.to(S + "k-armR", { rotation: -100, duration: 0.18, ease: "power4.in" }, hit - 0.18);
      tl.to(S + "kwrap", { x: 40, rotation: 10, duration: 0.18, ease: "power4.in" }, hit - 0.18);
      tl.fromTo(S + "bonk", { scale: 0, opacity: 0, transformOrigin: "50% 50%" }, { scale: 1, opacity: 1, duration: 0.25, ease: "back.out(3)" }, hit);
      tl.to(S + "bonk", { opacity: 0, duration: 0.2 }, hit + 0.9);
      tl.fromTo(S + "icewrap", { rotation: 0, svgOrigin: "880 1150" }, { rotation: 0.4, duration: 0.08, yoyo: true, repeat: 1 }, hit);
      swap(S + "ice-smirk", S + "ice-grin", hit + 0.5);
      tl.to([S + "ice-browL", S + "ice-browR"], { y: -10, duration: 0.25, ease: "back.out(3)" }, hit + 0.5);
      // a busy evening: dizzy stars, wobbly head
      tl.to(S + "kwrap", { x: 0, rotation: 0, duration: 0.4, ease: "power2.out" }, hit + 0.3);
      tl.to(S + "k-armR", { rotation: -30, duration: 0.4 }, hit + 0.3);
      swap(S + "k-m-flat", S + "k-m-o", hit + 0.3);
      tl.fromTo(S + "stars", { opacity: 0 }, { opacity: 1, duration: 0.2 }, C.busy);
      tl.fromTo(S + "stars", { rotation: 0, svgOrigin: "290 660" }, { rotation: 360, duration: 1.5, ease: "none", repeat: 1 }, C.busy);
      tl.fromTo(S + "k-head", { rotation: -6 }, { rotation: 6, duration: 0.3, ease: "sine.inOut", repeat: 7, yoyo: true }, C.busy);
      tl.to(S + "k-lids", { opacity: 1, duration: 0.01 }, C.busy + 0.1);
"""
scene(sid, world, js, cards)
