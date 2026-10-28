"""Shared world for episode 005 (Haaland in the Colosseum).

Inside the Colosseum: Haaland left, opponents right, feet on y = GY. Below the captions: a crowd-mood gauge
(thumb down ... thumb up) whose needle the scenes move. Graphics only, no text under the caption band.
"""
from scene import part  # noqa: F401

GY = 1150


def arena(sid):
    return part("colosseum", sid + "-col", GY=GY)


def gauge(sid):
    thumb = lambda x, up, col: (f'<g transform="translate({x},1760) scale(1,{-1 if not up else 1})"><rect x="-30" y="-18" width="60" height="50" rx="16" fill="{col}" stroke="#1a1a2e" stroke-width="6" />'
                                f'<rect x="-12" y="-62" width="22" height="50" rx="10" fill="{col}" stroke="#1a1a2e" stroke-width="6" /></g>')
    ticks = "".join(f'<path d="M{540 + 300 * __import__("math").cos(__import__("math").radians(180 - a)):.0f},{1760 - 300 * __import__("math").sin(__import__("math").radians(180 - a)):.0f} '
                    f'L{540 + 260 * __import__("math").cos(__import__("math").radians(180 - a)):.0f},{1760 - 260 * __import__("math").sin(__import__("math").radians(180 - a)):.0f}" stroke="#1a1a2e" stroke-width="8" />'
                    for a in range(0, 181, 30))
    return f"""
<g id="{sid}-gauge">
  <path d="M240,1760 A300,300 0 0 1 840,1760 Z" fill="#f4efe6" stroke="#1a1a2e" stroke-width="8" />
  <path d="M240,1760 A300,300 0 0 1 390,1500 L540,1760 Z" fill="#e0412f" opacity="0.8" />
  <path d="M690,1500 A300,300 0 0 1 840,1760 L540,1760 Z" fill="#1f9d55" opacity="0.8" />
  {ticks}
  {thumb(170, False, "#e0412f")}{thumb(910, True, "#1f9d55")}
  <g transform="translate(540,1760)"><g id="{sid}-needle"><path d="M-14,0 L0,-250 L14,0 Z" fill="#1a1a2e" /></g></g>
  <circle cx="540" cy="1760" r="30" fill="#ffd23f" stroke="#1a1a2e" stroke-width="7" />
</g>"""


def haaland(sid, x=260, scale=1.15):
    return f'<g transform="translate({x},{GY})"><g id="{sid}-kwrap"><g transform="scale({scale})">{part("striker", sid + "-h")}</g></g></g>'


def fighter(sid, kind, name, x, scale=1.05):
    return f'<g transform="translate({x},{GY})"><g id="{sid}-{name}"><g transform="scale({scale})">{part(kind, sid + "-" + name + "p")}</g></g></g>'


MEDITATE_JS = """
      // sit down cross-legged and float a little (Haaland's meditation celebration)
      const meditate = (at) => {
        tl.to(S + "kwrap", { y: 80, duration: 0.35, ease: "power2.inOut" }, at);
        tl.to(S + "h-legL", { rotation: 75, duration: 0.35 }, at);
        tl.to(S + "h-legR", { rotation: -75, duration: 0.35 }, at);
        tl.to(S + "h-armL", { rotation: 40, duration: 0.35 }, at + 0.1);
        tl.to(S + "h-armR", { rotation: -40, duration: 0.35 }, at + 0.1);
        tl.to(S + "h-lids", { opacity: 1, duration: 0.01 }, at + 0.4);
        tl.fromTo(S + "kwrap", { y: 80 }, { y: 60, duration: 0.9, ease: "sine.inOut", repeat: R(D - at - 0.4, 0.9), yoyo: true }, at + 0.4);
      };
      const needle = (deg, at, d = 0.6) => tl.to(S + "needle", { rotation: deg, transformOrigin: "50% 100%", duration: d, ease: "back.out(1.6)" }, at);
"""
