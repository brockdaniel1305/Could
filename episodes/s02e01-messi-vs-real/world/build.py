"""S2E01 v2 world layer: sprites (2D characters and props) for the 3D Bernabéu. The plot lives in director.js."""
import sys
from pathlib import Path

EP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EP.parents[1] / "tools/world3d"))
from world import sprite, messi, real, ball, write  # noqa: E402

NUMS = [1, 2, 3, 4, 5, 6, 8, 10, 11, 7, 9]
sprites = [messi("m")]
sprites.append(real("r0", 1, kit="#2bb3a3", shorts="#1a1a2e", socks="#2bb3a3", numc="#1a1a2e"))
sprites += [real(f"r{i}", n) for i, n in enumerate(NUMS) if i]
sprites += [real(f"q{i}", n) for i, n in enumerate([14, 15, 16])]
sprites.append(ball())

tumble = ('<g transform="translate(0,-60)"><g id="w3-tw-spin"><circle r="58" fill="none" stroke="#9a7440" stroke-width="7"/>'
          '<path d="M-50,-20 C-10,-60 40,-40 52,0 C40,40 -20,56 -46,24 C-30,0 10,-20 30,10 M-30,-44 C0,0 -10,30 20,50 M40,-30 C10,-10 -20,10 -50,0" '
          'fill="none" stroke="#b58a4c" stroke-width="6" stroke-linecap="round"/></g></g>')
subboard = ('<rect x="-8" y="-300" width="16" height="300" fill="#1a1a2e"/>'
            '<rect x="-120" y="-420" width="240" height="140" rx="16" fill="#111" stroke="#1a1a2e" stroke-width="8"/>'
            '<text x="-60" y="-325" text-anchor="middle" font-family="Inter" font-weight="900" font-size="76" fill="#3bff6a">IN</text>'
            '<text x="60" y="-325" text-anchor="middle" font-family="Inter" font-weight="900" font-size="76" fill="#ffd23f">×3</text>')
dugout = ('<path d="M-260,0 L-260,-250 Q0,-330 260,-250 L260,0 Z" fill="#a8d4ff" opacity="0.45" stroke="#1a1a2e" stroke-width="10"/>'
          '<rect x="-230" y="-110" width="460" height="34" rx="8" fill="#a50044" stroke="#1a1a2e" stroke-width="6"/>'
          '<rect x="-230" y="-76" width="460" height="18" fill="#1d3f9b"/>'
          '<rect x="-210" y="-58" width="18" height="58" fill="#1a1a2e"/><rect x="192" y="-58" width="18" height="58" fill="#1a1a2e"/>')
shirt = ('<g transform="translate(0,-120)"><path d="M-110,-70 L-60,-100 L60,-100 L110,-70 L90,-30 L70,-40 L70,90 L-70,90 L-70,-40 L-90,-30 Z" '
         'fill="#a50044" stroke="#1a1a2e" stroke-width="6"/><path d="M-40,-100 L-40,90 M0,-100 L0,90 M40,-100 L40,90" stroke="#1d3f9b" stroke-width="16"/>'
         '<text x="0" y="-40" text-anchor="middle" font-family="Inter" font-weight="900" font-size="34" fill="#ffd23f" stroke="#1a1a2e" stroke-width="2">MESSI</text>'
         '<text x="0" y="56" text-anchor="middle" font-family="Inter" font-weight="900" font-size="84" fill="#ffd23f" stroke="#1a1a2e" stroke-width="3">10</text></g>')
heart = ('<rect x="-6" y="-200" width="12" height="200" fill="#6b4a2a"/><rect x="-110" y="-330" width="220" height="150" rx="14" fill="#f4f4f2" stroke="#1a1a2e" stroke-width="7"/>'
         '<path d="M0,-200 C-50,-230 -66,-262 -44,-286 C-24,-302 -6,-290 0,-276 C6,-290 24,-302 44,-286 C66,-262 50,-230 0,-200 Z" fill="#ff3b5c" stroke="#1a1a2e" stroke-width="5"/>')
flag = ('<rect x="-4" y="-300" width="8" height="300" fill="#f4efe6" stroke="#1a1a2e" stroke-width="2"/>'
        '<path d="M4,-300 L110,-270 L4,-235 Z" fill="#ffd23f" stroke="#1a1a2e" stroke-width="5"/>')
sprites += [sprite("tw", tumble, 200, 200, 140), sprite("subboard", subboard, 300, 460, 440), sprite("dugout", dugout, 560, 360, 340),
            sprite("shirt", shirt, 260, 260, 240), sprite("heart", heart, 260, 360, 350), sprite("flag", flag, 260, 340, 320)]

write(EP, sprites, "")
