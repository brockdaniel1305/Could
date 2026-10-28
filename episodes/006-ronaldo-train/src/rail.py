"""Shared world for episode 006 (Ronaldo vs a high-speed train).

Scale: 120 px per metre (train roof 3.89 m = 467 px). Rail top at y = GY. Ronaldo's real jump (feet ~0.7 m up,
~0.75 s in the air) comes from his 2.56 m header; the numbers on the cards are computed in FACTS.md.
"""
from scene import part  # noqa: F401

GY = 1200          # rail top
PLAT = 1090        # platform edge (where people should stand)
M = 120            # px per metre


def y_m(m):
    return GY - m * M


def ruler(sid):
    ticks = "".join(f'<path d="M30,{y_m(m)} L{62 if m % 2 == 0 else 50},{y_m(m)}" stroke="#1a1a2e" stroke-width="5" />'
                    + (f'<text data-layout-ignore x="70" y="{y_m(m) + 10}" font-family="Inter" font-weight="900" font-size="28" fill="#1a1a2e">{m} m</text>' if m % 2 == 0 and m else "")
                    for m in range(0, 8))
    return f'<g id="{sid}-ruler" opacity="0.85"><path d="M30,{y_m(7)} L30,{GY}" stroke="#1a1a2e" stroke-width="5" />{ticks}</g>'


def station(sid):
    return part("station", sid + "-st")


def ronaldo(sid, x=250, y=GY, scale=0.9):
    return f'<g transform="translate({x},{y})"><g id="{sid}-kwrap"><g transform="scale({scale})">{part("forward", sid + "-r")}</g></g></g>'


def train(sid, x, name="train"):
    return f'<g transform="translate(0,{GY})"><g id="{sid}-{name}"><g transform="translate({x},0) scale(1.2)">{part("ice-train", sid + "-" + name[0] + "t")}</g></g></g>'


def hline(sid, name, m, color="#e0412f"):
    return f'<g id="{sid}-{name}" opacity="0"><path d="M30,{y_m(m)} L1080,{y_m(m)}" stroke="{color}" stroke-width="7" stroke-dasharray="22 14" /></g>'


SIU_JS = """
      // departures board text as a pure function of scene time: steps = [[t, text], ...]
      const board = (steps) => {
        const el = document.querySelector(S + "st-boardt");
        tl.to({}, { duration: D, ease: "none", onUpdate() {
          const t = this.time(); let txt = steps[0][1];
          for (const [at, s] of steps) if (t >= at) txt = s;
          if (el.textContent !== txt) el.textContent = txt;
        } }, 0);
      };
      // jump (feet ~0.7 m = 84 px), spin in the air, land arms down-out: SIUUU
      const jump = (at, h = 84, air = 0.75) => {
        tl.to(S + "kwrap", { y: 12, duration: 0.14, ease: "power2.in" }, at - 0.14);
        tl.to(S + "kwrap", { y: -h, duration: air / 2, ease: "power2.out" }, at);
        tl.to(S + "kwrap", { y: 0, duration: air / 2, ease: "power2.in" }, at + air / 2);
      };
      const siu = (at) => {
        jump(at);
        tl.to(S + "kwrap", { scaleX: -1, transformOrigin: "50% 100%", duration: 0.18, ease: "none", yoyo: true, repeat: 1 }, at + 0.02);
        tl.to(S + "r-num", { scaleX: -1, transformOrigin: "50% 50%", duration: 0.18, ease: "none", yoyo: true, repeat: 1 }, at + 0.02);
        tl.to(S + "r-armL", { rotation: 40, duration: 0.15 }, at + 0.75);
        tl.to(S + "r-armR", { rotation: -40, duration: 0.15 }, at + 0.75);
        tl.to(S + "r-legL", { rotation: 22, duration: 0.15 }, at + 0.75);
        tl.to(S + "r-legR", { rotation: -22, duration: 0.15 }, at + 0.75);
        tl.set(S + "r-m-smile", { opacity: 0 }, at + 0.75); tl.set(S + "r-m-o", { opacity: 1 }, at + 0.75);
      };
"""


# ---- v2: best of three -------------------------------------------------------------------------------------------
def scorebug(sid, a, b):
    """Match score top right (next to the logo): RONALDO a : b TRAINS. Change it with score(at, a, b)."""
    return (f'\n    <div class="score" id="{sid}-score"><span class="sn">CR7</span>'
            f'<span class="sv" id="{sid}-sa">{a}</span><span class="sc">:</span><span class="sv" id="{sid}-sb">{b}</span>'
            f'<span class="sn">TRAINS</span></div>')


SCORE_CSS = """
    .score { position: absolute; left: 560px; top: 184px; display: flex; align-items: center; gap: 14px; padding: 10px 22px;
             background: #1a1a2e; border: 5px solid #f4efe6; border-radius: 18px; }
    .score .sn { font: 700 28px/1 "CouldMono"; letter-spacing: 0.08em; color: #f4efe6; }
    .score .sv { font: 900 56px/1 "Inter"; color: #ffd23f; min-width: 34px; text-align: center; }
    .score .sc { font: 900 48px/1 "Inter"; color: #f4efe6; }"""

SCORE_JS = """
      // score bug: a pure function of time; the side that scores pops
      const score = (at, a, b, who) => {
        const ea = document.querySelector(S + "sa"), eb = document.querySelector(S + "sb"), a0 = ea.textContent, b0 = eb.textContent;
        tl.to({}, { duration: D, ease: "none", onUpdate() {
          const on = this.time() >= at; ea.textContent = on ? a : a0; eb.textContent = on ? b : b0;
        } }, 0);
        tl.fromTo(S + (who || "sa"), { scale: 1 }, { scale: 1.8, duration: 0.16, yoyo: true, repeat: 1, ease: "power2.out" }, at);
        tl.fromTo(S + "score", { rotation: 0 }, { rotation: -4, duration: 0.08, yoyo: true, repeat: 3 }, at);
      };
      const boardName = (txt) => { const n = document.querySelector(S + "st-boardn"); if (n) n.textContent = txt; };
"""

# Round 3 is filmed at floor level: 12 px per centimetre. Model ICE 1:87 -> 4.47 cm = 54 px tall.
CM = 12
FY = 1200          # floor / model track


def y_cm(c):
    return FY - c * CM


def room(sid):
    """Living-room floor with a model railway track, wall behind. Graphics only below the captions."""
    sleepers = "".join(f'<rect x="{x}" y="{FY - 2}" width="34" height="14" rx="3" fill="#6b4a2a" stroke="#1a1a2e" stroke-width="3" />' for x in range(0, 1100, 60))
    boards = "".join(f'<path d="M0,{y} L1080,{y}" stroke="#9c6b3c" stroke-width="5" />' for y in range(1300, 1920, 110))
    joints = "".join(f'<path d="M{x},{1300 + (i % 5) * 110} L{x},{1410 + (i % 5) * 110}" stroke="#9c6b3c" stroke-width="5" />' for i, x in enumerate(range(90, 1080, 170)))
    stripes = "".join(f'<rect x="{x}" y="0" width="40" height="{FY}" fill="#efe1c4" />' for x in range(0, 1080, 120))
    return (f'<rect x="0" y="0" width="1080" height="{FY}" fill="#f6ead2" />{stripes}'
            f'<rect x="0" y="{FY - 90}" width="1080" height="90" fill="#e8d6b0" stroke="#1a1a2e" stroke-width="5" />'
            f'<rect x="0" y="{FY}" width="1080" height="{1920 - FY}" fill="#c8915a" />{boards}{joints}'
            f'{sleepers}<path d="M0,{FY} L1080,{FY}" stroke="#9aa0a6" stroke-width="6" /><path d="M0,{FY + 6} L1080,{FY + 6}" stroke="#1a1a2e" stroke-width="3" />')


def ruler_cm(sid):
    ticks = "".join(f'<path d="M30,{y_cm(c)} L{62 if c % 20 == 0 else 50},{y_cm(c)}" stroke="#1a1a2e" stroke-width="5" />'
                    + (f'<text data-layout-ignore x="70" y="{y_cm(c) + 10}" font-family="Inter" font-weight="900" font-size="28" fill="#1a1a2e">{c} cm</text>' if c % 20 == 0 and c else "")
                    for c in range(0, 71, 10))
    return f'<g id="{sid}-ruler" opacity="0.85"><path d="M30,{y_cm(70)} L30,{FY}" stroke="#1a1a2e" stroke-width="5" />{ticks}</g>'


def hline_cm(sid, name, c, color="#e0412f"):
    return f'<g id="{sid}-{name}" opacity="0"><path d="M30,{y_cm(c)} L1080,{y_cm(c)}" stroke="{color}" stroke-width="7" stroke-dasharray="22 14" /></g>'


def boots(sid, x=430):
    """Ronaldo from the knee down at floor scale (only his legs fit in the frame). Origin = sole. Animate sid-kwrap."""
    leg = lambda dx, sock, boot: (
        f'<g transform="translate({dx},0)"><rect x="-38" y="-1500" width="76" height="1440" fill="{sock}" stroke="#1a1a2e" stroke-width="6" />'
        f'<rect x="-38" y="-760" width="76" height="40" fill="#e0412f" /><rect x="-38" y="-700" width="76" height="22" fill="#1f9d55" />'
        f'<path d="M-46,-70 L44,-70 Q70,-40 130,-34 Q160,-30 158,-8 L158,0 L-46,0 Z" fill="{boot}" stroke="#1a1a2e" stroke-width="6" stroke-linejoin="round" />'
        f'<path d="M-30,-40 L120,-30" stroke="#ffd23f" stroke-width="8" stroke-linecap="round" />'
        f'<g fill="#1a1a2e"><rect x="-30" y="0" width="14" height="12" /><rect x="40" y="0" width="14" height="12" /><rect x="110" y="0" width="14" height="12" /></g></g>')
    return (f'<g transform="translate({x},{FY})"><g id="{sid}-kwrap">'
            f'<g id="{sid}-legB">{leg(70, "#d9d9d6", "#c9302a")}</g><g id="{sid}-legF">{leg(0, "#f4f4f2", "#e0412f")}</g></g></g>')


def model_train(sid, x):
    """Model ICE, 1:87: 4.47 cm tall (54 px), ~30 cm long (361 px). Same part as the real one, thin strokes."""
    return (f'<g transform="translate(0,{FY})"><g id="{sid}-mt"><g class="mini" transform="translate({x},0) scale(0.223,0.138)">'
            f'{part("ice-train", sid + "-mtt")}</g></g></g>')


MINI_CSS = """
    .mini * { vector-effect: non-scaling-stroke; stroke-width: 3px; }"""
