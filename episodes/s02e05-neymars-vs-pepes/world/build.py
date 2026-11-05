"""S2E05 world layer: 11 Neymars, 11 Pepes and a referee in the athletic broadcast style (channel/kit/parts/athlete.svg)."""
import sys
from pathlib import Path

EP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EP.parents[1] / "tools/world3d"))
sys.path.insert(0, str(EP.parents[1] / "tools"))
from world import sprite, write, ball  # noqa: E402
from kit import part  # noqa: E402

# Neymar: short dark hair with bleached top, thin moustache-beard line; Pepe: bald with dark stubble beard
NEYMAR_HAIR = ('<path d="M-31,-14 Q-34,-46 0,-50 Q34,-46 31,-14 Q24,-30 0,-31 Q-24,-30 -31,-14 Z" fill="#2a1a10" stroke="#14141f" stroke-width="4" stroke-linejoin="round"/>'
               '<path d="M-20,-40 Q0,-56 20,-40 Q0,-46 -20,-40 Z" fill="#e8c46a" stroke="#14141f" stroke-width="3"/>'
               '<path d="M-14,30 Q0,36 14,30 L14,24 Q0,30 -14,24 Z" fill="#2a1a10"/>')
PEPE_HAIR = ('<path d="M-30,-18 Q-30,-44 0,-46 Q30,-44 30,-18 Q22,-36 0,-37 Q-22,-36 -30,-18 Z" fill="#c9926c" opacity="0.55"/>'
             '<path d="M-29,-4 Q-29,26 -13,35 Q0,42 13,35 Q29,26 29,-4 Q24,14 12,18 Q0,24 -12,18 Q-24,14 -29,-4 Z" fill="#2a1c14" opacity="0.75" stroke="#14141f" stroke-width="2"/>')
REF_HAIR = '<path d="M-30,-16 Q-33,-44 0,-46 Q33,-44 30,-16 Q22,-30 0,-31 Q-22,-30 -30,-16 Z" fill="#6b4a2a" stroke="#14141f" stroke-width="4"/>'
SHADOW = '<ellipse cx="0" cy="4" rx="64" ry="13" fill="#000" opacity="0.38"/>'


def athlete(name, hair, kit, kit2, stripes, shorts, socks, numc, num, skin):
    svg = part("athlete", f"w3-{name}x", HAIRSVG=hair, KITC=kit, KIT2=kit2, STRIPEOP=stripes, SHORTC=shorts, SOCKC=socks,
               NUMC=numc, NUM=num, SKIN=skin)
    return sprite(name, SHADOW + svg, 460, 600, 520)


sprites = []
for i in range(11):
    if i == 0:
        sprites.append(athlete("N0", NEYMAR_HAIR, "#2bb3a3", "#2bb3a3", 0, "#1a1a2e", "#2bb3a3", "#1a1a2e", "1", "#c68863"))
        sprites.append(athlete("P0", PEPE_HAIR, "#f07a1a", "#f07a1a", 0, "#1a1a2e", "#f07a1a", "#1a1a2e", "1", "#d9a07a"))
        continue
    sprites.append(athlete(f"N{i}", NEYMAR_HAIR, "#f6d32d", "#1f9d55", 0, "#1d4fb8", "#f4f4f2", "#1f9d55", "10", "#c68863"))
    sprites.append(athlete(f"P{i}", PEPE_HAIR, "#f4f4f2", "#f4f4f2", 0, "#f4f4f2", "#f4f4f2", "#14141f", "3", "#d9a07a"))
sprites.append(athlete("REF", REF_HAIR, "#111111", "#111111", 0, "#111111", "#111111", "#ffd23f", "", "#e3b48c"))
sprites.append(ball())

write(EP, sprites, "", extra_css="""
    .bub.follow { font-size: 60px; padding: 16px 30px; border-radius: 44px; }
    .bub.redcard { width: 70px; height: 96px; padding: 0; border-radius: 8px; background: #e0222b; border: 5px solid #14141f; box-shadow: 6px 6px 0 #14141f; font-size: 0; }
    .bub.yellow { width: 70px; height: 96px; padding: 0; border-radius: 8px; background: #ffd23f; border: 5px solid #14141f; box-shadow: 6px 6px 0 #14141f; font-size: 0; }""")
