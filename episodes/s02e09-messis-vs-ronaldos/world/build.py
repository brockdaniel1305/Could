"""S2E09 world layer: 11 prime Messis (Barça 2012, blaugrana stripes, No. 10) and 11 prime Ronaldos (Real 2014, white, No. 7),
referee, and the shirts the Messis hold up after the 92nd-minute winner."""
import sys
from pathlib import Path

EP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EP.parents[1] / "tools/world3d"))
sys.path.insert(0, str(EP.parents[1] / "tools"))
from world import sprite, write, ball  # noqa: E402
from kit import part  # noqa: E402

# Messi 2012: short brown hair with a light fringe; Ronaldo 2014: short dark hair, gelled quiff, shaved sides
MESSI_HAIR = ('<path d="M-31,-12 Q-34,-48 0,-50 Q34,-48 31,-12 Q24,-30 4,-30 Q-16,-30 -31,-12 Z" fill="#5a3a20" stroke="#14141f" stroke-width="4" stroke-linejoin="round"/>'
              '<path d="M-24,-30 Q-4,-42 20,-32 Q2,-30 -24,-22 Z" fill="#6e4a2a"/>'
              '<path d="M-14,30 Q0,38 14,30 L14,24 Q0,32 -14,24 Z" fill="#5a3a20" opacity="0.35"/>')
RONALDO_HAIR = ('<path d="M-29,-18 Q-30,-44 0,-46 Q30,-44 29,-18 Q22,-34 0,-35 Q-22,-34 -29,-18 Z" fill="#1a120e" opacity="0.55"/>'
                '<path d="M-24,-34 Q-20,-62 6,-60 Q30,-58 26,-36 Q12,-44 -24,-34 Z" fill="#1a120e" stroke="#14141f" stroke-width="4" stroke-linejoin="round"/>')
REF_HAIR = '<path d="M-30,-16 Q-33,-44 0,-46 Q33,-44 30,-16 Q22,-30 0,-31 Q-22,-30 -30,-16 Z" fill="#6b4a2a" stroke="#14141f" stroke-width="4"/>'
SHADOW = '<ellipse cx="0" cy="4" rx="64" ry="13" fill="#000" opacity="0.38"/>'
MSKIN, RSKIN = "#efc49e", "#d9a07a"
# the shirt held up to the crowd: back of a blaugrana No. 10; origin = bottom centre, ~110 px tall
SHIRT = ('<path d="M-46,-104 L-20,-112 Q0,-100 20,-112 L46,-104 L64,-74 L44,-64 L40,0 L-40,0 L-44,-64 L-64,-74 Z" fill="#a50044" stroke="#14141f" stroke-width="5" stroke-linejoin="round"/>'
         + "".join(f'<rect x="{x}" y="-104" width="11" height="104" fill="#1d3f9b"/>' for x in (-30, -8, 14))
         + '<text x="0" y="-62" text-anchor="middle" font-family="Inter" font-weight="900" font-size="20" fill="#ffd23f" stroke="#14141f" stroke-width="1">MESSI</text>'
         '<text x="0" y="-18" text-anchor="middle" font-family="Inter" font-weight="900" font-size="44" fill="#ffd23f" stroke="#14141f" stroke-width="2">10</text>')


def athlete(name, hair, kit, kit2, stripes, shorts, socks, numc, num, skin):
    svg = part("athlete", f"w3-{name}x", HAIRSVG=hair, KITC=kit, KIT2=kit2, STRIPEOP=stripes, SHORTC=shorts, SOCKC=socks,
               NUMC=numc, NUM=num, SKIN=skin)
    return sprite(name, SHADOW + svg, 460, 600, 520)


sprites = []
for i in range(11):
    if i == 0:
        sprites.append(athlete("M0", MESSI_HAIR, "#f2c230", "#f2c230", 0, "#1a1a2e", "#f2c230", "#1a1a2e", "1", MSKIN))
        sprites.append(athlete("R0", RONALDO_HAIR, "#2bb3a3", "#2bb3a3", 0, "#1a1a2e", "#2bb3a3", "#1a1a2e", "1", RSKIN))
        continue
    sprites.append(athlete(f"M{i}", MESSI_HAIR, "#a50044", "#1d3f9b", 1, "#1d2f6f", "#1d2f6f", "#ffd23f", "10", MSKIN))
    sprites.append(athlete(f"R{i}", RONALDO_HAIR, "#f4f4f2", "#f4f4f2", 0, "#f4f4f2", "#f4f4f2", "#14141f", "7", RSKIN))
sprites.append(athlete("REF", REF_HAIR, "#111111", "#111111", 0, "#111111", "#111111", "#ffd23f", "", "#e3b48c"))
for k in range(11):
    sprites.append(sprite(f"shirt{k}", SHIRT, 140, 130, 120))
sprites.append(ball())

write(EP, sprites, "", extra_css="""
    .bub.follow { font-size: 58px; padding: 16px 30px; border-radius: 44px; }
    .bub.small { font-size: 30px; padding: 8px 16px; }
    .quake { left: 0; top: 0; width: 1080px; height: 1920px; background: rgba(255, 255, 255, 0.0); }""")
