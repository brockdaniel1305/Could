"""Shared world for episode 004 (Upamecano vs the 1940 invasion).

Side view: the defender stands left, attackers come from the right (east -> west), like a match on a pitch drawn into
the Ardennes. No real-world insignia anywhere (plain grey tanks). Below the caption band: a chalk tactics board.
"""
from scene import part  # noqa: F401

GY = 1150


def forest(sid, ard=True):
    trees = "".join(f'<g transform="translate({x},{y}) scale({s})">{part("tree", f"{sid}-t{i}")}</g>'
                    for i, (x, y, s) in enumerate([(60, 900, 0.8), (190, 880, 0.7), (330, 905, 0.85), (470, 885, 0.7), (610, 900, 0.8),
                                                   (750, 880, 0.72), (890, 905, 0.85), (1030, 890, 0.75)] if ard else []))
    return f"""
<defs><linearGradient id="{sid}-sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9fd0f0" /><stop offset="1" stop-color="#e6f1dc" /></linearGradient></defs>
<rect x="0" y="0" width="1080" height="1920" fill="url(#{sid}-sky)" />
<g fill="#fff" stroke="#1a1a2e" stroke-width="4"><path id="{sid}-cl1" d="M130,330 q30,-40 70,-10 q30,-30 60,0 q30,10 10,40 l-150,0 q-20,-10 10,-30 z" /><path id="{sid}-cl2" d="M700,260 q30,-40 70,-10 q30,-30 60,0 q30,10 10,40 l-150,0 q-20,-10 10,-30 z" /></g>
<path d="M0,820 Q180,700 360,790 Q540,690 720,780 Q900,700 1080,790 L1080,1000 L0,1000 Z" fill="#8cbf7a" stroke="#1a1a2e" stroke-width="5" />
{trees}
<rect x="0" y="910" width="1080" height="1010" fill="#5aa04c" />
<g fill="#4f9443"><rect x="0" y="910" width="135" height="1010" /><rect x="270" y="910" width="135" height="1010" /><rect x="540" y="910" width="135" height="1010" /><rect x="810" y="910" width="135" height="1010" /></g>
<path d="M0,910 L1080,910" stroke="#1a1a2e" stroke-width="5" />
<g id="{sid}-lines" stroke="#f4efe6" stroke-width="8" fill="none" opacity="0.85">
  <path d="M0,{GY + 40} L1080,{GY + 40}" /><path d="M540,930 L540,1340" /><ellipse cx="540" cy="{GY + 40}" rx="170" ry="60" />
</g>"""


def board(sid):
    """Chalk tactics board under the captions (graphics only): defenders = blue dots, attackers = grey arrows."""
    return f"""
<g id="{sid}-board">
  <rect x="50" y="1370" width="980" height="500" rx="26" fill="#23412f" stroke="#7a5230" stroke-width="18" />
  <g stroke="#e8efe6" stroke-width="5" fill="none" opacity="0.75"><rect x="100" y="1420" width="880" height="400" rx="6" /><path d="M540,1420 L540,1820" /><circle cx="540" cy="1620" r="70" /></g>
  <g id="{sid}-def" fill="#4f7cff" stroke="#e8efe6" stroke-width="4">
    <circle id="{sid}-d0" cx="360" cy="1480" r="18" /><circle id="{sid}-d1" cx="360" cy="1580" r="22" /><circle id="{sid}-d2" cx="360" cy="1680" r="18" /><circle id="{sid}-d3" cx="360" cy="1770" r="18" />
  </g>
  <g id="{sid}-att" stroke="#c9ccc2" stroke-width="8" fill="none" stroke-linecap="round" stroke-linejoin="round">
    <path id="{sid}-a0" d="M940,1480 Q700,1460 420,1500" /><path id="{sid}-a1" d="M940,1600 Q700,1620 420,1600" /><path id="{sid}-a2" d="M940,1730 Q700,1760 420,1720" />
  </g>
</g>"""


def defender(sid, x, scale=1.15):
    return f'<g transform="translate({x},{GY})"><g id="{sid}-kwrap"><g transform="scale({scale})">{part("centre-back", sid + "-u")}</g></g></g>'


def tank(sid, name, x, scale=0.9, y=GY):
    return f'<g transform="translate({x},{y})"><g id="{sid}-{name}"><g transform="scale({scale})">{part("tank", sid + "-" + name + "t")}</g></g></g>'
