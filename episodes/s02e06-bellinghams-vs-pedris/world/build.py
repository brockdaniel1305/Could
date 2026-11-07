"""S2E06 world layer: 11 Bellinghams (white, No. 5) and 11 Pedris (blue-garnet, No. 8) plus a referee, athletic broadcast style."""
import sys
from pathlib import Path

EP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EP.parents[1] / "tools/world3d"))
sys.path.insert(0, str(EP.parents[1] / "tools"))
from world import sprite, write, ball  # noqa: E402
from kit import part  # noqa: E402

# Bellingham: short dark curly hair, Pedri: dark side-parted hair with a fringe
BELL_HAIR = ('<path d="M-31,-14 Q-34,-48 0,-50 Q34,-48 31,-14 Q24,-32 0,-33 Q-24,-32 -31,-14 Z" fill="#1a1210" stroke="#14141f" stroke-width="4" stroke-linejoin="round"/>'
             + "".join(f'<circle cx="{x}" cy="{y}" r="5" fill="#2a1c16"/>' for x, y in [(-18, -40), (-6, -45), (6, -45), (18, -40), (-24, -28), (24, -28)]))
PEDRI_HAIR = ('<path d="M-31,-12 Q-35,-48 0,-50 Q35,-48 31,-12 Q20,-30 -2,-26 Q-18,-24 -31,-12 Z" fill="#2a1a10" stroke="#14141f" stroke-width="4" stroke-linejoin="round"/>'
              '<path d="M-26,-24 Q-6,-40 20,-30 Q2,-30 -26,-16 Z" fill="#3a2414"/>')
REF_HAIR = '<path d="M-30,-16 Q-33,-44 0,-46 Q33,-44 30,-16 Q22,-30 0,-31 Q-22,-30 -30,-16 Z" fill="#6b4a2a" stroke="#14141f" stroke-width="4"/>'
SHADOW = '<ellipse cx="0" cy="4" rx="64" ry="13" fill="#000" opacity="0.38"/>'


def athlete(name, hair, kit, kit2, stripes, shorts, socks, numc, num, skin):
    svg = part("athlete", f"w3-{name}x", HAIRSVG=hair, KITC=kit, KIT2=kit2, STRIPEOP=stripes, SHORTC=shorts, SOCKC=socks,
               NUMC=numc, NUM=num, SKIN=skin)
    return sprite(name, SHADOW + svg, 460, 600, 520)


sprites = []
for i in range(11):
    if i == 0:
        sprites.append(athlete("B0", BELL_HAIR, "#2bb3a3", "#2bb3a3", 0, "#1a1a2e", "#2bb3a3", "#1a1a2e", "1", "#7a4e35"))
        sprites.append(athlete("P0", PEDRI_HAIR, "#f2c230", "#f2c230", 0, "#1a1a2e", "#f2c230", "#1a1a2e", "1", "#e3b48c"))
        continue
    sprites.append(athlete(f"B{i}", BELL_HAIR, "#f4f4f2", "#f4f4f2", 0, "#f4f4f2", "#f4f4f2", "#14141f", "5", "#7a4e35"))
    sprites.append(athlete(f"P{i}", PEDRI_HAIR, "#a50044", "#1d3f9b", 1, "#1d2f6f", "#1d2f6f", "#ffd23f", "8", "#e3b48c"))
sprites.append(athlete("REF", REF_HAIR, "#111111", "#111111", 0, "#111111", "#111111", "#ffd23f", "", "#e3b48c"))
sprites.append(ball())

write(EP, sprites, "", extra_css="""
    .bub.follow { font-size: 58px; padding: 16px 30px; border-radius: 44px; }
    .var { left: 60px; right: 60px; top: 300px; text-align: center; padding: 22px 0 26px; background: #14141f; border: 6px solid #4fd1ff;
           border-radius: 18px; color: #f4f4f2; font: 900 92px/1 "Inter"; letter-spacing: 0.06em; }
    .bub.small { font-size: 26px; padding: 8px 14px; }
    .bub.yellow { width: 70px; height: 96px; padding: 0; border-radius: 8px; background: #ffd23f; border: 5px solid #14141f; box-shadow: 6px 6px 0 #14141f; font-size: 0; }
    .var small { display: block; margin-top: 10px; font: 700 30px/1 "CouldMono"; color: #4fd1ff; letter-spacing: 0.2em; }""")
