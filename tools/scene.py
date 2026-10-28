"""Scene builder for COULD? episodes: a full-frame cartoon (1080x1920) with fact cards that fly in and out.

Used by episodes/<ep>/src/sN.py:

    from scene import *
    scene(sid, world_svg, js, cards=card(sid, "w", "WEIGHT", "52,310 t", 80, 420) + ...)

In `js`, `fly("w", C.tons, C.uns)` flies card "w" in on cue `tons` and out on cue `uns`.
Writes episodes/<ep>/compositions/<sid>.html (plain HyperFrames HTML, editable in the desktop app).
"""
import html as _html
import inspect
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from kit import part  # noqa: E402,F401

_caller = Path(inspect.stack()[-1].filename).resolve()
EP = next(p for p in _caller.parents if (p / "narration.json").exists())
TIMING = {s["id"]: s for s in json.loads((EP / "timing.json").read_text())["scenes"]}
TPL = (ROOT / "channel/kit/scene-template.html").read_text()
STYLE = re.search(r"<style>.*?</style>", TPL, re.S).group(0)


def card(sid, name, label, value, x, y, kind="", w=None):
    """A fact sticker at (x, y) px. kind: "" | "gold" | "red". Value may contain HTML."""
    width = f" width: {w}px;" if w else ""
    return (f'\n    <div class="card {kind}" id="{sid}-c-{name}" data-layout-allow-overflow data-layout-allow-overlap style="left: {x}px; top: {y}px;{width}">'
            f'<div class="ck">{_html.escape(label)}</div><div class="cv">{value}</div></div>')


def banner(sid, name, kicker, title, x, y):
    """Chapter banner (e.g. PLAN A / The Punch)."""
    return (f'\n    <div class="banner" id="{sid}-c-{name}" data-layout-allow-overflow data-layout-allow-overlap style="left: {x}px; top: {y}px;">'
            f'<div class="bk">{_html.escape(kicker)}</div><div class="bt">{title}</div></div>')


def scene(sid, world, js, cards="", extra_css=""):
    t = TIMING[sid]
    D = t["duration"]
    cues = json.dumps(t["cues"])
    out = f"""<template>
  <!-- COULD? scene {sid} · full-frame cartoon + flying fact cards. Source: src/{sid.split('-')[0]}.py, cues: timing.json -->
  {STYLE.replace("</style>", extra_css + "\n  </style>")}
  <div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920">
    <svg class="world" viewBox="0 0 1080 1920" id="{sid}-svg" data-layout-allow-overflow>
      <defs>
        <filter id="{sid}-boil" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence id="{sid}-turb" type="fractalNoise" baseFrequency="0.016" numOctaves="2" seed="1" /><feDisplacementMap in="SourceGraphic" scale="6" /></filter>
      </defs>
      <g filter="url(#{sid}-boil)">
{world}
      </g>
    </svg>
    <div class="logo" data-layout-ignore>COULD<b>?</b></div>
    <div class="live" data-layout-ignore><i></i>LIVE RECONSTRUCTION</div>{cards}
    <div class="dip" id="{sid}-dip" data-layout-ignore></div>
  </div>
  <script>
    (function () {{
      const S = "#{sid}-";
      const D = {D};
      const C = {cues};
      const tl = gsap.timeline({{ paused: true }});
      const turb = document.getElementById("{sid}-turb");
      tl.to({{}}, {{ duration: D, ease: "none", onUpdate() {{ turb.setAttribute("seed", 1 + (Math.floor(this.time() * 12) % 9)); }} }}, 0);
      // rig pivots: limbs swing from their top, heads nod from the neck
      const root = document.querySelector('[data-composition-id="{sid}"]');
      root.querySelectorAll('[id$="-armL"],[id$="-armR"],[id$="-legL"],[id$="-legR"]').forEach((el) => gsap.set(el, {{ transformOrigin: "50% 0%" }}));
      root.querySelectorAll('g[id$="-head"]').forEach((el) => gsap.set(el, {{ transformOrigin: "50% 100%" }}));
      const R = (len, cycle) => Math.max(0, Math.floor(len / cycle) - 1);
      // fact cards: fly in on a cue, land with a small overshoot, hold still, fly out
      const fly = (name, tin, tout, o = {{}}) => {{
        const el = S + "c-" + name, dir = o.from === "right" ? 1 : -1, rot = o.rot ?? (dir < 0 ? -3 : 3);
        const inFrom = o.from === "top" ? {{ y: -900, x: 0 }} : {{ x: dir * 1300, y: 0 }};
        tl.fromTo(el, {{ ...inFrom, rotation: dir * 18, opacity: 1 }}, {{ x: 0, y: 0, rotation: rot, duration: 0.55, ease: "back.out(1.5)" }}, tin);
        if (tout != null && tout < D - 0.05) {{
          // leave the way it came, so cards never cross each other
          const outTo = o.from === "top" || o.out === "up" ? {{ y: -1100 }} : {{ x: dir * 1400 }};
          tl.to(el, {{ ...outTo, rotation: dir * 14, duration: 0.38, ease: "power3.in" }}, tout);
        }}
      }};
      const pop = (sel, at) => tl.fromTo(sel, {{ opacity: 0, scale: 0.4, transformOrigin: "50% 50%" }}, {{ opacity: 1, scale: 1, duration: 0.45, ease: "back.out(2.2)" }}, at);
      const swap = (hide, showSel, at) => {{ tl.set(hide, {{ opacity: 0 }}, at); tl.set(showSel, {{ opacity: 1 }}, at); }};
      const blink = (lids, at) => {{ tl.set(lids, {{ opacity: 1 }}, at); tl.set(lids, {{ opacity: 0 }}, at + 0.12); }};
      const waves = (a, b) => {{
        tl.fromTo(a, {{ x: 0 }}, {{ x: -160, duration: 2, ease: "none", repeat: R(D, 2) }}, 0);
        if (b) tl.fromTo(b, {{ x: 0 }}, {{ x: -160, duration: 1.4, ease: "none", repeat: R(D, 1.4) }}, 0);
        // fish under the surface swim slowly left and bob
        [1, 2, 3].forEach((i) => {{
          const f = a.replace("-waves1", "-fish" + i);
          if (!document.querySelector(f)) return;
          tl.fromTo(f, {{ x: 0 }}, {{ x: -(60 + i * 25) * D / 4, duration: D, ease: "none" }}, 0);
          tl.fromTo(f, {{ y: -6 }}, {{ y: 6, duration: 0.9 + i * 0.2, ease: "sine.inOut", repeat: R(D, 0.9 + i * 0.2), yoyo: true }}, 0);
        }});
      }};
      const puffs = (pfx) => {{
        [1, 2, 3, 4].forEach((i) => tl.fromTo(`${{pfx}}-smoke${{i}}`, {{ y: 0, x: 0, scale: 0.6, opacity: 0.9, transformOrigin: "50% 50%" }},
          {{ y: -70, x: -30, scale: 1.8, opacity: 0, duration: 1.6, ease: "power1.out", repeat: R(D - i * 0.35, 1.6) }}, i * 0.35));
      }};
{js}
      tl.fromTo(S + "dip", {{ opacity: 0 }}, {{ opacity: 0.45, duration: 0.1, ease: "none" }}, D - 0.1);
      // render end -> start once so every element starts in its earliest state
      tl.progress(1).progress(0);
      window.__timelines["{sid}"] = tl;
    }})();
  </script>
</template>
"""
    (EP / f"compositions/{sid}.html").write_text(out)
    print("wrote", sid, D)
