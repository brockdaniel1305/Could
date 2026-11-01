"""Shared world for episode 007 (the Roman Empire vs prime Messi).

Side view on a grass battlefield (horizon y 860, front row feet on y = GY). Messi left, the legion right.
Figures: messi.svg (scale ~0.72 next to legionaries at ~0.82: 1.70 m vs ~1.75 m), legionary.svg, testudo.svg.
The deep army behind the front row is <use> copies of one legionary (cheap); only the front row is fully rigged.
Timing plans that both the scenes and the sound effects need (dribble passes, free kick) live here too (see sfx.py).
"""
from scene import part  # noqa: F401

GY = 1200
LEG_S = 0.82      # legionary scale
MES_S = 0.72      # Messi scale


def field(sid):
    return part("battlefield", sid + "-bf")


def messi(sid, x=230, y=GY, s=MES_S):
    """Messi: move sid-mw (x/y), rig ids sid-m-*."""
    return f'<g transform="translate({x},{y})"><g id="{sid}-mw"><g transform="scale({s})">{part("messi", sid + "-m")}</g></g></g>'


def ball(sid, x, y=GY - 16, s=0.75, name="ball"):
    """Football (r 22 * s). Move sid-<name>; spin sid-<name>-spin."""
    return f'<g transform="translate({x},{y})"><g id="{sid}-{name}"><g id="{sid}-{name}-spin"><g transform="scale({s})">{part("football", sid + "-" + name + "f")}</g></g></g></g>'


def roman(sid, name, x, y=GY, s=LEG_S):
    """A fully rigged legionary: wrapper sid-<name>, rig ids sid-<name>p-*."""
    return f'<g transform="translate({x},{y})"><g id="{sid}-{name}"><g transform="scale({s})">{part("legionary", sid + "-" + name + "p")}</g></g></g>'


def army_defs(sid):
    """One legionary in <defs> for the <use> copies (render once per scene, before army())."""
    return f'<defs><g id="{sid}-L">{part("legionary", sid + "-Lp")}</g></defs>'


def army(sid, x0, cols=6, rows=5, dx=112, s0=LEG_S, name="a"):
    """Rows of legionaries going back towards the horizon (back rows first). Each copy: sid-<name><r>-<c> (topple it)."""
    out = []
    for r in reversed(range(rows)):
        s = s0 * (1 - 0.11 * r)
        y = GY - 62 * r
        for c in range(cols):
            x = x0 + c * dx * (1 - 0.06 * r) + r * 34
            out.append(f'<g transform="translate({x:.0f},{y}) scale({s:.3f})"><g id="{sid}-{name}{r}-{c}"><use href="#{sid}-L" /></g></g>')
    return f'<g id="{sid}-{name}">' + "".join(out) + "</g>"


def scorebug(sid, a, b):
    """ROME a : b MESSI, top right next to the logo. Change it with score(at, a, b)."""
    return (f'\n    <div class="score" id="{sid}-score"><span class="sn">ROME</span>'
            f'<span class="sv" id="{sid}-sa">{a}</span><span class="sc">:</span><span class="sv" id="{sid}-sb">{b}</span>'
            f'<span class="sn">MESSI</span></div>')


def counter(sid, name, start="0"):
    return f'<span id="{sid}-{name}">{start}</span>'


def stamp(sid, word, color="#ffd23f", ink="#1a1a2e"):
    return f'\n    <div class="stamp" id="{sid}-stamp" style="border-color: {color}; color: {color}; text-shadow: 0 6px 0 {ink};">{word}</div>'


CSS = """
    .score { position: absolute; left: 560px; top: 184px; display: flex; align-items: center; gap: 14px; padding: 10px 22px;
             background: #1a1a2e; border: 5px solid #f4efe6; border-radius: 18px; }
    .score .sn { font: 700 28px/1 "CouldMono"; letter-spacing: 0.08em; color: #f4efe6; }
    .score .sv { font: 900 56px/1 "Inter"; color: #ffd23f; min-width: 34px; text-align: center; }
    .score .sc { font: 900 48px/1 "Inter"; color: #f4efe6; }
    .card .cv svg { display: block; margin-top: 6px; }
    .stamp { position: absolute; left: 90px; top: 520px; width: 900px; height: 360px; border: 24px solid #ffd23f; border-radius: 34px;
             display: flex; align-items: center; justify-content: center; font: 900 104px/1 "Inter"; opacity: 0;
             background: rgba(26, 26, 46, 0.35); letter-spacing: -0.02em; }"""

JS = """
      const N = (s) => S + s;
      // text that is a pure function of time: steps = [[t, text], ...]
      const label = (id, steps) => {
        const el = document.querySelector(S + id);
        tl.to({}, { duration: D, ease: "none", onUpdate() {
          const t = this.time(); let txt = steps[0][1];
          for (const [at, s] of steps) if (t >= at) txt = s;
          if (el.textContent !== txt) el.textContent = txt;
        } }, 0);
      };
      // number that counts from a to b between t0 and t0+d (eased), formatted with thousands separators
      const count = (id, a, b, t0, d, ease = "power2.out", suffix = "") => {
        const el = document.querySelector(S + id), o = { v: a };
        el.textContent = a.toLocaleString("en-US") + suffix;
        tl.fromTo(o, { v: a }, { v: b, duration: d, ease, onUpdate() { el.textContent = Math.round(o.v).toLocaleString("en-US") + suffix; } }, t0);
      };
      const score = (at, a, b) => {
        const ea = document.querySelector(S + "sa"), eb = document.querySelector(S + "sb"), a0 = ea.textContent, b0 = eb.textContent;
        tl.to({}, { duration: D, ease: "none", onUpdate() { const on = this.time() >= at; ea.textContent = on ? a : a0; eb.textContent = on ? b : b0; } }, 0);
        tl.fromTo(S + "sb", { scale: 1 }, { scale: 1.8, duration: 0.16, yoyo: true, repeat: 1, ease: "power2.out" }, at);
        tl.fromTo(S + "score", { rotation: 0 }, { rotation: -4, duration: 0.08, yoyo: true, repeat: 3 }, at);
      };
      const showScore = (at) => tl.fromTo(S + "score", { opacity: 0, scale: 0.3, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: 0.4, ease: "back.out(2.4)" }, at);
      // a Roman (prefix p = "<name>p") stamps his foot
      const stompR = (name, at) => {
        tl.to(S + name, { y: -18, duration: 0.12, ease: "power2.out" }, at - 0.12);
        tl.to(S + name, { y: 0, duration: 0.1, ease: "power3.in" }, at);
      };
      const look = (p, x, y, at, d = 0.2) => tl.to([S + p + "-pupL", S + p + "-pupR"], { x, y, duration: d }, at);
      const face = (p, show, at) => {
        ["m-flat", "m-o", "m-wavy", "m-smile"].forEach((m) => { if (document.querySelector(S + p + "-" + m)) tl.set(S + p + "-" + m, { opacity: m === show ? 1 : 0 }, at); });
      };
      // a Roman spins on the spot and stays dizzy: swirl eyes, wavy mouth, orbiting stars, swaying
      const dizzy = (name, at, spins = 3) => {
        const p = name + "p";
        tl.to(S + name, { scaleX: -1, transformOrigin: "50% 100%", duration: 0.09, ease: "none", yoyo: true, repeat: spins * 2 - 1 }, at);
        tl.set(S + p + "-swirl", { opacity: 1 }, at + 0.2);
        face(p, "m-wavy", at + 0.2);
        tl.set(S + p + "-stars", { opacity: 1 }, at + spins * 0.18);
        const t1 = at + spins * 0.18, rest = Math.max(0.5, D - t1);
        tl.fromTo(S + p + "-rotor", { rotation: 0 }, { rotation: 360, transformOrigin: "50% 50%", duration: 0.9, ease: "none", repeat: R(rest, 0.9) }, t1);
        tl.fromTo(S + p + "-body", { rotation: -7 }, { rotation: 7, transformOrigin: "50% 100%", duration: 0.45, ease: "sine.inOut", yoyo: true, repeat: R(rest, 0.45) }, t1);
      };
      // Messi running: legs and arms swing between t0 and t1
      const run = (t0, t1, cyc = 0.16) => {
        const n = R(t1 - t0, cyc);
        tl.fromTo(S + "m-legL", { rotation: -26 }, { rotation: 26, duration: cyc, ease: "sine.inOut", yoyo: true, repeat: n }, t0);
        tl.fromTo(S + "m-legR", { rotation: 26 }, { rotation: -26, duration: cyc, ease: "sine.inOut", yoyo: true, repeat: n }, t0);
        tl.fromTo(S + "m-armL", { rotation: 22 }, { rotation: -22, duration: cyc, ease: "sine.inOut", yoyo: true, repeat: n }, t0);
        tl.fromTo(S + "m-armR", { rotation: -22 }, { rotation: 22, duration: cyc, ease: "sine.inOut", yoyo: true, repeat: n }, t0);
        tl.to([S + "m-legL", S + "m-legR", S + "m-armL", S + "m-armR"], { rotation: 0, duration: 0.12 }, t1);
      };
      const kickR = (at) => {  // right leg swings back and through
        tl.to(S + "m-legR", { rotation: 35, duration: 0.1, ease: "power2.in" }, at - 0.12);
        tl.to(S + "m-legR", { rotation: -50, duration: 0.08, ease: "power3.out" }, at - 0.02);
        tl.to(S + "m-legR", { rotation: 0, duration: 0.1 }, at + 0.06);
      };
      // quadratic arc for an element whose parent sits at its start: offsets (dx, dy) to the end, apex height h
      const arc = (sel, t0, d, dx, dy, h, spinSel) => {
        const el = document.querySelector(sel), o = { p: 0 };
        tl.fromTo(o, { p: 0 }, { p: 1, duration: d, ease: "none", onUpdate() {
          const p = o.p, x = dx * p, y = dy * p - 4 * h * p * (1 - p);
          gsap.set(el, { x, y });
        } }, t0);
        if (spinSel) tl.fromTo(spinSel, { rotation: 0 }, { rotation: 720, duration: d, ease: "none", transformOrigin: "50% 50%" }, t0);
      };
      const drawOn = (sel, at, d = 0.6) => tl.fromTo(sel, { strokeDashoffset: 1.1 }, { strokeDashoffset: 0, duration: d, ease: "power1.inOut" }, at);
      const stampIn = (at) => {
        tl.fromTo(S + "stamp", { opacity: 0, scale: 2.4, rotation: -4 }, { opacity: 1, scale: 1, rotation: -8, duration: 0.18, ease: "power4.in" }, at);
        tl.fromTo(S + "svg", { x: 0 }, { x: 10, duration: 0.04, repeat: 5, yoyo: true }, at + 0.18);
      };
"""

# ---- dribble plan (s5): Messi stays at screen x MX, the camera moves the front line past him -------------------------
MX = 330
PASS0, PASS_DT, PASSES = 1.2, 1.2, 8
FRONT_X0, FRONT_DX = 760, 230
MOVES = ["stepover", "feint", "nutmeg", "roulette", "stepover", "nutmeg", "feint", "chop"]


def pass_times():
    return [PASS0 + i * PASS_DT for i in range(PASSES)]


# ---- free kick plan (s6, plan B, 65 px/m) ---------------------------------------------------------------------------
FK_RUN, FK_KICK, FK_FLIGHT = 0.9, 1.55, 1.2      # after the {{fk}} cue


def map_empire(sid, w=440, h=290):
    """Stylised map of the Roman Empire in AD 117 (red), sea on top. Grow it with attr r of #<sid>-mapclip (from Rome)."""
    X = lambda lon: (lon + 10) * w / 52
    Y = lambda lat: (57 - lat) * h / 31
    pts = lambda ll: " ".join(f"{X(a):.0f},{Y(b):.0f}" for a, b in ll)
    empire = [(-9.5, 43.5), (-1.5, 43.6), (-1.6, 47), (-4.5, 48.5), (1.5, 51), (4, 51.5), (6, 51.8), (7, 50.5), (8.5, 49.5), (8.3, 48.5),
              (10, 48.3), (13, 48.5), (16.5, 48), (19, 47.8), (22.5, 48), (24.5, 47.5), (27.5, 45.6), (30, 45), (35, 42.5),
              (41.5, 41.5), (44, 40), (44.5, 37), (42, 35), (36.5, 31), (34.5, 29.5), (33, 24), (30, 24), (29, 30.5), (25, 31.5),
              (20, 30.5), (15, 31.5), (10, 31), (8, 33), (3, 34.5), (-2, 34.5), (-6, 34), (-9.5, 33.5), (-9.8, 36), (-9.5, 43.5)]
    britain = [(-5.7, 50), (1.6, 51.2), (1.7, 52.8), (0, 53.5), (-1.4, 55), (-3.2, 55.1), (-3.3, 54.4), (-4.6, 53.3), (-4.4, 52.2), (-5.3, 51.6)]
    med = [(-5.6, 35.9), (-2, 36.7), (0.3, 38.6), (3.2, 42.2), (6, 43.1), (8.8, 44.4), (10.5, 43), (12.4, 41.6), (15.6, 38),
           (16.5, 39.4), (17.2, 40.4), (18.5, 40.1), (16.2, 41.8), (13.5, 43.6), (13.6, 45.7), (15.4, 44.4), (19.4, 41.8), (19.8, 39.5),
           (21.5, 37), (23, 36.4), (23.9, 38), (22.8, 40.3), (24.4, 40.9), (26.3, 40.6), (26.7, 39.2), (27.3, 37.5), (28.5, 36.7),
           (30.6, 36.8), (34.5, 36.5), (36.1, 35.8), (35.5, 33.5), (34.2, 31.3), (32, 31.2), (29.5, 30.9), (25, 31.8), (20, 30.9),
           (19.6, 32.6), (15.2, 32.3), (11, 33.2), (10, 35.5), (11.1, 37.1), (9.7, 37.3), (6.5, 37), (3, 36.8), (-1, 35.3), (-5.6, 35.9)]
    black = [(28, 41.3), (29.5, 41.2), (31.5, 41.2), (35.2, 42), (38, 40.9), (41.6, 41.6), (41.5, 43), (38.6, 44.4), (37.5, 45.3),
             (35, 45.1), (33.5, 44.6), (32.5, 45.4), (30.5, 46.6), (29.6, 45.2), (28.6, 44), (28, 42.5)]
    rx, ry = X(12.5), Y(41.9)
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" style="border-radius: 12px; border: 4px solid #1a1a2e;">'
            f'<rect width="{w}" height="{h}" fill="#e9dcc0" />'
            f'<clipPath id="{sid}-mapc"><circle id="{sid}-mapclip" cx="{rx:.0f}" cy="{ry:.0f}" r="0" /></clipPath>'
            f'<g clip-path="url(#{sid}-mapc)"><polygon points="{pts(empire)}" fill="#c0262d" /><polygon points="{pts(britain)}" fill="#c0262d" /></g>'
            f'<polygon points="{pts(britain)}" fill="none" stroke="#1a1a2e" stroke-width="2" />'
            f'<polygon points="{pts(med)}" fill="#7fb8d8" stroke="#1a1a2e" stroke-width="2" /><polygon points="{pts(black)}" fill="#7fb8d8" stroke="#1a1a2e" stroke-width="2" />'
            f'<circle cx="{rx:.0f}" cy="{ry:.0f}" r="6" fill="#ffd23f" stroke="#1a1a2e" stroke-width="2" /></svg>')


def map_britain(sid, w=300, h=330):
    """Northern Britain with Hadrian's Wall (draw on #<sid>-hwline, pathLength 1)."""
    X = lambda lon: (lon + 7) * w / 9.5
    Y = lambda lat: (59 - lat) * h / 9
    gb = [(-5.7, 50.1), (1.7, 51.3), (1.7, 52.8), (0.2, 53.5), (-0.5, 54.5), (-1.6, 55.6), (-2.1, 56.1), (-2.7, 56.4), (-1.8, 57.6),
          (-3.8, 57.7), (-3.2, 58.6), (-5, 58.6), (-5.6, 57.3), (-5.8, 56.3), (-5.2, 55.5), (-4.9, 54.8), (-3.6, 54.9), (-3.3, 54.3),
          (-3, 53.8), (-4.6, 53.3), (-4.2, 52.3), (-5.3, 51.8), (-4.3, 51.4), (-5.7, 50.1)]
    pts = " ".join(f"{X(a):.0f},{Y(b):.0f}" for a, b in gb)
    wall = f"M{X(-3.25):.0f},{Y(54.95):.0f} L{X(-2.6):.0f},{Y(54.98):.0f} L{X(-2.0):.0f},{Y(55.0):.0f} L{X(-1.45):.0f},{Y(54.99):.0f}"
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" style="border-radius: 12px; border: 4px solid #1a1a2e;">'
            f'<rect width="{w}" height="{h}" fill="#7fb8d8" /><polygon points="{pts}" fill="#9bb36b" stroke="#1a1a2e" stroke-width="3" />'
            f'<path id="{sid}-hwline" d="{wall}" pathLength="1" stroke-dasharray="1 1.2" stroke-dashoffset="1.1" fill="none" stroke="#c0262d" stroke-width="9" stroke-linecap="round" /></svg>')
