"""S2E02 world layer: Van Dijk, six bulls and the runners (mozos) as 2D billboards in 3D Pamplona. The plot lives in director.js."""
import sys
from pathlib import Path

EP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EP.parents[1] / "tools/world3d"))
sys.path.insert(0, str(EP.parents[1] / "tools"))
from world import sprite, write, SHADOW  # noqa: E402
from kit import part  # noqa: E402
from stadium import player  # noqa: E402

# Van Dijk: the bearded playmaker rig recoloured - darker skin, black hair and beard, plain red kit, number 4 (no badges)
vvd = part("messi", "w3-vd", **{"#e3b48c": "#7a4e35", "#3b2416": "#17110d", "#a50044": "#c8102e", "#1d3f9b": "#c8102e",
                                "#1d2f6f": "#c8102e", ">10<": ">4<", 'fill="#ffd23f" stroke="#1a1a2e" stroke-width="2"': 'fill="#f4f4f2" stroke="#1a1a2e" stroke-width="2"'})
sprites = [sprite("v", SHADOW + f'<g id="w3-vv">{vvd}</g>')]

BULL_SHADOW = '<ellipse cx="0" cy="4" rx="150" ry="18" fill="#000" opacity="0.3"/>'
for i in range(1, 7):
    sprites.append(sprite(f"b{i}", BULL_SHADOW + part("bull", f"w3-b{i}x"), 520, 520, 420))

# runners: white shirt and trousers, red neckerchief and sash
SCARF = ('<path d="M-30,-208 L0,-176 L30,-208 Z" fill="#d8202c" stroke="#1a1a2e" stroke-width="4" stroke-linejoin="round"/>'
         '<rect x="-46" y="-128" width="92" height="16" rx="5" fill="#d8202c" stroke="#1a1a2e" stroke-width="4"/>')
for i in range(8):
    sprites.append(sprite(f"m{i}", SHADOW + player("w3", f"m{i}x", 0, 0, 1.0, kit="#f4f4f2", shorts="#f4f4f2", socks="#f4f4f2",
                                                   numc="#f4f4f2", num="", tag=False) + SCARF))

flag = ('<rect x="-4" y="-200" width="8" height="200" fill="#6b4a2a" stroke="#1a1a2e" stroke-width="2"/>'
        '<path d="M4,-200 L96,-200 L96,-140 L4,-140 Z" fill="#ffd23f" stroke="#1a1a2e" stroke-width="5"/>'
        '<path d="M4,-200 L50,-170 L4,-140 M96,-200 L50,-170 L96,-140" fill="#e0412f" opacity="0.9"/>')
sprites.append(sprite("lflag", flag, 260, 260, 240))

write(EP, sprites, "", extra_css="\n    .bub.follow { font-size: 66px; padding: 16px 34px; border-radius: 44px; }\n    .bub.name { font-size: 54px; }")
