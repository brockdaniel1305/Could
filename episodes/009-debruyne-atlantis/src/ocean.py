"""Shared world for episode 009 (short): De Bruyne on the cliff at Gibraltar, the Atlantic, and Atlantis on the sea floor.

Surface: horizon y 900, cliff top (where De Bruyne stands) y CLIFF. Deep: sea floor y FLOOR, the X marker in front of the golden
statue at (540, FLOOR). Cards go in the sky (y 300-900); under the captions only water, rock and sand.
"""
import random

from scene import part  # noqa: F401

CLIFF = 975
FLOOR = 1150
KDB = dict(KITC="#8fd0f5", SHORTC="#f4f4f2", SOCKC="#8fd0f5", NUMC="#1a1a2e")


def kdb(sid, x=270, y=CLIFF, s=0.8):
    """De Bruyne caricature (sky-blue kit, no badge, strawberry-blond hair): move sid-mw, rig sid-m-*."""
    p = (part("mbappe", sid + "-m", **KDB).replace(">10</text>", ">17</text>")
         .replace("#1a1410", "#d9965a").replace("#8a5a3c", "#f2c9a0"))
    return f'<g transform="translate({x},{y})"><g id="{sid}-mw"><g transform="scale({s})">{p}</g></g></g>'


def surface(sid):
    random.seed(9)
    bands = "".join(f'<path d="M0,{y} L1080,{y}" stroke="#ffffff" stroke-width="5" opacity="{0.18 + 0.04 * (i % 3)}" stroke-dasharray="{60 + i * 8} {40 + i * 6}" />'
                    for i, y in enumerate(range(940, 1920, 70)))
    strata = "".join(f'<path d="M0,{y} Q200,{y + 18} {360 + (y % 90)},{y + 6}" fill="none" stroke="#a89d82" stroke-width="6" />' for y in range(1040, 1920, 90))
    return f'''
<rect x="0" y="0" width="1080" height="905" fill="#b8e3f7" />
<rect x="0" y="560" width="1080" height="345" fill="#d8f0fa" />
<circle cx="860" cy="300" r="70" fill="#ffd23f" stroke="#1a1a2e" stroke-width="5" />
<g fill="#fff" stroke="#1a1a2e" stroke-width="4" opacity="0.9"><path d="M560,420 q30,-40 70,-10 q30,-30 60,0 q30,10 10,40 l-150,0 q-20,-10 10,-30 z" /></g>
<rect x="0" y="900" width="1080" height="1020" fill="#2b7fb8" />
<rect x="0" y="900" width="1080" height="70" fill="#4a9bd0" />
<g id="{sid}-waves">{bands}</g>
<path d="M0,900 L1080,900" stroke="#1a1a2e" stroke-width="4" />
<path d="M0,{CLIFF + 8} L300,{CLIFF - 4} Q420,{CLIFF} 470,{CLIFF + 40} L520,1180 Q500,1400 560,1600 L600,1920 L0,1920 Z" fill="#cfc4a8" stroke="#1a1a2e" stroke-width="6" stroke-linejoin="round" />
{strata}
<path d="M0,{CLIFF + 8} L300,{CLIFF - 4} Q420,{CLIFF} 470,{CLIFF + 40}" fill="none" stroke="#6c9a4a" stroke-width="14" stroke-linecap="round" />'''


def fog(sid):
    blobs = "".join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#f4f7fa" opacity="0.94" />'
                    for x, y, rx, ry in ((700, 820, 160, 90), (860, 780, 200, 110), (1000, 830, 170, 100), (780, 880, 220, 70), (960, 900, 200, 60)))
    hand = ('<g id="HAND" opacity="0"><rect x="836" y="700" width="40" height="110" rx="18" fill="#8fd0f5" stroke="#1a1a2e" stroke-width="5" />'
            '<circle cx="856" cy="694" r="26" fill="#f2c9a0" stroke="#1a1a2e" stroke-width="5" /></g>')
    return f'<g id="{sid}-fog" opacity="0">{blobs}{hand.replace("HAND", sid + "-hand")}</g>'


def plato(sid, x=110, y=CLIFF, s=0.8):
    return f'''<g transform="translate({x},{y})"><g id="{sid}-pl"><g transform="scale({s})">
  <ellipse cx="0" cy="4" rx="50" ry="9" fill="#000" opacity="0.22" />
  <path d="M-48,-210 Q-60,-90 -44,0 L44,0 Q60,-90 48,-210 Q0,-226 -48,-210 Z" fill="#f4f1ea" stroke="#1a1a2e" stroke-width="5" stroke-linejoin="round" />
  <path d="M-40,-200 Q10,-140 40,-20" fill="none" stroke="#c9bfa6" stroke-width="10" />
  <g transform="translate(-50,-196)"><g id="{sid}-plL"><rect x="-12" y="0" width="24" height="80" rx="12" fill="#f4f1ea" stroke="#1a1a2e" stroke-width="5" /><circle cx="0" cy="88" r="14" fill="#e8c09a" stroke="#1a1a2e" stroke-width="5" /></g></g>
  <g transform="translate(50,-196)"><g id="{sid}-plR"><rect x="-12" y="0" width="24" height="80" rx="12" fill="#f4f1ea" stroke="#1a1a2e" stroke-width="5" /><circle cx="0" cy="88" r="14" fill="#e8c09a" stroke="#1a1a2e" stroke-width="5" /></g></g>
  <g transform="translate(0,-256)">
    <ellipse cx="0" cy="0" rx="40" ry="46" fill="#e8c09a" stroke="#1a1a2e" stroke-width="5" />
    <path d="M-38,10 Q-40,70 0,78 Q40,70 38,10 Q20,34 0,34 Q-20,34 -38,10 Z" fill="#d6d6d0" stroke="#1a1a2e" stroke-width="4" />
    <path d="M-40,-10 Q-46,-30 -34,-34 M40,-10 Q46,-30 34,-34" fill="none" stroke="#d6d6d0" stroke-width="10" stroke-linecap="round" />
    <path d="M-30,-22 Q-10,-36 10,-30 Q26,-34 32,-22" fill="none" stroke="#6b8f3a" stroke-width="8" stroke-linecap="round" />
    <circle cx="-14" cy="-2" r="5" fill="#1a1a2e" /><circle cx="14" cy="-2" r="5" fill="#1a1a2e" />
    <path d="M-12,22 Q0,16 12,22" fill="none" stroke="#1a1a2e" stroke-width="4" stroke-linecap="round" />
  </g>
</g></g></g>'''


def deep(sid):
    """Underwater world: rays, bubbles, fish, and the sea floor with Atlantis (group sid-floor slides up into view)."""
    random.seed(4)
    bubbles = "".join(f'<circle cx="{random.randint(60, 1020)}" cy="{random.randint(0, 1920)}" r="{random.randint(6, 18)}" fill="none" stroke="#d8f0fa" stroke-width="4" opacity="0.7" />' for _ in range(40))
    fish = "".join(f'<g transform="translate({x},{y})"><path d="M0,0 q30,-22 60,0 q-30,22 -60,0 z M60,0 l22,-16 l0,32 z" fill="{c}" stroke="#1a1a2e" stroke-width="4" /><circle cx="14" cy="-3" r="4" fill="#1a1a2e" /></g>'
                   for x, y, c in ((150, 500, "#ffb648"), (820, 900, "#ff7a59"), (300, 1300, "#ffd23f"), (900, 1600, "#ffb648"), (520, 300, "#ff7a59")))
    rays = "".join(f'<polygon points="{x},0 {x + 90},0 {x + 260},1920 {x + 120},1920" fill="#ffffff" opacity="0.06" />' for x in (80, 380, 700))
    cols = "".join(f'<g transform="translate({x},{FLOOR})"><rect x="-26" y="-300" width="52" height="300" fill="#e6c25a" stroke="#1a1a2e" stroke-width="5" />'
                   f'<rect x="-36" y="-316" width="72" height="20" fill="#d4ae46" stroke="#1a1a2e" stroke-width="5" /><path d="M-10,-280 L-10,-20 M10,-280 L10,-20" stroke="#c49a30" stroke-width="5" /></g>'
                   for x in (120, 250, 830, 960))
    statue = f'''<g transform="translate(540,{FLOOR - 70})">
  <rect x="-120" y="0" width="240" height="70" fill="#d4ae46" stroke="#1a1a2e" stroke-width="6" />
  <path d="M-60,-300 Q-70,-120 -54,0 L54,0 Q70,-120 60,-300 Q0,-320 -60,-300 Z" fill="#f0c94a" stroke="#1a1a2e" stroke-width="6" />
  <g transform="translate(-66,-292)"><rect x="-14" y="0" width="28" height="110" rx="14" fill="#f0c94a" stroke="#1a1a2e" stroke-width="5" /></g>
  <g transform="translate(66,-292)"><g id="{sid}-sarm"><rect x="-14" y="0" width="28" height="110" rx="14" fill="#f0c94a" stroke="#1a1a2e" stroke-width="5" />
    <g transform="translate(0,124)"><rect x="-18" y="-16" width="36" height="32" rx="10" fill="#f0c94a" stroke="#1a1a2e" stroke-width="5" /><rect x="-6" y="-40" width="14" height="28" rx="7" fill="#f0c94a" stroke="#1a1a2e" stroke-width="5" /></g></g></g>
  <g transform="translate(0,-370)">
    <ellipse cx="0" cy="0" rx="56" ry="64" fill="#f0c94a" stroke="#1a1a2e" stroke-width="6" />
    <path d="M-50,-30 Q0,-90 50,-30 Q30,-50 0,-52 Q-30,-50 -50,-30 Z" fill="#d4ae46" stroke="#1a1a2e" stroke-width="5" />
    <ellipse cx="-20" cy="2" rx="12" ry="13" fill="#fff" stroke="#1a1a2e" stroke-width="4" /><ellipse cx="20" cy="2" rx="12" ry="13" fill="#fff" stroke="#1a1a2e" stroke-width="4" />
    <circle id="{sid}-spL" cx="-20" cy="6" r="6" fill="#1a1a2e" /><circle id="{sid}-spR" cx="20" cy="6" r="6" fill="#1a1a2e" />
    <g id="{sid}-slids"><ellipse cx="-20" cy="2" rx="13" ry="14" fill="#e3b83f" stroke="#1a1a2e" stroke-width="4" /><ellipse cx="20" cy="2" rx="13" ry="14" fill="#e3b83f" stroke="#1a1a2e" stroke-width="4" /></g>
    <path d="M-18,34 Q0,46 18,34" fill="none" stroke="#1a1a2e" stroke-width="5" stroke-linecap="round" />
  </g></g>'''
    temple = (f'<g transform="translate(540,{FLOOR - 560})"><path d="M-260,0 L0,-120 L260,0 Z" fill="#e6c25a" stroke="#1a1a2e" stroke-width="6" stroke-linejoin="round" />'
              f'<rect x="-260" y="0" width="520" height="30" fill="#d4ae46" stroke="#1a1a2e" stroke-width="5" /></g>')
    rocks = "".join(f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r * 0.6:.0f}" fill="#7a6f5a" stroke="#1a1a2e" stroke-width="4" />' for x, y, r in ((80, 1420, 50), (980, 1500, 70), (360, 1700, 40), (760, 1800, 55)))
    weeds = "".join(f'<path d="M{x},1920 q-20,-80 0,-160 q20,-80 0,-160" fill="none" stroke="#3f8f5a" stroke-width="12" stroke-linecap="round" />' for x in (60, 200, 880, 1020))
    return f'''<g id="{sid}-deep" opacity="0">
  <rect x="0" y="0" width="1080" height="1920" fill="#15507f" />
  <rect x="0" y="0" width="1080" height="700" fill="#1f6aa3" opacity="0.7" />
  {rays}
  <g id="{sid}-bub">{bubbles}<g transform="translate(0,1920)">{bubbles}</g></g>
  <g id="{sid}-fish">{fish}</g>
  <g id="{sid}-floor">
    <radialGradient id="{sid}-gl"><stop offset="0" stop-color="#fff2b0" stop-opacity="0.9" /><stop offset="1" stop-color="#ffd23f" stop-opacity="0" /></radialGradient>
    <circle id="{sid}-glow" cx="540" cy="{FLOOR - 300}" r="460" fill="url(#{sid}-gl)" opacity="0" />
    <rect x="0" y="{FLOOR}" width="1080" height="{1920 - FLOOR}" fill="#c9b27a" />
    <path d="M0,{FLOOR} Q270,{FLOOR - 20} 540,{FLOOR} T1080,{FLOOR}" fill="#c9b27a" stroke="#1a1a2e" stroke-width="5" />
    {temple}{cols}{statue}
    <g transform="translate(540,{FLOOR + 14})"><path d="M-34,-14 L34,14 M-34,14 L34,-14" stroke="#c0262d" stroke-width="12" stroke-linecap="round" /></g>
    {rocks}{weeds}
  </g>
</g>'''


CSS = """
    .stamp { position: absolute; left: 190px; top: 470px; width: 700px; height: 300px; border: 24px solid #1f9d55; border-radius: 34px;
             display: flex; align-items: center; justify-content: center; font: 900 170px/1 "Inter"; color: #1f9d55; opacity: 0;
             background: rgba(244, 239, 230, 0.25); }
    .heart { position: absolute; left: 400px; top: 300px; width: 280px; height: 260px; opacity: 0; }"""

JS = """
      const count = (id, a, b, t0, d, ease = "power2.out") => {
        const el = document.querySelector(S + id), o = { v: a };
        el.textContent = String(a);
        tl.fromTo(o, { v: a }, { v: b, duration: d, ease, onUpdate() { el.textContent = String(Math.round(o.v)); } }, t0);
      };
      const kickR = (at, p = "m") => {
        tl.to(S + p + "-legR", { rotation: 35, duration: 0.12, ease: "power2.in" }, at - 0.14);
        tl.to(S + p + "-legR", { rotation: -55, duration: 0.08, ease: "power3.out" }, at - 0.02);
        tl.to(S + p + "-legR", { rotation: 0, duration: 0.2 }, at + 0.1);
      };
      const arc = (sel, t0, d, dx, dy, h, s1 = 1) => {
        const el = document.querySelector(sel), o = { p: 0 };
        tl.fromTo(o, { p: 0 }, { p: 1, duration: d, ease: "none", onUpdate() { const p = o.p; gsap.set(el, { x: dx * p, y: dy * p - 4 * h * p * (1 - p), scale: 1 + (s1 - 1) * p }); } }, t0);
      };
      const look = (p, x, y, at, d = 0.2) => tl.to([S + p + "-pupL", S + p + "-pupR"], { x, y, duration: d }, at);
"""
