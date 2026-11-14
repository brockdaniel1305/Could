"""S2E12 world layer: prime Usain Bolt (Jamaica yellow/green, race bib), the T-Rex (cartoon side view, bib on the belly), the starter."""
import sys
from pathlib import Path

EP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EP.parents[1] / "tools/world3d"))
sys.path.insert(0, str(EP.parents[1] / "tools"))
from world import sprite, write  # noqa: E402
from kit import part  # noqa: E402

BOLT_HAIR = '<path d="M-30,-18 Q-31,-46 0,-47 Q31,-46 30,-18 Q22,-36 0,-37 Q-22,-36 -30,-18 Z" fill="#1a120e" opacity="0.9"/>'
REF_HAIR = '<path d="M-30,-16 Q-33,-44 0,-46 Q33,-44 30,-16 Q22,-30 0,-31 Q-22,-30 -30,-16 Z" fill="#6b4a2a" stroke="#14141f" stroke-width="4"/>'
SHADOW = '<ellipse cx="0" cy="4" rx="64" ry="13" fill="#000" opacity="0.38"/>'
BIB = ('<g transform="translate(-20,-150)"><rect x="-40" y="-26" width="80" height="52" rx="6" fill="#f4f4f2" stroke="#14141f" stroke-width="5"/>'
       '<text x="0" y="14" text-anchor="middle" font-family="Inter" font-weight="900" font-size="34" fill="#14141f">5</text></g>')


def athlete(name, hair, kit, kit2, stripes, shorts, socks, numc, num, skin):
    svg = part("athlete", f"w3-{name}x", HAIRSVG=hair, KITC=kit, KIT2=kit2, STRIPEOP=stripes, SHORTC=shorts, SOCKC=socks,
               NUMC=numc, NUM=num, SKIN=skin)
    return sprite(name, SHADOW + svg, 460, 600, 520)


trex = part("trex", "w3-Rx")
trex = trex.replace('id="w3-Rx-body">', 'id="w3-Rx-body">', 1)
sprites = [athlete("B", BOLT_HAIR, "#f6d32d", "#1f9d55", 1, "#1f9d55", "#f6d32d", "#14141f", "4", "#6b4430"),
           athlete("S", REF_HAIR, "#1d3f9b", "#1d3f9b", 0, "#f4f4f2", "#f4f4f2", "#ffd23f", "", "#e3b48c"),
           sprite("R", '<g transform="scale(-1,1)">' + trex + '</g>' + BIB, 760, 420, 380)]

write(EP, sprites, "", extra_css="""
    .bub.follow { font-size: 58px; padding: 16px 30px; border-radius: 44px; }
    .bub.small { font-size: 30px; padding: 8px 16px; }
    .w3b g[id$="-jaw"] { transform-box: fill-box; transform-origin: 0% 0%; }
    .w3b g[id$="-head"] { transform-box: fill-box; transform-origin: 0% 100%; }
    .clock { left: auto; right: 40px; top: 110px; padding: 10px 22px; background: #14141f; border: 4px solid #ffd23f; border-radius: 10px;
             font: 900 64px/1 "CouldMono"; color: #ffd23f; letter-spacing: 0.04em; }
    .clock small { display: block; font: 700 20px/1 "CouldMono"; color: #f4f4f2; letter-spacing: 0.2em; margin-bottom: 6px; }""")
