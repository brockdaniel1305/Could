"""S2E04 world layer: 11 Messis and 11 Haalands in the new athletic "broadcast" style (channel/kit/parts/athlete.svg)."""
import sys
from pathlib import Path

EP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EP.parents[1] / "tools/world3d"))
sys.path.insert(0, str(EP.parents[1] / "tools"))
from world import sprite, write, ball  # noqa: E402
from kit import part  # noqa: E402

MESSI_HAIR = ('<path d="M-31,-16 Q-35,-46 0,-48 Q35,-46 31,-16 Q22,-32 0,-32 Q-22,-32 -31,-16 Z" fill="#3b2416" stroke="#14141f" stroke-width="4" stroke-linejoin="round"/>'
              '<path d="M-29,-4 Q-29,26 -13,35 Q0,42 13,35 Q29,26 29,-4 Q24,14 12,18 Q0,24 -12,18 Q-24,14 -29,-4 Z" fill="#3b2416" stroke="#14141f" stroke-width="3" stroke-linejoin="round"/>')
HAALAND_HAIR = ('<circle cx="0" cy="-48" r="12" fill="#e8c46a" stroke="#14141f" stroke-width="4"/>'
                '<path d="M-32,-12 Q-35,-48 0,-50 Q35,-48 32,-12 Q27,-36 0,-36 Q-27,-36 -32,-12 Z" fill="#e8c46a" stroke="#14141f" stroke-width="4" stroke-linejoin="round"/>'
                '<path d="M-12,-40 Q0,-44 12,-40" fill="none" stroke="#b8923a" stroke-width="3"/>')
SHADOW = '<ellipse cx="0" cy="4" rx="64" ry="13" fill="#000" opacity="0.38"/>'


def athlete(name, hair, kit, kit2, stripes, shorts, socks, numc, num, skin):
    svg = part("athlete", f"w3-{name}x", HAIRSVG=hair, KITC=kit, KIT2=kit2, STRIPEOP=stripes, SHORTC=shorts, SOCKC=socks,
               NUMC=numc, NUM=num, SKIN=skin)
    return sprite(name, SHADOW + svg, 460, 600, 520)


sprites = []
for i in range(11):
    if i == 0:   # keepers
        sprites.append(athlete("M0", MESSI_HAIR, "#f2c230", "#f2c230", 0, "#1a1a2e", "#f2c230", "#1a1a2e", "1", "#e3b48c"))
        sprites.append(athlete("H0", HAALAND_HAIR, "#f07a1a", "#f07a1a", 0, "#1a1a2e", "#f07a1a", "#1a1a2e", "1", "#f1c9a5"))
        continue
    sprites.append(athlete(f"M{i}", MESSI_HAIR, "#a50044", "#1d3f9b", 1, "#1d2f6f", "#1d2f6f", "#ffd23f", "10", "#e3b48c"))
    sprites.append(athlete(f"H{i}", HAALAND_HAIR, "#6cabdd", "#6cabdd", 0, "#f4f4f2", "#6cabdd", "#14141f", "9", "#f1c9a5"))
sprites.append(ball())

write(EP, sprites, "", extra_css="\n    .bub.follow { font-size: 60px; padding: 16px 30px; border-radius: 44px; }")
