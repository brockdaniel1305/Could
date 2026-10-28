"""Scene builder for COULD? episodes: fact panel + live cartoon stage, timed from timing.json.

Used by episodes/<ep>/src/sN.py:   from scene import *   then   scene(sid, kicker, head, rows, world_svg, js)
It writes episodes/<ep>/compositions/<sid>.html (plain HyperFrames HTML, editable in the desktop app).
"""
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


def rows(sid, items):
    out = []
    for i, (k, v, *cls) in enumerate(items, 1):
        c = " ".join(cls)
        out.append(f'<div class="row" id="{sid}-r{i}"><span class="rk">{k}</span><span class="rv {c}">{v}</span></div>')
    return "\n        ".join(out)


def scene(sid, kick, head, row_items, world, js, extra_css="", overlay=""):
    t = TIMING[sid]
    D = t["duration"]
    cues = json.dumps(t["cues"])
    html = f"""<template>
  <!-- COULD? scene {sid} · fact panel (top) + live cartoon reconstruction (stage). Cues: timing.json -->
  {STYLE.replace("</style>", extra_css + "\n  </style>")}
  <div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920">
    <div class="fp">
      <div class="kick" id="{sid}-kick">{kick}</div>
      <div class="head" id="{sid}-head">{head}</div>
      <div class="rows">
        {rows(sid, row_items)}
      </div>
    </div>
    <div class="stage" data-layout-allow-overflow>
      <svg viewBox="0 0 984 560" id="{sid}-svg">
        <defs>
          <filter id="{sid}-boil"><feTurbulence id="{sid}-turb" type="fractalNoise" baseFrequency="0.018" numOctaves="2" seed="1" /><feDisplacementMap in="SourceGraphic" scale="5" /></filter>
        </defs>
        <g filter="url(#{sid}-boil)">
{world}
        </g>
        <rect id="{sid}-dip" x="0" y="0" width="984" height="560" fill="#000" opacity="0" />
      </svg>
    </div>
    <div class="stage-border" data-layout-ignore></div>
    <div class="live" id="{sid}-live"><i></i>LIVE RECONSTRUCTION</div>
{overlay}
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
      root.querySelectorAll('[id$="-head"]').forEach((el) => {{ if (el.tagName === "g") gsap.set(el, {{ transformOrigin: "50% 100%" }}); }});
      // helpers
      const show = (sel, at, d = 0.35) => tl.fromTo(sel, {{ opacity: 0, x: -24 }}, {{ opacity: 1, x: 0, duration: d, ease: "expo.out" }}, at);
      const pop = (sel, at) => tl.fromTo(sel, {{ opacity: 0, scale: 0.4, transformOrigin: "50% 50%" }}, {{ opacity: 1, scale: 1, duration: 0.45, ease: "back.out(2.2)" }}, at);
      const swap = (hide, showSel, at) => {{ tl.set(hide, {{ opacity: 0 }}, at); tl.set(showSel, {{ opacity: 1 }}, at); }};
      const blink = (lids, at) => {{ tl.set(lids, {{ opacity: 1 }}, at); tl.set(lids, {{ opacity: 0 }}, at + 0.12); }};
      const waves = (a, b) => {{
        const n = Math.max(1, Math.floor(D / 2));
        tl.fromTo(a, {{ x: 0 }}, {{ x: -160, duration: 2, ease: "none", repeat: n - 1 }}, 0);
        if (b) tl.fromTo(b, {{ x: 0 }}, {{ x: -160, duration: 1.4, ease: "none", repeat: Math.floor(D / 1.4) }}, 0);
      }};
      const puffs = (pfx) => {{
        [1, 2, 3, 4].forEach((i) => tl.fromTo(`${{pfx}}-smoke${{i}}`, {{ y: 0, scale: 0.6, opacity: 0.9, transformOrigin: "50% 50%" }},
          {{ y: -70, x: -30, scale: 1.8, opacity: 0, duration: 1.6, ease: "power1.out", repeat: Math.floor(D / 1.6) }}, i * 0.35));
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
    (EP / f"compositions/{sid}.html").write_text(html)
    print("wrote", sid, D)
