import sys; sys.path.insert(0, __file__.rsplit('/episodes/', 1)[0] + '/tools')  # noqa: E702
from scene import *  # noqa: F403
sid = "s1-hook"
WL = 1150
world = f"""
{part("sea-night", sid + "-sea", WL=WL)}
<g transform="translate(930,{WL}) scale(1.5)">{part("iceberg-under", sid + "-iu")}{part("iceberg", sid + "-ice")}</g>
<g transform="translate(-420,{WL + 24}) scale(1.5)"><g id="{sid}-ship">
  {part("titanic", sid + "-tit")}
  <g transform="translate(585,-64) scale(0.6)">{part("keeper", sid + "-k")}</g>
</g></g>
{part("sea-front", sid + "-front", WL=WL + 22)}
"""
cards = (banner(sid, "q", "CASE FILE 001", "Could Manuel Neuer<br>save the Titanic?", 60, 330)
         + card(sid, "m", "METHOD", "Scientific", 120, 400, w=None)
         + card(sid, "t", "TIME SPENT", "Far too long", 230, 590, "gold"))
js = """
      // v3: opening punch-in (new first frame)
      tl.fromTo(S + "svg", { scale: 1.14 }, { scale: 1, transformOrigin: "50% 60%", duration: 0.8, ease: "power2.out" }, 0);
      waves(S + "sea-waves1", S + "front-waves2");
      puffs(S + "tit");
      tl.fromTo(S + "ship", { x: 0, rotation: -0.8, svgOrigin: "325 0" }, { x: 30, rotation: 0.8, duration: D, ease: "sine.inOut" }, 0);
      // frame 0 is the thumbnail: the question is already on screen
      tl.fromTo(S + "c-q", { opacity: 1, x: 0, y: 0, rotation: -2 }, { y: -1100, rotation: 8, duration: 0.4, ease: "power3.in" }, C.sci - 0.45);
      // keeper waves at the camera, then notices the iceberg
      tl.fromTo(S + "k-armR", { rotation: -150 }, { rotation: -120, duration: 0.3, ease: "sine.inOut", repeat: 5, yoyo: true }, 0);
      tl.to(S + "k-armR", { rotation: 0, duration: 0.4, ease: "power2.inOut" }, 1.9);
      tl.to([S + "k-pupL", S + "k-pupR"], { x: 5, duration: 0.25, ease: "power2.out" }, C.ev - 0.3);
      swap(S + "k-m-smile", S + "k-m-o", C.ev);
      blink(S + "k-lids", 1.2); blink(S + "k-lids", 4.4);
      // the iceberg: smug at 'Scientifically', creeping closer for 'far too long'
      tl.fromTo([S + "ice-browL", S + "ice-browR"], { y: 0 }, { y: -10, duration: 0.25, ease: "back.out(3)" }, C.sci);
      swap(S + "ice-smirk", S + "ice-grin", C.sci + 0.2);
      tl.fromTo(S + "ice", { x: 0 }, { x: -50, duration: D - C.long, ease: "power1.in" }, C.long);
      fly("m", C.sci, null, { from: "right" });
      fly("t", C.long, null);
"""
scene(sid, world, js, cards)
