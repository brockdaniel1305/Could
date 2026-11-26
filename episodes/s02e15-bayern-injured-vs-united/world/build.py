"""S2E15 world layer: Bayern's injured players (all red, with crutches, casts, bandages, a wheelchair) vs Manchester United
(red shirts, white shorts, black socks), United's new manager with an upside-down line-up, Bayern's physio, the referee.
Injuries are drawn into the athlete rig (casts/bandages inside the leg groups, crutches inside the arm group) so they move with the limbs."""
import re
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
        "bald": "",
    }[kind]


BEARD = lambda col: f'<path d="M-24,8 Q-22,34 0,40 Q22,34 24,8 Q14,24 0,26 Q-14,24 -24,8 Z" fill="{col}" opacity="0.75"/>'
HEADBAND = (f'<path d="M-31,-14 Q0,-26 31,-14 L31,-5 Q0,-17 -31,-5 Z" fill="#f4f1ea" stroke="{INK}" stroke-width="3"/>'
            f'<rect x="10" y="-22" width="12" height="12" fill="#f4f1ea" stroke="{INK}" stroke-width="2.5" transform="rotate(20 16 -16)"/>'
            '<path d="M13,-19 l6,6 M19,-19 l-6,6" stroke="#e0412f" stroke-width="2"/>')
# injuries drawn into the leg / arm groups (leg-local: leg rect x 6..27, y -152..-2 for legR; arm-local: shoulder at 0, hand at y 110)
CAST = (f'<rect x="1" y="-104" width="31" height="100" rx="10" fill="#f4f1ea" stroke="{INK}" stroke-width="4"/>'
        '<path d="M4,-90 L29,-80 M4,-70 L29,-60 M4,-50 L29,-40 M4,-30 L29,-20" stroke="#cfc6b4" stroke-width="3"/>')
BOOT = (f'<path d="M-2,-112 L34,-112 L36,-14 Q44,-12 44,0 L-6,0 L-4,-14 Z" fill="#2b2f36" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
        '<path d="M0,-92 L34,-92 M0,-70 L34,-70 M0,-48 L34,-48" stroke="#5b6270" stroke-width="5"/>')
THIGH = (f'<rect x="3" y="-150" width="27" height="40" rx="6" fill="#f4f1ea" stroke="{INK}" stroke-width="3.5"/>'
         '<path d="M5,-140 L28,-136 M5,-128 L28,-124 M5,-118 L28,-114" stroke="#cfc6b4" stroke-width="2.5"/>')
BRACE = (f'<rect x="2" y="-112" width="29" height="34" rx="6" fill="#1a1a2e" stroke="{INK}" stroke-width="3.5"/>'
         '<circle cx="16" cy="-95" r="6" fill="#5b6270"/>')
CRUTCH = (f'<path d="M14,-4 L10,268" stroke="#9aa3ad" stroke-width="8" stroke-linecap="round"/>'
          f'<path d="M14,-4 L10,268" stroke="{INK}" stroke-width="2" opacity="0.4"/>'
          f'<rect x="0" y="-12" width="30" height="12" rx="6" fill="#3a3f48" stroke="{INK}" stroke-width="3"/>'
          f'<rect x="2" y="104" width="22" height="9" rx="4" fill="#3a3f48" stroke="{INK}" stroke-width="2.5"/>'
          f'<rect x="4" y="262" width="12" height="12" rx="4" fill="#2b2f36"/>')
LEGL_FIX = lambda s: s  # (legL injuries are mirrored copies, see add())


def add(svg, name, group, extra):
    """append extra markup at the end of a rig group (so it moves with that limb)"""
    pat = re.compile(r'(<g id="w3-' + re.escape(name) + r'x-' + group + r'">.*?)(</g>)', re.S)
    out, n = pat.subn(lambda m: m.group(1) + extra + m.group(2), svg, count=1)
    assert n == 1, (name, group)
    return out


def player(name, num, kit, shorts, socks, numc, skin, hairsvg, inj=()):
    svg = part("athlete", f"w3-{name}x", HAIRSVG=hairsvg, KITC=kit, KIT2=kit, STRIPEOP=0, SHORTC=shorts, SOCKC=socks,
               NUMC=numc, NUM=num, SKIN=skin)
    for k in inj:
        if k == "cast": svg = add(svg, name, "legR", CAST)
        if k == "boot": svg = add(svg, name, "legR", BOOT)
        if k == "thigh": svg = add(svg, name, "legR", THIGH)
        if k == "thighL": svg = add(svg, name, "legL", f'<g transform="translate(-33,0)">{THIGH}</g>')
        if k == "brace": svg = add(svg, name, "legL", f'<g transform="translate(-33,0)">{BRACE}</g>')
        if k == "crutch": svg = add(svg, name, "armR", CRUTCH)
    return sprite(name, SHADOW + svg, 520, 700, 560)


FCB, MUN = "#dc052d", "#da291c"
sprites = []
# Bayern: the injury list
B = [  # name, num, skin, hair, injuries, kit override
    ("NEU", "1", "#f0c8a6", hair("short", "#d8b26a"), ("boot", "crutch"), "#2e8b57"),
    ("KIM", "3", "#e8c29a", hair("short", "#14141f") + HEADBAND, (), None),
    ("DAV", "19", "#6b4226", hair("buzz", "#14141f"), ("thigh",), None),
    ("PAV", "45", "#efc49e", hair("short", "#7a5a3a"), ("cast",), None),
    ("MUS", "10", "#a0673f", hair("curly", "#1c140f"), ("crutch", "thighL"), None),
    ("GNA", "7", "#7a4b2a", hair("buzz", "#14141f") + BEARD("#14141f"), ("thigh", "thighL"), None),
    ("DIA", "14", "#9a6a45", hair("curly", "#14141f"), ("crutch",), None),
    ("BUC", "40", "#efc49e", hair("short", "#6b4a2a"), ("brace",), None),
]
for n, num, skin, hs, inj, kit in B:
    sprites.append(player(n, num, kit or FCB, kit or FCB, kit or FCB, "#fff", skin, hs, inj))
# United: eleven fit players
U = [("U1", "1", "#e8c29a", "short", "#3a2a1a"), ("U2", "2", "#7a4b2a", "buzz", "#14141f"), ("U3", "5", "#efc49e", "quiff", "#a07a4a"),
     ("U4", "6", "#a0673f", "curly", "#14141f"), ("U5", "23", "#efc49e", "short", "#d8b26a"), ("U6", "8", "#e8c29a", "quiff", "#3a2a1a"),
     ("U7", "7", "#d9a07a", "short", "#1c140f"), ("U8", "18", "#7a4b2a", "buzz", "#14141f"), ("U9", "9", "#efc49e", "short", "#7a5a3a"),
     ("U10", "10", "#a0673f", "curly", "#1c140f"), ("U11", "11", "#e8c29a", "short", "#14141f")]
for n, num, skin, h, col in U:
    keeper = n == "U1"
    sprites.append(player(n, num, "#ffd23f" if keeper else MUN, "#14141f" if keeper else "#f4f4f2", "#14141f", INK if keeper else "#fff",
                          skin, hair(h, col)))
sprites.append(player("MGR", "", "#1a1a2e", "#1a1a2e", "#1a1a2e", "#fff", "#e3b48c", hair("short", "#8a8a8a")))
sprites.append(player("PHY", "+", "#14141f", "#14141f", "#14141f", "#fff", "#efc49e", hair("buzz", "#6b4a2a")))
sprites.append(player("REF", "", "#111111", "#111111", "#111111", "#ffd23f", "#e3b48c", hair("short", "#6b4a2a")))

# props: wheelchair with Saibari, the manager's upside-down line-up sheet
SAIB = part("athlete", "w3-SAIx", HAIRSVG=hair("curly", "#14141f"), KITC=FCB, KIT2=FCB, STRIPEOP=0, SHORTC=FCB, SOCKC=FCB, NUMC="#fff", NUM="21", SKIN="#8a5a3a")
WHEELCHAIR = (f'<ellipse cx="0" cy="4" rx="110" ry="16" fill="#000" opacity="0.35"/>'
              f'<g transform="translate(-6,-10) scale(0.92)"><g transform="translate(0,40)">{SAIB}</g></g>'
              f'<rect x="-70" y="-190" width="16" height="150" rx="6" fill="#5b6270" stroke="{INK}" stroke-width="4"/>'
              f'<rect x="-70" y="-120" width="150" height="16" rx="6" fill="#3a3f48" stroke="{INK}" stroke-width="4"/>'
              f'<circle cx="-30" cy="-60" r="58" fill="none" stroke="{INK}" stroke-width="12"/>'
              f'<circle cx="-30" cy="-60" r="58" fill="none" stroke="#9aa3ad" stroke-width="6"/>'
              f'<circle cx="-30" cy="-60" r="8" fill="{INK}"/><circle cx="70" cy="-14" r="14" fill="#2b2f36" stroke="{INK}" stroke-width="4"/>')
SHEET = (f'<rect x="-46" y="-120" width="92" height="120" rx="6" fill="#f4efe6" stroke="{INK}" stroke-width="5"/>'
         '<g transform="rotate(180 0 -60)"><text x="0" y="-92" text-anchor="middle" font-family="Inter" font-weight="900" font-size="20" fill="#1a1a2e">LINE-UP</text>'
         + "".join(f'<rect x="-34" y="{-80 + k * 14}" width="{50 + (k * 13) % 18}" height="6" rx="3" fill="#9aa3ad"/>' for k in range(5)) + "</g>")
sprites.append(sprite("wheelchair", WHEELCHAIR, 360, 520, 460))
sprites.append(sprite("sheet", SHEET, 140, 160, 140))
sprites.append(ball())

write(EP, sprites, "", extra_css="""
    .bub.follow { font-size: 58px; padding: 16px 30px; border-radius: 44px; }
    .bub.small { font-size: 30px; padding: 8px 16px; }
    .bub.fcb { background: #dc052d; color: #fff; }
    .bub.mun { background: #f4f4f2; color: #da291c; }""")
