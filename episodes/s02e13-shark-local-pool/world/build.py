"""S2E13 world layer: shark fins (bull shark, great white), the lifeguard, swimmers on floats, a golfer, props (coffee cup, signs)."""
import sys
from pathlib import Path

EP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EP.parents[1] / "tools/world3d"))
sys.path.insert(0, str(EP.parents[1] / "tools"))
from world import sprite, write  # noqa: E402
from kit import part  # noqa: E402

SHADOW = '<ellipse cx="0" cy="4" rx="64" ry="13" fill="#000" opacity="0.3"/>'
HAIR = lambda col: f'<path d="M-30,-16 Q-33,-46 0,-48 Q33,-46 30,-16 Q22,-32 0,-33 Q-22,-32 -30,-16 Z" fill="{col}" stroke="#14141f" stroke-width="4"/>'
CAP = '<path d="M-33,-10 Q-36,-50 0,-52 Q36,-50 33,-10 Q20,-26 0,-26 Q-20,-26 -33,-10 Z" fill="#f4f4f2" stroke="#14141f" stroke-width="4"/><rect x="-36" y="-14" width="72" height="9" rx="4" fill="#14141f" opacity="0.8"/>'


def athlete(name, hair, kit, shorts, skin, num=""):
    svg = part("athlete", f"w3-{name}x", HAIRSVG=hair, KITC=kit, KIT2=kit, STRIPEOP=0, SHORTC=shorts, SOCKC=skin, NUMC="#f4f4f2", NUM=num, SKIN=skin)
    return sprite(name, SHADOW + svg, 460, 600, 520)


def fin(name, body, belly):
    # a dorsal fin + a hint of back cutting the water, with a little bow wave; origin = water line
    return sprite(name, f'<g transform="scale(-1,1)"><ellipse cx="0" cy="6" rx="150" ry="16" fill="#ffffff" opacity="0.55"/>'
                        f'<path d="M-170,6 Q-40,-30 150,6 Z" fill="{body}" stroke="#14141f" stroke-width="5" stroke-linejoin="round"/>'
                        f'<path d="M-40,-14 Q-10,-150 60,-150 Q20,-90 70,-6 Z" fill="{body}" stroke="#14141f" stroke-width="6" stroke-linejoin="round"/>'
                        f'<path d="M-20,-30 Q4,-120 46,-138" fill="none" stroke="{belly}" stroke-width="5" opacity="0.6"/>'
                        f'<path d="M-190,10 Q-150,-2 -110,10 M110,10 Q150,-2 190,10" fill="none" stroke="#ffffff" stroke-width="6" stroke-linecap="round" opacity="0.8"/></g>', 420, 220, 170)


FLOAT = ('<ellipse cx="0" cy="-6" rx="120" ry="26" fill="#ff7a59" stroke="#14141f" stroke-width="5"/>'
         '<ellipse cx="0" cy="-12" rx="96" ry="12" fill="#ffb199"/>'
         '<circle cx="-70" cy="-44" r="26" fill="#e3b48c" stroke="#14141f" stroke-width="4"/><path d="M-96,-48 Q-70,-80 -44,-48 Z" fill="#6b4a2a"/>'
         '<rect x="-84" y="-52" width="28" height="9" rx="4" fill="#14141f"/>'
         '<path d="M-44,-30 Q20,-40 80,-28" fill="none" stroke="#e3b48c" stroke-width="18" stroke-linecap="round"/>')
CUP = ('<path d="M-22,-60 L22,-60 L16,0 L-16,0 Z" fill="#f4f4f2" stroke="#14141f" stroke-width="5" stroke-linejoin="round"/>'
       '<rect x="-24" y="-68" width="48" height="10" rx="3" fill="#7a4e35" stroke="#14141f" stroke-width="4"/>'
       '<path d="M-10,-80 Q-4,-92 -10,-104 M6,-80 Q12,-92 6,-104" fill="none" stroke="#9aa5b1" stroke-width="4" stroke-linecap="round"/>')
CLUB = '<path d="M0,0 L0,-150" stroke="#9aa5b1" stroke-width="7"/><path d="M-4,0 L22,0 L22,-12 L-4,-8 Z" fill="#5a5f69" stroke="#14141f" stroke-width="3"/>'


def sign(name, lines, bg="#f4f4f2", fg="#14141f", w=380):
    h = 60 + 52 * len(lines)
    txt = "".join(f'<text x="0" y="{-h + 70 + 52 * i}" text-anchor="middle" font-family="Inter" font-weight="900" font-size="40" fill="{fg}">{t}</text>' for i, t in enumerate(lines))
    return sprite(name, f'<rect x="-8" y="-40" width="16" height="40" fill="#5a5f69"/><rect x="{-w // 2}" y="{-h - 30}" width="{w}" height="{h}" rx="12" fill="{bg}" stroke="#14141f" stroke-width="7"/>{txt}',
                  w + 40, h + 120, h + 80)


def body(name, col, belly, water):
    # a whole shark side-on at the surface (nose right), the lower half under a band of water; origin = water line
    shark = (f'<path d="M-150,0 Q-60,-62 90,-30 Q140,-20 170,-2 Q140,22 90,26 Q-60,52 -150,0 Z" fill="{col}" stroke="#14141f" stroke-width="6" stroke-linejoin="round"/>'
             f'<path d="M-120,12 Q-40,40 90,22 Q40,8 -120,12 Z" fill="{belly}"/>'
             f'<path d="M-20,-46 Q10,-120 50,-118 Q30,-80 40,-34 Z" fill="{col}" stroke="#14141f" stroke-width="6" stroke-linejoin="round"/>'
             f'<path d="M-150,0 L-215,-60 Q-200,0 -215,56 Z" fill="{col}" stroke="#14141f" stroke-width="6" stroke-linejoin="round"/>'
             '<circle cx="110" cy="-10" r="8" fill="#14141f"/><circle cx="113" cy="-13" r="2.5" fill="#fff"/>'
             '<path d="M70,-14 Q74,0 70,12 M58,-16 Q62,0 58,14 M46,-16 Q50,0 46,16" fill="none" stroke="#14141f" stroke-width="4"/>'
             '<path d="M120,10 Q140,18 160,6" fill="none" stroke="#14141f" stroke-width="4"/><path d="M126,12 l4,7 l4,-6 l4,7 l4,-6 l4,6" fill="#fff" stroke="#14141f" stroke-width="2"/>')
    return sprite(name, f'<g transform="translate(0,-4)">{shark}</g><defs><linearGradient id="wb{name}" x1="0" x2="1"><stop offset="0" stop-color="{water}" stop-opacity="0"/><stop offset="0.15" stop-color="{water}"/><stop offset="0.85" stop-color="{water}"/><stop offset="1" stop-color="{water}" stop-opacity="0"/></linearGradient></defs><rect x="-250" y="2" width="460" height="34" fill="url(#wb{name})" opacity="0.95"/>'
                        '<path d="M-240,4 Q-210,-6 -180,4 T-120,4 T-60,4 T0,4 T60,4 T120,4 T180,4 T200,4" fill="none" stroke="#ffffff" stroke-width="6" stroke-linecap="round" opacity="0.85"/>',
                  480, 260, 150)


CUTOUT = ('<rect x="-7" y="-40" width="14" height="60" fill="#a8743f" stroke="#14141f" stroke-width="4"/>'
          '<path d="M-150,-30 Q-110,-190 30,-200 Q-10,-120 60,-30 Z" fill="#c9a26b" stroke="#14141f" stroke-width="6" stroke-linejoin="round"/>'
          '<path d="M-138,-36 Q-100,-180 22,-192 Q-16,-118 50,-36 Z" fill="#7c8794"/>'
          '<path d="M-150,-30 L60,-30" stroke="#14141f" stroke-width="6"/>')

sprites = [body("SHK", "#8a8370", "#c9c0a8", "#3a8394"), fin("BULL3", "#8a8370", "#c9c0a8"), sprite("cut", CUTOUT, 340, 280, 230), sprite("cutfin", CUTOUT.split("/>", 1)[1], 340, 280, 230),
           sign("pipe10", ["PIPE", "Ø 10 cm"], "#f4f4f2", "#14141f", 240), sign("salt", ["SEA", "SALT WATER"], "#1d3f9b", "#ffffff", 330),
           sign("fresh", ["RIVER", "FRESH WATER"], "#2bb34a", "#ffffff", 340), sign("deadend", ["DEAD END"], "#ffd23f", "#14141f", 320),
           sign("amz", ["AMAZON"], "#2bb34a", "#ffffff", 300), sign("iq", ["IQUITOS · PERU", "4,000 km"], "#ffd23f", "#14141f", 380),
           sign("hwy", ["HIGHWAY"], "#1f9d55", "#ffffff", 300),
           fin("BULL", "#8a8370", "#c9c0a8"), fin("GW", "#7c8794", "#e9eef5"), fin("BULL2", "#8a8370", "#c9c0a8"),
           athlete("LG", CAP, "#d8202c", "#d8202c", "#c68863"), athlete("GOLF", HAIR("#6b4a2a"), "#f4f4f2", "#2a2a33", "#e3b48c"),
           sprite("FLOAT1", FLOAT, 300, 140, 110), sprite("FLOAT2", FLOAT.replace("#ff7a59", "#4f9dff").replace("#ffb199", "#9cc8ff"), 300, 140, 110),
           sprite("cup", CUP, 80, 130, 110), sprite("club", CLUB, 60, 170, 160),
           sign("rules", ["NO RUNNING", "NO DIVING"]), sign("rules2", ["NO RUNNING", "NO DIVING", "NO SHARKS"], "#ffd23f"),
           sign("haz", ["WATER HAZARD"], "#f4f4f2"), sign("haz2", ["SHARK HAZARD"], "#d8202c", "#ffffff"),
           sign("speed", ["SPEED LIMIT", "30"], "#f4f4f2", "#14141f", 260)]

write(EP, sprites, "", extra_css="""
    .bub.follow { font-size: 58px; padding: 16px 30px; border-radius: 44px; }
    .bub.small { font-size: 30px; padding: 8px 16px; }
    .check { left: 60px; top: 300px; padding: 16px 22px; background: #14141f; border: 5px solid #f4f4f2; border-radius: 14px; box-shadow: 6px 6px 0 #000;
             font: 900 40px/1.25 "Inter"; color: #f4f4f2; }
    .check .h { font: 700 22px/1 "CouldMono"; color: #ffd23f; letter-spacing: 0.18em; margin-bottom: 10px; }
    .check span { display: inline-block; width: 46px; text-align: center; margin-right: 8px; } .check .x { color: #ff5a4f; } .check .ok { color: #4ee07a; } .check .q { color: #8a94a1; }
    .stamp { left: 140px; top: 640px; padding: 10px 40px; border: 16px solid #d8202c; border-radius: 18px; font: 900 170px/1 "Inter"; color: #d8202c;
             transform-origin: 50% 50%; background: rgba(255,255,255,0.15); }
    .kmc { left: 60px; right: 60px; top: 640px; text-align: center; font: 700 96px/1 "CouldMono"; color: #ffd23f; text-shadow: 0 5px 0 #14141f, 0 0 12px #14141f; }
    .panel { left: 50px; right: 50px; top: 470px; height: 760px; background: #f4efe6; border: 7px solid #14141f; border-radius: 22px; box-shadow: 10px 10px 0 #14141f; overflow: hidden; }
    .panel .cap { position: absolute; left: 24px; top: 18px; font: 700 26px/1 "CouldMono"; color: #14141f; letter-spacing: 0.14em; }
    .gauge { left: auto; right: 40px; top: 300px; width: 120px; height: 520px; background: #14141f; border: 5px solid #f4f4f2; border-radius: 16px; }
    .gauge i { position: absolute; left: 10px; right: 10px; bottom: 10px; background: linear-gradient(#7fd3ef, #2f8fb0); border-radius: 8px; }
    .gauge b { position: absolute; left: 0; right: 0; top: 12px; text-align: center; font: 700 20px/1 "CouldMono"; color: #ffd23f; }
    .verdict { left: 50px; right: 50px; top: 420px; padding: 26px 30px; background: #14141f; border: 6px solid #ffd23f; border-radius: 18px; box-shadow: 8px 8px 0 #000;
               font: 900 56px/1.3 "Inter"; color: #f4f4f2; }
    .verdict .x { color: #ff5a4f; } .verdict .ok { color: #4ee07a; } .verdict small { display: block; font: 800 30px/1.2 "Inter"; color: #ffd23f; margin-top: 12px; }""")
