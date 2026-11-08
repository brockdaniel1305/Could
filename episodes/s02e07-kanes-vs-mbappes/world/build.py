"""S2E07 world layer: 11 Kanes (white, No. 9) and 11 Mbappés (navy, No. 10), referee, linesman, the golden Ballon d'Or prop."""
import sys
from pathlib import Path

EP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EP.parents[1] / "tools/world3d"))
sys.path.insert(0, str(EP.parents[1] / "tools"))
from world import sprite, write, ball  # noqa: E402
from kit import part  # noqa: E402

# Kane: short light-brown hair, side parting; Mbappé: shaved head (dark buzz)
KANE_HAIR = ('<path d="M-31,-12 Q-34,-48 0,-50 Q34,-48 31,-12 Q26,-30 8,-32 Q-14,-34 -31,-12 Z" fill="#8a6440" stroke="#14141f" stroke-width="4" stroke-linejoin="round"/>'
             '<path d="M-20,-38 Q2,-48 24,-36 Q4,-40 -20,-38 Z" fill="#a37a52"/>')
MBAPPE_HAIR = '<path d="M-30,-18 Q-31,-46 0,-47 Q31,-46 30,-18 Q22,-36 0,-37 Q-22,-36 -30,-18 Z" fill="#1a120e" opacity="0.85"/>'
REF_HAIR = '<path d="M-30,-16 Q-33,-44 0,-46 Q33,-44 30,-16 Q22,-30 0,-31 Q-22,-30 -30,-16 Z" fill="#6b4a2a" stroke="#14141f" stroke-width="4"/>'
SHADOW = '<ellipse cx="0" cy="4" rx="64" ry="13" fill="#000" opacity="0.38"/>'
NAVY = "#1d2a5c"

# the Ballon d'Or: golden ball with panel lines on a dark plinth; origin = base centre, ~170 px tall
BDOR = ('<ellipse cx="0" cy="4" rx="60" ry="12" fill="#000" opacity="0.35"/>'
        '<path d="M-44,0 L44,0 L34,-38 L-34,-38 Z" fill="#2a2420" stroke="#14141f" stroke-width="5" stroke-linejoin="round"/>'
        '<rect x="-22" y="-30" width="44" height="12" rx="3" fill="#c9a24a" stroke="#14141f" stroke-width="3"/>'
        '<circle cx="0" cy="-98" r="62" fill="#f3c55b" stroke="#14141f" stroke-width="5"/>'
        '<path d="M-60,-104 Q0,-80 60,-104 M-34,-150 Q-10,-98 -30,-46 M34,-150 Q10,-98 30,-46 M-50,-130 Q0,-118 50,-130" fill="none" stroke="#b8862b" stroke-width="4"/>'
        '<ellipse cx="-22" cy="-124" rx="16" ry="10" fill="#fff6cf" opacity="0.8"/>')


def athlete(name, hair, kit, kit2, stripes, shorts, socks, numc, num, skin):
    svg = part("athlete", f"w3-{name}x", HAIRSVG=hair, KITC=kit, KIT2=kit2, STRIPEOP=stripes, SHORTC=shorts, SOCKC=socks,
               NUMC=numc, NUM=num, SKIN=skin)
    return sprite(name, SHADOW + svg, 460, 600, 520)


sprites = []
for i in range(11):
    if i == 0:
        sprites.append(athlete("K0", KANE_HAIR, "#2bb3a3", "#2bb3a3", 0, "#1a1a2e", "#2bb3a3", "#1a1a2e", "1", "#f0c8a6"))
        sprites.append(athlete("M0", MBAPPE_HAIR, "#f2c230", "#f2c230", 0, "#1a1a2e", "#f2c230", "#1a1a2e", "1", "#7a4e35"))
        continue
    sprites.append(athlete(f"K{i}", KANE_HAIR, "#f4f4f2", "#f4f4f2", 0, NAVY, "#f4f4f2", NAVY, "9", "#f0c8a6"))
    sprites.append(athlete(f"M{i}", MBAPPE_HAIR, NAVY, NAVY, 0, "#f4f4f2", "#d7263d", "#f4f4f2", "10", "#7a4e35"))
sprites.append(athlete("REF", REF_HAIR, "#111111", "#111111", 0, "#111111", "#111111", "#ffd23f", "", "#e3b48c"))
sprites.append(athlete("LIN", REF_HAIR, "#111111", "#111111", 0, "#111111", "#111111", "#ffd23f", "", "#d9a07a"))
sprites.append(sprite("bdor", BDOR, 200, 240, 200))
sprites.append(ball())

write(EP, sprites, "", extra_css="""
    .bub.follow { font-size: 58px; padding: 16px 30px; border-radius: 44px; }
    .bub.small { font-size: 30px; padding: 8px 16px; }
    .votes { left: 70px; right: 70px; top: 330px; padding: 22px 28px 26px; background: #14141f; border: 5px solid #f3c55b; border-radius: 18px;
             box-shadow: 8px 8px 0 #000; color: #f4f4f2; font: 900 34px/1 "Inter"; }
    .votes .hd { font: 700 26px/1 "CouldMono"; color: #f3c55b; letter-spacing: 0.16em; margin-bottom: 18px; }
    .votes .row { display: flex; align-items: center; gap: 16px; margin-top: 14px; }
    .votes .nm { width: 170px; } .votes .bar { height: 46px; border-radius: 8px; border: 4px solid #000; }
    .votes .pt { font: 800 32px/1 "CouldMono"; }
    .flash { left: 0; top: 0; width: 1080px; height: 1920px; background: rgba(120, 82, 30, 0.42); mix-blend-mode: multiply; }
    .flashlbl { left: 60px; top: 380px; padding: 12px 26px; background: #f4e3c0; color: #3a2a14; border: 5px solid #3a2a14; border-radius: 10px;
                font: 900 64px/1 "Inter"; transform: rotate(-4deg); }""")
