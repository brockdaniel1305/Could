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
