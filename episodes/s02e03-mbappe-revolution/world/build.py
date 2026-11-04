"""S2E03 world layer: Mbappé (Real Madrid kit), the revolutionary mob, seven prisoners, Napoleon on his horse, Real Madrid players."""
import sys
from pathlib import Path

EP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EP.parents[1] / "tools/world3d"))
sys.path.insert(0, str(EP.parents[1] / "tools"))
from world import sprite, write, SHADOW, real, ball  # noqa: E402
from kit import part  # noqa: E402
import re  # noqa: E402

# Mbappé the dictator: olive tunic with gold buttons, epaulettes and medals, red-and-gold sash, dark trousers, boots, peaked cap
OLIVE, GOLD, RED = "#3f4a32", "#d4a017", "#b0122b"
d = part("mbappe", "w3-mx", KITC=OLIVE, SHORTC="#23272e", SOCKC="#111111", NUMC=GOLD).replace(">10</text>", "></text>")
d = re.sub(r'(<g id="w3-mx-leg[LR]"><rect [^>]*?)fill="#8a5a3c"', r'\1fill="#23272e"', d)
d = re.sub(r'(<g id="w3-mx-arm[LR]"><rect [^>]*?)fill="#8a5a3c"', r'\1fill="' + OLIVE + '"', d)
d = d.replace('<g id="w3-mx-sash" opacity="0">', '<g id="w3-mx-sash">').replace('fill="#1d3f9b" stroke="#1a1a2e" stroke-width="3"', f'fill="{RED}" stroke="#1a1a2e" stroke-width="3"')
d = d.replace('<path d="M-30,-210 L-16,-212 L50,-134 L48,-122 Z" fill="#f4f4f2" />', f'<path d="M-30,-210 L-16,-212 L50,-134 L48,-122 Z" fill="{GOLD}" />')
deco = (f'<g>{"".join(f"<circle cx=\"0\" cy=\"{y}\" r=\"4.5\" fill=\"{GOLD}\" stroke=\"#1a1a2e\" stroke-width=\"2\"/>" for y in (-188, -168, -148, -128))}'
        f'<rect x="-62" y="-212" width="26" height="12" rx="4" fill="{GOLD}" stroke="#1a1a2e" stroke-width="3"/><rect x="36" y="-212" width="26" height="12" rx="4" fill="{GOLD}" stroke="#1a1a2e" stroke-width="3"/>'
        f'<circle cx="-30" cy="-176" r="6" fill="{GOLD}" stroke="#1a1a2e" stroke-width="2"/><circle cx="-18" cy="-174" r="6" fill="#c0262d" stroke="#1a1a2e" stroke-width="2"/><circle cx="-24" cy="-162" r="6" fill="#2b4f8f" stroke="#1a1a2e" stroke-width="2"/></g>')
d = d.replace('<text id="w3-mx-num"', deco + '<text id="w3-mx-num"', 1)
cap = (f'<path d="M-48,-26 Q-56,-78 0,-86 Q56,-78 48,-26 Z" fill="{OLIVE}" stroke="#1a1a2e" stroke-width="5" stroke-linejoin="round"/>'
       f'<rect x="-48" y="-38" width="96" height="13" fill="{RED}" stroke="#1a1a2e" stroke-width="3"/>'
       '<path d="M-52,-24 Q0,-6 52,-24 Q0,-30 -52,-24 Z" fill="#111" stroke="#1a1a2e" stroke-width="3"/>'
       f'<circle cx="0" cy="-54" r="9" fill="{GOLD}" stroke="#1a1a2e" stroke-width="3"/>')
d = d.replace('<g id="w3-mx-crown" opacity="0">', cap + '<g id="w3-mx-crown" opacity="0">', 1)
sprites = [sprite("m", SHADOW + d)]
CAPS = ["#c22f2f", "#c22f2f", "#2b4f8f", "#c22f2f", "#8a2b2b", "#c22f2f", "#2b4f8f", "#c22f2f"]
for i in range(8):
    sprites.append(sprite(f"c{i}", SHADOW + part("citizen", f"w3-c{i}x", CAPC=CAPS[i])))
for i in range(7):   # prisoners: grey caps, no pitchfork
    sprites.append(sprite(f"p{i}", SHADOW + part("citizen", f"w3-p{i}x", CAPC="#8d8a84").replace(f'id="w3-p{i}x-fork"', f'id="w3-p{i}x-fork" opacity="0"')))
horse = part("napoleon-horse", "w3-nx")
for leg, cls in [("hFL", "legA"), ("hBR", "legA"), ("hFR", "legB"), ("hBL", "legB")]:
    horse = horse.replace(f'id="w3-nx-{leg}"', f'id="w3-nx-{leg}" class="{cls}"')
sprites.append(sprite("nap", '<ellipse cx="0" cy="6" rx="210" ry="14" fill="#000" opacity="0.25"/>' + horse, 640, 700, 640))
sprites.append(real("r0", 1, kit="#2bb3a3", shorts="#1a1a2e", socks="#2bb3a3", numc="#1a1a2e"))
sprites += [real(f"r{i}", n) for i, n in [(1, 5), (2, 8), (3, 7)]]
sprites.append(ball())

write(EP, sprites, "", extra_css="\n    .bub.follow { font-size: 60px; padding: 16px 30px; border-radius: 44px; }")
