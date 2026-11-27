"""S2E16 world layer: Chelsea (blue shirts, blue shorts, white socks; keeper orange-black) vs eleven orange traffic cones
(the keeper cone wears goalkeeper gloves), Xabi Alonso with a tactics board, the referee."""
import sys
from pathlib import Path

EP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EP.parents[1] / "tools/world3d"))
sys.path.insert(0, str(EP.parents[1] / "tools"))
from world import sprite, write, ball  # noqa: E402
from kit import part  # noqa: E402

INK = "#14141f"
SHADOW = '<ellipse cx="0" cy="4" rx="64" ry="13" fill="#000" opacity="0.38"/>'


def hair(kind, col):
    return {
        "short": f'<path d="M-30,-14 Q-33,-46 0,-48 Q33,-46 30,-14 Q22,-30 0,-31 Q-22,-30 -30,-14 Z" fill="{col}" stroke="{INK}" stroke-width="4"/>',
        "buzz": f'<path d="M-29,-16 Q-30,-42 0,-44 Q30,-42 29,-16 Q20,-28 0,-29 Q-20,-28 -29,-16 Z" fill="{col}" opacity="0.85"/>',
        "curly": f'<path d="M-32,-10 Q-40,-40 -16,-50 Q0,-60 16,-50 Q40,-40 32,-10 Q24,-26 0,-28 Q-24,-26 -32,-10 Z" fill="{col}" stroke="{INK}" stroke-width="4"/>'
                 + "".join(f'<circle cx="{x}" cy="{y}" r="7" fill="{col}" stroke="{INK}" stroke-width="2"/>' for x, y in ((-22, -40), (-6, -50), (12, -48), (26, -36))),
        "quiff": f'<path d="M-29,-18 Q-30,-44 0,-46 Q30,-44 29,-18 Q22,-34 0,-35 Q-22,-34 -29,-18 Z" fill="{col}" opacity="0.6"/>'
                 f'<path d="M-24,-34 Q-20,-62 6,-60 Q30,-58 26,-36 Q12,-44 -24,-34 Z" fill="{col}" stroke="{INK}" stroke-width="4"/>',
        # receding, swept back (the manager)
        "swept": f'<path d="M-30,-12 Q-34,-40 -14,-46 Q0,-40 14,-46 Q34,-40 30,-12 Q24,-30 14,-34 Q0,-30 -14,-34 Q-24,-30 -30,-12 Z" fill="{col}" stroke="{INK}" stroke-width="4"/>',
    }[kind]


BEARD = lambda col: f'<path d="M-25,4 Q-24,36 0,42 Q24,36 25,4 Q14,22 0,24 Q-14,22 -25,4 Z" fill="{col}" opacity="0.85"/>'


def player(name, num, kit, shorts, socks, numc, skin, hairsvg):
    svg = part("athlete", f"w3-{name}x", HAIRSVG=hairsvg, KITC=kit, KIT2=kit, STRIPEOP=0, SHORTC=shorts, SOCKC=socks,
               NUMC=numc, NUM=num, SKIN=skin)
    return sprite(name, SHADOW + svg, 520, 700, 560)


CHE = "#034694"
sprites = []
C = [("C1", "1", "#e8c29a", "short", "#3a2a1a"), ("C2", "24", "#7a4b2a", "buzz", "#14141f"), ("C3", "6", "#efc49e", "quiff", "#a07a4a"),
     ("C4", "29", "#a0673f", "curly", "#14141f"), ("C5", "3", "#e8c29a", "short", "#6b4a2a"), ("C6", "25", "#6b4226", "buzz", "#14141f"),
     ("C7", "8", "#efc49e", "short", "#d8b26a"), ("C8", "10", "#d9a07a", "quiff", "#1c140f"), ("C9", "7", "#7a4b2a", "curly", "#14141f"),
     ("C10", "20", "#efc49e", "short", "#7a5a3a"), ("C11", "11", "#a0673f", "buzz", "#14141f")]
for n, num, skin, h, col in C:
    keeper = n == "C1"
    sprites.append(player(n, num, "#ff7a1a" if keeper else CHE, INK if keeper else CHE, INK if keeper else "#f4f4f2",
                          INK if keeper else "#fff", skin, hair(h, col)))
sprites.append(player("XA", "", "#1a1a2e", "#1a1a2e", "#1a1a2e", "#fff", "#e3b48c", hair("swept", "#3a2a1a") + BEARD("#3a2a1a")))
sprites.append(player("REF", "", "#111111", "#111111", "#111111", "#ffd23f", "#e3b48c", hair("short", "#6b4a2a")))

# traffic cones: drawn 300 px tall (unit 300 -> h metres); stripes; the keeper cone wears gloves
GLOVES = (f'<g><ellipse cx="-62" cy="-130" rx="20" ry="24" fill="#c6ff3a" stroke="{INK}" stroke-width="5"/>'
          f'<rect x="-74" y="-112" width="24" height="18" rx="5" fill="#14141f"/>'
          f'<ellipse cx="62" cy="-130" rx="20" ry="24" fill="#c6ff3a" stroke="{INK}" stroke-width="5"/>'
          f'<rect x="50" y="-112" width="24" height="18" rx="5" fill="#14141f"/>'
          f'<path d="M-44,-120 L-58,-126 M44,-120 L58,-126" stroke="{INK}" stroke-width="6" stroke-linecap="round"/></g>')


def cone(name, gloves=False, num=None):
    svg = ('<ellipse cx="0" cy="2" rx="96" ry="18" fill="#000" opacity="0.35"/>'
           f'<rect x="-92" y="-22" width="184" height="24" rx="6" fill="#ff6a13" stroke="{INK}" stroke-width="6"/>'
           f'<path d="M-62,-22 L-14,-292 Q0,-300 14,-292 L62,-22 Z" fill="#ff7a1a" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
           '<path d="M-50,-90 L50,-90 L42,-130 L-42,-130 Z" fill="#f6f6f2"/>'
           '<path d="M-34,-180 L34,-180 L28,-212 L-28,-212 Z" fill="#f6f6f2"/>'
           '<path d="M-20,-260 L-6,-285 Q0,-290 6,-285" stroke="#ffd0a8" stroke-width="7" fill="none" stroke-linecap="round"/>'
           '<path d="M30,-40 L4,-280" stroke="#c94e05" stroke-width="10" opacity="0.35"/>')
    if num:
        svg += f'<text class="num" x="0" y="-146" text-anchor="middle" font-family="Inter" font-weight="900" font-size="34" fill="{INK}">{num}</text>'
    if gloves:
        svg += GLOVES
    return sprite(name, svg, 260, 340, 310)


for k in range(1, 12):
    sprites.append(cone(f"K{k}", gloves=k == 1))

# props: tactics board (Alonso), the cone net bag, confetti
BOARD = (f'<rect x="-70" y="-110" width="140" height="100" rx="8" fill="#f4f4f2" stroke="{INK}" stroke-width="6"/>'
         '<rect x="-60" y="-100" width="120" height="80" fill="#2e8b57"/>'
         '<path d="M-40,-60 Q0,-95 40,-60" stroke="#fff" stroke-width="4" fill="none" stroke-dasharray="8 6"/>'
         '<path d="M34,-68 L44,-58 L30,-56 Z" fill="#fff"/>'
         + "".join(f'<path d="M{x - 6},-{y} L{x},-{y + 12} L{x + 6},-{y} Z" fill="#ff7a1a"/>' for x, y in ((-30, 44), (-6, 70), (16, 46), (8, 32)))
         + "".join(f'<circle cx="{x}" cy="-{y}" r="5" fill="#034694" stroke="#fff" stroke-width="2"/>' for x, y in ((-44, 52), (-20, 36), (40, 36))))
CONF = "".join(f'<rect x="{x}" y="{y}" width="14" height="22" rx="3" fill="{c}" transform="rotate({r} {x} {y})"/>'
               for x, y, r, c in ((-200, -500, 20, "#ff7a1a"), (-120, -380, -30, "#ffd23f"), (-40, -520, 50, "#f6f6f2"), (60, -420, -15, "#ff7a1a"),
                                  (150, -540, 35, "#ffd23f"), (210, -360, -40, "#f6f6f2"), (-180, -250, 10, "#ffd23f"), (100, -230, 60, "#ff7a1a"),
                                  (-80, -160, -50, "#f6f6f2"), (20, -320, 25, "#ffd23f"), (180, -150, -20, "#ff7a1a"), (-230, -120, 45, "#f6f6f2")))
sprites.append(sprite("board", BOARD, 160, 130, 115))
sprites.append(sprite("confetti", CONF, 520, 600, 580))
sprites.append(ball())

write(EP, sprites, "", extra_css="""
    .bub.follow { font-size: 58px; padding: 16px 30px; border-radius: 44px; }
    .bub.small { font-size: 30px; padding: 8px 16px; }
    .bub.che { background: #034694; color: #fff; }
    .bub.cone { background: #ff7a1a; color: #14141f; }""")
