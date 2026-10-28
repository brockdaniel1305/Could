import sys; sys.path.insert(0, __file__.rsplit('/episodes/', 1)[0] + '/tools')  # noqa: E702
from scene import *  # noqa: F403
sid = "s7-verdict"
WL = 430
world = f"""
{part("sea-night", sid + "-sea", WL=WL)}
<g transform="translate(120,{WL + 30}) scale(0.62)"><g id="{sid}-ship">{part("titanic", sid + "-tit")}</g></g>
<g id="{sid}-map" opacity="0"><g transform="translate(30,60)">
  <path d="M120,120 Q480,10 820,150" fill="none" stroke="#f4efe6" stroke-width="5" stroke-dasharray="14 12" />
  <circle cx="120" cy="120" r="12" fill="#e0412f" stroke="#1a1a2e" stroke-width="4" /><circle cx="820" cy="150" r="12" fill="#ffd23f" stroke="#1a1a2e" stroke-width="4" />
  <text x="150" y="96" text-anchor="middle" font-family="Inter" font-weight="900" font-size="28" fill="#f4efe6">HIS GOAL (MUNICH)</text>
  <text x="820" y="196" text-anchor="middle" font-family="Inter" font-weight="900" font-size="28" fill="#f4efe6">HIM</text>
  <rect x="380" y="40" width="200" height="50" rx="10" fill="#f4efe6" stroke="#1a1a2e" stroke-width="4" />
  <text x="480" y="74" text-anchor="middle" font-family="Inter" font-weight="900" font-size="28" fill="#1a1a2e">≈ 4,800 km</text></g>
</g>
<g transform="translate(780,{WL})"><g id="{sid}-icewrap">{part("iceberg", sid + "-ice")}
  <g transform="translate(-20,-226) scale(0.5)"><g id="{sid}-kwrap">{part("keeper", sid + "-k")}</g></g></g></g>
{part("sea-front", sid + "-front", WL=WL + 18)}
"""
js = """
      waves(S + "sea-waves1", S + "front-waves2");
      tl.fromTo(S + "head", { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.2, ease: "power4.out" }, 0.1);
      show(S + "r1", C.line + 0.6); show(S + "r2", C.p1); show(S + "r3", C.p2);
      tl.fromTo(S + "r3v", { opacity: 0 }, { opacity: 1, duration: 0.15 }, C.p3);
      // the Titanic goes down in the background regardless
      tl.fromTo(S + "ship", { rotation: 6, y: 0, svgOrigin: "600 0" }, { rotation: 24, y: 160, duration: D, ease: "power1.in" }, 0);
      tl.fromTo(S + "icewrap", { y: 0 }, { y: 6, duration: 1.6, ease: "sine.inOut", repeat: Math.floor(D / 1.6), yoyo: true }, 0);
      // he looks at us, hopeful
      tl.to([S + "k-pupL", S + "k-pupR"], { y: 3, duration: 0.3 }, C.q);
      tl.fromTo(S + "k-armR", { rotation: 0 }, { rotation: -160, duration: 0.4, ease: "back.out(2)" }, C.q + 0.4);
      // NO.
      const land = C.no + 0.18;
      tl.fromTo(S + "stamp", { opacity: 0, scale: 2.4, rotation: -4 }, { opacity: 1, scale: 1, rotation: -9, duration: 0.18, ease: "power4.in" }, C.no);
      tl.fromTo(S + "svg", { x: 0 }, { x: 8, duration: 0.04, repeat: 5, yoyo: true }, land);
      swap(S + "k-m-smile", S + "k-m-o", land);
      tl.to(S + "k-armR", { rotation: -20, duration: 0.3 }, land);
      tl.to(S + "stamp", { opacity: 0, scale: 0.9, duration: 0.25, ease: "power2.in" }, C.line + 0.2);
      // ... but furthest off his line in history
      tl.fromTo(S + "map", { opacity: 0 }, { opacity: 1, duration: 0.3 }, C.line + 0.5);
      tl.fromTo(S + "map path", { strokeDashoffset: 300 }, { strokeDashoffset: 0, duration: 1.2, ease: "power2.out" }, C.line + 0.5);
      swap(S + "k-m-o", S + "k-m-smile", C.line + 1.2);
      tl.to(S + "k-armR", { rotation: -150, duration: 0.35, ease: "back.out(2)" }, C.line + 1.4);
      tl.to(S + "k-armL", { rotation: 150, duration: 0.35, ease: "back.out(2)" }, C.line + 1.5);
      tl.to(S + "map", { opacity: 0, duration: 0.3 }, C.p1 + 0.2);
      // chance he tries anyway: 100 %
      tl.fromTo(S + "kwrap", { y: 0 }, { y: -30, duration: 0.25, ease: "power2.out", yoyo: true, repeat: 3 }, C.p3);
"""
scene(sid, "THE VERDICT", "Could he save it?",
      [("OFF HIS LINE BY", "≈ 4,800 km"), ("CHANCE OF SUCCESS", "0.03 %"), ("CHANCE HE TRIES ANYWAY", '<span id="s7-verdict-r3v">100 %</span>', "gold")], world, js,
      extra_css=".stamp { position: absolute; left: 240px; top: 700px; width: 600px; height: 380px; border: 22px solid #d6332a; border-radius: 30px; "
                "display: flex; align-items: center; justify-content: center; font: 900 260px/1 'Inter'; color: #d6332a; opacity: 0; background: rgba(244,239,230,0.12); }",
      overlay=f'    <div class="stamp" id="{sid}-stamp">NO.</div>')
