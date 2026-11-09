"""S2E08 world layer: 11 Yamals (Spain red, No. 19) and 11 young Messis (2006, long hair, blaugrana stripes, No. 19),
referee, the 2007 bathtub (baby Yamal), the World Cup trophy and half-time notebooks."""
import sys
from pathlib import Path

EP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EP.parents[1] / "tools/world3d"))
sys.path.insert(0, str(EP.parents[1] / "tools"))
from world import sprite, write, ball  # noqa: E402
from kit import part  # noqa: E402

# Yamal: short dark curls on top, faded sides; young Messi: long straight hair to the jaw with a fringe
YAMAL_HAIR = ('<path d="M-30,-16 Q-32,-46 0,-50 Q32,-46 30,-16 Q24,-34 0,-36 Q-24,-34 -30,-16 Z" fill="#1a120e" stroke="#14141f" stroke-width="4" stroke-linejoin="round"/>'
              + "".join(f'<circle cx="{x}" cy="{y}" r="6" fill="#2a1c16"/>' for x, y in [(-16, -42), (-4, -47), (8, -46), (19, -41)]))
MESSI_HAIR = ('<path d="M-36,22 Q-42,-48 0,-52 Q42,-48 36,22 L28,24 Q30,-18 18,-26 Q-2,-14 -22,-26 Q-30,-14 -28,24 Z" fill="#4a2c18" stroke="#14141f" stroke-width="4" stroke-linejoin="round"/>'
              '<path d="M-26,-30 Q-4,-44 22,-28 Q2,-24 -26,-18 Z" fill="#5c3820"/>')
REF_HAIR = '<path d="M-30,-16 Q-33,-44 0,-46 Q33,-44 30,-16 Q22,-30 0,-31 Q-22,-30 -30,-16 Z" fill="#6b4a2a" stroke="#14141f" stroke-width="4"/>'
SHADOW = '<ellipse cx="0" cy="4" rx="64" ry="13" fill="#000" opacity="0.38"/>'
YSKIN, MSKIN = "#8a5a3c", "#efc49e"

DUCK = ('<g><ellipse cx="0" cy="-22" rx="34" ry="22" fill="#ffd23f" stroke="#14141f" stroke-width="5"/>'
        '<circle cx="20" cy="-50" r="18" fill="#ffd23f" stroke="#14141f" stroke-width="5"/>'
        '<path d="M34,-52 L52,-46 L34,-40 Z" fill="#f07a1a" stroke="#14141f" stroke-width="4" stroke-linejoin="round"/>'
        '<circle cx="24" cy="-55" r="4" fill="#14141f"/></g>')
# 2007: baby Yamal in a foam bath; origin = base centre, ~230 px tall
baby = part("baby", "w3-babyx").replace("#f2c9a0", YSKIN)
TUB = (f'<ellipse cx="0" cy="4" rx="120" ry="16" fill="#000" opacity="0.3"/>'
       f'<g transform="translate(-6,-34) scale(0.95)">{baby}</g>'
       '<path d="M-118,-96 L118,-96 Q112,-6 86,0 L-86,0 Q-112,-6 -118,-96 Z" fill="#e9eef5" stroke="#14141f" stroke-width="6" stroke-linejoin="round"/>'
       '<rect x="-124" y="-108" width="248" height="16" rx="8" fill="#ffffff" stroke="#14141f" stroke-width="5"/>'
       + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#ffffff" stroke="#b9c8da" stroke-width="3"/>'
                 for x, y, r in [(-96, -112, 22), (-62, -122, 26), (58, -120, 24), (92, -110, 20), (-30, -114, 16), (30, -112, 15)])
       + f'<g transform="translate(70,-104) scale(0.8)">{DUCK}</g>')
BOOK = ('<rect x="-30" y="-44" width="60" height="44" rx="4" fill="#f4f4f2" stroke="#14141f" stroke-width="5"/>'
        '<path d="M0,-44 L0,0" stroke="#14141f" stroke-width="4"/>'
        '<path d="M-24,-34 L-6,-34 M-24,-24 L-6,-24 M-24,-14 L-8,-14 M6,-34 L24,-34 M6,-24 L22,-24" stroke="#4f7bff" stroke-width="3"/>')


def athlete(name, hair, kit, kit2, stripes, shorts, socks, numc, num, skin):
    svg = part("athlete", f"w3-{name}x", HAIRSVG=hair, KITC=kit, KIT2=kit2, STRIPEOP=stripes, SHORTC=shorts, SOCKC=socks,
               NUMC=numc, NUM=num, SKIN=skin)
    return sprite(name, SHADOW + svg, 460, 600, 520)


sprites = []
for i in range(11):
    if i == 0:
        sprites.append(athlete("Y0", YAMAL_HAIR, "#2bb3a3", "#2bb3a3", 0, "#1a1a2e", "#2bb3a3", "#1a1a2e", "1", YSKIN))
        sprites.append(athlete("M0", MESSI_HAIR, "#f2c230", "#f2c230", 0, "#1a1a2e", "#f2c230", "#1a1a2e", "1", MSKIN))
        continue
    sprites.append(athlete(f"Y{i}", YAMAL_HAIR, "#c8102e", "#c8102e", 0, "#1d2a5c", "#c8102e", "#ffd23f", "19", YSKIN))
    sprites.append(athlete(f"M{i}", MESSI_HAIR, "#a50044", "#1d3f9b", 1, "#1d2f6f", "#1d2f6f", "#ffd23f", "19", MSKIN))
sprites.append(athlete("REF", REF_HAIR, "#111111", "#111111", 0, "#111111", "#111111", "#ffd23f", "", "#e3b48c"))
sprites.append(sprite("tub", TUB, 300, 300, 260))
sprites.append(sprite("wc", part("trophy", "w3-wcx"), 180, 180, 150))
for k in range(5):
    sprites.append(sprite(f"book{k}", BOOK, 90, 70, 60))
sprites.append(ball())

write(EP, sprites, "", extra_css="""
    .bub.follow { font-size: 58px; padding: 16px 30px; border-radius: 44px; }
    .bub.small { font-size: 30px; padding: 8px 16px; }
    .flash { left: 0; top: 0; width: 1080px; height: 1920px; background: rgba(120, 82, 30, 0.42); mix-blend-mode: multiply; }
    .flashlbl { left: 60px; top: 380px; padding: 12px 26px; background: #f4e3c0; color: #3a2a14; border: 5px solid #3a2a14; border-radius: 10px;
                font: 900 64px/1 "Inter"; transform: rotate(-4deg); }
    .foam { left: -40px; width: 1160px; top: 1180px; height: 820px; }
    .foam i { position: absolute; border-radius: 50%; background: radial-gradient(circle at 35% 30%, #ffffff, #dfe8f3 60%, #b9c8da);
              border: 4px solid #9fb2c8; }
    .duck { left: 640px; top: 980px; width: 260px; height: 260px; }""")
