"""Style test: 3D stadium background (Three.js) + our 2D SVG characters as projected billboards in front."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "tools"))
from stadium import messi_fig, player, football, REAL, REAL_NUMS  # noqa: E402

OUT = Path(__file__).parents[1] / "index.html"


def sprite(cid, inner, w=420, h=520, oy=440):
    return (f'<div class="bb" id="{cid}"><svg width="{w}" height="{h}" viewBox="{-w // 2} {-oy} {w} {h}" '
            f'style="position:absolute;left:{-w // 2}px;top:{-oy}px;overflow:visible">{inner}</svg></div>')


chars = [sprite("c-messi", '<ellipse cx="0" cy="4" rx="70" ry="14" fill="#000" opacity="0.35"/>' + messi_fig("t", 0, 0, 1.0, name="m", tag=False))]
chars.append(sprite("c-ball", '<ellipse cx="0" cy="4" rx="26" ry="7" fill="#000" opacity="0.3"/>' + football("t", 0, -38, 1.0, name="ball"), 200, 200, 160))
for i, n in enumerate(REAL_NUMS):
    chars.append(sprite(f"c-r{i}", '<ellipse cx="0" cy="4" rx="70" ry="14" fill="#000" opacity="0.35"/>'
                        + player("t", f"r{i}", 0, 0, 1.0, num=n, tag=False, **REAL)))

html = (Path(__file__).parent / "template.tpl").read_text().replace("<!--CHARS-->", "\n".join(chars))
OUT.write_text(html)
print("wrote", OUT)
