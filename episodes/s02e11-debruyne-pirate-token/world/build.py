"""S2E11 world layer: Kevin De Bruyne (ginger, Belgium red, No. 7), a random teammate (grey hoodie), another player
(green hoodie) opening chests, plus props: football parachute, the hero chest (closed / open with glow), the pirate token."""
import sys
from pathlib import Path

EP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EP.parents[1] / "tools/world3d"))
sys.path.insert(0, str(EP.parents[1] / "tools"))
from world import sprite, write  # noqa: E402
from kit import part  # noqa: E402

KDB_HAIR = ('<path d="M-31,-12 Q-34,-48 0,-50 Q34,-48 31,-12 Q22,-30 2,-31 Q-20,-30 -31,-12 Z" fill="#d9894a" stroke="#14141f" stroke-width="4" stroke-linejoin="round"/>'
            '<path d="M-22,-32 Q0,-46 24,-34 Q4,-36 -22,-26 Z" fill="#e8a060"/>'
            '<path d="M-14,30 Q0,37 14,30 L14,25 Q0,31 -14,25 Z" fill="#d9894a" opacity="0.45"/>')
def HOOD(col):
    return (f'<path d="M-40,30 Q-48,-58 0,-62 Q48,-58 40,30 L32,32 Q36,-30 0,-34 Q-36,-30 -32,32 Z" fill="{col}" stroke="#14141f" stroke-width="4" stroke-linejoin="round"/>'
            f'<path d="M-8,34 L-8,52 M8,34 L8,52" stroke="#f4f4f2" stroke-width="3"/>')
SHADOW = '<ellipse cx="0" cy="4" rx="64" ry="13" fill="#000" opacity="0.38"/>'

CHEST = ('<ellipse cx="0" cy="4" rx="80" ry="12" fill="#000" opacity="0.3"/>'
         '<rect x="-70" y="-70" width="140" height="70" rx="6" fill="#8b4f22" stroke="#14141f" stroke-width="6"/>'
         '<path d="M-70,-70 Q-70,-118 0,-118 Q70,-118 70,-70 Z" fill="#a55e2a" stroke="#14141f" stroke-width="6" stroke-linejoin="round"/>'
         '<rect x="-52" y="-118" width="14" height="118" fill="#f3c55b" stroke="#14141f" stroke-width="4"/>'
         '<rect x="38" y="-118" width="14" height="118" fill="#f3c55b" stroke="#14141f" stroke-width="4"/>'
         '<rect x="-12" y="-82" width="24" height="26" rx="4" fill="#f3c55b" stroke="#14141f" stroke-width="4"/>')
CHEST_OPEN = ('<ellipse cx="0" cy="4" rx="80" ry="12" fill="#000" opacity="0.3"/>'
              '<ellipse cx="0" cy="-90" rx="120" ry="90" fill="#ffe27a" opacity="0.45"/>'
              '<rect x="-70" y="-70" width="140" height="70" rx="6" fill="#8b4f22" stroke="#14141f" stroke-width="6"/>'
              '<path d="M-70,-70 L-60,-150 L60,-150 L70,-70" fill="#5a3216" stroke="#14141f" stroke-width="6" stroke-linejoin="round"/>'
              '<ellipse cx="0" cy="-72" rx="62" ry="12" fill="#ffd23f"/>'
              '<rect x="-52" y="-70" width="14" height="70" fill="#f3c55b" stroke="#14141f" stroke-width="4"/>'
              '<rect x="38" y="-70" width="14" height="70" fill="#f3c55b" stroke="#14141f" stroke-width="4"/>')
TOKEN = ('<circle cx="0" cy="-60" r="58" fill="#ffd23f" stroke="#14141f" stroke-width="6"/>'
         '<circle cx="0" cy="-60" r="44" fill="none" stroke="#c9952a" stroke-width="5"/>'
         '<path d="M-26,-86 L26,-34 M26,-86 L-26,-34" stroke="#14141f" stroke-width="9" stroke-linecap="round"/>'
         '<path d="M-26,-86 L26,-34 M26,-86 L-26,-34" stroke="#e9eef5" stroke-width="5" stroke-linecap="round"/>'
         '<path d="M-36,-40 L-18,-40 M18,-40 L36,-40" stroke="#14141f" stroke-width="7" stroke-linecap="round"/>'
         '<ellipse cx="-20" cy="-88" rx="12" ry="7" fill="#fff6cf" opacity="0.8"/>')
CHUTE = ('<path d="M-130,-200 Q0,-330 130,-200 Q0,-230 -130,-200 Z" fill="#f4f4f2" stroke="#14141f" stroke-width="6" stroke-linejoin="round"/>'
         '<path d="M-40,-262 L0,-282 L40,-262 L30,-226 L-30,-226 Z" fill="#14141f"/>'
         '<path d="M-118,-206 L-96,-238 L-70,-224 M118,-206 L96,-238 L70,-224" fill="none" stroke="#14141f" stroke-width="6"/>'
         '<path d="M-126,-202 L-14,0 M-50,-218 L-6,0 M50,-218 L6,0 M126,-202 L14,0" stroke="#14141f" stroke-width="3"/>')


def athlete(name, hair, kit, kit2, stripes, shorts, socks, numc, num, skin):
    svg = part("athlete", f"w3-{name}x", HAIRSVG=hair, KITC=kit, KIT2=kit2, STRIPEOP=stripes, SHORTC=shorts, SOCKC=socks,
               NUMC=numc, NUM=num, SKIN=skin)
    return sprite(name, SHADOW + svg, 460, 600, 520)


sprites = [athlete("K", KDB_HAIR, "#c8102e", "#c8102e", 0, "#c8102e", "#c8102e", "#ffd23f", "7", "#f2c9a8"),
           athlete("T", HOOD("#8a8f98"), "#8a8f98", "#8a8f98", 0, "#2a2a33", "#2a2a33", "#8a8f98", "", "#e0ac7e"),
           athlete("O", HOOD("#4f9d69"), "#4f9d69", "#4f9d69", 0, "#2a2a33", "#2a2a33", "#4f9d69", "", "#c68863"),
           sprite("chute", CHUTE, 300, 360, 340), sprite("chest", CHEST, 200, 160, 140), sprite("chestopen", CHEST_OPEN, 280, 260, 220),
           sprite("token", TOKEN, 140, 140, 130), sprite("ochest", CHEST, 200, 160, 140)]

write(EP, sprites, "", extra_css="""
    .bub.follow { font-size: 58px; padding: 16px 30px; border-radius: 44px; }
    .bub.small { font-size: 30px; padding: 8px 16px; }
    .vision { left: 0; top: 0; width: 1080px; height: 1920px; }
    .brmap { left: auto; right: 40px; top: 96px; width: 220px; height: 220px; border-radius: 50%; border: 5px solid #f4f4f2; box-shadow: 0 0 0 4px #14141f, 6px 6px 0 4px #14141f; overflow: hidden; }
    .brstat { left: auto; right: 40px; top: 336px; width: 230px; display: flex; justify-content: space-between; font: 900 34px/1 "Inter"; color: #f4f4f2;
              text-shadow: 0 3px 0 #14141f, 0 0 8px #14141f; }
    .brbars { left: 50px; top: 1730px; width: 470px; }
    .brbars .bar { position: relative; height: 34px; margin-top: 10px; border: 4px solid #14141f; border-radius: 8px; background: #2a2a33; overflow: hidden; }
    .brbars .bar i { position: absolute; left: 0; top: 0; bottom: 0; width: 100%; }
    .brbars .sh i { background: linear-gradient(#5ec8ff, #2a8ad9); } .brbars .hp i { background: linear-gradient(#7ee35a, #3f9f2a); }
    .brbars .bar b { position: absolute; right: 12px; top: 2px; font: 900 24px/1 "Inter"; color: #fff; text-shadow: 0 2px 0 #14141f; }
    .brhot { left: auto; right: 40px; top: 1726px; display: flex; gap: 10px; }
    .brhot i { width: 76px; height: 76px; border: 4px solid #14141f; border-radius: 10px; background: rgba(20,20,31,0.55); font: 44px/76px "Inter"; text-align: center; font-style: normal; }
    .brhot i.gold { background: linear-gradient(#ffe27a, #e6a020); box-shadow: 0 0 18px #ffd23f; }
    .brfeed { left: 40px; top: 300px; padding: 10px 18px; background: rgba(20,20,31,0.72); border-radius: 8px; font: 800 30px/1.1 "Inter"; color: #f4f4f2; }
    .brfeed b { color: #5ec8ff; } .brfeed em { color: #ffd23f; font-style: normal; }
    .vision path { fill: none; stroke: #ffd23f; stroke-width: 10; stroke-dasharray: 28 22; stroke-linecap: round; filter: drop-shadow(0 0 10px #ffd23f); }""")
