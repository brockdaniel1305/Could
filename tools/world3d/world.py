"""Builds <ep>/world/world.html: the one continuous 3D layer of a "world" episode (narration.json "world": true).

The episode's world/build.py calls  write(ep, actors, props, bubbles, overlays_html, css)  and keeps its plot in
world/director.js (export default function plot(T) -> {actors, ball, shots, overlays, ...}, see tools/world3d/engine.js).
tools/build_episode.py then injects world.html into index.html in place of the per-scene compositions.
"""
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from stadium import messi_fig, player, football  # noqa: E402,F401

HERE = Path(__file__).resolve().parent
THREE = HERE / "lib/three.module.min.js"


def sprite(name, inner, w=460, h=560, oy=470):
    """A billboard: (0,0) of `inner` is the foot point; the engine moves/scales the wrapper."""
    return (f'<div class="w3b" id="w3-{name}"><svg width="{w}" height="{h}" viewBox="{-w // 2} {-oy} {w} {h}" '
            f'style="position:absolute;left:{-w // 2}px;top:{-oy}px;overflow:visible">{inner}</svg></div>')


SHADOW = '<ellipse cx="0" cy="4" rx="72" ry="15" fill="#000" opacity="0.32"/>'


def messi(name="m"):
    return sprite(name, SHADOW + messi_fig("w3", 0, 0, 1.0, name=name, tag=False))


def real(name, num, **kit):
    k = dict(kit="#f4f4f2", shorts="#f4f4f2", socks="#f4f4f2", numc="#1a1a2e")
    k.update(kit)
    return sprite(name, SHADOW + player("w3", name + "x", 0, 0, 1.0, num=num, tag=False, **k))


def ball():
    return (sprite("ballshadow", '<ellipse cx="0" cy="0" rx="40" ry="10" fill="#000"/>', 120, 60, 30)
            + sprite("ball", football("w3", 0, -38, 1.0, name="b"), 200, 200, 160))


CSS = """
    @font-face { font-family: "CouldMono"; font-weight: 400; src: url("assets/fonts/IBMPlexMono-400.woff2") format("woff2"); }
    @font-face { font-family: "CouldMono"; font-weight: 700; src: url("assets/fonts/IBMPlexMono-700.woff2") format("woff2"); }
    @font-face { font-family: "CouldSerif"; font-weight: 700; src: url("assets/fonts/PlayfairDisplay-700.woff2") format("woff2"); }
    #w3 { position: absolute; inset: 0; overflow: hidden; background: #0b1426; z-index: 1; }
    #w3-stage { position: absolute; inset: 0; }
    #w3-gl { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }
    #w3-chars { position: absolute; inset: 0; }
    .w3b { position: absolute; left: 0; top: 0; width: 0; height: 0; transform-origin: 0 0; display: none; }
    .w3b g[id$="-legL"], .w3b g[id$="-legR"], .w3b g[id$="-armL"], .w3b g[id$="-armR"] { transform-box: fill-box; transform-origin: 50% 0; }
    .w3b g[id$="-spin"] { transform-box: fill-box; transform-origin: 50% 50%; }
    .w3b .legA, .w3b .legB { transform-box: fill-box; transform-origin: 50% 0; }
    .w3-vig { position: absolute; inset: 0; pointer-events: none;
              background: radial-gradient(ellipse 85% 62% at 50% 52%, transparent 58%, rgba(4, 7, 18, 0.5) 100%); }
    .bub { position: absolute; left: 0; top: 0; display: none; padding: 10px 20px; border-radius: 22px; background: #f4efe6; border: 5px solid #1a1a2e;
           font: 900 46px/1 "Inter"; color: #1a1a2e; white-space: nowrap; box-shadow: 6px 6px 0 #1a1a2e; transform-origin: 50% 100%; }
    .bub.dark { background: #1a1a2e; color: #ffd23f; border-color: #ffd23f; }
    .bub.red { background: #e0412f; color: #fff; }
    .logo { position: absolute; left: 56px; top: 184px; font: 900 40px/1 "Inter"; letter-spacing: 0.06em; color: #f4efe6;
            -webkit-text-stroke: 2px #1a1a2e; paint-order: stroke fill; text-shadow: 3px 3px 0 #1a1a2e; }
    .logo b { color: #ffd23f; }
    .live { position: absolute; left: 56px; top: 238px; padding: 8px 14px; border-radius: 10px; background: rgba(10, 9, 8, 0.75);
            border: 3px solid #1a1a2e; font: 700 28px/1 "CouldMono"; letter-spacing: 0.1em; color: #f4efe6; }
    .live i { display: inline-block; width: 16px; height: 16px; margin-right: 10px; border-radius: 50%; background: #e0412f; }
    .ov { position: absolute; opacity: 0; transform-origin: 50% 50%; }
    .slam { left: 30px; right: 30px; text-align: center; font: 900 128px/0.95 "Inter"; color: #ffd23f;
            -webkit-text-stroke: 9px #1a1a2e; paint-order: stroke fill; }
    .slam b { color: #f4efe6; }
    .chip { padding: 16px 26px 20px; background: #f4efe6; border: 6px solid #1a1a2e; border-radius: 22px; box-shadow: 10px 10px 0 #1a1a2e; white-space: nowrap; }
    .chip .ck { font: 700 28px/1 "CouldMono"; letter-spacing: 0.08em; color: #6b6358; }
    .chip .cv { margin-top: 8px; font: 900 64px/1 "Inter"; letter-spacing: -0.02em; color: #1a1a2e; }
    .chip.gold { background: #ffd23f; } .chip.gold .ck { color: #5a4300; }
    .chip.red { background: #e0412f; } .chip.red .ck, .chip.red .cv { color: #fff; }
    .chip.dark { background: #1a1a2e; border-color: #ffd23f; } .chip.dark .ck { color: #ffd23f; } .chip.dark .cv { color: #f4efe6; }
    .hud { position: absolute; left: 520px; top: 184px; display: flex; align-items: center; gap: 12px; padding: 10px 18px; background: #1a1a2e;
           border: 4px solid #f4efe6; border-radius: 14px; font: 700 30px/1 "CouldMono"; color: #f4efe6; opacity: 0; }
    .hud .sc { font: 900 46px/1 "Inter"; color: #ffd23f; }
    .hud .mn { margin-left: 6px; padding: 6px 10px; border-radius: 8px; background: #e0412f; color: #fff; font: 700 28px/1 "CouldMono"; }
    .stam { position: absolute; left: 520px; top: 262px; display: flex; align-items: center; gap: 12px; font: 700 22px/1 "CouldMono"; color: #f4efe6;
            padding: 8px 14px; background: rgba(26, 26, 46, 0.88); border-radius: 12px; opacity: 0; }
    .stam .bar { position: relative; width: 230px; height: 18px; border: 3px solid #f4efe6; border-radius: 9px; overflow: hidden; }
    .stam .bar i { position: absolute; left: 0; top: 0; bottom: 0; background: #1f9d55; }
    .ft { left: 80px; right: 80px; top: 330px; padding: 26px 30px 30px; background: #12162a; border: 6px solid #ffd23f;
          border-radius: 18px; color: #f4efe6; text-align: center; }
    .ft .fth { font: 900 64px/1 "Inter"; color: #ffd23f; }
    .ft .fts { margin-top: 10px; font: 700 34px/1.2 "CouldMono"; }
    .ft .fts b { color: #ffd23f; font-family: "Inter"; font-size: 46px; }
    .ft table { width: 100%; margin-top: 16px; border-collapse: collapse; font: 700 27px/1.3 "CouldMono"; }
    .ft td { padding: 7px 4px; border-top: 2px solid #2a3355; text-align: left; }
    .ft td.k { text-align: right; width: 90px; color: #ffd23f; }
    .ft td.h { text-align: left; width: 90px; color: #f4efe6; }
    .conf { position: absolute; inset: 0; pointer-events: none; }
    .conf i { position: absolute; display: block; width: 16px; height: 24px; opacity: 0; }"""


def write(ep, sprites, overlays, extra_css=""):
    ep = Path(ep)
    timing = json.loads((ep / "timing.json").read_text())
    files = [(THREE, "assets/lib/three.module.min.js"), (ep / "world/director.js", "assets/world/director.js")]
    files += [(f, f"assets/world/{f.name}") for f in HERE.glob("*.js") if f.name != "dbg.mjs"]   # engine + every world module
    for src, dst in files:
        (ep / dst).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(src, ep / dst)
    T = {"duration": timing["duration"], "start": {}, "cue": {}}
    for s in timing["scenes"]:
        key = s["id"].split("-")[0]
        T["start"][key] = s["start"]
        T["start"][key + ".end"] = round(s["start"] + s["duration"], 3)
        for c, v in s["cues"].items():
            T["cue"][f"{key}.{c}"] = round(s["start"] + v, 3)
    html = f"""      <style>{CSS}{extra_css}
      </style>
      <div id="w3" data-layout-ignore>
        <div id="w3-stage">
          <canvas id="w3-gl" width="1080" height="1920"></canvas>
          <div id="w3-chars">
{chr(10).join("            " + s for s in sprites)}
          </div>
          <div class="w3-vig"></div>
        </div>
        <div class="logo">COULD<b>?</b></div>
        <div class="live"><i></i>LIVE RECONSTRUCTION</div>
        <div id="w3-ov">{overlays}</div>
      </div>
      <script>
        window.__T = {json.dumps(T)};
        window.__hf = window.__hf || {{}};
        window.__hf.buildReady = window.__hf.buildReady || {{}};
        window.__hf.buildReady.world = new Promise((r) => {{ window.__worldReady = r; }});
      </script>
      <script type="module">
        import {{ createWorld }} from "./assets/world/engine.js";
        import plot from "./assets/world/director.js";
        const w = createWorld(plot(window.__T));
        window.addEventListener("hf-seek", (e) => w.renderAt(e.detail.time));
        w.renderAt(0);
        window.__worldReady();
      </script>"""
    (ep / "world/world.html").write_text(html)
    print("wrote", ep / "world/world.html")
