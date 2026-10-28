import sys; sys.path.insert(0, __file__.rsplit('/episodes/', 1)[0] + '/tools')  # noqa: E702
from scene import *  # noqa: F403
sid = "s7-verdict"
WL = 1150
world = f"""
{part("sea-night", sid + "-sea", WL=WL)}
<g transform="translate(40,{WL + 40}) scale(0.9)"><g id="{sid}-ship">{part("titanic", sid + "-tit")}</g></g>
<g id="{sid}-map" opacity="0">
  <path d="M150,640 Q470,420 740,600" fill="none" stroke="#f4efe6" stroke-width="7" stroke-dasharray="18 14" />
  <circle cx="150" cy="640" r="16" fill="#e0412f" stroke="#1a1a2e" stroke-width="5" /><circle cx="740" cy="600" r="16" fill="#ffd23f" stroke="#1a1a2e" stroke-width="5" />
  <text x="150" y="700" text-anchor="middle" font-family="Inter" font-weight="900" font-size="32" fill="#f4efe6" stroke="#1a1a2e" stroke-width="1">HIS GOAL</text>
  <text x="150" y="736" text-anchor="middle" font-family="Inter" font-weight="900" font-size="28" fill="#f4efe6">(MUNICH)</text>
</g>
<g transform="translate(760,{WL})"><g id="{sid}-icewrap"><g transform="scale(1.5)">{part("iceberg-under", sid + "-iu")}{part("iceberg", sid + "-ice")}
  <g transform="translate(-20,-226) scale(0.5)"><g id="{sid}-kwrap">{part("keeper", sid + "-k")}</g></g></g></g></g>
{part("sea-front", sid + "-front", WL=WL + 22)}
"""
cards = (banner(sid, "b", "THE VERDICT", "Could he save it?", 60, 330)
         + card(sid, "km", "OFF HIS LINE BY", "≈ 4,800 km", 280, 330, "gold")
         + card(sid, "p1", "CHANCE OF SUCCESS", "0.03 %", 80, 360)
         + card(sid, "p2", "CHANCE HE TRIES ANYWAY", '<span id="s7-verdict-p3v">100 %</span>', 80, 540, "gold"))
css = """
    .stamp { position: absolute; left: 170px; top: 560px; width: 740px; height: 440px; border: 26px solid #d6332a; border-radius: 34px;
             display: flex; align-items: center; justify-content: center; font: 900 300px/1 "Inter"; color: #d6332a; opacity: 0;
             background: rgba(244, 239, 230, 0.16); }"""
cards += f'\n    <div class="stamp" id="{sid}-stamp">NO.</div>'
js = """
      waves(S + "sea-waves1", S + "front-waves2");
      fly("b", 0.1, C.no - 0.15, { from: "top" });
      fly("km", C.line + 1.3, C.p1 - 0.1, { from: "right" });
      fly("p1", C.p1, null);
      fly("p2", C.p2, null, { from: "right" });
      tl.fromTo(S + "p3v", { opacity: 0 }, { opacity: 1, duration: 0.15 }, C.p3);
      // the Titanic goes down in the background regardless
      tl.fromTo(S + "ship", { rotation: 6, y: 0, svgOrigin: "600 0" }, { rotation: 24, y: 180, duration: D, ease: "power1.in" }, 0);
      tl.fromTo(S + "icewrap", { y: 0 }, { y: 8, duration: 1.6, ease: "sine.inOut", repeat: R(D, 1.6), yoyo: true }, 0);
      // he looks at us, hopeful
      tl.to([S + "k-pupL", S + "k-pupR"], { y: 3, duration: 0.3 }, C.q);
      tl.fromTo(S + "k-armR", { rotation: 0 }, { rotation: -160, duration: 0.4, ease: "back.out(2)" }, C.q + 0.4);
      // NO.
      const land = C.no + 0.18;
      tl.fromTo(S + "stamp", { opacity: 0, scale: 2.4, rotation: -4 }, { opacity: 1, scale: 1, rotation: -9, duration: 0.18, ease: "power4.in" }, C.no);
      tl.fromTo(S + "svg", { x: 0 }, { x: 10, duration: 0.04, repeat: 5, yoyo: true }, land);
      swap(S + "k-m-smile", S + "k-m-o", land);
      tl.to(S + "k-armR", { rotation: -20, duration: 0.3 }, land);
      tl.to(S + "stamp", { opacity: 0, scale: 0.9, duration: 0.25, ease: "power2.in" }, C.line + 0.2);
      // ... but no goalkeeper ever came further off his line
      tl.fromTo(S + "map", { opacity: 0 }, { opacity: 1, duration: 0.3 }, C.line + 0.5);
      tl.fromTo(S + "map path", { strokeDashoffset: 400 }, { strokeDashoffset: 0, duration: 1.2, ease: "power2.out" }, C.line + 0.5);
      swap(S + "k-m-o", S + "k-m-smile", C.line + 1.2);
      tl.to(S + "k-armR", { rotation: -150, duration: 0.35, ease: "back.out(2)" }, C.line + 1.4);
      tl.to(S + "k-armL", { rotation: 150, duration: 0.35, ease: "back.out(2)" }, C.line + 1.5);
      tl.to(S + "map", { opacity: 0, duration: 0.3 }, C.p1 - 0.1);
      // chance he tries anyway: 100 %
      tl.fromTo(S + "kwrap", { y: 0 }, { y: -40, duration: 0.25, ease: "power2.out", yoyo: true, repeat: 3 }, C.p3);
"""
scene(sid, world, js, cards, extra_css=css)
