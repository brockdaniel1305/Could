"""S2E03 world layer: Mbappé (Real Madrid kit), the revolutionary mob, seven prisoners, Napoleon on his horse, Real Madrid players."""
import sys
from pathlib import Path

EP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EP.parents[1] / "tools/world3d"))
sys.path.insert(0, str(EP.parents[1] / "tools"))
from world import sprite, write, SHADOW, real, ball  # noqa: E402
from kit import part  # noqa: E402

sprites = [sprite("m", SHADOW + part("mbappe", "w3-mx", KITC="#f4f4f2", SHORTC="#f4f4f2", SOCKC="#f4f4f2", NUMC="#1a1a2e"))]
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
