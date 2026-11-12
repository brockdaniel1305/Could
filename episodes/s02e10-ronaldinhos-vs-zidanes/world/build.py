"""S2E10 world layer: 11 prime Ronaldinhos (Barça 2005, stripes, No. 10, long curls, headband, big grin) and 11 prime Zidanes
(Real 2002, white, No. 5, bald with floodlight shine), referee."""
import sys
from pathlib import Path

EP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EP.parents[1] / "tools/world3d"))
sys.path.insert(0, str(EP.parents[1] / "tools"))
from world import sprite, write, ball  # noqa: E402
from kit import part  # noqa: E402

# Ronaldinho: long dark curls to the shoulders, white headband, the famous grin; Zidane: bald, short dark rim, shine on top
DINHO_HAIR = ('<path d="M-40,34 Q-48,-50 0,-54 Q48,-50 40,34 L30,36 Q34,-14 22,-26 L-22,-26 Q-34,-14 -30,36 Z" fill="#1a120e" stroke="#14141f" stroke-width="4" stroke-linejoin="round"/>'
              + "".join(f'<circle cx="{x}" cy="{y}" r="7" fill="#2a1c16"/>' for x, y in [(-36, 6), (-38, 22), (36, 6), (38, 22), (-24, -44), (0, -50), (24, -44)])
              + '<rect x="-34" y="-34" width="68" height="10" rx="4" fill="#f4f4f2" stroke="#14141f" stroke-width="3"/>'
              '<path d="M-15,15 Q0,31 15,15 Z" fill="#ffffff" stroke="#14141f" stroke-width="3.5" stroke-linejoin="round"/>'
              '<path d="M-12,18 L12,18 M-6,16 L-6,24 M0,16 L0,26 M6,16 L6,24" stroke="#c9c9c9" stroke-width="1.6"/>')
ZIDANE_HAIR = ('<path d="M-31,-6 Q-33,-20 -28,-30 L-24,-22 Q-27,-12 -26,-4 Z M31,-6 Q33,-20 28,-30 L24,-22 Q27,-12 26,-4 Z" fill="#3a2a1e" opacity="0.7"/>'
               '<ellipse cx="-8" cy="-38" rx="12" ry="6" fill="#ffffff" opacity="0.75" transform="rotate(-18 -8 -38)"/>')
REF_HAIR = '<path d="M-30,-16 Q-33,-44 0,-46 Q33,-44 30,-16 Q22,-30 0,-31 Q-22,-30 -30,-16 Z" fill="#6b4a2a" stroke="#14141f" stroke-width="4"/>'
SHADOW = '<ellipse cx="0" cy="4" rx="64" ry="13" fill="#000" opacity="0.38"/>'
DSKIN, ZSKIN = "#8a5a3c", "#e3b48c"


def athlete(name, hair, kit, kit2, stripes, shorts, socks, numc, num, skin):
    svg = part("athlete", f"w3-{name}x", HAIRSVG=hair, KITC=kit, KIT2=kit2, STRIPEOP=stripes, SHORTC=shorts, SOCKC=socks,
               NUMC=numc, NUM=num, SKIN=skin)
    return sprite(name, SHADOW + svg, 460, 600, 520)


sprites = []
for i in range(11):
    if i == 0:
        sprites.append(athlete("D0", DINHO_HAIR, "#f2c230", "#f2c230", 0, "#1a1a2e", "#f2c230", "#1a1a2e", "1", DSKIN))
        sprites.append(athlete("Z0", ZIDANE_HAIR, "#2bb3a3", "#2bb3a3", 0, "#1a1a2e", "#2bb3a3", "#1a1a2e", "1", ZSKIN))
        continue
    sprites.append(athlete(f"D{i}", DINHO_HAIR, "#a50044", "#1d3f9b", 1, "#1d2f6f", "#1d2f6f", "#ffd23f", "10", DSKIN))
    sprites.append(athlete(f"Z{i}", ZIDANE_HAIR, "#f4f4f2", "#f4f4f2", 0, "#f4f4f2", "#f4f4f2", "#14141f", "5", ZSKIN))
sprites.append(athlete("REF", REF_HAIR, "#111111", "#111111", 0, "#111111", "#111111", "#ffd23f", "", "#e3b48c"))
sprites.append(ball())

write(EP, sprites, "", extra_css="""
    .bub.follow { font-size: 58px; padding: 16px 30px; border-radius: 44px; }
    .bub.small { font-size: 30px; padding: 8px 16px; }""")
